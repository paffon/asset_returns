import pandas as pd


def calculate_profit_percentage(prices: pd.Series,
                                start_date: str,
                                end_date: str) -> float:
    """
    Calculates the percentage of profit for buying in the first date and selling in the second date.
    If the provided start or end date is not found, it picks the closest available date following it.

    :param prices: Pandas series of closing prices for the ticker. Index should be datetime64[ns].
    :param start_date: Start date in 'YYYY-MM-DD' format.
    :param end_date: End date in 'YYYY-MM-DD' format.

    :return: Percentage of profit as a float value if dates are valid, otherwise asset_returns an error message.
    """

    # Convert start_date and end_date to datetime format
    start_date = pd.to_datetime(start_date)
    end_date = pd.to_datetime(end_date)

    # If start_date is not found, get the next available date
    if start_date not in prices.index:
        start_date = prices.index[prices.index > start_date].min()

    # If end_date is not found, get the next available date
    if end_date not in prices.index:
        end_date = prices.index[prices.index > end_date].min()

    # Get closing prices for start_date and end_date
    start_price = prices.loc[start_date]
    end_price = prices.loc[end_date]

    # Calculate profit percentage
    profit_percentage = ((end_price - start_price) / start_price) + 1

    return profit_percentage
