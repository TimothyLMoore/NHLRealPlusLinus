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
    time = shift['Time'].to_numpy()
    pd_goal = shift['Goals'].div(shift['Time'])
    pd_goal = pd_goal.multiply(3600)
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
    w_shift_matrix = np.zeros((len(shift_list),len(shift)),dtype=int)
    for i in range(len(shift_list)):
        for j in shift_list[i][1][0]:
            w_shift_matrix[i][j] = -1 * time[j]
            shift_matrix[i][j] = -1
        for j in shift_list[i][1][1]:
            w_shift_matrix[i][j] = 1 * time[j]
            shift_matrix[i][j] = 1 * time[j]

    print("XtwX1.....")
    XtwX = np.matmul(w_shift_matrix, np.transpose(shift_matrix))
    print("Ridge1...")
    ridge = np.add(XtwX, np.identity(len(shift_list)))
    print("Inverse1.....")
    XtwXinv = inv(ridge)
    print("Xtwb1.....")
    Xtwb = np.matmul(XtwXinv,w_shift_matrix)
    print("NetGoals.....")
    net_goals = np.matmul(Xtwb, np_goal)

    print("XtwX2.....")
    XtwX = np.matmul(np.absolute(w_shift_matrix), np.transpose(np.absolute(shift_matrix)))
    print("Ridge2...")
    ridge = np.add(XtwX, np.identity(len(shift_list)))
    print("Inverse2.....")
    XtwXinv = inv(ridge)
    print("Xtwb2.....")
    Xtwb = np.matmul(XtwXinv,np.absolute(w_shift_matrix))
    print("TotGoals.....")
    tot_goals = np.matmul(Xtwb, tot_goal)

    total_time = w_shift_matrix.sum(axis=1)

    return np.transpose(net_goals), np.transpose(tot_goals), np.transpose(total_time)


if __name__ == '__main__':
    path = os.getcwd()
    directory = os.path.join(path,"hockey_scraper_data","csvs")
    with open(os.path.join(directory,"Shifts.csv"), "+r") as f:
        current_df = pd.read_csv(f)
    net_goal_mat, tot_goal_mat, TOI  = shifts_converter(current_df)
    net_goal_mat.tofile(os.path.join(directory,'NetGoals.csv'), sep = ',')
    tot_goal_mat.tofile(os.path.join(directory,'TotalGoals.csv'), sep = ',')
    TOI.tofile(os.path.join(directory,'TOI.csv'), sep = ',')
