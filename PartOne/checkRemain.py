import os
import re

finished = []
results = os.listdir("PartOne/part1Results")
for i in results:
    finished.append(i[0:9].strip())

largeFiles = []
largeFile = open("PartOne/largeFiles.txt", "r")
for i in largeFile.readlines():
    largeFiles.append(i[0:9].strip())

notfinished = []
dataset = open("PartOne/datasets.tsv", "r")
for i in dataset.readlines():
    name = i.split("\t")[0].strip()
    if name not in finished and name not in largeFiles:
        notfinished.append(name)

with open('PartOne/secondRunFiles.txt', 'w') as f:
    for item in notfinished:
        f.write("%s.tsv.gz\n" % item)
