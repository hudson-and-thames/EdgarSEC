from edgarsec import EdgarClient
import json

if __name__ == "__main__":
    client = EdgarClient()  # initialize the EdgarClient
    cik = '0000320193'  # Apple Inc.
    company_concept = client.get_company_concept(cik='0000320193')  # get the concept for Apple Inc.
    print(json.dumps(company_concept, indent=4))