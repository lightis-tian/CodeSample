#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   data.py
@Time    :   2025/06/16 07:56:16
@Author  :   He, Tian Lightis
@Version :   1.0
@Contact :   lightis_tian@163.com
@Desc    :   It's a code sample to load datasets from a YAML configuration file.
'''

from pathlib import Path
import pandas as pd
import yaml
from loguru import logger



class DataLoader:
    """
    DataLoader class to load datasets from a configuration file.
    This class reads a YAML configuration file to determine the paths and columns of datasets,
    and loads the datasets into pandas DataFrames.
    Attributes:
        datasets (dict): A dictionary to store loaded datasets.
        config (dict): Configuration loaded from the YAML file.
    """

    def __init__(self, config_file: str):
        self.datasets = {}
        with open(config_file, 'r', encoding='utf-8') as file:
            self.config = yaml.safe_load(file)

        logger.info(f"DataLoader initialized with config file: {config_file}")


    def load_data(self) -> pd.DataFrame:
        """
        Load dataset from config file.

        Returns:
            dict{dataset_name: pd.DataFrame}
        """
        try:
            for dataset in self.config.keys():
                target_path = self.__get_dataset_path(self.config[dataset]['path'])
                data = pd.read_csv(target_path, usecols=self.config[dataset]['columns'])

                self.datasets[dataset] = data
        except pd.errors.EmptyDataError:
            logger.exception("No data found in the file.")
        except (FileNotFoundError, pd.errors.ParserError, KeyError) as e:
            logger.exception(f"An error occurred while loading the data: {e}")


    def __get_dataset_path(self, path: str) -> Path:
        """
        Get the path to the dataset file.

        Args:
            path (str): Path configured in the config YAML file.

        Returns: dataset path
        """
        if Path(path).is_absolute():
            target_path = Path(path)
        else:
            target_path = Path.cwd().parent / 'Datasets' / path
        return target_path


    def save_dataset_csv(self, dataset_name: str, save_path: str):
        """
        Save a specific dataset to a CSV file.

        Args:
            dataset_name (str): The name of the dataset to save.
            file_path (str): The path where the dataset should be saved.
        """
        if dataset_name in self.datasets:
            self.datasets[dataset_name].to_csv(save_path, index=False)
            logger.info(f"Dataset '{dataset_name}' saved to {save_path}")
        else:
            logger.error(f"Dataset '{dataset_name}' not found.")


def save_as_excel(data: pd.DataFrame, file_path: str, **kwargs):
    """
    Save a DataFrame to an Excel file.
    Will ceate the directory if it does not exist and ensure the file has a .xlsx extension.

    Args:
        data (pd.DataFrame): The DataFrame to save.
        file_path (str): The path where the Excel file should be saved.
        **kwargs: Additional keyword arguments for pandas Excel writer.
    """
    try:
        file_path = Path(file_path)
        if file_path.suffix.lower() != '.xlsx':
            file_path = file_path.with_suffix('.xlsx')
        # Ensure the directory exists
        file_path.parent.mkdir(parents=True, exist_ok=True)

        kwargs['index'] = kwargs.get('index', False)

        data.to_excel(file_path, engine='openpyxl', **kwargs)
        logger.info(f"Data saved to {file_path}")
    except (ValueError, FileNotFoundError, PermissionError) as e:
        logger.error(f"Failed to save data to Excel: {e}")
