"""Create: Players shift matrix (player x shifts matrix with 1 if the players plays home team on the shift -1 if away)

The function in this file will load in the Shift CSV conver tit to the required np.array for calculations

Author: Tim Moore
Date: 22-04-22
"""
import pandas as pd
import os
import numpy as np

def shifts_converter(shift):
    shift_dict = {}
    shift = shift.drop(['Unnamed: 0','Time', 'Goals'], axis = 1)
    np_shift = shift.to_numpy().astype(int)
    print(np_shift)
    shift_index = 0
    for i in np_shift:
        shift_player = 0
        for j in i:
            if j not in shift_dict:
                shift_dict{j}


if __name__ == '__main__':
    path = os.getcwd()
    directory = os.path.join(path,"hockey_scraper_data","csvs")
    with open(os.path.join(directory,"Shifts.csv"), "+r") as f:
        current_df = pd.read_csv(f)
    shift_mat  = shifts_converter(current_df)
    #shift_mat.to_csv(os.path.join(directory,'ShiftMatrix.csv'))
