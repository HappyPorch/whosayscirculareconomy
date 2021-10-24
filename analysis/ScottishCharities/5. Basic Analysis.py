import os, sys, json, csv
from validator_collection import checkers
from urllib.parse import urlparse
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import lib.data_files as data

sourceDir = "ScottishCharities"
sourceFile = os.path.join(sourceDir, "4. collated_search_results_coords.json")
outputFile = os.path.join(sourceDir, "5. Results_Found.json")


# read file
with open(data.get_temp(sourceFile), 'r') as myfile:
    sourceData=myfile.read()

# parse file
sourceJson = json.loads(sourceData)


for result in sourceJson:
    on_home_page = False
    about_section_count = 0
    pdf_count = 0
    count_top_level_pages = 0
    for o in result["organic_results"]:

        #is on home page?
        link_root = o["link"].replace("http://","").replace("https://","").strip("/")
        if checkers.is_domain(link_root):
            on_home_page = True
            #print("...is on home page: {}".format(o["link"]))

        #count top level pages
        u = urlparse(o["link"])
        path = u.path.strip("/")
        if path.count("/") == 0:
            count_top_level_pages += 1

        #count about section
        if path.startswith("about"):
            #print("...is in about section: {} - domain = {}".format(path, link_root))
            about_section_count += 1
        
        #count pdfs
        ext = os.path.splitext(path)[1]
        if ext == ".pdf":
            pdf_count += 1

    count_results = len(result["organic_results"])

    summary = {
        "search_term_found": 1,
        "searched_domain": result["domain"],
        "results_count": count_results,
        "found_on_home_page": on_home_page,
        "top_level_page_count": count_top_level_pages,
        "about_section_page_count": about_section_count,
        "PDF_file_count": pdf_count
    }
    result["summary"] = summary


# output json
data.save_temp_json(sourceJson, outputFile)