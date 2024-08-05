import asyncio
import pandas as pd
import yfinance as yf
from yahooquery import search

companies = [
    "Apple Inc.",
    "Microsoft Corporation",
    "Amazon.com Inc.",
    "Alphabet Inc.",
    "Facebook, Inc.",
    "Tesla, Inc.",
    "Walmart Inc.",
    "JPMorgan Chase & Co.",
    "Johnson & Johnson",
    "Visa Inc.",
    "Procter & Gamble Co.",
    "UnitedHealth Group Inc.",
    "Home Depot Inc.",
    "Mastercard Inc.",
    "Bank of America Corp.",
    "Netflix Inc.",
    "Coca-Cola Company",
    "Pfizer Inc.",
    "Intel Corporation",
    "Verizon Communications Inc.",
    "AT&T Inc.",
    "Adobe Inc.",
    "Cisco Systems Inc.",
    "PepsiCo Inc.",
    "Nike Inc.",
    "Chevron Corporation",
    "Exxon Mobil Corporation",
    "McDonald's Corporation",
    "Boeing Company",
    "General Electric Company",
    "IBM Corporation",
    "Citigroup Inc.",
    "Wells Fargo & Company",
    "Goldman Sachs Group Inc.",
    "Salesforce.com Inc.",
    "Merck & Co. Inc.",
    "Walt Disney Company",
    "Costco Wholesale Corporation",
    "Oracle Corporation",
    "American Express Company",
    "Caterpillar Inc.",
    "Amgen Inc.",
    "3M Company",
    "Starbucks Corporation",
    "Honeywell International Inc.",
    "Lockheed Martin Corporation",
    "Target Corporation",
    "General Motors Company",
    "Ford Motor Company",
    "FedEx Corporation",
    "United Parcel Service Inc.",
    "Uber Technologies Inc.",
    "Airbnb, Inc.",
    "Advanced Micro Devices Inc.",
    "NVIDIA Corporation",
    "PayPal Holdings Inc.",
    "Booking Holdings Inc.",
    "Lowe's Companies Inc.",
    "Qualcomm Inc.",
    "Comcast Corporation",
    "Deere & Company",
    "Eli Lilly and Company",
    "Bristol-Myers Squibb Company",
    "BlackRock Inc.",
    "Thermo Fisher Scientific Inc.",
    "Gilead Sciences Inc.",
    "Broadcom Inc.",
    "Texas Instruments Inc.",
    "Medtronic plc",
    "Accenture plc",
    "Danaher Corporation",
    "Raytheon Technologies Corporation",
    "American Tower Corporation",
    "Union Pacific Corporation",
    "Shopify Inc.",
    "Zoom Video Communications Inc.",
    "CVS Health Corporation",
    "Anthem Inc.",
    "Micron Technology Inc.",
    "Philip Morris International Inc.",
    "Morgan Stanley",
    "Colgate-Palmolive Company",
    "DuPont de Nemours Inc.",
    "Altria Group Inc.",
    "ConocoPhillips",
    "Kimberly-Clark Corporation",
    "Intuit Inc.",
    "Activision Blizzard Inc.",
    "General Mills Inc.",
    "Mondelez International Inc.",
    "Intuitive Surgical Inc.",
    "Kraft Heinz Company",
    "Delta Air Lines Inc.",
    "Southwest Airlines Co.",
    "Marriott International Inc.",
    "Hilton Worldwide Holdings Inc.",
    "Stryker Corporation",
    "Biogen Inc.",
    "Illumina Inc.",
    "Vertex Pharmaceuticals Inc."
]

from edgarsec import EdgarClient
import json


async def main():
    client = EdgarClient()
    filings = await client.company_tickers()  # Example CIK
    #print(json.dumps(filings, indent=4))  # Handle the response as needed
    await client.close()
    return filings


def get_ticker(company_name):
    search_results = search(company_name)
    if search_results['quotes']:
        # Return the first match's ticker symbol
        return search_results['quotes'][0]['symbol']
    else:
        return None


# Run the example
if __name__ == "__main__":
    fillings = asyncio.run(main())
    dataframe = pd.DataFrame.from_dict(fillings, orient='index')

    for company_name in companies[:1]:
        ticker = get_ticker(company_name)
        print(f"company name: {company_name} --- ticker name {ticker}")
        if ticker:
            cik = dataframe[dataframe['ticker'] == ticker]['cik_str'].values[0]
            print(cik)

        dataframe_file = pd.read_csv("../2024q2/sub.txt", sep='\t')

        rows = dataframe_file[dataframe_file['cik'] == int(cik)]

        second_file = pd.read_csv("../2024q2/num.txt", sep='\t')

        for adsh in rows['adsh'].values:
            rows2 = second_file[second_file['adsh'] == adsh]
        print(rows['adsh'].values)
