"""Create: Players shift matrix (player x shifts matrix with 1 if the players plays home team on the shift -1 if away)

The function in this file will load in the Shift CSV conver tit to the required np.array for calculations

Author: Tim Moore
Date: 22-04-22
"""
import pandas as pd
import os
import numpy as np
from numpy.linalg import inv

def shifts_converter(shift, players):

    shift = shift.dropna()

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

    play_order = []
    shift_list = []
    for key, val in shift_dict.items():
        shift_list.append([key, val])
        play_order.append(key)

    play_order.append(9999999)


    shift_matrix = np.zeros((len(shift_list),len(shift)),dtype=int)
    w_combined_shift = np.zeros((1,len(shift)),dtype=int)
    combined_shift = np.zeros((1,len(shift)),dtype=int)
    w_shift_matrix = np.zeros((len(shift_list),len(shift)),dtype=int)
    for i in range(len(shift_list)):
        for j in shift_list[i][1][0]:
            w_shift_matrix[i][j] = -1 * time[j]
            shift_matrix[i][j] = -1
        for j in shift_list[i][1][1]:
            w_shift_matrix[i][j] = 1 * time[j]
            shift_matrix[i][j] = 1

    total_time = np.absolute(w_shift_matrix).sum(axis=1)
    del_rows = []
    for i in range(len(total_time)):
        if total_time[i] < 90000:
            combined_shift = np.add(combined_shift, shift_matrix[i])
            w_combined_shift = np.add(w_combined_shift, w_shift_matrix[i])
            del_rows.append(i)

    shift_matrix = np.delete(shift_matrix, (del_rows), axis=0)
    shift_matrix = np.append(shift_matrix,combined_shift, axis = 0)
    w_shift_matrix = np.delete(w_shift_matrix, (del_rows), axis=0)
    w_shift_matrix = np.append(w_shift_matrix,w_combined_shift, axis = 0)
    total_time = np.delete(total_time, (del_rows), axis=0)
    total_time = np.append(total_time,np.absolute(w_combined_shift).sum(axis=1), axis = 0)


    for i in sorted(del_rows, reverse=True):
        del play_order[i]

    print("XtwX1.....")
    XtwX = np.matmul(w_shift_matrix, np.transpose(shift_matrix))
    print(XtwX)
    print("Ridge1...")
    ridge = np.add(XtwX, np.identity(len(total_time)))
    print(ridge)
    print("Inverse1.....")
    XtwXinv = inv(ridge)
    print(XtwXinv)
    print("Xtwb1.....")
    Xtwb = np.matmul(XtwXinv,w_shift_matrix)
    print(Xtwb)
    print("NetGoals.....")
    net_goals = np.matmul(Xtwb, np_goal)
    print(net_goals)

    print("XtwX2.....")
    XtwX = np.matmul(np.absolute(w_shift_matrix), np.transpose(np.absolute(shift_matrix)))
    print(XtwX)
    print("Ridge2...")
    ridge = np.add(XtwX, np.identity(len(total_time)))
    print(ridge)
    print("Inverse2.....")
    XtwXinv = inv(ridge)
    print(XtwXinv)
    print("Xtwb2.....")
    Xtwb = np.matmul(XtwXinv,np.absolute(w_shift_matrix))
    print(Xtwb)
    print("TotGoals.....")
    tot_goals = np.matmul(Xtwb, tot_goal)
    print(tot_goals)



    pd_net_goals = pd.DataFrame(net_goals, index = play_order, columns = ["NetGoals"])
    pd_tot_goals = pd.DataFrame(tot_goals, index = play_order, columns = ["TotGoals"])
    pd_toi = pd.DataFrame(total_time, index = play_order, columns = ["TOI"])

    combined = pd.concat([pd_net_goals, pd_tot_goals, pd_toi], axis = 1)

    '''print(players)
    print(combined)
    combined.join(players, on=None, how='left')'''
    return combined


if __name__ == '__main__':
    path = os.getcwd()
    directory = os.path.join(path,"hockey_scraper_data","csvs")
    with open(os.path.join(directory,"Shifts.csv"), "+r") as f:
        current_df = pd.read_csv(f)
    with open(os.path.join(directory,"Players.csv"), "+r") as f:
        player_df = pd.read_csv(f)
    combined_final  = shifts_converter(current_df, player_df)
    combined_final.to_csv(os.path.join(directory,'Final.csv'))
