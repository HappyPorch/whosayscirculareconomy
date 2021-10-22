import sys, os
import csv
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import lib.data_files as data
import helpers
import tldextract

sourceDir = "ScottishCharities"
sourceFile = data.get_source(os.path.join(sourceDir, "CharityExport-05-Jul-2021.csv"))


invalidLines_tempfile = os.path.join(sourceDir, "invalidLines.csv")
filteredOut_tempfile = os.path.join(sourceDir, "filteredOut.csv")
filteredIn_tempfile = os.path.join(sourceDir, "filteredIn.csv")
outputData_tempfile = os.path.join(sourceDir, "cleanedData.csv")


# open source csv and filter
count = 0
filteredIn = []
invalidLines = []
filteredOut = []
outputData = []
outputDataFields = ["Charity Number","Website_domain","Charity Name","Registered Date","Known As","Charity Status","Postcode","Constitutional Form","Geographical Spread","Main Operating Location","Purposes","Beneficiaries","Activities","Objectives","Website","Most recent year income","Regulatory Type"]
with open(sourceFile, mode='r') as csv_file:
    csv_reader = csv.DictReader(csv_file)
    line_count = 0
    for row in csv_reader:
        if line_count == 0:
            count = 0
        elif helpers.filter_by_location(row["Main Operating Location"]) and helpers.filter_by_purposes(row["Purposes"]) and helpers.filter_by_activities(row["Activities"]) and helpers.filter_by_income(row["Most recent year income"]) and helpers.filter_by_name(row["Charity Name"]):
            domain =helpers.getdomain(row["Website"])
            if domain and helpers.filter_by_domain(domain): 
                website = row["Website"]
                sub,dom,suf = tldextract.extract(website)
                if (not suf):
                    row["_invalid_reason"] = "Invalid website domain"
                    invalidLines.append(row)
                else:
                    domain = sub + "." + dom + '.' + suf
                    if (sub == "www" or not sub):
                        domain = dom + '.' + suf
                    row["Website_domain"] = domain
                    filteredIn.append(row)
                    outputRow = {}
                    for outputField in outputDataFields:
                        outputRow[outputField] = row[outputField]
                    outputData.append(outputRow)
            else:
                row["_invalid_reason"] = "Invalid or no website"
                invalidLines.append(row)
            count += 1
        else:
            filteredOut.append(row)
        line_count += 1
    print(f'Processed {line_count} lines.')


data.save_temp_csv(invalidLines, invalidLines_tempfile)
data.save_temp_csv(filteredOut, filteredOut_tempfile)
data.save_temp_csv(filteredIn, filteredIn_tempfile)
data.save_temp_csv(outputData, outputData_tempfile)

print("Original = {}, filteredIn = {}, Invalid = {}, filteredOut = {}".format(line_count, len(filteredIn), len(invalidLines), len(filteredOut)))


