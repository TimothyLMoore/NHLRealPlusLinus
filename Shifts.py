"""Convert Cleaned Data into easier to process shifts

The function in this file will load in the clean CSV and combine multiple rows where the same players play into 1 shift for easier processing

Author: Tim Moore
Date: 22-04-12
"""
import pandas as pd
import os

def shifts(clean_data):
    check_cols = ['Period',
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
                  'homePlayer6_id']
    home_cols = ['homePlayer1_id',
                 'homePlayer2_id',
                 'homePlayer3_id',
                 'homePlayer4_id',
                 'homePlayer5_id',
                 'homePlayer6_id']
    shift_df = pd.DataFrame(columns = ['Time', 'Goals',
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
                  'homePlayer6_id'])
    for i, row in clean_data.iterrows():
        print(i)
        if i == 100:
            return shift_df

        if i == 0:
            shift_start = row.copy()

        goal = 0
        if row['Event'] == "GOAL":
            if row["p1_ID"] in row[home_cols]:
                goal += 1
            else:
                goal -= 1

        if (shift_start['Period'] != row['Period'] or shift_start['awayPlayer1_id'] != row['awayPlayer1_id'] or
        shift_start['awayPlayer2_id'] != row['awayPlayer2_id'] or shift_start['awayPlayer3_id'] != row['awayPlayer3_id'] or
        shift_start['awayPlayer4_id'] != row['awayPlayer4_id'] or shift_start['awayPlayer5_id'] != row['awayPlayer5_id'] or
        shift_start['homePlayer1_id'] != row['homePlayer1_id'] or shift_start['homePlayer2_id'] != row['homePlayer2_id'] or
        shift_start['homePlayer3_id'] != row['homePlayer3_id'] or shift_start['homePlayer4_id'] != row['homePlayer4_id'] or
        shift_start['homePlayer5_id'] != row['homePlayer5_id'] or shift_start['awayPlayer6_id'] != row['awayPlayer6_id'] or
        shift_start['homePlayer6_id'] != row['homePlayer6_id']):
            #print(shift_start)
            if (last_shift["Seconds_Elapsed"]-shift_start["Seconds_Elapsed"]) != 0:
                shift_df.loc[len(shift_df.index)] = [last_shift["Seconds_Elapsed"]-shift_start["Seconds_Elapsed"], goal,
                                                     shift_start['awayPlayer1_id'], shift_start['awayPlayer2_id'],
                                                     shift_start['awayPlayer3_id'], shift_start['awayPlayer4_id'],
                                                     shift_start['awayPlayer5_id'], shift_start['awayPlayer6_id'],
                                                     shift_start['homePlayer1_id'], shift_start['homePlayer2_id'],
                                                     shift_start['homePlayer3_id'], shift_start['homePlayer4_id'],
                                                     shift_start['homePlayer5_id'], shift_start['homePlayer6_id']]
            goal = 0
            shift_start = row.copy()



        last_shift = row.copy()

    return shift_df

if __name__ == '__main__':
    path = os.getcwd()
    directory = os.path.join(path,"hockey_scraper_data","csvs")
    with open(os.path.join(directory,"CleanedData.csv"), "+r") as f:
        current_df = pd.read_csv(f)
    out_df = shifts(current_df)
    out_df.to_csv(os.path.join(directory,'Shifts.csv'))

