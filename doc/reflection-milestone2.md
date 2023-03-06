# reflection-milestone2

So far, all four main plots have been completed using daily data. Minute data will be added in a later stage.

### The current content of the dashboard includes:
- Plot 1. Line plot: Comparison of global indices
- Plot 2. Bar chart: Growth rate for each sector
- Plot 3. Line plot: Close price of the top 5 companies in each sector
- Plot 4. Pie chart: Volume of the top 5 companies in each sector

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
