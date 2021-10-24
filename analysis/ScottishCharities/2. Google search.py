
import sys, os, csv
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import lib.data_files as data
import project_secrets, lib.serpAPI as serpAPI

searchTerm = "circular economy"

sourceDir = "ScottishCharities"
sourceFile = data.get_temp(os.path.join(sourceDir, "1. cleanedData.csv"))


domains = []
maxDomains = -1 # -1 will seach all domains in source file

with open(sourceFile, mode='r') as csv_file:
    csv_reader = csv.DictReader(csv_file)
    line_count = 0
    for row in csv_reader:
        line_count += 1
        if maxDomains < 0 or line_count <= maxDomains:
            d = []
            d.append(row["Charity Number"])
            d.append(row["Website_domain"])
            domains.append(d)


count = 0
for d in domains:
    outputFile = data.get_temp(os.path.join(sourceDir,"search_results", d[1] + ".json"))
    serpAPI.search(searchTerm, d[0], d[1], outputFile, project_secrets.serapi_key)
    count += 1

print("Searches completed: {}".format(count))

