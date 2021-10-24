import os, sys, json, csv
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import lib.data_files as data
import lib.postcode as postcode

sourceDir = "ScottishCharities"
sourceFile = os.path.join(sourceDir, "3. collated_search_results.json")
outputFile = os.path.join(sourceDir, "4. collated_search_results_coords.json")


# read file
with open(data.get_temp(sourceFile), 'r') as myfile:
    sourceData=myfile.read()

# parse file
sourceJson = json.loads(sourceData)

#add postcode coords 
for s in sourceJson:
    charity = s["charity"]
    if "postcode" in charity and "postcode_coords" not in charity:
        #lookup coord for postcode
        charity["postcode_coords"] = postcode.lookup_coords(charity["postcode"])


# output json
data.save_temp_json(sourceJson, outputFile)