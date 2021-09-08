import csv
import pandas as pd
import time

file = "/home/ubuntu/RealTimeKin/0_Wireless/ Interval_IMU_data.csv"
cur_data = [1] * 13
cur_data[0] = 'WT530000141603'


# Atime = time.time()

csv_PD = pd.read_csv(file,index_col='ID')

# print(csv_PD)
# print(cur_data)
Atime = time.time()
csv_PD.loc[cur_data[0]] = cur_data[1:]
# row_id = csv_PD[csv_PD['ID'] == 
Btime = time.time()
csv_PD.to_csv(file)
# print(row_id)

# Btime = time.time()
print(Btime - Atime)
print(csv_PD)
# print(csv_PD.'ID'=='WT530000141603')
# cur_data = list

