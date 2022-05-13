"""This file completes the process of the calculation

Output a CSV with Players, Net Goals/60, Total Goals/60, Net Corsi/60, Total Corsi/60 and Offense and Defnse Contributions

Author: Tim Moore
Date: 22-04-22
"""
import pandas as pd
import os
import numpy as np
from numpy.linalg import inv

def shifts_converter(shift, players):
     """
    Combines Shift and Players CSV

    :param shift: dataframe output by previous module
           players: Data frame with Players ID and Names for join

    :return: combined: Dataframe with all desired information
    """

    new_row = {'PlayerID':9999999, 'Player':"Replacement Player"}
    players = players.append(new_row, ignore_index=True)
    shift = shift.dropna()

    shift_dict = {}
    time = shift['Time'].to_numpy()
    pd_goal = shift['Goals'].div(shift['Time'])
    pd_goal = pd_goal.multiply(3600)
    np_goal = pd_goal.to_numpy()
    pd_netCorsi = shift['NetCorsi'].div(shift['Time']).multiply(3600)
    np_netCorsi = pd_netCorsi.to_numpy()
    pd_totCorsi = shift['TotCorsi'].div(shift['Time']).multiply(3600)
    np_totCorsi = pd_totCorsi.to_numpy()
    tot_goal = np.absolute(np_goal)
    shift = shift.drop(['Unnamed: 0','Time', 'Goals','NetCorsi','TotCorsi'], axis = 1)
    np_shift = shift.to_numpy().astype(int)


    shift_index = 0
    for i in np_shift:
        shift_player = 0
        for j in i:
            if j not in shift_dict:
                shift_dict[j] = [[],[]]
            if 0 <= shift_player <= 4:
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
        if total_time[i] < 75000:
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
    print("Ridge1...")
    ridge = np.add(XtwX, np.identity(len(total_time)))
    print("Inverse1.....")
    XtwXinv = inv(ridge)
    print("Xtwb1.....")
    Xtwb = np.matmul(XtwXinv,w_shift_matrix)
    print("NetGoals.....")
    net_goals = np.matmul(Xtwb, np_goal)
    print("NetCorsi.....")
    net_corsi = np.matmul(Xtwb, np_netCorsi)


    print("XtwX2.....")
    XtwX = np.matmul(np.absolute(w_shift_matrix), np.transpose(np.absolute(shift_matrix)))
    print("Ridge2...")
    ridge = np.add(XtwX, np.identity(len(total_time)))
    print("Inverse2.....")
    XtwXinv = inv(ridge)
    print("Xtwb2.....")
    Xtwb = np.matmul(XtwXinv,np.absolute(w_shift_matrix))
    print("TotGoals.....")
    tot_goals = np.matmul(Xtwb, tot_goal)
    print("TotCorsi.....")
    tot_corsi = np.matmul(Xtwb, np_totCorsi)

    pd_players = pd.DataFrame(play_order, columns = ["PlayerID"])
    pd_players = pd.merge(pd_players, players, on = "PlayerID", how = "inner")
    pd_net_goals = pd.DataFrame(net_goals, columns = ["NetGoals"])
    pd_tot_goals = pd.DataFrame(tot_goals, columns = ["TotGoals"])
    pd_toi = pd.DataFrame(total_time, columns = ["TOI"])
    pd_toi = pd_toi.divide(60)
    pd_net_corsi = pd.DataFrame(net_corsi, columns = ["NetCorsi"])
    pd_tot_corsi = pd.DataFrame(tot_corsi, columns = ["TotCorsi"])

    combined = pd.concat([pd_players, pd_toi, pd_net_goals, pd_tot_goals, pd_net_corsi, pd_tot_corsi], axis = 1)
    combined['Offense'] = combined["NetGoals"] + combined["TotGoals"]
    combined['Offense'] = combined['Offense'].divide(2)
    combined['Defense'] = combined["NetGoals"] - combined["TotGoals"]
    combined['Defense'] = combined['Defense'].divide(2)
    combined['OffCorsi'] = combined["NetCorsi"] + combined["TotCorsi"]
    combined['OffCorsi'] = combined['OffCorsi'].divide(2)
    combined['DefCorsi'] = combined["NetCorsi"] - combined["TotCorsi"]
    combined['DefCorsi'] = combined['DefCorsi'].divide(2)

    return combined


if __name__ == '__main__':
    path = os.getcwd()
    directory = os.path.join(path,"hockey_scraper_data","csvs")
    with open(os.path.join(directory,"Shifts.csv"), "+r") as f:
        current_df = pd.read_csv(f)
    with open(os.path.join(directory,"Players.csv"), "+r") as f:
        player_df = pd.read_csv(f, header=None, names=['PlayerID', 'Player'])
    combined_final = shifts_converter(current_df, player_df)
    combined_final.to_csv(os.path.join(directory,'Final.csv'))
