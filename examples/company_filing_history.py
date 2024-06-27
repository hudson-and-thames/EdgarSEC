from edgarsec import EdgarClient
import json

if __name__ == "__main__":
    api = EdgarClient()  # initialize the EdgarClient
    cik = '0000320193'  # Apple Inc.
    filings = api.get_company_filings(cik='0000320193')  # get the filings for Apple Inc.
    company_concept = api.get_company_concept(cik='0000320193')  # get the concept for Apple Inc.
    company_fact = api.get_company_facts(cik='0000320193')  # get the facts for Apple Inc.
    companyies_frames = api.get_frames(period='CY2024Q2I')
    print(json.dumps(companyies_frames, indent=4))# get the frames for Apple Inc.
    #print(json.dumps(company_fact, indent=4))
    #print(json.dumps(company_concept, indent=4))
    #print(json.dumps(filings, indent=4))
