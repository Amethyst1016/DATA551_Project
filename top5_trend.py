import dash
from dash import html
from dash import dcc
from dash.dependencies import Input, Output, State
import altair as alt
import dash_bootstrap_components as dbc
import pandas as pd
import plotly
import plotly.express as px

# Read in global data
df = pd.read_csv('data/SP500_merged.csv')

sector_name = df['GICS Sector'].unique().tolist()

sector_symbol = []
for i in sector_name:
    sector_symbol.append(df[df['GICS Sector'] == i]['Symbol'].unique().tolist())


def growth_rate_company(duration):
    company_growth_rate = []

    for i in range(len(sector_name)):
        grow_rate = []

        for n in sector_symbol[i]:
            dff = df[df['GICS Sector'] == sector_name[i]][df['Symbol'] == n]
            grow_rate.append(dff.iloc[len(dff) - 1, 1] / dff.iloc[len(dff) - 1 - duration, 1] - 1)

        company_growth_rate.extend([{'sector': sector_name[i],
                                     'company': n, 'growth_rate': g
                                     } for n, g in zip(sector_symbol[i], grow_rate)])

    company_growth_rate = pd.DataFrame(company_growth_rate)

    return company_growth_rate


company_growth_rate = growth_rate_company(90)

top_5 = company_growth_rate.groupby('sector').apply(lambda x: x.nlargest(5, 'growth_rate'))
top_5 = top_5.reset_index(drop=True)

top_5_symbol = []
for i in sector_name:
    top_5_symbol.append(top_5[top_5['sector'] == i]['company'].unique().tolist())

df_top_5 = df[df['Symbol'].isin(top_5_symbol[0] + top_5_symbol[1] + top_5_symbol[2] + top_5_symbol[3] +
                                top_5_symbol[4] + top_5_symbol[5] + top_5_symbol[6] + top_5_symbol[7] +
                                top_5_symbol[8] + top_5_symbol[9] + top_5_symbol[10])]

# remove Healthcare sector
df_top_5 = df_top_5[df_top_5['GICS Sector'] != 'Health Care']


# Define the sectors and their symbols
sector_name = df_top_5['GICS Sector'].unique().tolist()
symbols_by_sector = {sector: df_top_5[df_top_5['GICS Sector'] == sector]['Symbol'].unique() for sector in sector_name}

#####


# create dash app
app = dash.Dash(__name__)

# Define the dropdown for sector selection
sectors = df_top_5['GICS Sector'].unique().tolist()
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

# Define the layout of the app
app.layout = html.Div([
    html.Iframe(
        id='scatter',
        style={'border-width': '0', 'width': '100%', 'height': '400px'}),
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


