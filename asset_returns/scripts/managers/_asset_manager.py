import json
import os
from typing import List

import pandas as pd

from scripts.matcher import match_asset_choice
from scripts.gain_calculator import calculate_profit_percentage


def read_config(config_name: str):
    """
    Reads the <name>_config.json file located two folders up in the config
    directory.

    :return: Dictionary containing the data from the config file as dict.
    """
    # Get the current script's directory
    script_dir = os.path.dirname(os.path.abspath(__file__))

    # Navigate two folders up to reach the config directory
    config_path = os.path.abspath(
        os.path.join(script_dir, f'../../config/{config_name}.json')
    )

    # Read the JSON file
    with open(config_path, 'r') as file:
        config_data = json.load(file)
    file.close()

    return config_data


class AssetManager:
    def __init__(self, config_name: str) -> None:
        config = read_config(config_name)

        self._asset_type = config['asset_type']
        self._options = config['options']

        # maps from the actual asset name to the prices series
        self._assets_series = {}

    def _match_asset_choice(self, user_input: str) -> str:
        return match_asset_choice(
            user_input=user_input,
            asset_dict=self._options,
            asset_class=self._asset_type)

    def load_multiple(self, assets: List[str]) -> None:
        for asset in assets:
            self.load_single(asset=asset)

    def load_single(self, asset: str) -> pd.Series:
        """
        Loads the data for the given asset if it wasn't loaded already, and returns it.
        """
        if asset not in self._options.values():
            asset = self._match_asset_choice(asset)

        if asset not in self._assets_series:
            print(f'Getting {asset} data')
            self._assets_series[asset] = self._get_prices_data_from_api(asset)

        return self._assets_series[asset]

    def _get_prices_data_from_api(self, asset: str) -> pd.Series:
        """
        Returns a pd.Series with index of type datetime64[ns].
        :param asset: name of the asset.
        :return: the data of the asset in  a dataframe format.
        """
        raise NotImplementedError("_get_data_from_api() method not implemented"
                                  f" for {self.__class__.__name__}")

    def calculate_profit(self,
                         asset: str,
                         start_date: str,
                         end_date: str) -> float:

        prices = self.load_single(asset=asset)

        return calculate_profit_percentage(
            prices=prices,
            start_date=start_date,
            end_date=end_date)
