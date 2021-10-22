
import sys, os, csv
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import lib.data_files as data
import project_secrets, lib.serpAPI as serpAPI

searchTerm = "circular economy"

sourceDir = "ScottishCharities"
sourceFile = data.get_temp(os.path.join(sourceDir, "cleanedData.csv"))


domains = []
maxDomains = 100 # -1 will seach all domains in source file

with open(sourceFile, mode='r') as csv_file:
    csv_reader = csv.DictReader(csv_file)
    line_count = 0
    for row in csv_reader:
        line_count += 1
        if maxDomains > 0 and line_count <= maxDomains:
            domains.append(row["Website_domain"])


count = 0
for d in domains:
    outputFile = data.get_temp(os.path.join(sourceDir,"search_results", d + ".json"))
    serpAPI.search(searchTerm, d, outputFile, project_secrets.serapi_key)
    count += 1

print("Searches completed: {}".format(count))

