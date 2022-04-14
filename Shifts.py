"""Convert Cleaned Data into easier to process shifts

The function in this file will load in the clean CSV and combine multiple rows where the same players play into 1 shift for easier processing

Author: Tim Moore
Date: 22-04-12
"""
import pandas as pd

def shifts(clean_data):
    shift_df = pd.Dataframe()
    for i, row in clean_data.iterrows():
        if i == 0:
            shift_start = row
        if shift_start["period"] != row["period"]:

