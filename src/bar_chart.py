import dash
from dash import html
from dash import dcc
from dash.dependencies import Input, Output, State
import pandas as pd
import plotly.graph_objs as go

df = pd.read_csv('data/SP500_merged.csv')
df = df[df['Symbol'] != 'GEHC']
# GEHC only have 44 values, if we want to know the data for past 1 year, for each Symbol at least have 360 values

sector_name = df['GICS Sector'].unique().tolist()
sector_symbol = []
for i in sector_name:
      sector_symbol.append(df[df['GICS Sector']==i]['Symbol'].unique().tolist())

def growth_rate(duration, df):
      df['Date'] = pd.to_datetime(df['Date'])
      end_date = df['Date'].max()
      start_date = end_date - pd.DateOffset(days=duration)
      dff = df[df['Date'].between(start_date, end_date)]
      sector_growth_rate = dff.groupby('GICS Sector')['Close'].apply(lambda x: x.iloc[-1] / x.iloc[0] - 1).reset_index(name='growth_rate')
      return sector_growth_rate


app = dash.Dash(__name__)

app.layout = html.Div([
      html.H2("Sector Growth Rates"),
      html.Div([
            html.Label("Duration:"),
            dcc.Dropdown(
                  id="duration",
                  options=[
                  {"label": "Past week", "value": 7},
                  {"label": "Past month", "value": 30},
                  {"label": "Past quarter", "value": 90},
                  {"label": "Past half year", "value": 180},
                  {"label": "Past year", "value": 360},
                  ],
                  value=7,
                  clearable=False,
            ),
      ], style={"width": "25%", "display": "inline-block"}),
      html.Div(id='output-container', children=[]),
])

@app.callback(
      Output(component_id='output-container', component_property='children'),
      [Input(component_id='duration', component_property='value')]
)
def update_output(duration):
      sector_growth_rate = growth_rate(duration, df)
      fig = go.Figure(data=[
            go.Bar(
                  x=sector_growth_rate['GICS Sector'], 
                  y=sector_growth_rate['growth_rate'], 
                  marker_color=sector_growth_rate['growth_rate'].apply(lambda x: 'green' if x > 0 else 'red')
            )
      ])
      fig.update_layout(
            title='Sector Growth Rates',
            xaxis_title='Sector',
            yaxis_title='Growth Rate',
            xaxis={'categoryorder':'total descending'}
      )
      return dcc.Graph(
            id='example-graph',
            figure=fig
      )

if __name__ == '__main__':
      app.run_server(debug=True)
