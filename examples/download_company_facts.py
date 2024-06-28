from edgarsec import EdgarClient
import json

if __name__ == "__main__":
    api = EdgarClient()  # initialize the EdgarClient
    cik = '0000320193'  # Apple Inc.
    api.download_company_facts(file_path='../data/companyfacts.zip')