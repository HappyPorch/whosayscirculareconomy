import os, sys, json
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import lib.data_files as data

sourceDir = "ScottishCharities"
search_results_folder = data.get_temp(os.path.join(sourceDir, "search_results"))
outputFile = os.path.join(sourceDir, "collated_search_results.json")
results_notfound_outputFile = os.path.join(sourceDir, "collated_results_notfound.csv")
results_noexactmatch_outputFile = os.path.join(sourceDir, "collated_results_noexactmatch.csv")

domain_count = 0
results_count = 0

results_found = []
results_notfound = []
results_noexactmatch = []

for filename in os.listdir(search_results_folder):
    if filename.endswith(".json"): 
        domain_count += 1

        domain = filename[: -len(".json")]

         # read file
        with open(os.path.join(search_results_folder, filename), 'r') as myfile:
            search_result=myfile.read()

        # parse file
        search_result = json.loads(search_result)

        #filter those with no results
        if "error" in search_result and search_result["error"] == "Google hasn't returned any results for this query.":
            print("...no results for: {}".format(domain))
            results_notfound.append({ "domain": domain})
            continue

        results_count += len(search_result["organic_results"])

        exactmatch_organic_results = []
        for o in search_result["organic_results"]:
            if "missing" not in o and "circular economy" in o["snippet"].lower():
                exactmatch_organic_results.append(o)
        
        if len(exactmatch_organic_results) == 0:
                results_noexactmatch.append( { "domain": domain} )
        else:
            result = {
            "domain": domain,
            "identifier": search_result["identifier"],
            "organic_results": exactmatch_organic_results
            }
            results_found.append(result)


data.save_temp_json(results_found, outputFile)
data.save_temp_csv(results_notfound, results_notfound_outputFile)
data.save_temp_csv(results_noexactmatch, results_noexactmatch_outputFile)


print("Results collated: Domains: {} Orgainic Results total: {}".format(domain_count, results_count))