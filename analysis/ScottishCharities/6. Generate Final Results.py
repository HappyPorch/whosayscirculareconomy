import os, sys, json, csv
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import lib.data_files as data

sourceDir = "ScottishCharities"
sourceFile = os.path.join(sourceDir, "Results_Found.json")
allSearchedSourceFile = os.path.join(sourceDir, "cleanedData.csv")
outputFile = os.path.join(sourceDir, "ScottishCharities_results.json")



# read file
with open(data.get_temp(sourceFile), 'r') as myfile:
    sourceData=myfile.read()

sourceJson = json.loads(sourceData)


# read file
with open(data.get_temp(allSearchedSourceFile), mode='r') as csv_file:
    csv_reader = csv.DictReader(csv_file)
    allSearchedSource = [x for x in csv_reader]


results = []
for result in sourceJson:
    row = {
        "charity_number": result["charity"]["number"],
        "charity_name": result["charity"]["name"],
        "charity_registered_date": result["charity"]["registered_date"],
        "charity_known_as": result["charity"]["known_as"],
        "charity_postcode": result["charity"]["postcode"],
        "charity_main_location": result["charity"]["main_location"],
        "charity_status": result["charity"]["status"],
        "charity_constitutional_form": result["charity"]["constitutional_form"],
        "charity_geographical_spread": result["charity"]["geographical_spread"],
        "charity_main_operating_location": result["charity"]["main_operating_location"],
        "charity_purposes": result["charity"]["purposes"],
        "charity_beneficiaries": result["charity"]["beneficiaries"],
        "charity_activities": result["charity"]["activities"],
        "charity_objectives": result["charity"]["objectives"],
        "search_term_found": 1,
        "searched_domain": result["domain"],
        "results_count": result["summary"]["results_count"],
        "found_on_home_page": result["summary"]["found_on_home_page"],
        "top_level_page_count": result["summary"]["top_level_page_count"],
        "about_section_page_count": result["summary"]["about_section_page_count"],
        "PDF_file_count": result["summary"]["PDF_file_count"],
    }
    results.append(row)

#todo: append charities with no search term found

#todo: change JS filter_bypurpose to use purposes array 

data.save_temp_json(results, outputFile)