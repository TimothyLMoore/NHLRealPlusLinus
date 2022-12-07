"""NHL Game Data Downloader

The function in this file will download the data produced by the nhl for all game sinthe requested season and
dump a seperate CSV for each season in a folder called "hockey_scraper_data" from where the file was run.

Author: Tim Moore
Date: 22-04-06
"""

import hockey_scraper
import os

def downloadGames(years):
    """
    Scrape the data for the years required for calculation

    :param years: Years of games you wish to download

    :return: None
    """

    path = os.getcwd()
    USER_PATH = os.path.join(path,"hockey_scraper_data")

    if os.path.exists(USER_PATH):
        print("Path is good")
    else:
        os.mkdir(USER_PATH)
        print("Path created")

    for year in years:
        hockey_scraper.scrape_seasons([year], False, docs_dir=USER_PATH)

if __name__ == '__main__':
    years_to_download = [2022]
    downloadGames(years_to_download)


