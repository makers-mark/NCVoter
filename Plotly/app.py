# Run this app with `python app.py` and
# visit http://127.0.0.1:8050/ in your web browser.

from dash import Dash, html, dcc, Input, Output, ctx
import dash
import dash_bootstrap_components as dbc
from dash_bootstrap_templates import load_figure_template
import plotly.express as px
import pandas as pd
import plotly.graph_objects as go
import os

load_figure_template('LUX')

gitRepo = 'https://raw.githubusercontent.com/makers-mark/NCVoter/main/Data/'
localRepo = 'c:\\ncvoter\\Data'

app = dash.Dash(external_stylesheets=[dbc.themes.LUX])

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
		'fillcolor': 'rgba(255,255,255,{})'.format(traceOpacity),
		'tracecolor': 'white'
	},
	'Green': {
		'fillcolor': 'rgba(20,155,20,{})'.format(traceOpacity),
		'tracecolor': 'green'
	},
	'White': {
		'fillcolor': 'rgba(100,100,100,{})'.format(traceOpacity),
		'tracecolor': 'rgba(40,40,40,1)'
	},
	'Black': {
		'fillcolor': 'rgba(0,0,0,{})'.format(traceOpacity),
		'tracecolor': 'rgba(0,0,0,1)'
	},
	'AmericanIndian': {
		'fillcolor': 'rgba(255,0,0,{})'.format(traceOpacity),
		'tracecolor': 'red'
	},
	'NativeHawaiian': {
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
	'UndisclosedGender': {
		'fillcolor': 'rgba(20,155,20,{})'.format(traceOpacity),
		'tracecolor': 'green'
	}
}

#directory = localRepo
directory = gitRepo

width=3
gridcolor='rgba(100,100,100,0.8)'
title=''
percent=False

#counties = [ f.name.title() for f in os.scandir(directory) if f.is_dir() ]
counties = ['ALAMANCE', 'ALEXANDER', 'ALLEGHANY', 'ANSON', 'ASHE', 'AVERY', 'BEAUFORT', 'BERTIE', 'BLADEN', 'BRUNSWICK', 'BUNCOMBE', 'BURKE', 'CABARRUS', 'CALDWELL', 'CAMDEN', 'CARTERET', 'CASWELL', 'CATAWBA', 'CHATHAM', 'CHEROKEE', 'CHOWAN', 'CLAY', 'CLEVELAND', 'COLUMBUS', 'CRAVEN', 'CUMBERLAND', 'CURRITUCK', 'DARE', 'DAVIDSON', 'DAVIE', 'DUPLIN', 'DURHAM', 'EDGECOMBE', 'FORSYTH', 'FRANKLIN', 'GASTON', 'GATES', 'GRAHAM', 'GRANVILLE', 'GREENE', 'GUILFORD', 'HALIFAX', 'HARNETT', 'HAYWOOD', 'HENDERSON', 'HERTFORD', 'HOKE', 'HYDE', 'IREDELL', 'JACKSON', 'JOHNSTON', 'JONES', 'LEE', 'LENOIR', 'LINCOLN', 'MACON', 'MADISON', 'MARTIN', 'MCDOWELL', 'MECKLENBURG', 'MITCHELL', 'MONTGOMERY', 'MOORE', 'NASH', 'NEW HANOVER', 'NORTHAMPTON', 'ONSLOW', 'ORANGE', 'PAMLICO', 'PASQUOTANK', 'PENDER', 'PERQUIMANS', 'PERSON', 'PITT', 'POLK', 'RANDOLPH', 'RICHMOND', 'ROBESON', 'ROCKINGHAM', 'ROWAN', 'RUTHERFORD', 'SAMPSON', 'SCOTLAND', 'STANLY', 'STOKES', 'SURRY', 'SWAIN', 'TRANSYLVANIA', 'TYRRELL', 'UNION', 'VANCE', 'WAKE', 'WARREN', 'WASHINGTON', 'WATAUGA', 'WAYNE', 'WILKES', 'WILSON', 'YADKIN', 'YANCEY']



dropdownList = [{'label': x.title() + ' County', 'value': x } for x in counties]
dropdownList.insert(0, {'label': 'Statewide', 'value': 'Statewide'})

SIDEBAR_STYLE = {
    "position": "fixed",
    "top": 0,
    "left": 0,
    "bottom": 0,
    "width": "24rem",
    "padding": "2rem 1rem",
	"backgroundColor": "#eeeeee"
}

sidebar = html.Div(
    [
        html.H4(id='title'),
        html.Hr(),
        dbc.Nav(
            [
				dcc.Dropdown(
					dropdownList,
					'Statewide',
					id = "dataFrame"
				),html.Hr(),
				html.H4('Annotations'),
				dcc.Checklist(
					['Federal Election', 'Midterm Election', 'Voter Roll Purge'],
					inline=False,
					id='annotations'
				), html.Hr(),
				html.H4('Party'),
				dcc.Checklist(
					['Republicans', 'Democrats', 'Unaffiliated', 'Libertarians', 'Green'],
					value = ['Republicans', 'Democrats', 'Unaffiliated'],
					inline=False,
					id='partyDataset'
				), html.Hr(),
				html.H4('Race'),
				dcc.Checklist(
					[
						{'label': 'White', 'value': 'White'},
						{'label': 'Black', 'value': 'Black'},
						{'label': 'Other', 'value': 'Other'},
						{'label': 'American Indian', 'value': 'AmericanIndian'},
						{'label': 'Native Hawaiian', 'value': 'NativeHawaiian'}, 
						{'label': 'Hispanic', 'value': 'Hispanic'}
					],
					inline=False,
					id='raceDataset'
				), html.H4(),
				html.H4('Sex'),
				dcc.Checklist(
					[
						{'label': 'Male', 'value': 'Male'}, 
						{'label': 'Female', 'value': 'Female'},
						{'label': 'Undisclosed Gender', 'value': 'UndisclosedGender'}
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
			pills=True,
		),
	],
	style=SIDEBAR_STYLE,
)

app.layout = html.Div(children=[

	dbc.Row(
		[dbc.Col(sidebar),
		dbc.Col(dcc.Graph(id='my-graph'), width = 10, style = {'padding':'0px', 'marginLeft':'1px', 'marginTop':'10px','marginRight':'0px'})
		]
	)

])

@app.callback(
	Output(component_id='title', component_property='children'),
	Input('dataFrame', 'value'))
def update_title(values):
	if (values == 'Statewide'):
		return 'North Carolina Voter Registration Statistics'
	else:
		return u'{} County Voter Registration Statistics'.format(values)

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
		presidentialElections = ["2020-11-3", "2016-11-6", "2012-11-6", "2008-11-4", "2004-11-2"]
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
				line_width=1
		)
	elif (value == 'Voter Roll Purge'):
		for i in range(2005, 2025, 2):
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
				line_width=1
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
	#print(ctx.triggered_id)
	#print('Triggered id is ' + ctx.triggered_id)

	traces = []
	#print('dataFrame triggered_id')
	if (dataFrame == 'Statewide'):
		df = pd.read_csv("{}/alpha.csv".format(directory))
	else:
		#values = values.replace(" County", "")
		df = pd.read_csv("{}/{}/{}.csv".format(directory, dataFrame, dataFrame))

	if (partyDataset is not None):
		traces = [update_trace(x, df, percent) for x in partyDataset]
	if (raceDataset is not None):
		traces += [update_trace(x, df, percent) for x in raceDataset]
	if (sexDataset is not None):
		traces += [update_trace(x, df, percent) for x in sexDataset]

	data = traces

	layout = go.Layout(
		title=dict(
			text=title,
			xanchor='center',
			x=0.5
		),
		xaxis = {'showgrid': False},
		yaxis = {'showgrid': False},
		font=dict(
			family='Courier New',
			size=24,
			#color='rgba(200,200,200,0.8)'
		),
		showlegend = True,
		hoverlabel=dict(
			#bgcolor='rgba(50,50,50,0.75)',
			font=dict(
				family='Courier New',
				size=16,
				#color='rgba(200,200,220,1)'
			)
		),
		hovermode='x unified',
		xaxis_tickangle=-45,
		#xaxis_color='rgba(200,200,200,0.7)',  #font for years
		#yaxis_color='rgba(200,200,200,0.7)',  #font for Number
		#paper_bgcolor='rgba(20,20,30,0.9)',
		#paper_bgcolor='rgba(200,200,210,0.9)',
		#plot_bgcolor='rgba(210,210,220,0.9)',
		#plot_bgcolor='rgba(50,50,75,0.9)',
		legend=dict(
			xanchor='left',
			yanchor='top',
			x=0,
			y=0.2,
			font=dict(
				family='Courier New',
				size=16,
				#color='rgba(255,255,255,0.98)'
			),
			#bgcolor='rgba(50,50,50,0.5)',
			#bordercolor='Black',
			borderwidth=2
		)
		#yaxis_range=[15, 49]
	)
	fig = go.Figure(data=data, layout=layout)

	fig.update_xaxes(
		gridcolor=gridcolor,
		nticks=29,
		tickfont_size=18,
		type='date',
		hoverformat='<i><b>%b %d, %Y</b></i>'
	)

	#fig.layout.plot_bgcolor = 'black'
	#fig.layout.paper_bgcolor = 'black'
	fig.layout.template = 'presentation'
	if (annotations):
		[draw_annotations(a, fig) for a in annotations]
	if (percent):
		fig.update_yaxes(gridcolor=gridcolor, mirror='ticks', tickfont_size=18, tickformat= '.0%')
		#fig.update_traces(customdata=df['Date'], hovertemplate='%{customdata|%b %d %Y}<br>%{y:.02%}<extra></extra>')
		fig.update_traces(hovertemplate='%{y:.02%}')
	else:
		fig.update_yaxes(gridcolor=gridcolor, mirror='ticks', tickfont_size=18)#, tickformat='%{y:,}')
		fig.update_traces(hovertemplate='%{y:,}')
		
	return fig
	
	#if ((ctx.triggered_id == 'dataFrame') or (ctx.triggered_id == None)):
	#elif (ctx.triggered_id == 'annotations'):
	#	return [draw_annotations(a) for a in values2]

if __name__ == '__main__':
    app.run_server(debug=True)