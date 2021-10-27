import os, sys, json, csv
from datetime import date
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import lib.data_files as data

today = date.today()

sourceDir = "CRNS"
originalSourceFile = data.get_source(os.path.join(sourceDir, "CRNS_Map_data_26Oct2021.json"))

sourceFile = os.path.join(sourceDir, "5. Results_Found.json")
allSearchedSourceFile = os.path.join(sourceDir, "1. cleanedData.json")
outputFile = os.path.join(sourceDir, "6. CE_Search_CRNS_{}.json".format(today.strftime("%Y%m%d")))



# read file
with open(data.get_temp(sourceFile), 'r') as myfile:
    sourceData=myfile.read()

results = json.loads(sourceData)


# read file
with open(data.get_temp(allSearchedSourceFile), 'r') as myfile:
    allSearchedSourceData=myfile.read()
allSearchedSource = json.loads(allSearchedSourceData)


allIds = set(x["id"] for x in allSearchedSource)
searchFoundIds = set(x["org"]["id"] for x in results)
searchNotFoundIds = allIds.difference(searchFoundIds)
unmatched = list(x for x in allSearchedSource if x["id"] in searchNotFoundIds)
for c in unmatched:
    result = {
        "org": c,
        "summary": {
            "search_term_found": 0
        }
    }
    results.append(result)


with open(originalSourceFile, 'r') as myfile:
    originalSourceFileData=myfile.read()
originalSourceJson = json.loads(originalSourceFileData)

output = {
    "meta": {
    "search_date" : today.strftime("%d %b, %Y"),
    "source_count": len(originalSourceJson)
    },
    "data": results
}

data.save_temp_json(output, outputFile)