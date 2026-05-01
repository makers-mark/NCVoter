#Requires -Version 5.1

$directory = "c:\ncvoter"
$debug     = $false
$isUpdated = $false

# Ensure required directories exist
foreach ($path in "$directory", "$directory\Data") {
    if (-not (Test-Path $path)) {
        New-Item -Force -Path $path -ItemType Directory | Out-Null
    }
}

# ── Shared request configuration ────────────────────────────────────────────
$userAgent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.5005.61 Safari/537.36"

$dateApiHeaders = @{
    "authority"         = "vt.ncsbe.gov"
    "accept"            = "*/*"
    "accept-encoding"   = "gzip, deflate, br"
    "accept-language"   = "en-US,en;q=0.9"
    "origin"            = "https://vt.ncsbe.gov"
    "referer"           = "https://vt.ncsbe.gov/RegStat/"
    "sec-fetch-dest"    = "empty"
    "sec-fetch-mode"    = "cors"
    "sec-fetch-site"    = "same-origin"
    "sec-gpc"           = "1"
    "x-requested-with"  = "XMLHttpRequest"
}

$dataPageHeaders = @{
    "authority"                 = "vt.ncsbe.gov"
    "accept"                    = "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8"
    "accept-encoding"           = "gzip, deflate, br"
    "accept-language"           = "en-US,en;q=0.9"
    "cache-control"             = "max-age=0"
    "referer"                   = "https://vt.ncsbe.gov/RegStat/"
    "sec-fetch-dest"            = "document"
    "sec-fetch-mode"            = "navigate"
    "sec-fetch-site"            = "same-origin"
    "sec-fetch-user"            = "?1"
    "sec-gpc"                   = "1"
    "upgrade-insecure-requests" = "1"
}

# ── Phase 1: Download missing date CSVs ─────────────────────────────────────
if (-not $debug) {
    $startYear = 2004
    $endYear   = (Get-Date).Year + 1
    $yearSpan  = $endYear - $startYear

    for ($year = $startYear; $year -le $endYear; $year++) {
        $pct = [int](($year - $startYear) / $yearSpan * 100)
        Write-Progress -Activity "Checking available report dates" -Status "Year $year" -PercentComplete $pct

        $session           = New-Object Microsoft.PowerShell.Commands.WebRequestSession
        $session.UserAgent = $userAgent

        try {
            $datesAvailable = Invoke-WebRequest -UseBasicParsing `
                -Uri     "https://vt.ncsbe.gov/RegStat/GetLookupReportDates/" `
                -Method  POST `
                -WebSession $session `
                -Headers $dateApiHeaders `
                -ContentType "application/x-www-form-urlencoded; charset=UTF-8" `
                -Body    "ReportYear=$year" | ConvertFrom-Json
        } catch {
            Write-Warning "Could not retrieve dates for $year`: $_"
            continue
        }

        foreach ($dateText in $datesAvailable.Text) {
            # Reformat MM/dd/yyyy -> yyyy-MM-dd
            $formatted = $dateText -replace '^(\d{2})/(\d{2})/(\d{4})$', '$3-$1-$2'
            $filePath  = "$directory\Data\$formatted.csv"

            if (Test-Path $filePath) {
                Write-Host "  SKIP  $formatted" -ForegroundColor DarkGray
            } else {
                Write-Host "  FETCH $formatted" -ForegroundColor Cyan

                $urlDate     = [Uri]::EscapeDataString($dateText)
                $dataSession = New-Object Microsoft.PowerShell.Commands.WebRequestSession
                $dataSession.UserAgent = $userAgent

                try {
                    $response = Invoke-WebRequest -UseBasicParsing `
                        -Uri        "https://vt.ncsbe.gov/RegStat/Results/?date=$urlDate" `
                        -WebSession $dataSession `
                        -Headers    $dataPageHeaders

                    if ($response.Content -match 'var data = \[.*') {
                        $json = $Matches[0].Replace("var data = ", "") | ConvertFrom-Json
                        $json | Export-Csv -LiteralPath $filePath -NoTypeInformation -Force
                        $isUpdated = $true
                        Write-Host "    OK    $formatted" -ForegroundColor Green
                    } else {
                        Write-Warning "    No data block found for $formatted"
                    }
                } catch {
                    Write-Warning "    Request failed for $formatted`: $_"
                }
            }
        }
    }
    Write-Progress -Activity "Checking available report dates" -Completed
}

# ── Phase 2: Aggregate per-county and statewide CSVs ────────────────────────
if ($isUpdated) {
    $csvHeader = '"Date","Democrats","Republicans","Green","Constitution","Libertarians","Unaffiliated","White","Black","American Indian","Native Hawaiian","Other","Hispanic","Male","Female","Undisclosed Gender","No Labels","Multiracial","Undesignated","Total"'

    # Hashtable of StringBuilders replaces dynamic variables (avoids O(n²) string concat)
    $countyBuilders = @{}
    $countyDirPaths = @{}
    $stateRows      = [System.Collections.Generic.List[string]]::new()

    Write-Host "`nAggregating data files..." -ForegroundColor Yellow

    $dataFiles = Get-ChildItem -Path "$directory\Data" -File -Filter "*.csv" |
        Where-Object { $_.BaseName -ne "alpha" } |
        Sort-Object {
            [datetime]::ParseExact($_.BaseName, 'yyyy-MM-dd',
                [System.Globalization.CultureInfo]::InvariantCulture)
        }

    $totalFiles = $dataFiles.Count
    $fileIndex  = 0

    foreach ($file in $dataFiles) {
        $fileIndex++
        $baseName = $file.BaseName
        Write-Progress -Activity "Aggregating" `
            -Status "$baseName  ($fileIndex / $totalFiles)" `
            -PercentComplete ($fileIndex / $totalFiles * 100)

        $csvRows = Import-Csv -LiteralPath $file.FullName

        # Initialise county builder/directory on first encounter
        foreach ($row in $csvRows) {
            $cn = $row.CountyName
            if (-not $countyBuilders.ContainsKey($cn)) {
                $sb = [System.Text.StringBuilder]::new()
                $sb.AppendLine($csvHeader) | Out-Null
                $countyBuilders[$cn] = $sb

                $countyDir = "$directory\Data\$cn"
                $countyDirPaths[$cn] = $countyDir
                if (-not (Test-Path $countyDir)) {
                    New-Item -Force -Path $countyDir -ItemType Directory | Out-Null
                    Write-Host "  DIR   $cn" -ForegroundColor DarkCyan
                }
            }
        }

        # Accumulate statewide totals while building per-county rows
        $tTotal=$tDems=$tRepubs=$tGreen=$tConst=$tLib=$tUnafil=0
        $tWhite=$tBlack=$tAI=$tNH=$tOther=$tHisp=0
        $tMale=$tFemale=$tUGender=$tNoLabels=$tMulti=$tUndes=0

        foreach ($row in $csvRows) {
            $cn = $row.CountyName
            $countyBuilders[$cn].AppendLine(
                "`"$baseName`",`"$($row.Democrats)`",`"$($row.Republicans)`",`"$($row.Green)`",`"$($row.Constitution)`",`"$($row.Libertarians)`",`"$($row.Unaffiliated)`",`"$($row.White)`",`"$($row.Black)`",`"$($row.AmericanIndian)`",`"$($row.NativeHawaiian)`",`"$($row.Other)`",`"$($row.Hispanic)`",`"$($row.Male)`",`"$($row.Female)`",`"$($row.UnDisclosedGender)`",`"$($row.NoLabels)`",`"$($row.Multiracial)`",`"$($row.Undesignated)`",`"$($row.Total)`""
            ) | Out-Null

            $tTotal    += [long]$row.Total;           $tDems    += [long]$row.Democrats
            $tRepubs   += [long]$row.Republicans;     $tGreen   += [long]$row.Green
            $tConst    += [long]$row.Constitution;    $tLib     += [long]$row.Libertarians
            $tUnafil   += [long]$row.Unaffiliated;    $tWhite   += [long]$row.White
            $tBlack    += [long]$row.Black;           $tAI      += [long]$row.AmericanIndian
            $tNH       += [long]$row.NativeHawaiian;  $tOther   += [long]$row.Other
            $tHisp     += [long]$row.Hispanic;        $tMale    += [long]$row.Male
            $tFemale   += [long]$row.Female;          $tUGender += [long]$row.UnDisclosedGender
            $tNoLabels += [long]$row.NoLabels;        $tMulti   += [long]$row.Multiracial
            $tUndes    += [long]$row.Undesignated
        }

        $stateRows.Add("`"$baseName`",`"$tDems`",`"$tRepubs`",`"$tGreen`",`"$tConst`",`"$tLib`",`"$tUnafil`",`"$tWhite`",`"$tBlack`",`"$tAI`",`"$tNH`",`"$tOther`",`"$tHisp`",`"$tMale`",`"$tFemale`",`"$tUGender`",`"$tNoLabels`",`"$tMulti`",`"$tUndes`",`"$tTotal`"")
    }
    Write-Progress -Activity "Aggregating" -Completed

    # Write per-county CSVs
    Write-Host "`nWriting county files..." -ForegroundColor Yellow
    foreach ($cn in $countyBuilders.Keys) {
        Set-Content -Path "$($countyDirPaths[$cn])\$cn.csv" `
            -Value $countyBuilders[$cn].ToString() -Force
    }

    # Write statewide alpha.csv
    $alphaContent = ($csvHeader, ($stateRows -join [Environment]::NewLine)) -join [Environment]::NewLine
    Set-Content -Path "$directory\Data\alpha.csv" -Value $alphaContent -Force
    Write-Host "alpha.csv written  ($($stateRows.Count) date entries)" -ForegroundColor Green
}

# ── Phase 3: Commit and push ─────────────────────────────────────────────────
if ($isUpdated) {
    Write-Host "`nCommitting to GitHub..." -ForegroundColor Yellow
    Set-Location $directory
    &git add .        2>&1 | Out-Null
    &git commit -m "data" 2>&1 | Out-Null

    # Merge stderr->stdout so PowerShell doesn't misclassify git's
    # informational remote-tracking lines as error records.
    &git push -u origin main 2>&1 | ForEach-Object {
        if ($_ -is [System.Management.Automation.ErrorRecord]) {
            Write-Host $_.Exception.Message -ForegroundColor DarkGray
        } else {
            Write-Host $_
        }
    }
    Write-Host "`nRepository updated successfully." -ForegroundColor Green
}
