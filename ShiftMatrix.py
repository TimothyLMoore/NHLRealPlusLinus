"""Create: Players shift matrix (player x shifts matrix with 1 if the players plays home team on the shift -1 if away)

The function in this file will load in the Shift CSV conver tit to the required np.array for calculations

Author: Tim Moore
Date: 22-04-22
"""
import pandas as pd
import os
import numpy as np
from numpy.linalg import inv

def shifts_converter(shift):
    shift_dict = {}
    pd_time = shift['Time']
    np_time = np.zeroes((len(pd_time), len(pd_time)), dtype=int)
    np.fill_diagonal(np_time, pd_time)
    pd_goal = shift['Goal'].div(shift['Time'])
    pd_goal = pd_goal.div(3600)
    np_goal = pd_goal.to_numpy()
    tot_goal = np.absolute(np_goal)
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


    Xtw = np.matmul(shift_matrix, np_time)
    XtwX = np.matmul(Xtw, np.transpose(shift_matrix))
    ridge = np.add(XtwX, np.identity(len(shift_list)))
    Xtwb = np.matmul(Xtw, np_goal)
    XtwXinv = inv(ridge)
    net_goals = np.matmul(XtwXinv, Xtwb)

    Xtw = np.matmul(np.absolute(shift_matrix), np_time)
    XtwX = np.matmul(Xtw, np.transpose(np.absolute(shift_matrix)))
    ridge = np.add(XtwX, np.identity(len(shift_list)))
    Xtwb = np.matmul(Xtw, tot_goal)
    XtwXinv = inv(ridge)
    tot_goals = np.matmul(XtwXinv, Xtwb)

    return net_goals, tot_goals


if __name__ == '__main__':
    path = os.getcwd()
    directory = os.path.join(path,"hockey_scraper_data","csvs")
    with open(os.path.join(directory,"Shifts.csv"), "+r") as f:
        current_df = pd.read_csv(f)
    net_goal_mat, tot_goal_mat  = shifts_converter(current_df)
    net_goal_mat.tofile(os.path.join(directory,'NetGoals.csv'), sep = ',')
    tot_goal_mat.tofile(os.path.join(directory,'TotalGoals.csv'), sep = ',')
