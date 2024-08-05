from edgarsec import EdgarClient
import json
import yfinance as yf


async def main():
    client = EdgarClient()
    filings = await client.company_tickers()  # Example CIK
    print(json.dumps(filings, indent=4))  # Handle the response as needed
    await client.close()


# Run the example
if __name__ == "__main__":
    import asyncio

    asyncio.run(main())