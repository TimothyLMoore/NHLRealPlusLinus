"""Convert Cleaned Data into easier to process shifts

The function in this file will load in the clean CSV and combine multiple rows where the same players play into 1 shift for easier processing

Author: Tim Moore
Date: 22-04-12
"""
import pandas as pd

def shifts(clean_data):
    check_cols = ['period',
                  'awayPlayer1_id',
                  'awayPlayer2_id',
                  'awayPlayer3_id',
                  'awayPlayer4_id',
                  'awayPlayer5_id',
                  'awayPlayer6_id',
                  'homePlayer1_id',
                  'homePlayer2_id',
                  'homePlayer3_id',
                  'homePlayer4_id',
                  'homePlayer5_id',
                  'homePlayer6_id',]
    home_cols = ['homePlayer1_id',
                 'homePlayer2_id',
                 'homePlayer3_id',
                 'homePlayer4_id',
                 'homePlayer5_id',
                 'homePlayer6_id',]
    shift_df = pd.Dataframe()
    for i, row in clean_data.iterrows():
        if i == 0:
            shift_start = row

        goal = 0
        if row['Event'] == "Goal":
            if row["p1_id"] in row[home_cols]:
                goal += 1
            else:
                goal -= 1

        if shift_start[check_cols] != row[check_cols]:

