from edgarsec import EdgarClient

if __name__ == "__main__":
    client = EdgarClient()  # initialize the EdgarClient
    client.download_filing_history(file_path='../data/submissions.zip')