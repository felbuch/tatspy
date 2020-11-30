# -*- coding: utf-8 -*-
"""
Created on Sun Nov 29 21:28:34 2020

@author: Felipe
"""

class stock():

    def __init__(self, ticker, country):
        
        '''Creates an instance of the class stock.
        
        
        Parameters:
        ----------
        ticker : str
            The stock's ticker e.g. PETR4
        country : str
            The country in which it is negotiated e.g. brazil
        
        Returns:
        --------
        None
        
        Attributes:
        ------
                
        * ticker: str
            the stock's ticker, inputed by the user
        * country: str
            the country in which it is negotiated, inputed by the user
        * currency: str
            the currency in which the stock prices are expressed in
        * historical_prices: pandas dataframe
            a dataframe with OHLC prices
        * indicators: pandas dataframe
            a dataframe with technical indicators
        
        Example:
        --------
        >>> stock('petr4','brazil')
                
        
        '''
        
        self.ticker = ticker
        self.country = country
        self.currency = None
        self.historical_prices = None
        self.indicators = None
        
    def get_stock_historical_prices(self, from_date = None, to_date = None):
        
        '''Get historical data on OHLC prices for a specified period
        
        Parameters:
        -----------
        from_date: str
            First day of historical data.
            Expressed in dd/mm/yyyy format
            If missing, it will correspond to the first day of the year of to_date
        to_date: str
            Last day of historical data.
            Expressed in dd/mm/yyyy format
            If missing, it will correspond to the present date (i.e. today)
        
        Returns:
        --------
        dataframe
            A pandas dataframe containing OHLC prices for the specified period
        
        Notes:
        ------
        
        If to_date is missing, it defaults to the present date (i.e. today)
        
        If from_date is missing, it defaults to the first day of the same year of to_date.
        
        If both to_date and from_date are missing, it returns the series of prices YTD.
        This is because to_date will default to the present day, and from_date will default
        to the start of the same year.
        
        This function uses the investpy package (Alvaro Bartolome del Canto, 2018-2020)
        
        Examples:
        --------
        >>> s = stock('petr4','brazil')
        >>> s.get_stock_historical_prices('30/10/2020', '30/11/2020')
        
        >>> s = stock('mglu3','brazil')
        >>> s.get_stock_historical_prices() #Get stock prices YTD
        
        References:
        -----------
        Alvaro Bartolome del Canto. (2018-2020). investpy - Financial Data Extraction from Investing.com with Python. https://github.com/alvarobartt/investpy.

        
        '''
        
        from investpy import get_stock_historical_data
        from datetime import datetime
        
        #--------------------------------------------------------------------------
        # Missing inputs
        #--------------------------------------------------------------------------
        #If to_date is not provided, set it to today
        if to_date == None:
            #set to_date to today
            to_date = datetime.today().date().strftime('%d/%m/%Y')
                
        #If from_date is not provided, set it to first day of the year of to_date
        #This way, we'll get the historical data Year-To-Date
        if from_date == None:
            year = to_date.split('/')[-1]
            from_date = f'01/01/{year}'
        #--------------------------------------------------------------------------
            
        #--------------------------------------------------------------------------
        # Get historical prices
        #--------------------------------------------------------------------------
        
        #Get historical prices
        hp = get_stock_historical_data(stock=self.ticker, 
                                       country=self.country, 
                                       from_date=from_date, 
                                       to_date=to_date)
        
        #save currency as class property
        #then drop currency from historic prices dataframe
        self.currency = hp.Currency.drop_duplicates()[0]
        hp = hp.drop(columns='Currency')
                
        #save atributes to self
        self.historical_prices = hp
        
        return(hp)
        
    def get_technical_indicators(self,
                                 indicators = ['simple_moving_average',
                                               'exponential_moving_average',
                                               'RSI',
                                               'bollinger_bands',
                                               'bollinger_bands_indicator',
                                               'MACD',
                                               'stochastic',
                                               'VWAP',
                                               'ATR',
                                               'ADX',
                                               'parabolic_SAR',
                                               'parabolic_SAR_indicator'
                                               'TRIX'],
                                 clean_dataframe = True,
                                 normalize=False):
        
        '''Calculates time series of technical indicators
        
        Parameters:
        -----------
        * indicators: list
            List of strings referring to the names of the indicators to be calculated.
            Possible values for these strings are the following:
            
            -'simple_moving_average' : simple moving average of stock price
            -'exponential_moving_average': exponential moving average of stock price
            -'RSI': Relative Strength Index
            -'bollinger_bands': Bollinger Bands
            -'bollinger_bands_indicator': Indicates if stock price close to bands, suggesting price reversal
            -'MACD' : Moving Average Convergence-Divergence
            -'stochastic': Stochastic Oscillator
            -'VWAP': Volume Weighted Average Price
            -'ATR': Average True Range
            -'ADX': Average Directional Index
            -'parabolic_SAR': Parabolic SAR
            -'parabolic_SAR_indicator: Indicates if parabolic SAR suggests a price reversal upwards (+1) or downwards (-1)
            -'TRIX': Triple Exponential Average
        * clean_dataframe: bool
            If True, removes missing data from first days, due to lag of indicators.
            See Notes for further explanation.
        * normalize: bool
            If FALSE (default), indicators are presented without any transformation.
            If TRUE, indicators measured in monetary units will be divided by the closing price
            each day. Thus, the indicator is shown as a fraction of the stock price.
            See Notes section for a list of indicators that are affected by this parameter.
        
        Returns:
        --------
        dataframe
            A pandas dataframe containing time series values of technical indicators
        
        Notes:
        ------
        
        Some indicators do not exist for the first days in the dataframe.
        Setting clean_dataframe = TRUE removes these days.
        
        Selecting 'bollinger_bands' as an indicator, creates 3 indicators:
        
        - 'bb_low' : Inferior band value
        - 'bb_mean' : Average value of the band
        - 'bb_high' : Upper band value
        
        Selecting 'bollinger_bands_indicator' as an indicator, creates 2 indicators:
        
        - bbi_high: 1 if stock price close to upper bollinger band, and 0 otherwise
        - bbi_low: 1 if stock price close to lower bollinger band, and 0 otherwise
        
        Selecting 'MACD' as an indicator, creates 3 indicators:
        
        - MACD: MACD line
        - MACD_signal: MACD signal line
        - MACD_histogram: the difference between MACD and its signal line
        
        Selecting 'stochastic' as an indicator, creates 2 indicators:
        
        - 'stochastic': the stochastic oscillator 
        - 'stochastic_signal': the stochastic oscillator signal

        Selecting 'parabolic_SAR' as an indicator, creates 2 indicators:
        
        - 'psar_up': the parabolic SAR values during an upward trend. 
        - 'psar_down': the parabolic SAR values during a downward trend. 
        
        During a downward trend, psar_up values are N/A.
        Similarly, during an upward trend, psar_down values are N/A.
        As a result, this indicator is not considered when dropping missing values
        (which happens when the clean_dataframe parameter is set to TRUE).
        
        Selecting 'parabolic_SAR_indicator' creates an indicator which has value
        1, if it indicates an upward trend, and -1, if it indicates a downward trend.
        A value of zero means no price reversal is being suggested.

        If normalize=TRUE, the values of the following indicators
        will be divided by the stock's closing price each day:
        
        -'simple_moving_average' : simple moving average of stock price
        -'exponential_moving_average': exponential moving average of stock price
        -'bollinger_bands': Bollinger Bands
        -'MACD' : Moving Average Convergence-Divergence line
        -'VWAP': Volume Weighted Average Price
        -'ATR': Average True Range
        -'parabolic_SAR': Parabolic SAR
        -'TRIX': Triple Exponential Average

        Examples:
        --------
        >>> s = stock('petr4','brazil')
        >>> s.get_stock_historical_prices('30/10/2020', '30/11/2020')
        >>> s.technical_indicators()
        
        References:
        -----------
        
        In this package, we use the ta package, developped by Darío López Padial (aka Bukosabino)
        and available at https://github.com/bukosabino/ta.
        I was unable to find a proper way to reference this package.
       
        '''
        
        import ta #technical analysis indicators
        
        df = self.historical_prices
        
        #setup for normalization
        if normalize:
            #normalization factor
            nf = 1/df.Close
        else:
            nf = 1
        
        #Create technical analysis indicators
        ######################################################
        # Simple Moving Average
        ######################################################
        if 'simple_moving_average' in indicators:
            df['simple_moving_average'] = ta.trend.sma_indicator(df.Close) * nf
        
        ######################################################
        # Exponential Moving Average
        ######################################################
        if 'exponential_moving_average' in indicators:
            df['exponential_moving_average'] = ta.trend.ema_indicator(df.Close) * nf

        ######################################################
        #RSI
        ######################################################
        if 'RSI' in indicators:
            df['RSI'] = ta.momentum.RSIIndicator(df.Close).rsi()
            
        
        ######################################################
        #Bollinger Bands
        ######################################################
        if 'bollinger_bands' in indicators:
            
            df['bb_low'] = ta.volatility.bollinger_lband(df.Close) * nf
            df['bb_mean'] = ta.volatility.bollinger_mavg(df.Close) * nf
            df['bb_high'] = ta.volatility.bollinger_hband(df.Close) * nf
            
        if 'bollinger_bands_indicator' in indicators:
            
            # Add Bollinger Band high indicator
            df['bbi_high'] = ta.volatility.bollinger_hband_indicator(df.Close)
            
            # Add Bollinger Band low indicator
            df['bbi_low'] = ta.volatility.bollinger_lband_indicator(df.Close)
            
        ######################################################
        # MACD
        ###################################################### 
        if 'MACD' in indicators:
            
            df['MACD'] = ta.trend.macd(df.Close) * nf
            df['MACD_signal'] = ta.trend.macd_signal(df.Close) * nf
            df['MACD_histogram'] = ta.trend.macd_diff(df.Close) * nf
        
        ######################################################
        # Stochastic
        ######################################################
        if 'stochastic' in indicators:
            
            df['stochastic'] = ta.momentum.stoch(high = df.High, 
                                                 low=df.Low, 
                                                 close=df.Close)
            df['stochastic_signal'] = ta.momentum.stoch_signal(high = df.High,
                                                               low=df.Low, 
                                                               close=df.Close)
               
        ######################################################
        # VWAP
        ######################################################
        if 'VWAP' in indicators:
            
            df['VWAP'] = ta.volume.volume_weighted_average_price(high = df.High,
                                                                 low = df.Low,
                                                                 close = df.Close,
                                                                 volume = df.Volume) * nf
        
        ######################################################
        # ATR
        ######################################################
        if 'ATR' in indicators:
            
            df['ATR'] = ta.volatility.average_true_range(high = df.High,
                                                         low = df.Low, 
                                                         close = df.Close) * nf
        
        ######################################################
        # ADX
        ######################################################
        if 'ADX' in indicators:

            df['ADX'] = ta.trend.adx(high = df.High,
                                     low = df.Low, 
                                     close = df.Close)
        
        ######################################################
        # Parabolic SAR
        ######################################################
        if 'parabolic_SAR' in indicators:

            df['psar_down'] = ta.trend.psar_down(high = df.High, 
                                                 low = df.Low, 
                                                 close = df.Close) * nf
            df['psar_up'] = ta.trend.psar_up(high = df.High, 
                                             low = df.Low, 
                                             close = df.Close) * nf
        
        ######################################################
        # Parabolic SAR indicator
        ######################################################
        if 'parabolic_SAR_indicator' in indicators:
            
            psar_up_indicator = ta.trend.psar_down_indicator(df.High, 
                                                             df.Low, 
                                                             df.Close)

            psar_down_indicator = ta.trend.psar_down_indicator(df.High, 
                                                               df.Low, 
                                                               df.Close)
            
            df['psar_indicator'] = psar_up_indicator - psar_down_indicator
        
        ######################################################
        # TRIX
        ######################################################
        
        if 'TRIX' in indicators:
            
            df['trix'] = ta.trend.trix(df.Close)
        
        #drop price variables except price
        df = df.drop(columns=['Open',
                              'Close',
                              'High',
                              'Low',
                              'Volume'])
        
        #remove missing values if user asks for it
        if clean_dataframe:
            #we consider all columns in the dataset,
            #except those from the parabolic SAR,
            #since at least one of psar_up or psar_down is always an N/A value.
            columns_subset = df.columns[~df.columns.str.startswith('psar')]
            
            #Considering all other columns,
            #drop missing values row-wise
            df = df.dropna(subset = columns_subset)
        
        #Save new dataset: technical analysis dataframe
        self.indicators = df
                
        return(self.indicators)
    
    def lag_indicators(self, 
                       lags = [5], 
                       clean_dataframe=True):
        
        '''
        Lag indicators
        
        Parameters:
        -----------
        * lags: list
            List with the numbers of periods to lag the indicators.
            This list should contain integer values, either positive or negative.
            For example, [5, 14, 50] will produce series lagged by 5, 14 and 50 days.
        
        * clean_dataframe: bool
            If True, removes missing data from first days, due to lag of indicators.
        
        Returns:
        --------
        dataframe
            A pandas dataframe with technical indicators lagged up to n_max days
        
        '''
        
        import pandas as pd
        
        #get dataframe with technical indicators
        df = self.indicators
        
        #setup
        column_names = df.columns
        list_of_dfs = [df]
        
        #for each requested lag
        for i in lags:
            #produce a dataframe of lagged values
            df_lagged = df.shift(i)
            #set column names
            #e.g., RSI_14, for RSI lagged by 14 time periods
            df_lagged.columns = [name + '_lag_' + str(i) for name in column_names]
            #append lagged dataframe to list of dataframes
            list_of_dfs.append(df_lagged)
        
        #Concatenate all dataframes
        df = pd.concat(list_of_dfs, axis=1)
        
        
        #remove missing values if user asks for it
        if clean_dataframe:
            #we consider all columns in the dataset,
            #except those from the parabolic SAR,
            #since at least one of psar_up or psar_down is always an N/A value.
            columns_subset = df.columns[~df.columns.str.startswith('psar')]
            
            #Considering all other columns,
            #drop missing values row-wise
            df = df.dropna(subset = columns_subset)

        
        #drop missing values due to lagging
        #df = df.dropna()
        self.lagged_indicators = df
        return(self.lagged_indicators)
        
    

    


        