import sys, os
import json
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import lib.data_files as data
import lib.helpers as lib_helpers
import tldextract
from datetime import datetime

sourceDir = "CRNS"
sourceFile = data.get_source(os.path.join(sourceDir, "CRNS_Map_data_26Oct2021.json"))


invalid_tempfile = os.path.join(sourceDir, "1. invalid.json")
duplicateDomains_tempfile = os.path.join(sourceDir, "1. duplicateDomains.json")
filteredOut_tempfile = os.path.join(sourceDir, "1. filteredOut.json")
filteredIn_tempfile = os.path.join(sourceDir, "1. filteredIn.json")
outputData_tempfile = os.path.join(sourceDir, "1. cleanedData.json")


# open source csv and filter
count = 0
filteredIn = []
invalid = []
filteredOut = []
duplicateDomains = []
duplicatesToRemove = []
outputData = []

with open(data.get_temp(sourceFile), 'r') as myfile:
    sourceData=myfile.read()
sourceJson = json.loads(sourceData)

for row in sourceJson:
    webUrl = row["location"]["extra_fields"]["website"]
    domain =lib_helpers.getdomain(webUrl)
    if domain and lib_helpers.filter_by_domain(domain): 
        website = webUrl
        sub,dom,suf = tldextract.extract(website)
        if (not suf):
            row["_invalid_reason"] = "Invalid website domain"
            invalid.append(row)
            continue

        domain = sub + "." + dom + '.' + suf
        if (sub == "www" or not sub):
            domain = dom + '.' + suf

        row["Website_domain"] = domain
        filteredIn.append(row)

        #todo: check for duplicate domains
        duplicates = list(x for x in outputData if x["Website_domain"] == domain and x["id"] not in duplicatesToRemove)
        if (len(duplicates) > 0):
            duplicatesToRemove.append(duplicates[0]["id"]) #there are no duplicates so we can ignore
        
        outputData.append(row)
    else:
        row["_invalid_reason"] = "Invalid or no website"
        invalid.append(row)
    count += 1
print(f'Processed {count} items.')


data.save_temp_json(invalid, invalid_tempfile)
data.save_temp_json(filteredOut, filteredOut_tempfile)
data.save_temp_json(filteredIn, filteredIn_tempfile)
data.save_temp_json(outputData, outputData_tempfile)
data.save_temp_json(duplicateDomains, duplicateDomains_tempfile)

print("Original = {}, filteredIn = {}, Invalid = {}, filteredOut = {}, duplicate = {}, finalOutput = {}".format(count, len(filteredIn), len(invalid), len(filteredOut), len(duplicateDomains), len(outputData)))


