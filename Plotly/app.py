# Run this app with `python app.py` and
# visit http://127.0.0.1:8050/ in your web browser.

from dash import Dash, html, dcc, Input, Output
import string
import dash_bootstrap_components as dbc
from dash_bootstrap_templates import load_figure_template
#import plotly.express as px
import pandas as pd
import plotly.graph_objects as go
import os
import flask
from waitress import serve

flask_server = flask.Flask(__name__)

load_figure_template(['CYBORG', 'DARKLY'])#('LUX')

gitRepo = 'https://raw.githubusercontent.com/makers-mark/NCVoter/main/Data'
#localRepo = 'c:\\ncvoter\\Data'
#backupRepo = 'C:\\ncvoter-6-10-23.backup\\Data'
backupRepo = 'C:\\ncvoter-6-10-23.backup\\tessstfornewCAT'

localRepo = 'c:\\ncvoter\\Data'

app = Dash(__name__,server=flask_server,external_stylesheets=[dbc.themes.DARKLY])
server = app.server

traceOpacity = 0.1
colors = {
    'Republicans': {
		'fillcolor': 'rgba(255,0,0,{})'.format(traceOpacity),
		'tracecolor': 'red'
	},
    'Democrats': {
		'fillcolor': 'rgba(0,0,255,{})'.format(traceOpacity),
		'tracecolor': 'blue'
	},
	'Unaffiliated': {
		'fillcolor': 'rgba(236,245,39,{})'.format(traceOpacity),
		'tracecolor': 'yellow'
	},
	'Libertarians': {
		'fillcolor': 'rgba(155,155,155,{})'.format(traceOpacity),
		'tracecolor': 'rgba(200,200,200,1)'
	},
	'Green': {
		'fillcolor': 'rgba(20,155,20,{})'.format(traceOpacity),
		'tracecolor': 'green'
	},
	'White': {
		'fillcolor': 'rgba(100,100,100,{})'.format(traceOpacity),
		'tracecolor': 'rgba(10,10,10,1)'
	},
	'Black': {
		'fillcolor': 'rgba(20,20,20,{})'.format(traceOpacity),
		'tracecolor': 'rgba(0,0,0,1)'
	},
	'American Indian': {
		'fillcolor': 'rgba(255,0,0,{})'.format(traceOpacity),
		'tracecolor': 'red'
	},
	'Native Hawaiian': {
		'fillcolor': 'rgba(20,155,20,{})'.format(traceOpacity),
		'tracecolor': 'green'	
	},
	'Other': {
		'fillcolor': 'rgba(245,39,241,{})'.format(traceOpacity),
		'tracecolor': 'pink'
	},
	'Hispanic': {
		'fillcolor': 'rgba(245,176,39,{})'.format(traceOpacity),
		'tracecolor': 'green'
	},
	'Male': {
		'fillcolor': 'rgba(0,0,255,{})'.format(traceOpacity),
		'tracecolor': 'blue'
	},
	'Female': {
		'fillcolor': 'rgba(245,39,241,{})'.format(traceOpacity),
		'tracecolor': 'pink'
	},
	'Undisclosed Gender': {
		'fillcolor': 'rgba(157,39,245,{})'.format(traceOpacity),
		'tracecolor': 'hotpink'
	},
	'Multiracial': {
		'fillcolor': 'rgba(157,39,245,{})'.format(traceOpacity),
		'tracecolor': 'brown'
	},
	'Undesignated': {
		'fillcolor': 'rgba(157,39,245,{})'.format(traceOpacity),
		'tracecolor': 'green'
	},
	'No Labels': {
		'fillcolor': 'rgba(157,39,245,{})'.format(traceOpacity),
		'tracecolor': 'purple'
	}
}

directory = localRepo
#directory = gitRepo

width=3
gridcolor='rgba(70,70,70,0.8)'
title=''
percent=False

#counties = [ f.name.title() for f in os.scandir(directory) if f.is_dir() ]
counties = ['ALAMANCE', 'ALEXANDER', 'ALLEGHANY', 'ANSON', 'ASHE', 'AVERY', 'BEAUFORT', 'BERTIE', 'BLADEN', 'BRUNSWICK', 'BUNCOMBE', 'BURKE', 'CABARRUS', 'CALDWELL', 'CAMDEN', 'CARTERET', 'CASWELL', 'CATAWBA', 'CHATHAM', 'CHEROKEE', 'CHOWAN', 'CLAY', 'CLEVELAND', 'COLUMBUS', 'CRAVEN', 'CUMBERLAND', 'CURRITUCK', 'DARE', 'DAVIDSON', 'DAVIE', 'DUPLIN', 'DURHAM', 'EDGECOMBE', 'FORSYTH', 'FRANKLIN', 'GASTON', 'GATES', 'GRAHAM', 'GRANVILLE', 'GREENE', 'GUILFORD', 'HALIFAX', 'HARNETT', 'HAYWOOD', 'HENDERSON', 'HERTFORD', 'HOKE', 'HYDE', 'IREDELL', 'JACKSON', 'JOHNSTON', 'JONES', 'LEE', 'LENOIR', 'LINCOLN', 'MACON', 'MADISON', 'MARTIN', 'MCDOWELL', 'MECKLENBURG', 'MITCHELL', 'MONTGOMERY', 'MOORE', 'NASH', 'NEW HANOVER', 'NORTHAMPTON', 'ONSLOW', 'ORANGE', 'PAMLICO', 'PASQUOTANK', 'PENDER', 'PERQUIMANS', 'PERSON', 'PITT', 'POLK', 'RANDOLPH', 'RICHMOND', 'ROBESON', 'ROCKINGHAM', 'ROWAN', 'RUTHERFORD', 'SAMPSON', 'SCOTLAND', 'STANLY', 'STOKES', 'SURRY', 'SWAIN', 'TRANSYLVANIA', 'TYRRELL', 'UNION', 'VANCE', 'WAKE', 'WARREN', 'WASHINGTON', 'WATAUGA', 'WAYNE', 'WILKES', 'WILSON', 'YADKIN', 'YANCEY']

dropdownList = [{'label': x.title() + ' County', 'value': x } for x in counties]
dropdownList.insert(0, {'label': 'Statewide', 'value': 'Statewide'})

SIDEBAR_STYLE = {
    #"position": "fixed",
    #"top": 0,
    #"left": 0,
    #"bottom": 0,
    "padding": "1rem",
	#"backgroundColor": "#eeeeee",
    "position": "fixed",
    "top": '0.5rem',
    "left": '0.5rem',
    "bottom": '0.5rem',
    "width": "14rem",
    "paddingTop": "1rem",
	"paddingLeft": "1rem",
	'paddingBottom': '1rem',
	"overflowY": "auto",
	"boxSizing": "unset",
	"color": "rgb(173, 175, 174)",
	#"borderBox": "2px",
	'border': '4px',
	'borderStyle': 'groove',
	'borderColor': '#111',
	
}

sidebar = html.Div(
    [
        dbc.Nav(
            [
				dcc.Dropdown(
					dropdownList,
					'Statewide',
					id = "dataFrame",
					clearable = False,
					style = {
						'cursor': 'pointer'
					},
				),html.Hr(),
				html.H5('Annotations'),
				dcc.Checklist(
					['Federal Election', 'Midterm Election', 'Voter Roll Purge'],
					inline=False,
					id='annotations'
				), html.Hr(),
				html.H5('Party'),
				dcc.Checklist(
					['Republicans', 'Democrats', 'Unaffiliated', 'Libertarians', 'Green', 'No Labels'],
					value = ['Republicans', 'Democrats', 'Unaffiliated'],
					inline=False,
					id='partyDataset'
				), html.Hr(),
				html.H5('Race'),
				dcc.Checklist(
					[
						{'label': 'White', 'value': 'White'},
						{'label': 'Black', 'value': 'Black'},
						{'label': 'Other', 'value': 'Other'},
						{'label': 'American Indian', 'value': 'American Indian'},
						{'label': 'Native Hawaiian', 'value': 'Native Hawaiian'}, 
						{'label': 'Hispanic', 'value': 'Hispanic'},
						{'label': 'Multiracial', 'value': 'Multiracial'},
						{'label': 'Undesignated', 'value': 'Undesignated'}
					],
					inline=False,
					id='raceDataset'
				), html.Hr(),
				html.H5('Sex'),
				dcc.Checklist(
					[
						{'label': 'Male', 'value': 'Male'}, 
						{'label': 'Female', 'value': 'Female'},
						{'label': 'Undisclosed Gender', 'value': 'Undisclosed Gender'}
					],
					inline=False,
					id='sexDataset'
				), html.Hr(),
				dcc.Checklist(
					['Percent'],
					inline=False,
					id='percent'
				)
			],
			vertical=True,
			pills=False,
		),
	],
	style=SIDEBAR_STYLE,
)

CONTENT_STYLE = {
    "margin-left": "15rem",
	"height": "100vh"
}

content = html.Div([dcc.Graph(id='my-graph', style = CONTENT_STYLE)])

app.layout = html.Div([ sidebar, content ])  #dbc.Container(children=[

	#dbc.Row(
	#	[dbc.Col(sidebar),
	#	dbc.Col(dcc.Graph(id='my-graph'))#, width = 10, style = {'padding':'0px', 'marginLeft':'1px', 'marginTop':'10px','marginRight':'0px'})
	#	]
	#)

#],
#fluid = True,
#className = "dbc")

@app.callback(
	Output(component_id='title', component_property='children'),
	Input('dataFrame', 'value'))
def update_trace(dataset, df, percent):
	def getY():
		if (percent):
			return df[dataset]/df['Total']
		else:
			return df[dataset]
	traces = go.Scatter(
		x=df['Date'],
		y=getY(),
		fill='tozeroy',
		hoveron='points+fills',
		fillcolor=colors[dataset]['fillcolor'],
		line=dict(
			color=colors[dataset]['tracecolor'],
			width=width),
		name=dataset
	)
	return traces

def draw_annotations(value, fig):
	if (value == 'Federal Election'):
		presidentialElections = ["2020-11-3", "2016-11-6", "2012-11-6", "2008-11-4", "2004-11-2", "2024-11-5"]
		#fig = go.Figure()
		for i in presidentialElections:
			fig.add_shape(type='line',
				opacity=0.75,
				x0=i,
				y0=0,
				x1=i,
				y1=1,
				#y1=max(df[df['Date'] == "{}-01-01".format(i)]['Republicans'].max(), df[df['Date'] == "{}-01-01".format(i)]['Democrats'].max(), df[df['Date'] == "{}-01-01".format(i)]['Unaffiliated'].max()),
				line=dict(color='Red'), #color='rgba(50,50,75,0.9)'),
				xref='x',
				yref='paper',
				#text_annotation="January 1st, {} Voter Roll Purge".format(i),
				exclude_empty_subplots=True,
				layer='below',
				line_dash='dot', #solid dot dash longdash dashdot longdashdot
				line_width=3
			)
	elif (value == 'Midterm Election'):		
		midtermElections = ["2022-11-8", "2018-11-6", "2014-11-4", "2010-11-2", "2006-11-7"]
		for i in midtermElections:
			fig.add_shape(type='line',
				opacity=0.75,
				x0=i,
				y0=0,
				x1=i,
				y1=1,
				#y1=max(df[df['Date'] == "{}-01-01".format(i)]['Republicans'].max(), df[df['Date'] == "{}-01-01".format(i)]['Democrats'].max(), df[df['Date'] == "{}-01-01".format(i)]['Unaffiliated'].max()),
				line=dict(color='White'), #color='rgba(50,50,75,0.9)'),
				xref='x',
				yref='paper',
				#text_annotation="January 1st, {} Voter Roll Purge".format(i),
				exclude_empty_subplots=False,
				layer='above',
				line_dash='dot', #solid dot dash longdash dashdot longdashdot
				line_width=2
		)
	elif (value == 'Voter Roll Purge'):
		for i in range(2005, 2026, 2):
			#if math.isnan(max(df[df['Date'] == "{}-01-01".format(i)]['Republicans'].max(), df[df['Date'] == "{}-01-01".format(i)]['Democrats'].max(), df[df['Date'] == "{}-01-01".format(i)]['Unaffiliated'].max())):
			#	interpolate("{}-01-01".format(i), "Republicans", "Democrats", "Unaffiliated", "Libertarians")

			fig.add_shape(type='line',
				opacity=0.75,
				x0="{}-01-01".format(i),
				y0=0,
				x1="{}-01-01".format(i),
				y1=1,
				#y1=max(df[df['Date'] == "{}-01-01".format(i)]['Republicans'].max(), df[df['Date'] == "{}-01-01".format(i)]['Democrats'].max(), df[df['Date'] == "{}-01-01".format(i)]['Unaffiliated'].max()),
				line=dict(color='Orange'), #color='rgba(50,50,75,0.9)'),
				xref='x',
				yref='paper',
				#text_annotation="January 1st, {} Voter Roll Purge".format(i),
				exclude_empty_subplots=True,
				layer='below',
				line_dash='longdashdot', #solid dot dash longdash dashdot longdashdot
				line_width=2
			)
	return fig	

@app.callback(
		Output(component_id='my-graph', component_property = 'figure'),
		Input('dataFrame', 'value'),
		Input('annotations', 'value'),
		Input('partyDataset', 'value'),
		Input('raceDataset', 'value'),
		Input('sexDataset', 'value'),
		Input('percent', 'value')
	)
def update_graph(dataFrame, annotations, partyDataset, raceDataset, sexDataset, percent):
	#print(dataFrame)
	#datasets = filter(None, partyDataset + raceDataset + sexDataset)
	#datasets = [x[0] for x in (partyDataset, raceDataset)]
	#datasets = [x for x in (raceDataset, partyDataset, sexDataset) if x]
	#datasets += [x for x in sexDataset if not None]
	#datasets = filter(None, partyDataset)
	#datasets += filter(None, raceDataset)
	#datasets += filter(None, sexDataset)
	def update_title(value):
		if (value == 'Statewide'):
			return 'North Carolina Voter Registration Statistics'
		else:
			return string.capwords(u'{} County Voter Registration Statistics'.format(value))
	if (dataFrame is None):
		dataFrame = 'Statewide'
	if (dataFrame == 'Statewide'):
		df = pd.read_csv("{}/alpha.csv".format(directory))
	else:
		if (directory == gitRepo):        ##Fix for the county (New Hanover) that has a space in the name
			df = pd.read_csv("{}/{}/{}.csv".format(directory, dataFrame.replace(" ", "%20"), dataFrame.replace(" ", "%20")))
		else:
			df = pd.read_csv("{}/{}/{}.csv".format(directory, dataFrame, dataFrame))
	#traces = [update_trace(x, df, percent) for x in {datasets}]
	
	if (partyDataset is not None):
		traces = [update_trace(x, df, percent) for x in partyDataset]
	if (raceDataset is not None):
		traces += [update_trace(x, df, percent) for x in raceDataset]
	if (sexDataset is not None):
		traces += [update_trace(x, df, percent) for x in sexDataset]

	data = traces

	layout = go.Layout(
		uirevision = '1', # keep zoom when changing dropdown datasets
		title=dict(
			text=update_title(dataFrame),
			xanchor='center',
			x=0.5,
			font=dict(
				size=30
			)
		),
		#xaxis = {'showgrid': True},
		#yaxis = {'showgrid': False},
		xaxis = dict(
			# title = "Dates",
			linecolor = "#BCCCDC",  # Sets color of X-axis line
			showgrid = False,  # Removes X-axis grid lines
			zeroline = False, # thick line at x=0
			showline = False, #removes X-axis line
			showticklabels=True, # axis ticklabels
			visible = True,  # numbers below

			showspikes = True,  #shows vertical line on hover
			spikemode  = 'toaxis+across',   #shows vertical line on hover
			spikesnap = 'cursor',
			
			spikedash = 'solid', #shows vertical line on hover
			spikecolor = "rgba(10,10,10,0.7)",
			spikethickness = 1,
			gridcolor=gridcolor,
			nticks=29,
			tickfont_size=16,
			type='date',
			hoverformat='<b>%b %d, %Y</b>'
		),
		yaxis = dict(
			# title="Price",  
			linecolor="#BCCCDC",  # Sets color of Y-axis line
			gridcolor = gridcolor,
			showgrid= True,  # Removes Y-axis grid lines  
			zeroline = False, # thick line at x=0
			showline = False, #removes Y-axis line
			showspikes = False,
			showticklabels=True, # axis ticklabels
			visible = True,  # numbers below
			tickfont_size = 16
		),
		#font=dict(  #axis'
			#family='Nunito Sans',
			#size=20,
			#color='rgba(200,200,200,0.8)'
		#),
		showlegend = False,
		hoverdistance = -1,
		hoverlabel=dict(
			bgcolor='rgba(20,20,20,0.85)',
			font=dict(
				family='Nunito Sans',
				size=18,
				#color='rgba(200,200,220,1)'
			)
		),
		hovermode='x unified',
		xaxis_tickangle=-45,
		#xaxis_color='rgba(200,200,200,0.7)',  #font for years
		#yaxis_color='rgba(200,200,200,0.7)',  #font for Number
		paper_bgcolor='rgba(20,20,30,0)',
		#paper_bgcolor='rgba(200,200,210,0.9)',
		plot_bgcolor='rgba(210,210,220,0)',
		#plot_bgcolor='rgba(50,50,75,0.9)',
		legend=dict(
			xanchor='left',
			yanchor='bottom',
			x=0.01,
			y=0.02,
			font=dict(
				family = 'Nunito Sans',
				size=14,
				#color='rgba(255,255,255,0.98)'
			),
			bgcolor='rgba(220,220,220,0.75)',
			#bordercolor='Black',
			borderwidth=2
		)
		#yaxis_range=[15, 49]
	)
	fig = go.Figure(data=data, layout=layout)

	#fig.layout.plot_bgcolor = 'black'
	#fig.layout.paper_bgcolor = 'black'
	#fig.layout.template = 'presentation'
	if (annotations):
		[draw_annotations(a, fig) for a in annotations]
	if (percent):
		fig.update_yaxes(gridcolor=gridcolor, mirror='ticks', tickfont_size=18, tickformat= '.0%')
		#fig.update_traces(customdata=df['Date'], hovertemplate='%{customdata|%b %d %Y}<br>%{y:.02%}<extra></extra>')
		fig.update_traces(hovertemplate='%{y:.02%}')
	else:
		fig.update_yaxes(gridcolor=gridcolor, mirror='ticks', tickfont_size=18)#, tickformat='%{y:,}')
		fig.update_traces(hovertemplate='%{y:,}')
		
	#fig['layout']['uirevision'] = '1'
	return fig
	
	#if ((ctx.triggered_id == 'dataFrame') or (ctx.triggered_id == None)):
	#elif (ctx.triggered_id == 'annotations'):
	#	return [draw_annotations(a) for a in values2]

if __name__ == '__main__':
	serve(app.server, host="0.0.0.0", port=12223, threads=96)
    #app.run_server(debug=False, use_reloader = True)