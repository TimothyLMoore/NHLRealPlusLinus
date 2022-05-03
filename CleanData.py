"""Clean Game Data

The function in this file read in each season CSV into a dataframe extract the necessary data into a
more manageable dataframe

Author: Tim Moore
Date: 22-04-06
"""

import pandas as pd
import os
import math

def CleanData(directory):
    """
    Data Cleaning function takes in all data in csvs folders
    creates anew dataframe with events, periods, seconds elapsed, and all players playing
    Then write that Dataframe to the csvs folder.

    :param directory: directory where season csvs are lovated

    :return: None
    """
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

    player_list = {}

    df = pd.DataFrame()
    for root,dirs,files in os.walk(directory):
        for file in files:
           if file.endswith(".csv"):
               with open(os.path.join(directory,file), "+r") as f:
                    current_df = pd.read_csv(f)
                    df = df.append(current_df)

    df_5v5 = df[df['Strength'] == "5x5"]

    for i, row in df_5v5.iterrows():
        if row["awayPlayer1_id"] not in player_list and not (math.isnan(row["awayPlayer1_id"])):
            player_list[row["awayPlayer1_id"]] = row["awayPlayer1"]
        if row["awayPlayer2_id"] not in player_list and not (math.isnan(row["awayPlayer2_id"])):
            player_list[row["awayPlayer2_id"]] = row["awayPlayer2"]
        if row["awayPlayer3_id"] not in player_list and not (math.isnan(row["awayPlayer3_id"])):
            player_list[row["awayPlayer3_id"]] = row["awayPlayer3"]
        if row["awayPlayer4_id"] not in player_list and not (math.isnan(row["awayPlayer4_id"])):
            player_list[row["awayPlayer4_id"]] = row["awayPlayer4"]
        if row["awayPlayer5_id"] not in player_list and not (math.isnan(row["awayPlayer5_id"])):
            player_list[row["awayPlayer5_id"]] = row["awayPlayer5"]
        if row["awayPlayer6_id"] not in player_list and not (math.isnan(row["awayPlayer6_id"])):
            player_list[row["awayPlayer6_id"]] = row["awayPlayer6"]
        if row["homePlayer1_id"] not in player_list and not (math.isnan(row["homePlayer1_id"])):
            player_list[row["homePlayer1_id"]] = row["homePlayer1"]
        if row["homePlayer2_id"] not in player_list and not (math.isnan(row["homePlayer2_id"])):
            player_list[row["homePlayer2_id"]] = row["homePlayer2"]
        if row["homePlayer3_id"] not in player_list and not (math.isnan(row["homePlayer3_id"])):
            player_list[row["homePlayer3_id"]] = row["homePlayer3"]
        if row["homePlayer4_id"] not in player_list and not (math.isnan(row["homePlayer4_id"])):
            player_list[row["homePlayer4_id"]] = row["homePlayer4"]
        if row["homePlayer5_id"] not in player_list and not (math.isnan(row["homePlayer5_id"])):
            player_list[row["homePlayer5_id"]] = row["homePlayer5"]
        if row["homePlayer6_id"] not in player_list and not (math.isnan(row["homePlayer6_id"])):
            player_list[row["homePlayer6_id"]] = row["homePlayer6"]


    players = pd.DataFrame.from_dict(player_list, orient='index')

    df_cleaned = df_5v5.drop(drop_cols, axis = 1)
    df_cleaned.to_csv(os.path.join(directory,'CleanedData.csv'))
    players.to_csv(os.path.join(directory,'Players.csv'))


if __name__ == '__main__':
    path = os.getcwd()
    USER_PATH = os.path.join(path,"hockey_scraper_data","csvs")
    CleanData(USER_PATH)
