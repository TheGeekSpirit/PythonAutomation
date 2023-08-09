import csv
import sys
import os

directory = "G:\My Drive\Parent Folder\Project Folder"

# open output file to put all of the serials in
with open("allSerials.csv", mode="w", newline="") as csv_file:
    csv_writer = csv.writer(csv_file)

# loop through each file in directory
    for file in os.listdir(directory):
        filePath = os.path.join(directory, file)
        fileData = csv.reader(open(filePath))

        # loop through each serial in file and write it to the combined file
        for serial in fileData:
            csv_writer.writerow(serial)