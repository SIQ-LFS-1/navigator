import os
import csv
import sys
import json

resultDirectory = sys.argv[1]
filePath = os.path.normpath(f"{resultDirectory}/hashCheck.json")
csvSavePath = os.path.normpath(f"{resultDirectory}/urlInfo.csv")

# Opening JSON file and loading the data
# into the variable data
with open(filePath) as json_file:
    data = json.load(json_file)

resultData = data

# CSV File to Store URL Information...
data_file = open(f"{csvSavePath}", 'w', newline='')

# create the csv writer object
csv_writer = csv.writer(data_file)

# Counter variable used for writing
# headers to the CSV file
count = 0

for result in resultData:
    if count == 0:
        # Writing headers of CSV file
        header = result.keys()
        csv_writer.writerow(header)
        count += 1

    # Writing data of CSV file
    csv_writer.writerow(result.values())

data_file.close()
