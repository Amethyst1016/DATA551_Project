# Proposal

### Section 1: Motivation and purpose
- Our role: Data scientist investment-support group
- Target audience: Individual investors/ Personal Traders

Choosing a stock to invest in can be a daunting task given the vast array of options in the market. To simplify the process and provide individual investors with a clear and easy-to-use tool for navigating the stock market, we have created a dashboard that enables users to manage and organize the wealth of information available. Our approach is centred around the idea that the stock market is defined by the movement of both broad indexes and individual stocks. By tracking the movement of broad indexes across countries, users can then drill down to explore the performance of individual sectors within the S&P500. Finally, our dashboard helps users identify the most promising companies within these sectors, enabling them to quickly and easily find stocks that align with their investment preferences. This streamlines the process of sifting through information and allows investors to make more informed decisions about where to put their money.

### Section 2: Description of data
The API package yfinance generates the data source, which consists of two types of data. The first type is global indices, including S&P500 Index, FTSE100 Index, EURO STOXX 50 Index, HANG SENG Index, and SSE Index. These indices cover mainstream trading markets in the US, UK, Europe, Hong Kong, and Shanghai (China). The data contains three columns: Date, Open, and Close. The second type of data includes information on over 500 companies maintained by S&P Dow Jones Indices. This dataset contains six variables: Date, Open, Close, Volume, Symbol, and GICS Sector.


The datasets are generated for two different time ranges and intervals, one for daily information over a year and the other for minute-by-minute information over 7 days. The use of different time intervals allows users to observe both macro and micro trading movements, providing them with more flexibility to apply their own trading strategies to their investments.


By analyzing this data, we can gain new insights, such as the growth rate of the broad market index, the growth rate between sectors, and the growth rate of individual companies over different time periods. Based on this information, we can identify the Top10 and Tail10 growth rates over time and visualize the data accordingly.

### Section 3: Research questions and usage scenario
Lily is an individual investor who wants to keep abreast of an updated stock market trend in a timely manner. Specifically, she is interested in not only the overall stock price trend using market and sector indices, but also the specific company stock price trend and growth rate ranking. This information will be valuable for her to improve their investment strategy.

When Lily uses this stock dashboard, she can choose the time on a daily, weekly or monthly basis according to her need. From the macro aspect, she can compare S&P 500 with other indexes of different countries to get insights into the global macroeconomic environment and reduce the risk of holding all investments in one country. From a micro perspective, this dashboard using the top-down method provides information on the top 5 growth rate sectors and top 5 growth rate stocks inside each sector combined with trading volume in order to help investors to make informed investment decisions.
