import dash
from dash import html
from dash import dcc
from dash.dependencies import Input, Output
import altair as alt
import dash_bootstrap_components as dbc
import pandas as pd


# Read in global data
df = pd.read_csv('data/SP500_merged.csv')
df = df[df['Symbol'] != 'GEHC']
# GEHC only have 44 values, if we want to know the data for past 1 year, for each Symbol at least have 360 values

sector_name = df['GICS Sector'].unique().tolist()
sector_symbol = df['Symbol'].unique().tolist()


# Define a function to calculate the growth rate of each company (sector_symbol) in each sector (sector_name)
def growth_rate_company(duration, df):
    # duration: number of days to calculate the growth rate
    # df: the dataframe to be used
    df['Date'] = pd.to_datetime(df['Date'], utc=True)
    end_date = df['Date'].max()
    start_date = end_date - pd.DateOffset(days = duration)
    dff = df[df['Date'].between(start_date, end_date)]

    # Calculate the growth rate of each company in each sector
    company_growth_rate = dff.groupby(['GICS Sector', 'Symbol']).apply(lambda x: (x['Close'].iloc[-1] - x['Close'].iloc[0])/x['Close'].iloc[0]).reset_index(name='Growth Rate')

    return company_growth_rate


# Define a function to subset the original df to only include the top 5 companies in each sector
def top_5_company(duration, df):

    company_growth_rate = growth_rate_company(duration, df)

    # Filter the top 5 companies in each sector
    top_5 = company_growth_rate.groupby('GICS Sector').apply(lambda x: x.nlargest(5, 'Growth Rate'))
    top_5 = top_5.reset_index(drop=True)

    # Obtain the symbol of top 5 companies in each sector
    top_5_symbol = top_5['Symbol'].unique().tolist()

    # Subset the df to only include the top 5 companies in each sector
    df_top_5 = df[df['Symbol'].isin(top_5_symbol)]

    return df_top_5


# df: set duration = 90 days for now, can be changed later depending on the user input
df_top_5 = top_5_company(90, df)

# Define the sectors and their symbols
sectors = df_top_5['GICS Sector'].unique().tolist()
symbols_by_sector = {sector: df_top_5[df_top_5['GICS Sector'] ==
                                            sector]['Symbol'].unique() for sector in sector_name}


###################################################
############       Dash App        ################
###################################################

# create dash app
app = dash.Dash(__name__)

# Define the dropdown for sector selection
dropdown_sector = dcc.Dropdown(
    id='dropdown_sector',
    options=[{'label': sector, 'value': sector} for sector in sectors],
    value=sectors[0]
)

# Define the checkboxes for company selection
checkbox_company = dcc.Checklist(
    id='checkbox_company',
    options=[],
    value=[]
)

# Define the graph for the trend line plot
# graph_trend_line = dcc.Graph(id='graph_trend_line')
# dcc.Graph would not work with altair, so we use html.Iframe instead

# Define the layout of the app
app.layout = html.Div([
    html.Iframe(
        id='scatter',
        style={'border-width': '0',
               'width': '100%',
               'height': '400px'}),
    dropdown_sector,
    checkbox_company
])


# Define the callback to update the options of the checkbox based on the selected sector
@app.callback(
    Output('checkbox_company', 'options'),
    Input('dropdown_sector', 'value')
)
def update_company_options(selected_sector):
    df_top_5_selected_sector = df_top_5[df_top_5['GICS Sector'] == selected_sector]
    top_5_symbol = df_top_5_selected_sector['Symbol'].unique().tolist()
    options = [{'label': symbol, 'value': symbol} for symbol in top_5_symbol]
    return options


# Define the callback to update the graph based on the selected sector and companies
@app.callback(
    Output('scatter', 'srcDoc'),
    [Input('dropdown_sector', 'value'),
     Input('checkbox_company', 'value')]
)
def update_trend_line(selected_sector, selected_companies):
    df_top_5_selected_sector = df_top_5[df_top_5['GICS Sector'] == selected_sector]

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
        width=800,
        height=400,
        title='Top 5 Companies by Growth Rate'
    ).interactive()
    return chart.to_html()


# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)


