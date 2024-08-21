from edgarsec import EdgarClient
import json

client = EdgarClient()


async def main():
    await client.connect()
    filings = await client.get_company_concept(cik='0000320193', taxonomy='us-gaap', tag="AccountsPayableCurrent")  # Example CIK
    print(json.dumps(filings, indent=4))  # Handle the response as needed
    await client.close()


# Run the example
if __name__ == "__main__":
    import asyncio

    asyncio.run(main())
