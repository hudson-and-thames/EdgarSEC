from edgarsec import EdgarClient
import json

if __name__ == "__main__":
    client = EdgarClient()  # initialize the EdgarClient
    cik = '0000320193'  # Apple Inc.
    company_facts = client.get_company_facts(cik='0000320193')  # get the facts for Apple Inc.
    print(json.dumps(company_facts, indent=4))
