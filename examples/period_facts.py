from edgarsec import EdgarClient
import json

if __name__ == "__main__":
    api = EdgarClient()  # initialize the EdgarClient
    companies_frame = api.get_frames(period='CY2024Q2I')
    print(json.dumps(companies_frame, indent=4))
