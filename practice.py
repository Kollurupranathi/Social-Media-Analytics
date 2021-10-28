import pandas as pd
def getDataCountByState(data=pd.read_csv("data/politicaldata.csv"), colName="sentiment", dataToCount="negative"):
    temp={}
    for index, row in data.iterrows():
        if colName=="" and dataToCount=='':
            if row['state'] not in temp:
                temp[row['state']]=0
            temp[row['state']]+=1
        if colName!="" and dataToCount!='':
            if row[colName]==dataToCount:
                if row['state'] not in temp:
                    temp[row['state']]=0
            temp[row['state']]+=1   
    print(temp)