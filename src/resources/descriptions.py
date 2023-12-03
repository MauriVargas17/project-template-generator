sentiment_description = """
    This endpoint analyzes sentiment of financial text.

    Args:
        text (str): Text to analyze sentiment of in ENGLISH.

    Returns:
        Sentiment: Sentiment of the text, with confidence and how positive or negative it is, plus the time it took to analyze.

    Examples:
        "Stock Prices Soar as Company Beats Earnings Expectations"
        "Global Markets Experience Volatility Amid Economic Uncertainty"
        "Tech Giant Announces Record-Breaking Profits in Q3"
        "Investors React to Central Bank's Decision on Interest Rates"
        "Market Analysts Predict a Bearish Trend in the Coming Weeks"
       
    """
analysis_description = """
    This endpoint analyzes financial text.
          
    Args:
        text (str): Text to analyze sentiment of in ENGLISH.
          
    Returns:
        Analysis: Analysis of the text, with POS tagging, NER, embedding and sentiment, plus the time it took to analyze.
    
    Examples:
        "Stock Prices Soar as Company Beats Earnings Expectations as said by analyst Jack Dorsey at Yahoo Finance"
        "Global Markets Experience Volatility Amid Economic Uncertainty according to Wall Street Journal president Steven Mnuchin"
        "Tech Giant Announces Record-Breaking Profits in Q3 since investing in emerging markets such as China and India"
        "Investors React to Central Bank's Decision on Interest Rates made by the Fed"
        "Market Analysts Predict a Bearish Trend in the Coming Weeks, as said by recognized investor Gary Marcus"  
          """

reports_description = """
    This endpoint generates a report of financial analysis.
    It will include all entries made with the endpoint /analysis.

    Returns:
        CSV with all entries made with the endpoint /analysis

    

"""