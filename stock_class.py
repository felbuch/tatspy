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
    
    def __calculate_indicator(self, indicator, nf, include_flags):
        
        '''An auxiliary function called by the get_technical_indicators method.
        This function is not meant to be used by the user.
        
        Parameters:
        -----------
        * indicator: tuple
            A tuple representing a request by the user to calculate a certain indicator.
            It is an element of the indicators argument in the get_technical_indicators method.
            For further explanation of this argument, please refer to that function's docstring.
        
        * nf: int or pandas Series
            Normalizing factor.
            1 if normalize=False in the get_technical_indicators method (default)
            Otherwise, it is the inverse of the stock's closing price
            Please refer to the get_technical_indicators method's docstring for details.
        
        * include_flags: bool
            Whether to include flags for selected indicators.
            Please refer to the get_technical_indicators method's docstring for details
        
        Returns:
        --------
        An updated version of the indicator attribute, containing the calculated indicator.
        Note that this may mean multiple additional columns, depending on the indicator.
        
        '''
        
        import pandas as pd
        import ta
        
        #Initialize dataframe
        if isinstance(self.indicators, pd.DataFrame):
            df = self.indicators
        else:
            df = self.historical_prices
        
        indicator_type, column_name, kwargs = indicator
        if indicator_type == 'sma':
                
            ##########################
            ## Simple Moving Average
            ##########################
            df[column_name] = ta.trend.sma_indicator(df.Close, **kwargs) * nf
            
        elif indicator_type == 'ema':
               
            ###############################
            ## Exponential Moving Average
            ###############################
            df[column_name] = ta.trend.ema_indicator(df.Close, **kwargs) * nf
                
        elif indicator_type == 'rsi':
            ##############################
            ## Relative Strength Index
            #############################
            df[column_name] = ta.momentum.RSIIndicator(df.Close, **kwargs).rsi()
                
        elif indicator_type == 'bb':
                
            ##############################
            ## Bollinger Bands
            #############################
                
            #note: the bollinger band mean does not receive all parameters received by the bands
            df[column_name + '_low'] = ta.volatility.bollinger_lband(df.Close, **kwargs) * nf
            df[column_name + '_mean'] = ta.volatility.bollinger_mavg(df.Close, n = kwargs['n']) * nf 
            df[column_name + '_high'] = ta.volatility.bollinger_hband(df.Close, **kwargs) * nf
                
            if include_flags:
                    
                # Add Bollinger Band low flag
                df[column_name + '_low_flag'] = ta.volatility.bollinger_lband_indicator(df.Close, **kwargs)

                # Add Bollinger Band high flag
                df[column_name + '_high_flag'] = ta.volatility.bollinger_hband_indicator(df.Close, **kwargs)
            
        elif indicator_type == 'macd':
                
            #########################################
            ## Moving Average Convergence-Divergence
            #########################################
                
            #note: the macd line propper does not receive all parameters received by the signal and histogram  
            df[column_name] = ta.trend.macd(df.Close, n_slow = kwargs['n_slow'], n_fast = kwargs['n_fast']) * nf
            df[column_name + '_signal'] = ta.trend.macd_signal(df.Close, **kwargs) * nf
            df[column_name + '_histogram'] = ta.trend.macd_diff(df.Close, **kwargs) * nf
            
        elif indicator_type == 'stoch':
                
            #########################################
            ## Stochastic Oscillator
            #########################################
                
            df[column_name] = ta.momentum.stoch(high = df.High, 
                                                low=df.Low, 
                                                close=df.Close,
                                                **kwargs)
            df[column_name + '_signal'] = ta.momentum.stoch_signal(high = df.High,
                                                                    low=df.Low, 
                                                                    close=df.Close,
                                                                    **kwargs)
        elif indicator_type == 'vwap':
                
            ##################################
            ## Volume Weighted Average Price
            ##################################
                
            df[column_name] = ta.volume.volume_weighted_average_price(high = df.High,
                                                                      low = df.Low,
                                                                      close = df.Close,
                                                                      volume = df.Volume,
                                                                      **kwargs) * nf
        elif indicator_type == 'atr':
                
            ########################
            ## Average True Range
            ########################
                
            df[column_name] = ta.volatility.average_true_range(high = df.High,
                                                               low = df.Low, 
                                                                close = df.Close,
                                                                **kwargs) * nf
        elif indicator_type == 'adx':
                
            ##################################
            ## Average Directional Index
            ###################################
                
            df[column_name] = ta.trend.adx(high = df.High,
                                           low = df.Low, 
                                           close = df.Close,
                                           **kwargs)
            
        elif indicator_type == 'psar':
            
            ##################
            ## Parabolic SAR
            ##################
                
            df[column_name + '_down'] = ta.trend.psar_down(high = df.High, 
                                                           low = df.Low, 
                                                           close = df.Close,
                                                           **kwargs) * nf
            
            df[column_name + '_up'] = ta.trend.psar_up(high = df.High, 
                                                       low = df.Low, 
                                                       close = df.Close,
                                                       **kwargs) * nf
                
            if include_flags:
                    
                #flags when trend reverses upwards
                psar_up_indicator = ta.trend.psar_up_indicator(df.High, 
                                                               df.Low, 
                                                               df.Close,
                                                               **kwargs)
                #flags when trend reverses downwards
                psar_down_indicator = ta.trend.psar_down_indicator(df.High,
                                                                   df.Low, 
                                                                   df.Close,
                                                                   **kwargs)
                    
                #flags when trend reverses upwards (+1) or downwards (-1)
                df[column_name + '_flag'] = psar_up_indicator - psar_down_indicator
            
        elif indicator_type == 'trix':
                
            #########################
            ## Triple Exponential
            ########################
                
            df[column_name] = ta.trend.trix(df.Close, **kwargs)
        
        #Update indicators table in self
        self.indicators = df
            
        return(df)

        
        
    
            
    def get_technical_indicators(self,
                                 indicators = [('sma', None, {'n':12}),
                                               ('ema', None, {'n': 12}),
                                               ('rsi', None, {'n':14}),
                                               ('bb', None, {'n':20, 'ndev':2}),
                                               ('macd',None,{'n_fast':12, 'n_slow':26, 'n_sign':9}),
                                               ('stoch', None, {'n':14, 'd_n':3}),
                                               ('vwap', None, {'n': 14}),
                                               ('atr', None, {'n': 14}),
                                               ('adx', None, {'n':14}),
                                               ('psar', None, {'step': 0.02, 'max_step':0.2}),
                                               ('trix', None, {'n': 15})],
                                 include_flags = True,
                                 clean_dataframe = True,
                                 normalize=False):
        
        
        '''Calculates time series of technical indicators
        
        Parameters:
        -----------
        * indicators: list of tuples
            List of tuples referring to the indicators to be calculated.
            Each tuple contains 3 elements:
            - a short identifier of the type of indicator to be calculated (a string);
            - the name of the column containing this indicator in the dataframe (a string)
            - a dictionary containing the parameters used to calculate the indicator (a dictionary).
            
            Thus, for instace, suppose we want to calculate a 5-days simple moving average and
            call it sma5. The tuple would be:
            ('sma', 'sma5', {'n': 5})
            
            If the column name is set to None (default), columns are named as the indicators they represent.
            For example,
            ('sma', None, {'n': 5})
            produces a column named 'sma'.
            
            Possible values for the short identifier (1st position in the tuple) are:
            
            -'sma' : simple moving average of stock price
            -'ema': exponential moving average of stock price
            -'rsi': Relative Strength Index
            -'bb': Bollinger Bands
            -'macd' : Moving Average Convergence-Divergence
            -'stoch': Stochastic Oscillator
            -'vwap': Volume Weighted Average Price
            -'atr': Average True Range
            -'adx': Average Directional Index
            -'psar': Parabolic SAR
            -'trix': Triple Exponential Average
            
        *include_flags: bool
            If True, includes a flags for bollinger bands and parabolic SAR.
            In the case of bollinger bands, two flags are created, 
            signaling whether stock price is close to the upper or lower bands.
            In the case of parabolic SAR, a single flag is created.
            This flag equals +1 if the trend reversed upwards, or -1 if the trend reversed downwards.
            In both cases, a flag value of zero means no flag at all i.e. a mere continuation of the previous trend.
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
        
        Setting include_flags = True creates 2 additional indicators:
        
        - bb_high_flag: 1 if stock price close to upper bollinger band, and 0 otherwise
        - bb_low_flag: 1 if stock price close to lower bollinger band, and 0 otherwise
        
        Selecting 'MACD' as an indicator, creates 3 indicators:
        
        - 'macd': MACD line
        - 'macd_signal': MACD signal line
        - 'macd_histogram': the difference between MACD and its signal line
        
        Selecting 'stoch' (stochastic) as an indicator, creates 2 indicators:
        
        - 'stoch': the stochastic oscillator 
        - 'stoch_signal': the stochastic oscillator signal

        Selecting 'psar' (parabolic SAR) as an indicator, creates 2 indicators:
        
        - 'psar_up': the parabolic SAR values during an upward trend. 
        - 'psar_down': the parabolic SAR values during a downward trend. 
        
        During a downward trend, psar_up values are N/A.
        Similarly, during an upward trend, psar_down values are N/A.
        As a result, this indicator is not considered when dropping missing values
        (which happens when the clean_dataframe parameter is set to TRUE).
        
        Setting include_flags = True creates an indicator which has value
        1, if it indicates an upward trend, and -1, if it indicates a downward trend.
        A value of zero means no price reversal is being suggested.

        If normalize=TRUE, the values of the following indicators
        will be divided by the stock's closing price each day:
        
        -'sma' : simple moving average of stock price
        -'ema': exponential moving average of stock price
        -'bb': Bollinger Bands
        -'macd' : Moving Average Convergence-Divergence line
        -'vwap': Volume Weighted Average Price
        -'atr': Average True Range
        -'psar': Parabolic SAR
        -'trix': Triple Exponential Average

        Examples:
        --------
        >>> s = stock('petr4','brazil')
        >>> s.get_stock_historical_prices('30/10/2020', '30/11/2020')
        >>> s.technical_indicators()
        
        Raises:
        -------
        Assertion Error if two columns have the same name
        
        References:
        -----------
        
        In this package, we use the ta package, developped by Darío López Padial (aka Bukosabino)
        and available at https://github.com/bukosabino/ta.
        I was unable to find a proper way to reference this package.
       
        '''
        
        import ta #technical analysis indicators
        
        #Get historical prices
        df = self.historical_prices
        
        #Get indicators names
        indicators_names = list(map(lambda x: x[0], indicators))
                    
        #Set missing names of columns
        #The column names appear on the second element of the indicator's tuple.
        #If it is None, we set it equal to the indicator name
        indicators = list(map(lambda x: 
                              (x[0], x[0], x[2]) if x[1] == None
                              else x, indicators))
        
        #assert column names are unique
        assert len(set([i[1] for i in indicators])) == len(indicators), 'Two or more indicators have the same name. Please specify a unique name for each indicator'
                
        #setup for normalization
        if normalize:
            #normalization factor
            nf = 1/df.Close
        else:
            nf = 1
        
        ## Calculate all indicators requested by user
        for i in indicators:
            df = self.__calculate_indicator(i, nf = nf, include_flags = include_flags)
        
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
    
    def heikenashi(self):
        
        '''Calculates the Heiken-Ashi candles time series
        
        Parameters:
        -----------
        None
        
        Returns:
        --------
        Pandas DataFrame
        A dataframe with columns Open, High, Low and Close, containing Heiken-Ashi prices
        time series
        
        '''
        
        import pandas as pd
        
        #Get data on historical prices
        df = self.historical_prices
        
        #Select only info referring to prices
        #i.e. drop volume
        price_columns = ['Open','High','Low','Close']
        df = df.loc[:, price_columns]
        
        #Create dataframe to store Heiken-Ashi prices
        ha = pd.DataFrame(columns = price_columns) #ha, as in Heiken-Ashi
        
        #Calculate Heiken-Ashi prices and populate dataframe
        ha['Low'] = df.apply(lambda x: min(x),axis = 1)
        ha['High'] = df.apply(lambda x: max(x),axis = 1)
        ha['Open'] = df.shift(1).apply(lambda x: (x[0] + x[3])/2, axis=1)
        ha['Close'] = df.apply(lambda x: sum(x)/4, axis = 1)
        
        return(ha)
       
       
       
    

    


        