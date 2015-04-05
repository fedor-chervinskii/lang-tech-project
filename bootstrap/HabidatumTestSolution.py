import numpy as np
import pandas as pd
from pandas import DataFrame, read_csv

def check_intersection(left1, right1, left2, right2, testSameLength):
    return right1>= left2 and right2 >= left1 and (testSameLength or right1-left1 != right2-left2)

def testSegments(filename, testSameLength = False):
    data = pd.read_csv(filename)

    #Get groups of lines by slope
    #First set the horizontal slopes, that could give us division by 0
    data.loc[data.start_lat == data.end_lat,"slope"] = 0

    #Now set all the normal slopes
    otherData = data.loc[data.slope!=0]
    data.loc[data.slope!=0,"slope"] = (otherData.start_lon - otherData.end_lon)/(otherData.start_lat - otherData.end_lat)
    data["slope"] = np.round(data["slope"], decimals=5)

    #Get the angle and transform all the coordinates, so we would work in 1D
    data["angle"] = np.round(np.arctan(data["slope"]),decimals=5)

    data["start_lat_rot"] =  data["start_lat"] * np.cos(-data["angle"]) - data["start_lon"] * np.sin(-data["angle"]);
    data["start_lon_rot"] = data["start_lon"] * np.cos(-data["angle"]) + data["start_lat"] * np.sin(-data["angle"]);

    data["end_lat_rot"] =  data["end_lat"] * np.cos(-data["angle"]) - data["end_lon"] * np.sin(-data["angle"]);

    #We will need to sort the data so we could go from left to right and find overlapping lines
    data["left_lat"] = data[["end_lat_rot","start_lat_rot"]].min(axis=1)
    data["right_lat"] = data[["end_lat_rot","start_lat_rot"]].max(axis=1)

    #Group by slope and proceed with ones that have at least a pair of the same slopes
    bySlope = data.groupby("angle")
    filteredData = bySlope.filter(lambda x: len(x) > 1)
    filteredGroup = filteredData.groupby("angle")

    routesThatIntersect = []

    #Now for each slope we will be looking for overlaping
    for slope, group in filteredGroup:
        #Group by same longtitude and proceed with ones that have at least a pair, so they can be on the same line
        sameLongtitude = group.groupby("start_lon_rot")
        multiplePathsOnLine = sameLongtitude.filter(lambda x: len(x) > 1)
        sameLongtitude = multiplePathsOnLine.groupby("start_lon_rot")
        #Now for each route check if it interesect any other route in it's group
        for start_lon_rot, longtitudeGroup in sameLongtitude:
            sortedPaths = longtitudeGroup.sort("left_lat", ascending=1)
            for index, currentRow in sortedPaths.iterrows():

                if index in routesThatIntersect:
                    continue
                interescts = 0

                for indexToCheck, otherRow in sortedPaths[sortedPaths.index!=index].iterrows():
                    if check_intersection(currentRow.left_lat, currentRow.right_lat, otherRow.left_lat, otherRow.right_lat, testSameLength):
                        #If so — add it to the list, as well the one that it intersects
                        interescts = 1
                        routesThatIntersect.append(indexToCheck)
                if interescts:
                    routesThatIntersect.append(index)

    print len(routesThatIntersect)
    data.loc[routesThatIntersect].to_csv("overlappingSegments.csv")

testSegments('segments_1000.csv', False)
