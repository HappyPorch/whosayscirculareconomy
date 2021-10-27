import os, sys, json, csv
from datetime import date
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import lib.data_files as data
import lib.postcode as postcode

today = date.today()

sourceDir = "CRNS"
sourceFile = os.path.join(sourceDir, "6. CE_Search_CRNS_{}.json".format(today.strftime("%Y%m%d")))
outputFile = os.path.join(sourceDir, "6. CE_Search_CRNS_{}.json".format(today.strftime("%Y%m%d")))


# read file
with open(data.get_temp(sourceFile), 'r') as myfile:
    sourceData=myfile.read()

# parse file
sourceJson = json.loads(sourceData)

#add postcode info 
for s in sourceJson["data"]:
    location = s["org"]["location"]
    if "postal_code" in location and "postal_code_info" not in location:
        #lookup coord for postcode
        location["postal_code_info"] = postcode.lookup_coords(location["postal_code"])


# output json
data.save_temp_json(sourceJson, outputFile)