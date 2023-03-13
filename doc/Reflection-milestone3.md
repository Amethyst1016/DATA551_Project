# Reflection-milestone3

So far, all four main plots have been completed using daily data. Minute data will be added in a later stage.

### The current content of the dashboard includes:
- Plot 1. Line plot: Comparison of global indices
- Plot 2. Bar chart: Growth rate for each sector
- Plot 3. Line plot: Close price of the top 5 companies in each sector
- Plot 4. Pie chart: Volume of the top 5 companies in each sector

### Reflection on implementing the dashboard a second time in another language.
On the one hand, having prior experience with the design and development process in Python made the process of implementing the dashboard in R more efficient and streamlined. On the other hand, working with R requires a learning curve and have posed new challenges that were not present during the first implementation. From Python to R, it’s not just copy and paste. Although the main framework is similar, the details are different, which includes the difference in grammar, function and package. Overall, this experience gave us a valuable learning experience, as it provides an opportunity to gain new insights, expand our skillset, and learn how to work with different tools and technologies.

### Reflection on current process:
Plot 1, which originally compared the S&P500 to other global indices, now only compares two global indices, but users can freely choose which two to compare.
For Plot 2, the growth rate is calculated based on a chosen time period, and in the next stage, hovering over a bar will display the top 5 companies in that sector.
For Plot 3 and 4, the original design was to display the top 5 companies' price line (in Plot 3) and volume percentage (in Plot 4) when selecting a sector. 
However, due to time constraints, we cannot highlight the specified company one both plots.

The overall framework has been completed, from tracking global indices to individual companies' stock prices. This framework is helpful for individual investors to monitor trends and gather information. 
However, there are still many details that need to be considered, such as:

### Limitations and future improvement
Prior to generating the plots, the first step is to complete data processing, which involves generating daily and minute data for global indices and companies in the S&P 500. However, due to the large amount of data, downloading and processing can be time-consuming and inconvenient for users when launching the app.

When selecting multiple (more than two) global indices in Plot 1, the lines in the plot may not be distinct due to the different Close prices of the indices.
The method of calculating growth rate in Plot 2 and 3 is currently slow, which affects the user experience. Improvements to the calculation method will be made in the future.

Except the stock price, investors also care about the PE ratio of a stock, which provides a simple and quick way to assess the valuation of a company's stock. The PE ratio is a valuable tool for investors to use when making investment decisions. A stock with a low PE ratio may be undervalued and present a good investment opportunity, while a stock with a high PE ratio may be overvalued and not present a good investment opportunity. Therefore, we can add plot 5 (PE ratio in top 5 companies) with plot3 and 4 to give investors diverse metrics to better make an investment decision.

