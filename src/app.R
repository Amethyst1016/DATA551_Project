library(dash)
library(dashCoreComponents)
library(dashHtmlComponents)
library(dashBootstrapComponents)
library(ggplot2)
library(plotly)
library(tidyverse)
library(zoo)

df_line_chart <- read_csv('Global_index.csv')
colnames(df_line_chart) <- make.names(colnames(df_line_chart))
df_line_chart <- df_line_chart |>
  mutate(Date = as.Date(Date)) |>
  mutate(S.P_original = na.approx(S.P_original)) |>
  mutate(S.P_energy = na.approx(S.P_energy)) |>
  mutate(S.P_industry = na.approx(S.P_industry)) |>
  mutate(S.P_consumer = na.approx(S.P_consumer)) |>
  mutate(FTSE_100 = na.approx(FTSE_100)) |>
  mutate(Euro_Stoxx_50 = na.approx(Euro_Stoxx_50)) |>
  mutate(HANG_SENG = na.approx(HANG_SENG)) |>
  mutate(Nikkei_225 = na.approx(Nikkei_225))

df_bar_chart <- read_csv('SP500_merged.csv')
colnames(df_bar_chart) <- make.names(colnames(df_bar_chart))
df_bar_chart <- mutate(df_bar_chart, Date = as.Date(Date))
df_bar_chart <- filter(df_bar_chart, Symbol != 'GEHC')

select_time_range <- function(df, time_range){
  end <- max(df$Date)
  start <- end - time_range
  df_selected <- filter(df, Date>=start, Date<=end)
  df_selected
}

top_5_company <- function(time_range, df){
  df_selected <- select_time_range(df, time_range)
  company_growth_rate <- df_selected |>
    group_by(GICS.Sector, Symbol)|>
    filter(row_number() == 1 | row_number() == n()) |>
    mutate(diff=Close-lag(Close,default=first(Close)), min=lag(Close,default=first(Close))) |>
    filter(diff != 0) |>
    mutate(Growth.Rate = diff/min) |>
    select(-diff, -min)
  top_5 <- company_growth_rate |>
    arrange(desc(Growth.Rate)) |>
    group_by(GICS.Sector) |>
    slice(1:5) |>
    group_by(Symbol) |>
    pull(Symbol)
  df_top_5 <- df_selected |>
    filter(Symbol %in% top_5)
  df_top_5
}

app <- Dash$new(external_stylesheets = dbcThemes$BOOTSTRAP)

US_Market  <- list('font-size'=15, 'text-align'='left', 'color'='#036d90', 'margin-left'=20)
other_Market <- list('font-size'=15, 'text-align'='left', 'margin-left'=20)
labels <- list('display'='inline', 'font-size'=20, 'margin-left'=5)
page_height <- '100vh'

symbols <- list(
  list('label'='S.P_original', 'value'='S.P_original'),
  list('label'='S.P_energy', 'value'='S.P_energy'),
  list('label'='S.P_industry', 'value'='S.P_industry'),
  list('label'='S.P_consumer', 'value'='S.P_consumer'),
  list('label'='FTSE_100', 'value'='FTSE_100'),
  list('label'='Euro_Stoxx_50', 'value'='Euro_Stoxx_50'),
  list('label'='HANG_SENG', 'value'='HANG_SENG'),
  list('label'='Nikkei_225', 'value'='Nikkei_225')
)

app$layout(
  htmlDiv(list(
    htmlDiv(list( # left part
      htmlDiv(
        list(htmlP('Summary of Stock Symbol', style=list('font-size'=20,'text-align'='center')),
        htmlP('SP500 - US Market', style=US_Market),
        htmlP('FTSE_100 - London Market', style=other_Market),
        htmlP('Euro_Stoxx_50 - Europe Market', style=other_Market),
        htmlP('HANG_SENG - Hong Kong Market', style=other_Market),
        htmlP('Nikkei_225 - Toyko Market', style=other_Market)),
        style=list('border-style'='solid', 'border-color'='#a1979e', 'margin'=10)
      ),
      dccRadioItems(
        id='time_range_selector',
        options=list(
          list('label'='Last 7 Days', 'value'=7),
          list('label'='Last 30 Days', 'value'=30),
          list('label'='Last 90 Days', 'value'=90),
          list('label'='Last 180 Days', 'value'=180),
          list('label'='Last year', 'value'=365)
        ),
        value=7,
        labelStyle=list('display'='block', 'margin'=20)
      )
    ), style=list('width'='20%','height'='100vh','float'='left','margin'=0,'background'='#e1edd5')),
    htmlDiv(list(# right part
      dbcTabs(list(
        # tab 1 -  Stock markets compare trend plot
        dbcTab(htmlDiv(
          htmlDiv(list(
            htmlDiv(list(
              dccDropdown(
                id='symbol-dropdown',
                options=symbols,
                value='S.P_original',
                style=list('width'=200, 'float'='left')
              ),
              dccDropdown(
                id='compare-dropdown',
                options=symbols,
                value='FTSE_100',
                style=list('width'=200, 'float'='left')
              )
            ), style=list('height'='10%')),
            dccGraph(id='line-chart', figure=c(), style=list('height'='90%'))
        ), style=list('width'='100%', 'height'='90vh'))
      ), label='Stock markets compare trend plot'),
      # tab 2 - SP500 sectors growth rate rank
      dbcTab(htmlDiv(
        id='bar-chart',
        children=c(),
        style=list('width'='100%','height'='90vh')
      ), label='SP500 sectors growth rate rank'),
      # tab 3 - Top 5 companies in SP500 GICS sectors
      dbcTab(list(
        htmlDiv(list(
          dccDropdown(
            id='dropdown_sector',
            options=c(),
            value=c(),
            style=list('width'=300, 'float'='left')),
          dccChecklist(
            id='checkbox_company',
            options=c(),
            value=c(),
            style=list('float'='left', 'margin-left'=10))
        )),
        htmlDiv(htmlIframe(
          id='scatter', 
          style=list('width'='100%', 'height'='70vh', 'margin-left'='10%', 'margin-top'='10%')
        )),
        htmlDiv(htmlIframe(
          id='pie', 
          style=list('width'='100%', 'height'='70vh', 'margin-left'='10%', 'margin-top'='10%')
        ))
      ), label='Top 5 companies in SP500 GICS sectors')
    ))
  ), style=list('width'='80%', 'height'='100%', 'float'='right', 'margin'=0))
))
)

app$run_server(debug = T)
