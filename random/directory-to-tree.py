import os
import csv

fp = os.path.expanduser("source/")

data = []
for path, direcs, files in os.walk(fp):
    for f in files:
        data.append((path, f))
dest = os.path.expanduser("destination.csv")
with open(dest, 'w') as f:
    writer = csv.writer(f)
    for d in data:
        writer.writerow(d)


