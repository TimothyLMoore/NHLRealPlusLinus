"""Clean Game Data

The function in this file read in each season CSV into a dataframe extract the necessary data into a
more manageable dataframe

Author: Tim Moore
Date: 22-04-06
"""

import pandas as pd
import os

def CleanData(directory):
    drop_cols = ['Unnamed: 0',
                 'Game_Id',
                 'Date',
                 'Description',
                 'Time_Elapsed',
                 'Strength',
                 'Ev_Zone',
                 'Type',
                 'Ev_Team',
                 'Home_Zone',
                 'Away_Team',
                 'Home_Team',
                 'p1_name',
                 'p1_ID',
                 'p2_name',
                 'p2_ID',
                 'p3_name',
                 'p3_ID',
                 'awayPlayer1',
                 'awayPlayer2',
                 'awayPlayer3',
                 'awayPlayer4',
                 'awayPlayer5',
                 'awayPlayer6',
                 'homePlayer1',
                 'homePlayer2',
                 'homePlayer3',
                 'homePlayer4',
                 'homePlayer5',
                 'homePlayer6',
                 'Away_Players',
                 'Home_Players',
                 'Away_Score',
                 'Home_Score',
                 'Away_Goalie',
                 'Away_Goalie_Id',
                 'Home_Goalie',
                 'Home_Goalie_Id',
                 'xC',
                 'yC',
                 'Home_Coach',
                 'Away_Coach']

    df = pd.DataFrame()
    for root,dirs,files in os.walk(directory):
        for file in files:
           if file.endswith(".csv"):
               with open(os.path.join(directory,file), "+r") as f:
                    current_df = pd.read_csv(f)
                    df = df.append(current_df)
    df_5v5 = df[df['Strength'] == "5x5"]
    df_cleaned = df_5v5.drop(drop_cols, axis = 1)
    df_cleaned.to_csv(os.path.join(directory,'CleanedData.csv'))


if __name__ == '__main__':
    path = os.getcwd()
    USER_PATH = os.path.join(path,"hockey_scraper_data","csvs")
    CleanData(USER_PATH)
