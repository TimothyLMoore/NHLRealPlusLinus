"""Clean Game Data

The function in this file read in each season CSV into a dataframe extract the necessary data into a
more manageable dataframe

Author: Tim Moore
Date: 22-04-06
"""

import pandas as pd
import os

def CleanData(directory):
    df = pd.DataFrame()
    for root,dirs,files in os.walk(directory):
        for file in files:
           if file.endswith(".csv"):
               with open(os.path.join(directory,file), "+r") as f:
                    current_df = pd.read_csv(f)
                    df = df.append(current_df)
    df.to_csv(os.path.join(directory,'combined_data.csv'))


if __name__ == '__main__':
    path = os.getcwd()
    USER_PATH = os.path.join(path,"hockey_scraper_data","csvs")
    CleanData(USER_PATH)
