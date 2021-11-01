import pandas as pd
dt=pd.read_csv("data/politicaldata.csv")
temp={}
coulumnData = dt['message']
unique = {}
# print(dt['message'])
for index in coulumnData:
    if index in unique.keys():
        unique[index] += 1
    else:
        unique[index] = 1
print(unique)
    #   temp[row['message']]=0
# print(temp)
#     if row["message"] not in temp:
#        temp[row["message"]]=0
#     temp[row["message"]]+=1
# print(temp)      