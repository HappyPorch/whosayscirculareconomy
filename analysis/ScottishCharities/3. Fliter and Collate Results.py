import os, sys, json, csv
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import lib.data_files as data

sourceDir = "ScottishCharities"
charityData_file = os.path.join(sourceDir, "cleanedData.csv")
search_results_folder = data.get_temp(os.path.join(sourceDir, "search_results"))
outputFile = os.path.join(sourceDir, "collated_search_results.json")
results_notfound_outputFile = os.path.join(sourceDir, "collated_results_notfound.csv")
results_noexactmatch_outputFile = os.path.join(sourceDir, "collated_results_noexactmatch.csv")

domain_count = 0
results_count = 0

results_found = []
results_notfound = []
results_noexactmatch = []

#get the charity data so we can match it with search results
with open(data.get_temp(charityData_file)) as csv_file:
    rdr = csv.DictReader(csv_file, delimiter=',')
    charitiesList = [x for x in rdr]

#loop through search results, filter only those where seacrh term was found as exact match and collate with charity data
for filename in os.listdir(search_results_folder):
    if filename.endswith(".json"): 
        domain_count += 1

        domain = filename[: -len(".json")]

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
            if "missing" not in o and "circular economy" in o["snippet"].lower():
                exactmatch_organic_results.append(o)
        
        if len(exactmatch_organic_results) == 0:
                results_noexactmatch.append( { "domain": domain} )
        else:
            #find charity data
            matched_charity = {}
            matched_charities = list(x for x in charitiesList if x["Charity Number"] in search_result["identifier"])
            if (len(matched_charities) == 1):
                matched_charity = matched_charities[0]
            else:
                raise Exception("Duplicate charity numbers found")

            #build result
            result = {
            "domain": domain,
            "charity": {
                "number": matched_charity.get("Charity Number",""),
                "name": matched_charity.get("Charity Name",""),
                "registered_date": matched_charity.get("Registered Date",""),
                "known_as": matched_charity.get("Known As",""),
                "postcode": matched_charity.get("Postcode",""),
                "main_location": matched_charity.get("Main Operating Location",""),
                "status": matched_charity.get("Charity Status",""),
                "constitutional_form": matched_charity.get("Constitutional Form",""),
                "geographical_spread": matched_charity.get("Geographical Spread",""),
                "main_operating_location": matched_charity.get("Main Operating Location",""),
                "purposes": matched_charity.get("Purposes","").strip("'").split("','"),
                "beneficiaries": matched_charity.get("Beneficiaries",""),
                "activities": matched_charity.get("Activities",""),
                "objectives": matched_charity.get("Objectives",""),
                },
            "organic_results": exactmatch_organic_results
            }
            results_found.append(result)


data.save_temp_json(results_found, outputFile)
data.save_temp_csv(results_notfound, results_notfound_outputFile)
data.save_temp_csv(results_noexactmatch, results_noexactmatch_outputFile)


print("Results collated: Domains: {} Orgainic Results total: {}".format(domain_count, results_count))