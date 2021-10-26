
from validator_collection import checkers

def getdomain(website):
    website = website.strip().strip("/")
    if ("/" in website and not website.startswith("http")):
        website = "http://" + website
    if (checkers.is_domain(website)):
        return website
    elif (checkers.is_url(website)):
        return website
    return 0


def filter_by_domain(domain):
    ignore = ["facebook.com", "bbc.co.uk", ".ac.uk", ".gov.uk", ".clacksweb.org.uk", "sites.google.com"] #".ed.ac.uk", ".abdn.ac.uk", ".napier.ac.uk", ".napierstudents.com", ".gsa.ac.uk", ".gcu.ac.uk", ".gla.ac.uk", ".strath.ac.uk", ".cityofglasgowcollege.ac.uk"]
    for i in ignore:
        if i in domain:
            return 0
    return 1
