# retail-dragon

This repository includes work I'm doing in the quest to implement [Artemis Capital](https://www.artemiscm.com/)'s [Dragon Portfolio](https://docsend.com/view/kyfbekuvz6udng75) as a retail investor in India.

## Retail semi-Dragon

[retail_proto_dragon.py](https://github.com/vinamrsachdeva/retail-dragon/blob/main/retail_proto_dragon.py), tests three portfolios, each re-balanced monthly to achieve an equal weight for [SPY](https://finance.yahoo.com/quote/SPY/history?period1=728265600&period2=1693872000&interval=1d&filter=history&frequency=1d&includeAdjustedClose=true), [AGG](https://finance.yahoo.com/quote/AGG/history?period1=1064793600&period2=1693872000&interval=1d&filter=history&frequency=1d&includeAdjustedClose=true), [DJP](https://finance.yahoo.com/quote/DJP/history?period1=1162166400&period2=1693872000&interval=1d&filter=history&frequency=1d&includeAdjustedClose=true), [GLD](https://finance.yahoo.com/quote/GLD/) and one long volatility or tail-risk hedging ETF ([VXZ](https://finance.yahoo.com/quote/VXZ/history?period1=1516838400&period2=1693872000&interval=1d&filter=history&frequency=1d&includeAdjustedClose=true), [VIXM](https://finance.yahoo.com/quote/VIXM/history?period1=1294099200&period2=1693872000&interval=1d&filter=history&frequency=1d&includeAdjustedClose=true) and [TAIL](https://finance.yahoo.com/quote/TAIL/history?period1=1491436800&period2=1693872000&interval=1d&filter=history&frequency=1d&includeAdjustedClose=true)), against SPY for drawdowns and CAGR. This is different from what is exactly suggested by Artemis; hence, I'm calling it the 'Retail semi-Dragon', what I hope eventually transforms into something close enough to the real Dragon Portfolio.

### Drawdowns

![](https://github.com/vinamrsachdeva/retail-dragon/blob/main/drawdowns/with_VXZ.png)

![](https://github.com/vinamrsachdeva/retail-dragon/blob/main/drawdowns/with_VIXM.png)

![](https://github.com/vinamrsachdeva/retail-dragon/blob/main/drawdowns/with_TAIL.png)

### Results

|Metric                  |Portfolio with VXZ      |SPY                     |Portfolio with VIXM     |SPY                     |Portfolio with TAIL     |SPY                     |
|------------------------|------------------------|------------------------|------------------------|------------------------|------------------------|------------------------|
|Time Period (YYYY-MM-DD)|2018-01-25 to 2023-09-01                        ||2011-01-04 to 2023-09-01                        ||2017-04-06 to 2023-09-01                        ||
|Max Drawdown (%)        |-15.521553225771292     |-34.104746812138636     |-40.86891578110916      |-34.104746812138636     |-15.321137072656295     |-34.104746812138636     |
|CAGR (%)                |5.578063771146136       |8.66724352309529        |-0.967539446469412      |10.535870836416784      |2.847609394107775       |10.690655429072882      |

### Data

All data has been downloaded from [Yahoo Finance](https://finance.yahoo.com/).
