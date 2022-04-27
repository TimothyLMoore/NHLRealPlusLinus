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

    shift_index = 0
    for i in np_shift:
        shift_player = 0
        for j in i:
            if j not in shift_dict:
                shift_dict[j] = [[],[]]
            if 0 <= shift_player <= 5:
                shift_dict[j][0].append(shift_index)
            else:
                shift_dict[j][1].append(shift_index)
            shift_player += 1
        shift_index += 1


    shift_list = []
    for key, val in shift_dict.items():
        shift_list.append([key, val])

    shift_list.sort()

    shift_matrix = np.zeros((len(shift_list),len(shift)),dtype=int)
    for i in range(len(shift_list)):
        for j in shift_list[i][1][0]:
            shift_matrix[i][j] = -1
        for j in shift_list[i][1][1]:
            shift_matrix[i][j] = 1


    print(np.shape(shift_matrix))

    return shift_matrix, np.absolute(shift_matrix)


if __name__ == '__main__':
    path = os.getcwd()
    directory = os.path.join(path,"hockey_scraper_data","csvs")
    with open(os.path.join(directory,"Shifts.csv"), "+r") as f:
        current_df = pd.read_csv(f)
    net_shift_mat, tot_shift_mat  = shifts_converter(current_df)
    #net_shift_mat.tofile(os.path.join(directory,'NetShiftMatrix.csv'), sep = ',')
    #tot_shift_mat.tofile(os.path.join(directory,'TotalShiftMatrix.csv'), sep = ',')
