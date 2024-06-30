from edgarsec import EdgarClient
import json

if __name__ == "__main__":
    client = EdgarClient()  # initialize the EdgarClient
    cik = '0000320193'  # Apple Inc.
    filings = client.get_company_filings(cik='0000320193')  # get the filings for Apple Inc.
    print(json.dumps(filings, indent=4))
