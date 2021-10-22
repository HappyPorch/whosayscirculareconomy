from serpapi import GoogleSearch
import json, os, time

def search(searchTerm, domain, outputFile, serapi_key):
    print("..checking: {}".format(domain))
    site_limited_search_term = '"{}" site:{}'.format(searchTerm, domain)

    do_search = True

    if (os.path.exists(outputFile)):
        # read file
        with open(outputFile, 'r') as myfile:
            data=myfile.read()

        # parse file
        prev_search_result = json.loads(data)

        if "search_metadata" in prev_search_result and "status" in prev_search_result["search_metadata"]:
            print("...prev search: {}".format(prev_search_result["search_metadata"]["status"]))
            do_search = False

    if (do_search):
        print("...searching: {}".format(domain))
        params = {
        "engine": "google",
        "q": site_limited_search_term,
        "api_key": serapi_key,
        "location": "Edinburgh,Scotland,United Kingdom"
        }

        search = GoogleSearch(params)
        results = search.get_dict()

        with open(outputFile, "w", encoding='utf-8') as f:
            json.dump(results, f, indent=2)

        #max 1000 requests per hr
        time.sleep(5)


