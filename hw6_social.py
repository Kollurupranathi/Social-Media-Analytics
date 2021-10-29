"""
Social Media Analytics Project
Name: Kolluru Pranathi
Roll Number: 2021501024
"""

import hw6_social_tests as test

project = "Social" # don't edit this

### PART 1 ###

import pandas as pd
import nltk
nltk.download('vader_lexicon', quiet=True)
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import matplotlib.pyplot as plt; plt.rcdefaults()
import numpy as np
endChars = [ " ", "\n", "#", ".", ",", "?", "!", ":", ";", ")" ]

'''
makeDataFrame(filename)
#3 [Check6-1]
Parameters: str
Returns: dataframe
'''
def makeDataFrame(filename):
    data=pd.read_csv(filename)
    return data
    


'''
parseName(fromString)
#4 [Check6-1]
Parameters: str
Returns: str
'''
def parseName(fromString):
    nameStart = fromString.find(":")
    nameEnd=fromString.find("(")
    name = fromString[nameStart+2:nameEnd-1]
    return name


'''
parsePosition(fromString)
#4 [Check6-1]
Parameters: str
Returns: str
'''
def parsePosition(fromString):
    positionStart = fromString.find("(")
    positionEnd=fromString.find("from")
    position = fromString[positionStart+1:positionEnd-1]
    return position


'''
parseState(fromString)
#4 [Check6-1]
Parameters: str
Returns: str
'''
def parseState(fromString):
    stateStart = fromString.find("from")+len("from ")
    stateEnd=fromString.find(")")
    state = fromString[stateStart:stateEnd]
    return state


'''
findHashtags(message)
#5 [Check6-1]
Parameters: str
Returns: list of strs
'''
def findHashtags(message):

    hash = []
    trigger = 0
    result = '#'
    for letter in message:
        if letter == '#':
            if trigger == 1:
                hash.append(result)
                result = '#'
            trigger = 1
            continue
        elif (letter in endChars) and trigger == 1:
            hash.append(result)
            result = '#'
            trigger = 0
        elif trigger == 1:
            result += letter

    if trigger == 1:
        hash.append(result)
    return hash

'''
getRegionFromState(stateDf, state)
#6 [Check6-1]
Parameters: dataframe ; str
Returns: str
'''
def getRegionFromState(stateDf, state):
    row=stateDf.loc[stateDf['state'] == state, 'region']
    return row.values[0]


'''
addColumns(data, stateDf)
#7 [Check6-1]
Parameters: dataframe ; dataframe
Returns: None
'''
def addColumns(data, stateDf):
    names=[]
    positions=[]
    states=[]
    regions=[]
    hashtags=[]
    for index, row in data.iterrows():
      value=row['label']
      names.append(parseName(value))
      positions.append(parsePosition(value))
      states.append(parseState(value))
      regions.append(getRegionFromState(stateDf, parseState(value)))
      text=row['text']
      hashtags.append(findHashtags(text))
    data['name']=names
    data['position']=positions
    data['state']=states
    data['region']=regions
    data['hashtags']=hashtags
    return


### PART 2 ###

'''
findSentiment(classifier, message)
#1 [Check6-2]
Parameters: SentimentIntensityAnalyzer ; str
Returns: str
'''
def findSentiment(classifier, message):
    score = classifier.polarity_scores(message)['compound']
    if score< (-0.1):
        return 'negative'
    elif score>0.1:
        return 'positive'
    else:
        return 'neutral'


'''
addSentimentColumn(data)
#2 [Check6-2]
Parameters: dataframe
Returns: None
'''
def addSentimentColumn(data):
    classifier = SentimentIntensityAnalyzer()
    empty=[]
    for index, row in data.iterrows():
        empty.append(findSentiment(classifier, row['text']))
    data['sentiment']=empty
    return


'''
getDataCountByState(data, colName, dataToCount)
#3 [Check6-2]
Parameters: dataframe ; str ; str
Returns: dict mapping strs to ints
'''
def getDataCountByState(data, colName, dataToCount):
    temp={}
    for index, row in data.iterrows():
        if colName=="" and dataToCount=='':
            if row['state'] not in temp:
                temp[row['state']]=0
            temp[row['state']]+=1
        elif row[colName]==dataToCount:
            if row['state'] not in temp:
                temp[row['state']]=0
            temp[row['state']]+=1   
    return temp


'''
getDataForRegion(data, colName)
#4 [Check6-2]
Parameters: dataframe ; str
Returns: dict mapping strs to (dicts mapping strs to ints)
'''
def getDataForRegion(data, colName):
    Final = {}
    for index, row in data.iterrows():
        reg = row['region']
        val = row[colName]
        if reg not in Final:
            temp = {}
            temp[val] = 1
            Final[reg] = temp
        else:
            if val not in Final[reg]:
                Final[reg][val] = 1
            else:
                Final[reg][val]+= 1
    return Final


'''
getHashtagRates(data)
#5 [Check6-2]
Parameters: dataframe
Returns: dict mapping strs to ints
'''
def getHashtagRates(data):
    tempo={}
    for x in data['hashtags']:
        for j in x:
            if (j not in tempo) and len(j)!=0:
                tempo[j]=0
            tempo[j]+=1
    return tempo



'''
mostCommonHashtags(hashtags, count)
#6 [Check6-2]
Parameters: dict mapping strs to ints ; int
Returns: dict mapping strs to ints
'''
def mostCommonHashtags(hashtags, count):
    keys= list(hashtags.keys())
    values= list(hashtags.values())
    x=sorted(values)
    x.reverse()
    k={}
    for j in range(0,count):
        for p in range(len(values)):
            if x[j]==values[p] and len(k)!=count:
                k[keys[p]]=x[j]
    return k      
   
    

'''
getHashtagSentiment(data, hashtag)
#7 [Check6-2]
Parameters: dataframe ; str
Returns: float
'''
def getHashtagSentiment(data, hashtag):
    score=0
    hashno=0
    for index, row in data.iterrows():
        if hashtag in findHashtags(row['text']):
            hashno+=1
            x= row['sentiment']  
            if x=='positive':
              score+=1
            if x=='negative':
              score-=1
            if x=='neutral':
              score+=0  
    return (score/hashno)
 

### PART 3 ###

'''
graphStateCounts(stateCounts, title)
#2 [Hw6]
Parameters: dict mapping strs to ints ; str
Returns: None
'''
def graphStateCounts(stateCounts, title):
    import matplotlib.pyplot as plt
    x=list(stateCounts.keys())
    y=list(stateCounts.values())
    fig = plt.figure(figsize = (15, 5))
    plt.bar(x, y, color ='blue',width = 0.4)
    plt.xlabel("states")
    plt.ylabel("numbers")
    plt.title(title)
    plt.show()
    return


'''
graphTopNStates(stateCounts, stateFeatureCounts, n, title)
#3 [Hw6]
Parameters: dict mapping strs to ints ; dict mapping strs to ints ; int ; str
Returns: None
'''
def graphTopNStates(stateCounts, stateFeatureCounts, n, title):
    return


'''
graphRegionComparison(regionDicts, title)
#4 [Hw6]
Parameters: dict mapping strs to (dicts mapping strs to ints) ; str
Returns: None
'''
def graphRegionComparison(regionDicts, title):
    return


'''
graphHashtagSentimentByFrequency(data)
#4 [Hw6]
Parameters: dataframe
Returns: None
'''
def graphHashtagSentimentByFrequency(data):
    return


#### PART 3 PROVIDED CODE ####
"""
Expects 3 lists - one of x labels, one of data labels, and one of data values - and a title.
You can use it to graph any number of datasets side-by-side to compare and contrast.
"""
def sideBySideBarPlots(xLabels, labelList, valueLists, title):
    import matplotlib.pyplot as plt

    w = 0.8 / len(labelList)  # the width of the bars
    xPositions = []
    for dataset in range(len(labelList)):
        xValues = []
        for i in range(len(xLabels)):
            xValues.append(i - 0.4 + w * (dataset + 0.5))
        xPositions.append(xValues)

    for index in range(len(valueLists)):
        plt.bar(xPositions[index], valueLists[index], width=w, label=labelList[index])

    plt.xticks(ticks=list(range(len(xLabels))), labels=xLabels, rotation="vertical")
    plt.legend()
    plt.title(title)

    plt.show()

"""
Expects two lists of probabilities and a list of labels (words) all the same length
and plots the probabilities of x and y, labels each point, and puts a title on top.
Expects that the y axis will be from -1 to 1. If you want a different y axis, change plt.ylim
"""
def scatterPlot(xValues, yValues, labels, title):
    import matplotlib.pyplot as plt
    fig, ax = plt.subplots()

    plt.scatter(xValues, yValues)

    # make labels for the points
    for i in range(len(labels)):
        plt.annotate(labels[i], # this is the text
                    (xValues[i], yValues[i]), # this is the point to label
                    textcoords="offset points", # how to position the text
                    xytext=(0, 10), # distance from text to points (x,y)
                    ha='center') # horizontal alignment can be left, right or center

    plt.title(title)
    plt.ylim(-1, 1)

    # a bit of advanced code to draw a line on y=0
    ax.plot([0, 1], [0.5, 0.5], color='black', transform=ax.transAxes)

    plt.show()


### RUN CODE ###

# This code runs the test cases to check your work
if __name__ == "__main__":
    # print("\n" + "#"*15 + " WEEK 1 TESTS " +  "#" * 16 + "\n")
    # test.week1Tests()
    # print("\n" + "#"*15 + " WEEK 1 OUTPUT " + "#" * 15 + "\n")
    # test.runWeek1()
    
    # df = makeDataFrame("data/politicaldata.csv")
    # stateDf = makeDataFrame("data/statemappings.csv")
    # addColumns(df, stateDf)
    # addSentimentColumn(df)
    # # test.testGetDataForRegion(df)
    # # test.testMostCommonHashtags(df)
    # test.testGetHashtagSentiment(df)
    # Uncomment these for Week 2 ##
    # print("\n" + "#"*15 + " WEEK 2 TESTS " +  "#" * 16 + "\n")
    # test.week2Tests()
    # print("\n" + "#"*15 + " WEEK 2 OUTPUT " + "#" * 15 + "\n")
    # test.runWeek2()

    ## Uncomment these for Week 3 ##
    print("\n" + "#"*15 + " WEEK 3 OUTPUT " + "#" * 15 + "\n")
    test.runWeek3()
