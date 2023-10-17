# retail-dragon

This repository contains code that I've written to evaluate the performance of some exchange-traded products to implement [Artemis Capital](https://www.artemiscm.com/)'s [Dragon Portfolio](https://docsend.com/view/kyfbekuvz6udng75) as a retail investor in India with a cash account with [tastytrade](https://tastytrade.com/) in the US.

## Retail semi-Dragon

[retail_semi_dragon.py](https://github.com/vinamrsachdeva/retail-dragon/blob/main/retail_semi_dragon.py), tests three portfolios, each re-balanced monthly to achieve an equal weight for [SPY](https://finance.yahoo.com/quote/SPY/history?period1=728265600&period2=1693872000&interval=1d&filter=history&frequency=1d&includeAdjustedClose=true), [AGG](https://finance.yahoo.com/quote/AGG/history?period1=1064793600&period2=1693872000&interval=1d&filter=history&frequency=1d&includeAdjustedClose=true), [DJP](https://finance.yahoo.com/quote/DJP/history?period1=1162166400&period2=1693872000&interval=1d&filter=history&frequency=1d&includeAdjustedClose=true), [GLD](https://finance.yahoo.com/quote/GLD/) and one long volatility or tail-risk hedging ETF ([VXZ](https://finance.yahoo.com/quote/VXZ/history?period1=1516838400&period2=1693872000&interval=1d&filter=history&frequency=1d&includeAdjustedClose=true), [VIXM](https://finance.yahoo.com/quote/VIXM/history?period1=1294099200&period2=1693872000&interval=1d&filter=history&frequency=1d&includeAdjustedClose=true) and [TAIL](https://finance.yahoo.com/quote/TAIL/history?period1=1491436800&period2=1693872000&interval=1d&filter=history&frequency=1d&includeAdjustedClose=true)), against a 60-40 portfolio with SPY and AGG for drawdowns and CAGR. This is different from what is exactly suggested by Artemis because it doesn't follow commodity trends and doesn't roll puts and calls depending on if the market is down or up 5% as backtested by Artemis; hence, I'm calling it the 'Retail semi-Dragon', what I hope eventually transforms into something close enough to the real Dragon Portfolio.

### Drawdowns

![](https://github.com/vinamrsachdeva/retail-dragon/blob/main/drawdowns/with_VXZ.png)

![](https://github.com/vinamrsachdeva/retail-dragon/blob/main/drawdowns/with_VIXM.png)

![](https://github.com/vinamrsachdeva/retail-dragon/blob/main/drawdowns/with_TAIL.png)

### Results

|Metric                  |Portfolio with VXZ      |60-40 SPY-AGG           |Portfolio with VIXM     |60-40 SPY-AGG           |Portfolio with TAIL     |60-40 SPY-AGG           |
|------------------------|------------------------|------------------------|------------------------|------------------------|------------------------|------------------------|
|Time Period (YYYY-MM-DD)|2018-01-25 to 2023-09-01|2018-01-25 to 2023-09-01|2011-01-04 to 2023-09-01|2011-01-04 to 2023-09-01|2017-04-06 to 2023-09-01|2017-04-06 to 2023-09-01|
|Max Drawdown (%)        |-15.52                  |-21.76                  |-40.87                  |-21.76                  |-15.32                  |-21.76                  |
|CAGR (%)                |5.58                    |4.64                    |-0.97                   |6.21                    |2.85                    |5.88                    |

### Data

All data has been downloaded from [Yahoo Finance](https://finance.yahoo.com/).
