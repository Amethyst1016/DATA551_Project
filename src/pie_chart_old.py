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


# Define the layout of the app
app.layout = html.Div([
    html.Iframe(
        id='scatter',
        style={'border-width': '0',
               'width': '100%',
               'height': '400px'}),
    dropdown_sector

])

# Define the callback to update the graph based on the selected sector
@app.callback(
    Output('scatter', 'srcDoc'),
    Input('dropdown_sector', 'value')
)
def update_pie_chart(selected_sector):
    df_top_5_selected_sector = df_top_5[df_top_5['GICS Sector'] == selected_sector]

    chart = alt.Chart(df_top_5_selected_sector).mark_arc().encode(
        color='Symbol:N',
        theta='Volume:Q'
    )
    return chart.to_html()


# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)
