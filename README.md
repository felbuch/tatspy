# tatspy
A package to calculate time series of technical analysis indicators for stocks

## Description

tatspy is a package you can use to get information such as:
* the historical prices of a stock over a given period
* the values of technical analysis indicators (such as MACD, bollinger bands etc.) over a given period.

It features not only american stocks, but also stocks from around the globe, featuring countries such as Brazil, Spain, and others.

## For example...

For example, you could use tatspy to get the daily values of the MACD, bollinger bands, parabolic SAR and ATR (among other) for Brazil's Petrobras.

## Package contents

The tatspy package defines a class called `stock`.
It receives two attributes: the stock's `ticker` and its `country`
This stock has a couple of useful methods:

* `get_stock_historical_prices` : returns the historical prices (OHLC) of a stock for a given period, defined by the user.
* `get_technical_indicators` : returns a dataframe with time series for a set of technical analysis indicators
* `lag_indicators`: returns a dataframe with specified lags of technical analysis indicators, for Time Series analysis

The outputs of these methods are also saved as class attributes within each instance.

## Available Technical Analysis Indicators

At present, the following technical analysis indicators are made available by tatspy:

1. 'simple_moving_average' : simple moving average of stock price  
2. 'exponential_moving_average': exponential moving average of stock price  
3. 'RSI': Relative Strength Index  
4. 'bollinger_bands': Bollinger Bands  
5. 'bollinger_bands_indicator': Indicates if stock price close to bands, suggesting price reversal
6. 'MACD' : Moving Average Convergence-Divergence
7. 'stochastic': Stochastic Oscillator
8. 'VWAP': Volume Weighted Average Price
9. 'ATR': Average True Range
10. 'ADX': Average Directional Index
11. 'parabolic_SAR': Parabolic SAR
12. 'parabolic_SAR_indicator: Indicates if parabolic SAR suggests a price reversal upwards (+1) or downwards (-1)
13. 'TRIX': Triple Exponential Average

## Installing tatspy

Just pip install it:

```python
!pip install tatspy
```

## Quick start

Suppose you're interested in stocks from Brazil's retailer Magalu (ticker = mglu3), year-to-date.

First, load the `stock` class:

```python
from tatspy.stock_class import stock
```

Now, create an instance of this class:

```python
>>> my_stock = stock('mglu3', 'brazil')
```

To get historical prices and volume, run...

```python
>>> my_stock.get_stock_historical_prices()
```

This command will return a dataframe with OHLC prices and volume, which you can save as a variable.
Alternatively, you can also access this dataframe using...

```python
>>> my_stock.historical_prices
```

To get technical analysis indicators for the same period, just run...

```python
>>> my_stock.get_technical_indicators()
```
This command will return a dataframe with technical indicators, which you can save as a variable.
Alternatively, you can also access this dataframe using...

```python
>>> my_stock.technical_indicators
```

Now suppose you want to lag these indicators by 5 and 10 days. 
You can simply run...

```python
>>> my_stock.lag_indicators(lags=[5,10])
```

## Citations

I am grateful for the authors of the following packages, which have been very helpful in building tatspy:

* Alvaro Bartolome del Canto. (2018-2020). investpy - Financial Data Extraction from Investing.com with Python. https://github.com/alvarobartt/investpy.
* Darío López Padial (aka Bukosabino). ta. https://github.com/bukosabino/ta.

