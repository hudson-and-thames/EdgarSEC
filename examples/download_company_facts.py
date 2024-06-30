from edgarsec import EdgarClient

if __name__ == "__main__":
    client = EdgarClient()  # initialize the EdgarClient
    client.download_company_facts(file_path='../data/companyfacts.zip')
