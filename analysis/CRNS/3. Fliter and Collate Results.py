import os, sys, json, csv
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import lib.data_files as data

sourceDir = "CRNS"
sourceData_file = os.path.join(sourceDir, "1. cleanedData.json")
search_results_folder = data.get_temp(os.path.join(sourceDir, "search_results"))
outputFile = os.path.join(sourceDir, "3. collated_search_results.json")
results_notfound_outputFile = os.path.join(sourceDir, "3. collated_results_notfound.json")
results_noexactmatch_outputFile = os.path.join(sourceDir, "3. collated_results_noexactmatch.json")

domain_count = 0
results_count = 0

results_found = []
results_notfound = []
results_noexactmatch = []

#get the original data so we can match it with search results
with open(data.get_temp(sourceData_file), 'r') as myfile:
    sourceData=myfile.read()
sourceJson = json.loads(sourceData)

#loop through search results, filter only those where seacrh term was found as exact match and collate with charity data
for filename in os.listdir(search_results_folder):
    if filename.endswith(".json"): 
        domain_count += 1

        domain = filename[: -len(".json")]
        print("..checking: {}".format(domain))

         # read file
        with open(os.path.join(search_results_folder, filename), 'r') as myfile:
            search_result=myfile.read()

        search_result = json.loads(search_result)

        #filter those with no results
        if "error" in search_result and search_result["error"] == "Google hasn't returned any results for this query.":
            print("...no results for: {}".format(domain))
            results_notfound.append({ "domain": domain})
            continue

        results_count += len(search_result["organic_results"])

        #filter those with exact match results
        exactmatch_organic_results = []
        for o in search_result["organic_results"]:
            if "snippet" in o and "missing" not in o and "circular economy" in o["snippet"].lower():
                exactmatch_organic_results.append(o)
        
        if len(exactmatch_organic_results) == 0:
                results_noexactmatch.append( { "domain": domain} )
        else:
            #find source data
            matched = {}
            matched_sources = list(x for x in sourceJson if x["id"] in search_result["identifier"])
            if (len(matched_sources) == 1):
                matched = matched_sources[0]
            else:
                #same domain for multiple orgs, so lets just chosoe the first
                matched = matched_sources[0]
                
            #build result
            result = {
            "domain": domain,
            "org": matched,
            "organic_results": exactmatch_organic_results
            }
            results_found.append(result)


data.save_temp_json(results_found, outputFile)
data.save_temp_json(results_notfound, results_notfound_outputFile)
data.save_temp_json(results_noexactmatch, results_noexactmatch_outputFile)


print("Results collated: Domains: {} Orgainic Results total: {}".format(domain_count, results_count))