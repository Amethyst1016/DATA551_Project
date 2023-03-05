import pandas as pd
import plotly.graph_objects as go
import dash
from dash import html
from dash import dcc
from dash.dependencies import Input, Output
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# Load data for multiple global indices
df = pd.read_csv('data/Global_index.csv')
df['date'] = pd.to_datetime(df['date'])
df.set_index('date', inplace=True)

# Interpolate null values
df = df.interpolate()

symbols = df.columns

def moving_average(df, symbol, window_size):
      ma = df[symbol].rolling(window=window_size).mean()
      return ma

app = dash.Dash(__name__)

app.layout = html.Div(
      [
            dcc.Dropdown(
                  id='symbol-dropdown',
                  options=[{'label': symbol, 'value': symbol} for symbol in symbols],
                  value='S&P_original'
            ),
            dcc.Dropdown(
                  id='compare-dropdown',
                  options=[{'label': symbol, 'value': symbol} for symbol in symbols],
                  value='FTSE_100'
            ),
            dcc.RadioItems(
                  id='moving-average-radio',
                  options=[
                        {'label': 'None', 'value': 0},
                        {'label': '7 Days', 'value': 7},
                        {'label': '15 Days', 'value': 15},
                        {'label': '30 Days', 'value': 30},
                  ],
                  value=0
            ),
            dcc.Graph(id='line-chart', figure={}),
      ]
)

@app.callback(Output('line-chart', 'figure'), [Input('symbol-dropdown', 'value'), Input('compare-dropdown', 'value'), Input('moving-average-radio', 'value')])
def update_line_chart(symbol, compare_symbol, moving_average_window):
      fig = make_subplots(specs=[[{"secondary_y": True}]])
      
      # Add trace for selected index
      fig.add_trace(go.Scatter(x=df.index, y=df[symbol], name=symbol), secondary_y=False)

      # Add trace for comparison index
      fig.add_trace(go.Scatter(x=df.index, y=df[compare_symbol], name=compare_symbol), secondary_y=True)

      if moving_average_window != 0:
            # Add trace for selected index moving average
            ma = moving_average(df, symbol, moving_average_window)
            fig.add_trace(go.Scatter(x=df.index, y=ma, name='{}-Day Moving Average ({})'.format(moving_average_window, symbol)), secondary_y=False)

            # Add trace for comparison index moving average
            ma_compare = moving_average(df, compare_symbol, moving_average_window)
            fig.add_trace(go.Scatter(x=df.index, y=ma_compare, name='{}-Day Moving Average ({})'.format(moving_average_window, compare_symbol)), secondary_y=True)

      fig.update_layout(
            height=600,
            width=1000,
            xaxis=dict(title='Date'),
            yaxis=dict(title=symbol),
            yaxis2=dict(title=compare_symbol, overlaying='y', side='right'),
            hovermode='x',
      )

      return fig


if __name__ == "__main__":
      app.run_server(debug=True)