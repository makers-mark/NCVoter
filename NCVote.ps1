#Add-Type -AssemblyName System.Windows.Forms
#Add-Type -AssemblyName System.Windows.Forms.DataVisualization
#clear
$directory = "c:\ncvoter"

if (-not(Test-Path -Path "$directory")){
    new-item -Force -Path "$directory\" -ItemType directory
}
if (-not(Test-Path -Path "$directory\Data")){
    new-item -Force -Path "$directory\Data\" -ItemType directory
}

$Matches = ''
$debug = $false
$formattedDateTitle = ''
$counties = ''
$exportCsv = ''
$content = ''

if ($debug -eq $false){
    for ($i = 2004; $i -lt 2024;$i++){

        $datesAvailable = ''

        $session = New-Object Microsoft.PowerShell.Commands.WebRequestSession
        $session.UserAgent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.5005.61 Safari/537.36"
        #$session.Cookies.Add((New-Object System.Net.Cookie("__RequestVerificationToken", "K5mqveCv66x_BYmXi2UA1wiaZntRAeYrmp9TAxzQBvQAO1B3eT0HuoGP2ZRfmUanNwFhVD8ZduqQ8d8rafRXdihmaAI20plFDQaktY0OfnE1", "/", "vt.ncsbe.gov")))
        #$session.Cookies.Add((New-Object System.Net.Cookie("ARRAffinity", "e42d68261b7ad0b3d017a6e9293662b884cdeb694462a884eb4f3c46bae0f771", "/", ".vt.ncsbe.gov")))
        #$session.Cookies.Add((New-Object System.Net.Cookie("ARRAffinitySameSite", "e42d68261b7ad0b3d017a6e9293662b884cdeb694462a884eb4f3c46bae0f771", "/", ".vt.ncsbe.gov")))
        $datesAvailable = Invoke-WebRequest -UseBasicParsing -Uri "https://vt.ncsbe.gov/RegStat/GetLookupReportDates/" `
        -Method "POST" `
        -WebSession $session `
        -Headers @{
        "authority"="vt.ncsbe.gov"
          "method"="POST"
          "path"="/RegStat/GetLookupReportDates/"
          "scheme"="https"
          "accept"="*/*"
          "accept-encoding"="gzip, deflate, br"
          "accept-language"="en-US,en;q=0.9"
          "origin"="https://vt.ncsbe.gov"
          "referer"="https://vt.ncsbe.gov/RegStat/"
          "sec-fetch-dest"="empty"
          "sec-fetch-mode"="cors"
          "sec-fetch-site"="same-origin"
          "sec-gpc"="1"
          "x-requested-with"="XMLHttpRequest"
        } `
        -ContentType "application/x-www-form-urlencoded; charset=UTF-8" `
        -Body "ReportYear=$i" | ConvertFrom-Json

        #Write-Host $datesAvailable.Text

        foreach ($dates in $datesAvailable.Text){

            $totalDemocrats      = 0
            $totalRepublicans    = 0
            $totalUnaffiliated   = 0
            $totalGreen          = 0
            $totalConstitution   = 0
            $totalLibertarian    = 0
            $totalWhite          = 0
            $totalBlack          = 0
            $totalAmericanIndian = 0
            $totalNativeHawaiian = 0
            $totalOther          = 0
            $totalHispanic       = 0
            $totalMale           = 0
            $totalFemale         = 0
            $totalUndisclosedGen = 0

            $dateTitle =  $dates
            #Write-Host $dateTitle
            $formattedDateTitle = $dateTitle.replace("/","-")
            #$formattedDateTitle -f "yyyy-MM-dd" 
            [string]$year = $formattedDateTitle.Substring($formattedDateTitle.Length -4)
            [string]$MMdd = $formattedDateTitle.Substring(0, 5)
            $formattedDateTitle = "$year-$MMdd"


            #write-host $formattedDateTitle
            if (test-path "$directory\Data\$formattedDateTitle.csv"){
                Write-Host("File exists, skipping!`r`n")
            } else {
                Write-Host("Downloading and creating $formattedDateTitle")

                $urlDateTitle = $dateTitle.Replace("/","%2F")

                $session = New-Object Microsoft.PowerShell.Commands.WebRequestSession
                $session.UserAgent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.5005.61 Safari/537.36"
                #$session.Cookies.Add((New-Object System.Net.Cookie("__RequestVerificationToken", "K5mqveCv66x_BYmXi2UA1wiaZntRAeYrmp9TAxzQBvQAO1B3eT0HuoGP2ZRfmUanNwFhVD8ZduqQ8d8rafRXdihmaAI20plFDQaktY0OfnE1", "/", "vt.ncsbe.gov")))
                #$session.Cookies.Add((New-Object System.Net.Cookie("ARRAffinity", "e42d68261b7ad0b3d017a6e9293662b884cdeb694462a884eb4f3c46bae0f771", "/", ".vt.ncsbe.gov")))
                #$session.Cookies.Add((New-Object System.Net.Cookie("ARRAffinitySameSite", "e42d68261b7ad0b3d017a6e9293662b884cdeb694462a884eb4f3c46bae0f771", "/", ".vt.ncsbe.gov")))
                $results = Invoke-WebRequest -UseBasicParsing -Uri "https://vt.ncsbe.gov/RegStat/Results/?date=$urlDateTitle" `
                -WebSession $session `
                -Headers @{
                "authority"="vt.ncsbe.gov"
                    "method"="GET"
                    "path"="/RegStat/Results/?date=10%2F17%2F2020"
                    "scheme"="https"
                    "accept"="text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9"
                    "accept-encoding"="gzip, deflate, br"
                    "accept-language"="en-US;q=0.8"
                    "cache-control"="max-age=0"
                    "referer"="https://vt.ncsbe.gov/RegStat/"
                    "sec-fetch-dest"="document"
                    "sec-fetch-mode"="navigate"
                    "sec-fetch-site"="same-origin"
                    "sec-fetch-user"="?1"
                    "sec-gpc"="1"
                    "upgrade-insecure-requests"="1"
                }

                $results -match 'var data = \[.*'

                $data = $Matches.Values
                $json = $data.Replace("var data = ", "")

                #$json = $json.ToString()

                #$data = $data.split("[").split("]")

                $json = $json | ConvertFrom-Json

                foreach ($item in $json)
                {
                    $totalRepublicans    += $item.Republicans
                    $totalDemocrats      += $item.Democrats
                    $totalGreen          += $item.Green
                    $totalConstitution   += $item.Constitution
                    $totalLibertarian    += $item.Libertarians
                    $totalUnaffiliated   += $item.Unaffiliated
                    $totalWhite          += $item.White
                    $totalBlack          += $item.Black
                    $totalAmericanIndian += $item.AmericanIndian
                    $totalNativeHawaiian += $item.NativeHawaiian
                    $totalOther          += $item.Other
                    $totalHispanic       += $item.Hispanic
                    $totalMale           += $item.Male
                    $totalFemale         += $item.Female
                    $totalUndisclosedGen += $item.UnDisclosedGender
                }

                #Write-Host "Democrats " $totalDemocrats
                #Write-Host "Republicans " $totalRepublicans

                $csv = $json | ConvertTo-Csv
                Write-Host $formattedDateTitle
                $json | Export-Csv -LiteralPath "$directory\Data\$formattedDateTitle.csv" -NoTypeInformation -Force
            }
        }  #end foreach ($date in $datesAvailable.Text)
    }  #end for ($i = 2004; $i -lt 2023;$i++)

}
    #$exportCsv = [pscustomobject] @{}
    $exportCsv       = "`"Date`",`"Democrats`",`"Republicans`",`"Green`",`"Constitution`",`"Libertarians`",`"Unaffiliated`",`"White`",`"Black`",`"AmericanIndian`",`"NativeHawaiian`",`"Other`",`"Hispanic`",`"Male`",`"Female`",`"UndisclosedGender`",`"Total`"`r`n"
    #$exportCountyCsv = "`"Date`",`"Democrats`",`"Republicans`",`"Green`",`"Constitution`",`"Libertarians`",`"Unaffiliated`",`"White`",`"Black`",`"AmericanIndian`",`"NativeHawaiian`",`"Other`",`"Hispanic`",`"Male`",`"Female`",`"UndisclosedGender`",`"Total`",`"Dpercent`",`"Rpercent`",`"Upercent`"`r`n"
    $i = 0
    Get-ChildItem –Path "$directory\Data\" -File | Sort-Object{$_.BaseName -as [datetime] | Select -First 1} |
    Foreach-Object {
        
        $baseName = $_.BaseName
        if ($baseName -eq "alpha"){
            return
        }
        #$dateTimeObj = $baseName
        #[datetime]::ParseExact($dateTimeObj, 'yyyy-MM-dd', $null)
        #Write-Host $dateTimeObj
        #$year = (Get-Date $dateTimeObj).Year
        #$dayOfYear = (Get-Date $dateTimeObj).DayOfYear -1
        #if ($year % 4 -eq 0){
        #    [string]$dayOfYearPercent = (($dayOfYear * 100) / 366) / 100
        #} else {
        #    [string]$dayOfYearPercent = (($dayOfYear * 100) / 365) / 100
        #}
        #Write-Host $dayOfYearPercent
        #if ($dayOfYearPercent -eq "0"){
        #    $xValueYearString = "$year"
        #} else {
        #    $dayOfYearPercent = $dayOfYearPercent.Split(".")[1]
        #    $xValueYearString = "$year.$dayOfYearPercent"
        #}

        #Write-Host $xValueYearString
        Write-Host $_.BaseName
        
        $csvFile = Import-Csv -LiteralPath $_.FullName

        $total             = 0
        $dems              = 0
        $repubs            = 0
        $green             = 0
        $constitution      = 0
        $libertarian       = 0
        $unafil            = 0
        $white             = 0
        $black             = 0
        $americanIndian    = 0
        $nativeHawaiian    = 0
        $other             = 0
        $hispanic          = 0
        $male              = 0
        $female            = 0
        $undisclosedGender = 0

        if ($i -eq 0){
            ForEach($county in $csvFile){
                $i++
                Write-Host $county
                if (Get-Variable -Name $county.CountyName -ErrorAction SilentlyContinue){
                    Get-Variable -Name $county.CountyName | Remove-Variable
                    Write-Host "Removing $($county.CountyName)"
                    Write-Host "Creating $($county.CountyName)"
                    New-Variable -Name $county.CountyName -Value "`"Date`",`"Democrats`",`"Republicans`",`"Green`",`"Constitution`",`"Libertarians`",`"Unaffiliated`",`"White`",`"Black`",`"AmericanIndian`",`"NativeHawaiian`",`"Other`",`"Hispanic`",`"Male`",`"Female`",`"UndisclosedGender`",`"Total`"`r`n"
                } else {
                    New-Variable -Name $county.CountyName -Value "`"Date`",`"Democrats`",`"Republicans`",`"Green`",`"Constitution`",`"Libertarians`",`"Unaffiliated`",`"White`",`"Black`",`"AmericanIndian`",`"NativeHawaiian`",`"Other`",`"Hispanic`",`"Male`",`"Female`",`"UndisclosedGender`",`"Total`"`r`n"
                    Write-Host "Creating $($county.CountyName)"
                }
                #[string]$directory = $county.CountyName
                if (Test-Path -Path "$directory\Data\$($county.CountyName)"){
                    Write-Host "$directory\Data\$($county.CountyName) already Exists."
                } else {
                    new-item -Force -Path "$directory\Data\$($county.CountyName)\" -ItemType directory
                    Write-Host "Creating Folder $directory\Data\$($county.CountyName)"
                    #Write-Host $county.CountyName
                }
            }
        }

        ForEach($county in $csvFile){
            #[string]$name = $county.CountyName
            (Get-Variable -name $($county.CountyName)).Value += "`"$baseName`",`"$($county.Democrats)`",`"$($county.Republicans)`",`"$($county.Green)`",`"$($county.Constitution)`",`"$($county.Libertarians)`",`"$($county.Unaffiliated)`",`"$($county.White)`",`"$($county.Black)`",`"$($county.AmericanIndian)`",`"$($county.NativeHawaiian)`",`"$($county.Other)`",`"$($county.Hispanic)`",`"$($county.Male)`",`"$($county.Female)`",`"$($county.UnDisclosedGender)`",`"$($county.Total)`"`r`n"
            #Write-Host "$($county.Democrats)"

            #Write-Host $county.CountyName
            #Write-Host $county.Total
            $total += $county.Total
            $repubs += $county.Republicans
            $dems += $county.Democrats
            $unafil += $county.Unaffiliated
            $green += $county.Green
            $constitution += $county.Constitution
            $libertarian += $county.Libertarians
            $white += $county.White
            $black += $county.Black
            $americanIndian += $county.AmericanIndian
            $nativeHawaiian += $county.NativeHawaiian
            $other += $county.Other
            $hispanic += $county.Hispanic
            $male += $county.Male
            $female += $county.Female
            $undisclosedGender += $county.UnDisclosedGender

        }
        
        $exportCsv += "`"$baseName`",`"$dems`",`"$repubs`",`"$green`",`"$constitution`",`"$libertarian`",`"$unafil`",`"$white`",`"$black`",`"$americanIndian`",`"$nativeHawaiian`",`"$other`",`"$hispanic`",`"$male`",`"$female`",`"$undisclosedGender`",`"$total`"`r`n"
  
       
    }
$directories = Get-ChildItem –Path "$directory\Data" -Directory 

foreach ($county in $directories){
    #Write-Host $county
    $content = (Get-Variable -name $county).Value
    if (Test-Path "$directory\Data\$county\$county.csv"){
        Remove-Item "$directory\Data\$county\$county.csv"
    }
    Set-Content -Path "$directory\Data\$county\$county.csv" -Value $content -Force
}

Set-Content -Path "$directory\Data\alpha.csv" -Value $exportCsv -Force
#Export-Csv -InputObject $exportCsv -Path "c:\ffmpeg\csvTest.csv" -Force -NoTypeInformation


#$excel = New-Object -ComObject Excel.Application 
#$excel.Visible = $false

#$workbook = $excel.Worksheets.Item(0)
#$excelWorkBook = $excel.Workbooks.Open("c:\csv\$formattedDateTitle.csv").SaveAs("c:\csv\$formattedDateTitle.xlsx",51)


#$excel.Quit()

#explorer.exe "/Select,c:\csv\temp.xlsx"

