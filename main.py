#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   main.py
@Time    :   2025/06/16 07:58:18
@Author  :   He, Tian Lightis
@Version :   1.0
@Contact :   lightis_tian@163.com
@Desc    :   It's to generate e excel report to show player's salary in every minutes
'''

from loguru import logger
from utils.data import DataLoader, save_as_excel


def player_salary_on_play_time(config_file:str):
    """
    Generate a report of player salary on play minutes.
    Args:
        config_file (str): Path to the YAML configuration file.
    Returns:
        pd.DataFrame: DataFrame containing player statistics with salary per minute.
    """
    logger.info("Generating player salary report based on play minutes...")

    # Load the dataset
    data_loader = DataLoader(config_file=config_file)
    data_loader.load_data()

    # Generate the report
    player_stats = data_loader.datasets['player_stats']
    player_salary = data_loader.datasets['player_salaries']

    # Calculate player salary on each play minutes
    df = player_stats.merge(player_salary,
                            left_on='name',
                            right_on='Player',
                            how='left')

    df['salary_per_minute'] = df['Annual'] / df['minutes']

    # Format report: Order, Rename, Style...
    df.columns = df.columns.str.lower().str.replace(' ', '_')
    df = df[['name', 'team', 'age', 'nation', 'position', 'minutes', 'salary_per_minute']]

    save_as_excel(df, 'player_salary_report.xlsx')


if __name__ == '__main__':
    player_salary_on_play_time('utils/dataset.yaml')
