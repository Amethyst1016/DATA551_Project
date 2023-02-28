import dash
from dash import html
from dash import dcc
from dash.dependencies import Input, Output
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd

# Load data for a given symbol
def get_stock_data(symbol):
      file_path = '/Users/gawain/Desktop/3.UBC/Block5/Data551-Dataviz_II/Python+Dash快速web应用开发/SP500_merged.csv'
      df = pd.read_csv(file_path)
      df = df[df['Symbol'] == symbol]
      df = df[['Date', 'Close']]
      return df

# Load SP500 data
def get_Sp500_data():
      sp500_file_path = '/Users/gawain/Desktop/3.UBC/Block5/Data551-Dataviz_II/Python+Dash快速web应用开发/SP500_2010_2023.csv'
      sp500_df = pd.read_csv(sp500_file_path, )
      sp500_df.rename(columns={'date': 'Date'}, inplace=True)
      sp500_df = sp500_df[['Date', 'Close']]
      sp500_df.rename(columns={'Close': 'SP500 Close'}, inplace=True)
      return sp500_df

sp500_df = get_Sp500_data()

# Load data for multiple symbols
symbols = ['MMM', 'AAPL', 'GOOG']  # List of symbols to load
dfs = {symbol: get_stock_data(symbol) for symbol in symbols}  # Dictionary of DataFrames for each symbol

# Create line chart with multiple lines
fig = go.Figure()
fig.add_trace(go.Scatter(x=sp500_df['Date'], y=sp500_df['SP500 Close'], name='SP500'))

app = dash.Dash(__name__)

app.layout = html.Div(
      [
            dcc.Dropdown(
                  id='symbol-dropdown',
                  options=[{'label': symbol, 'value': symbol} for symbol in symbols],
                  value=symbols[0]
            ),
            dcc.Graph(id='line-chart', figure=fig),
      ]
)

@app.callback(Output('line-chart', 'figure'), [Input('symbol-dropdown', 'value')])
def update_line_chart(symbol):
      df = get_stock_data(symbol)
      fig = go.Figure()
      fig.add_trace(go.Scatter(x=sp500_df['Date'], 
                                    y=sp500_df['SP500 Close'], 
                                    name='SP500'),
                                    )
      fig.add_trace(go.Scatter(x=df['Date'], 
                                    y=df['Close'], 
                                    name=symbol, 
                                    yaxis='y2'),
                                    )
      
      fig.update_layout(
            height=600,
            width=1000,
            yaxis=dict(title='SP500 Close'),
            yaxis2=dict(
                  title=symbol,
                  overlaying='y',
                  side='right',
                  range=[0, df['Close'].max()*1.2],
                  showgrid=False, # remove grid lines for the second x-axis
            ),

      )

      return fig

if __name__ == "__main__":
      app.run_server(debug=True)
