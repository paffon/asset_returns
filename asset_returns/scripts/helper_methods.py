from datetime import datetime
from typing import List
import os

import pandas as pd


def days_since_2008():
    """
    Calculates the number of days since January 1st, 2008, up to the current date.

    :return: Number of days (integer).
    """
    # Get the current date
    current_date = datetime.now()

    # January 1st, 2008
    start_date = datetime(2008, 1, 1)

    # Calculate the difference in days
    days_difference = (current_date - start_date).days

    return days_difference


def find_extreme_price_dates(
        prices: pd.Series, start_date: str,
        time_delta: pd.Timedelta, min_or_max: str
) -> List[str]:
    """
    Divides the prices series into chunks, starting from the start_date.
    Finds either minimum or maximum prices within each chunk and asset_returns the dates when these extreme prices occurred.

    :param prices: Pandas series of prices for the ticker. Index should be datetime64[ns].
    :param start_date: Starting date in 'YYYY-MM-DD' format.
    :param time_delta: Time delta to determine chunk size.
    :param min_or_max: Specify 'min' to find minimum prices or 'max' to find maximum prices.

    :return: List of dates when the extreme prices were found within each chunk.
    """

    # Convert start_date to datetime format and handle an invalid date format
    start_date = pd.to_datetime(start_date)

    # Determine whether to use min() or max() function
    if min_or_max == 'min':
        extreme_function = min
    elif min_or_max == 'max':
        extreme_function = max
    else:
        raise ValueError("Invalid min_or_max parameter. Choose 'min' or 'max'.")

    # Initialize list to store dates of extreme prices
    extreme_price_dates = []

    # Create chunks based on time_delta starting from start_date
    current_date = start_date
    while current_date < prices.index[-1]:
        chunk = prices.loc[current_date: current_date + time_delta]

        # Find the date(s) of the extreme price in the chunk
        if not chunk.empty:
            extreme_price_date = chunk[chunk == extreme_function(chunk)].index.strftime('%Y-%m-%d').tolist()
            extreme_price_dates.extend(extreme_price_date)

        current_date += time_delta

    return extreme_price_dates


def find_target_folder(target_folder: str, inner_path: str) -> str:
    current_dir = os.getcwd()  # Get the current directory

    while not os.path.basename(current_dir) == target_folder and current_dir != "/":
        current_dir = os.path.dirname(current_dir)  # Move up one level

    result = os.path.join(current_dir, inner_path)

    return result


def enrich_series(series: dict, step_size: int, steps: int) -> dict:
    enriched_series = series.copy()

    for i in range(1, steps + 1):
        for asset_name, price_series in series.items():
            new_name = f'{asset_name}-{step_size * i}-shift'
            shifted_series = price_series.shift(-i * step_size, freq='D')  # Shift the series by step_size * i
            enriched_series[new_name] = shifted_series

    return enriched_series
