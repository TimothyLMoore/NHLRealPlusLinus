"""Convert Cleaned Data into easier to process shifts

The function in this file will load in the clean CSV and combine multiple rows where the same players play into 1 shift for easier processing

Author: Tim Moore
Date: 22-04-12
"""
import pandas as pd
import os

def shifts(clean_data):
    """
    Further Data Cleaning function takes in previous dataframe and return a dataframe with each shift combined into 1 row

    :param clean_data: dataframe output by previous module

    :return: shift_df
    """

    # Create the output DF
    shift_df = pd.DataFrame(columns = ['Time', 'Goals','NetCorsi','TotCorsi',
                  'awayPlayer1_id',
                  'awayPlayer2_id',
                  'awayPlayer3_id',
                  'awayPlayer4_id',
                  'awayPlayer5_id',
                  'homePlayer1_id',
                  'homePlayer2_id',
                  'homePlayer3_id',
                  'homePlayer4_id',
                  'homePlayer5_id',
                  ])

    #Iterate through the cleaned df
    for i, row in clean_data.iterrows():


        if i % 1000 == 0:
            print(i/len(clean_data)*100, "%")

        #Required for initial shift
        if i == 0:
            shift_start = row.copy()
            goal = 0
            netCorsi = 0
            totCorsi = 0
            start_time=0
            last_index = -1


        if row['Event'] == "GOAL":
            if row["p1_ID"] in [row['homePlayer1_id'], row['homePlayer2_id'],
                                row['homePlayer3_id'], row['homePlayer4_id'],
                                row['homePlayer5_id']]:
                goal += 1
                netCorsi += 1
                totCorsi += 1
            else:
                goal -= 1
                netCorsi -= 1
                totCorsi += 1

        if row['Event'] == "SHOT" or row['Event'] == "MISS" or row['Event'] == "BLOCK":
            if row["p1_ID"] in [row['homePlayer1_id'], row['homePlayer2_id'],
                                row['homePlayer3_id'], row['homePlayer4_id'],
                                row['homePlayer5_id']]:
                netCorsi += 1
                totCorsi += 1
            else:
                netCorsi -= 1
                totCorsi += 1

        #Comparing rows to see shift changes ***Can this be cleaner?***
        if (row["Unnamed: 0"] != last_index + 1 or shift_start['Period'] != row['Period'] or shift_start['awayPlayer1_id'] != row['awayPlayer1_id'] or
        shift_start['awayPlayer2_id'] != row['awayPlayer2_id'] or shift_start['awayPlayer3_id'] != row['awayPlayer3_id'] or
        shift_start['awayPlayer4_id'] != row['awayPlayer4_id'] or shift_start['awayPlayer5_id'] != row['awayPlayer5_id'] or
        shift_start['homePlayer1_id'] != row['homePlayer1_id'] or shift_start['homePlayer2_id'] != row['homePlayer2_id'] or
        shift_start['homePlayer3_id'] != row['homePlayer3_id'] or shift_start['homePlayer4_id'] != row['homePlayer4_id'] or
        shift_start['homePlayer5_id'] != row['homePlayer5_id']):

            toi = last_time-start_time

            if toi <= 0: #Can't have shift with 0 time
                toi = 1

            shift_df.loc[len(shift_df.index)] = [toi, goal, netCorsi, totCorsi,
                                                     shift_start['awayPlayer1_id'], shift_start['awayPlayer2_id'],
                                                     shift_start['awayPlayer3_id'], shift_start['awayPlayer4_id'],
                                                     shift_start['awayPlayer5_id'], shift_start['homePlayer1_id'],
                                                 shift_start['homePlayer2_id'], shift_start['homePlayer3_id'],
                                                 shift_start['homePlayer4_id'], shift_start['homePlayer5_id']]
            goal = 0
            netCorsi = 0
            totCorsi = 0
            shift_start = row.copy()
            start_time = last_time
            if row["Unnamed: 0"] != last_index + 1:
                start_time = row["Seconds_Elapsed"]

        last_index = row["Unnamed: 0"]
        last_time=row["Seconds_Elapsed"]


    return shift_df

if __name__ == '__main__':
    path = os.getcwd()
    directory = os.path.join(path,"hockey_scraper_data","csvs")
    with open(os.path.join(directory,"CleanedData.csv"), "+r") as f:
        current_df = pd.read_csv(f)
    out_df = shifts(current_df)
    out_df.to_csv(os.path.join(directory,'Shifts.csv'))


