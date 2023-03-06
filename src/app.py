import dash
from dash import html, dcc
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output
import altair as alt
from plotly.subplots import make_subplots
import plotly.graph_objects as go
from data_processing import *

# get data
df_line_chart = get_daily_data()

# general info
df_compare = select_time_range(df_line_chart.dropna(), 2)
cols = df_compare.columns.tolist()[1:]
growth_rates = {}
for i in cols:
    ls = df_compare[i].tolist()
    growth_rates[i] = round((ls[1]-ls[0])/ls[0]*100, 4)

df_line_chart['Date'] = pd.to_datetime(df_line_chart['Date'])
df_line_chart.set_index('Date', inplace=True)
# Interpolate null values
df_line_chart = df_line_chart.interpolate()
df_line_chart.reset_index(inplace=True)
df_line_chart.rename({'index':'Date'})
symbols = df_line_chart.columns

df_bar_chart = pd.read_csv('SP500_merged.csv', parse_dates=['Date'])
df_bar_chart = df_bar_chart[df_bar_chart['Symbol'] != 'GEHC']

# Define a function to subset the original df to only include the top 5 companies in each sector
def top_5_company(time_range, df):
    df_selected = select_time_range(df, time_range)
    company_growth_rate = df_selected.groupby(['GICS Sector', 'Symbol']).apply(lambda x: (x['Close'].iloc[-1] - x['Close'].iloc[0])/x['Close'].iloc[0]).reset_index(name='Growth Rate')

    # Filter the top 5 companies in each sector
    top_5 = company_growth_rate.groupby('GICS Sector').apply(lambda x: x.nlargest(5, 'Growth Rate'))
    top_5 = top_5.reset_index(drop=True)

    # Obtain the symbol of top 5 companies in each sector
    top_5_symbol = top_5['Symbol'].unique().tolist()

    # Subset the df to only include the top 5 companies in each sector
    df_top_5 = df_selected[df_selected['Symbol'].isin(top_5_symbol)]

    return df_top_5


# css
app = dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])
US_Market = {'font-size': '15px', 'text-align':'left', 'color':'#036d90', 'margin-left':'20px'}
other_Market = {'font-size': '15px', 'text-align':'left', 'margin-left':'20px'}
labels = {'display':'inline', 'font-size':'20px', 'margin-left':'5px'}
page_height = '100vh'

app.layout = html.Div([
    # left part
    html.Div([
        # growth rate info
        html.Div([
            html.P('Growth Rate Summary\n of '+str(df_compare['Date'].max())[:10], style={'font-size': '25px', 'text-align':'center'}),
            html.P('US Market', style=US_Market),
            html.P(f'- SP500: {growth_rates[cols[0]]}%', style=US_Market),
            html.P(f'- SP500 Energy: {+growth_rates[cols[1]]}%', style=US_Market),
            html.P(f'- SP500 Industry: {+growth_rates[cols[2]]}%', style=US_Market),
            html.P(f'- SP500 Consumer: {+growth_rates[cols[3]]}%', style=US_Market),
            html.P('London Market', style=other_Market),
            html.P(f'- FTSE_100: {+growth_rates[cols[4]]}%', style=other_Market),
            html.P('Europe Market', style=other_Market),
            html.P(f'- Euro_Stoxx_50: {+growth_rates[cols[5]]}%', style=other_Market),
            html.P('Hong Kong Market', style=other_Market),
            html.P(f'- HANG_SENG: {+growth_rates[cols[6]]}%', style=other_Market),
            html.P('Toyko Market', style=other_Market),
            html.P(f'- Nikkei_225: {+growth_rates[cols[7]]}%', style=other_Market),
        ], style={'border-style':'solid', 'border-color':'#a1979e', 'margin':'10px'}),
        # radio
        html.Div([
            dcc.RadioItems(
                id='time_range_selector',
                options=[
                    {'label':html.P(['Last 7 Days'], style=labels), 'value':7},
                    {'label':html.P(['Last 30 Days'], style=labels), 'value':30},
                    {'label':html.P(['Last 90 Days'], style=labels), 'value':90},
                    {'label':html.P(['Last 180 Days'], style=labels), 'value':180},
                    {'label':html.P(['Last Year'], style=labels), 'value':365}
                ], value=7, labelStyle={'display': 'block'}
            )
        ], style={'margin':'20px'})
    ], style={'width':'20%', 'height':'100%', 'float':'left', 'margin':'0px', 'background':'#e1edd5'}),
    # right part
    html.Div([
        dbc.Tabs([
            # tab 1 -  Stock markets compare trend plot
            dbc.Tab(html.Div([
                html.Div([
                    html.Div([
                        dcc.Dropdown(
                            id='symbol-dropdown',
                            options=[{'label': symbol, 'value': symbol} for symbol in symbols],
                            value='S&P_original',
                            style={'width': '200px', 'float':'left'}),
                        dcc.Dropdown(
                            id='compare-dropdown',
                            options=[{'label': symbol, 'value': symbol} for symbol in symbols],
                            value='FTSE_100',
                            style={'width': '200px', 'float':'left'})
                    ], style={'height':'10%'}),
                    dcc.Graph(id='line-chart', figure={}, style={'height':'90%'})
                ], style={'width':'100%', 'height':'90vh'})
            ]), label='Stock markets compare trend plot'),
            # tab 2 - SP500 sectors growth rate rank
            dbc.Tab(html.Div([
                html.Div([
                    html.Div(id='bar-chart', children=[])
                ], style={'width':'100%', 'height':'90vh'})
            ]), label='SP500 sectors growth rate rank'),
            # tab 3 - 
            dbc.Tab(html.Div([
                html.Div([
                    dcc.Dropdown(
                        id='dropdown_sector',
                        options=[],
                        value=[],
                        style={'width':'300px', 'float':'left'}),
                    dcc.Checklist(
                        id='checkbox_company',
                        options=[],
                        value=[],
                        style={'float':'left', 'margin-left':'10px'}),
                ], style={'width':'100%', 'display':'inline-block'}),
                html.Div([
                    html.Iframe(
                        id='scatter', style={'width': '100%', 'height': '70vh', 'margin-left':'10%', 'margin-top':'10%'})
                ], style={'width':'50%', 'height':'90vh', 'float':'left'}),
                html.Div([
                    html.Iframe(
                        id='pie', style={'width': '100%', 'height': '70vh', 'margin-left':'10%', 'margin-top':'10%'})
                ], style={'width':'50%', 'height':'90vh', 'float':'right'})
            ]), label='Top 5 companies in SP500 GICS sectors')
        ])
    ], style={'width':'80%', 'height':'100%', 'float':'right', 'margin':'0px'})
], style={'height':page_height, 'margin':'0px'})

@app.callback(Output('line-chart', 'figure'), 
    [Input('symbol-dropdown', 'value'), 
     Input('compare-dropdown', 'value'),
     Input('time_range_selector', 'value')])
def update_line_chart(symbol, compare_symbol, time_range):
    df_selected = select_time_range(df_line_chart, time_range)
    fig = make_subplots(specs=[[{"secondary_y": True}]])
    # Add trace for selected index
    fig.add_trace(go.Scatter(x=df_selected['Date'], y=df_selected[symbol], name=symbol), secondary_y=False)
    # Add trace for comparison index
    fig.add_trace(go.Scatter(x=df_selected['Date'], y=df_selected[compare_symbol], name=compare_symbol), secondary_y=True)

    fig.update_layout(
        xaxis=dict(title='Date'),
        yaxis=dict(title=symbol, 
                    showgrid=False),
        yaxis2=dict(title=compare_symbol, 
                            overlaying='y', 
                            side='right'),
        hovermode='x',
        title='{} vs {} Price'.format(symbol, compare_symbol),
    )
    return fig

@app.callback(Output('bar-chart', 'children'),
    [Input('time_range_selector', 'value')])
def update_output(time_range):
    df_selected = select_time_range(df_bar_chart, time_range)
    sector_growth_rate = df_selected.groupby('GICS Sector')['Close'].apply(lambda x: x.iloc[-1] / x.iloc[0] - 1).reset_index(name='growth_rate')
    fig = go.Figure(data=[
        go.Bar(x=sector_growth_rate['GICS Sector'], 
               y=sector_growth_rate['growth_rate'], 
               marker_color=sector_growth_rate['growth_rate'].apply(lambda x: 'green' if x > 0 else 'red'))])
    fig.update_layout(
        title='Sector Growth Rates',
        xaxis_title='Sector',
        yaxis_title='Growth Rate',
        xaxis={'categoryorder':'total descending'})
    return dcc.Graph(
        id='example-graph',
        figure=fig)

@app.callback(
    Output('dropdown_sector', 'options'),
    [Input('time_range_selector', 'value')]
)
def update_company_options(time_range):
    df_top_5 = top_5_company(time_range, df_bar_chart)
    sectors = df_top_5['GICS Sector'].unique().tolist()
    options = [{'label': sector, 'value': sector} for sector in sectors]
    return options

@app.callback(
    Output('dropdown_sector', 'value'),
    [Input('time_range_selector', 'value')]
)
def update_company_options(time_range):
    df_top_5 = top_5_company(time_range, df_bar_chart)
    sectors = df_top_5['GICS Sector'].unique().tolist()
    return sectors[0]

# Define the callback to update the options of the checkbox based on the selected sector
@app.callback(
    Output('checkbox_company', 'options'),
    [Input('dropdown_sector', 'value'),
     Input('time_range_selector', 'value')]
)
def update_company_options(selected_sector, time_range):
    df_top_5 = top_5_company(time_range, df_bar_chart)
    df_top_5_selected_sector = df_top_5[df_top_5['GICS Sector'] == selected_sector]
    top_5_symbol = df_top_5_selected_sector['Symbol'].unique().tolist()
    options = [{'label': symbol, 'value': symbol} for symbol in top_5_symbol]
    return options

@app.callback(
    Output('checkbox_company', 'value'),
    [Input('dropdown_sector', 'value'),
     Input('time_range_selector', 'value')]
)
def update_company_options(selected_sector, time_range):
    df_top_5 = top_5_company(time_range, df_bar_chart)
    df_top_5_selected_sector = df_top_5[df_top_5['GICS Sector'] == selected_sector]
    top_5_symbol = df_top_5_selected_sector['Symbol'].unique().tolist()
    return top_5_symbol

# Define the callback to update the graph based on the selected sector and companies
@app.callback(
    Output('scatter', 'srcDoc'),
    [Input('dropdown_sector', 'value'),
     Input('checkbox_company', 'value'),
     Input('time_range_selector', 'value')]
)
def update_trend_line(selected_sector, selected_companies, time_range):
    df_top_5 = top_5_company(time_range, df_bar_chart)

    df_top_5_selected_sector = df_top_5[df_top_5['GICS Sector'] == selected_sector]
    df_top_5_selected_sector['Date'] = df_top_5_selected_sector['Date'].astype(str).str[:10]
    df_top_5_selected_sector['Date'] = pd.to_datetime(df_top_5_selected_sector['Date'], format='%Y-%m-%d')
    if not selected_companies:
        # If no companies are selected, return an empty dataframe
        df_top_5_selected_sector_company = pd.DataFrame(columns=df_top_5.columns)
    else:
        # Filter the dataframe based on the selected companies
        df_top_5_selected_sector_company = df_top_5_selected_sector[
            df_top_5_selected_sector['Symbol'].isin(selected_companies)]

    chart = alt.Chart(df_top_5_selected_sector_company).mark_line().encode(
        x='Date:T',
        y='Close:Q',
        color='Symbol:N',
        tooltip=['Symbol:N', 'Close:Q']
    ).properties(
        title='Top 5 Companies by Growth Rate'
    ).interactive()
    return chart.to_html()

# Define the callback to update the graph based on the selected sector
@app.callback(Output('pie', 'srcDoc'),
    [Input('dropdown_sector', 'value'),
     Input('time_range_selector', 'value')])
def update_pie_chart(selected_sector, time_range):
    df_top_5 = top_5_company(time_range, df_bar_chart)

    df_top_5_selected_sector = df_top_5[df_top_5['GICS Sector'] == selected_sector]
    df_top_5_selected_sector['Date'] = df_top_5_selected_sector['Date'].astype(str).str[:10]
    df_top_5_selected_sector['Date'] = pd.to_datetime(df_top_5_selected_sector['Date'], format='%Y-%m-%d')

    df_summary = df_top_5_selected_sector.groupby('Symbol', as_index=False).sum('Volume')
    df_summary['Proportion'] = df_summary['Volume']/sum(df_summary['Volume'])
    chart = alt.Chart(df_summary).mark_arc().encode(
        color='Symbol:N',
        theta='Volume:Q',
        tooltip=['Symbol:N', 'Volume:Q', 'Proportion:Q']
    ).properties(
        title='Top 5 Companies Volume Proportion'
    ).configure_view(
        strokeWidth=0
    )
    return chart.to_html()

if __name__ == '__main__':
    app.run_server(debug=True)