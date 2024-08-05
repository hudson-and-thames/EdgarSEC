from edgarsec import EdgarClient
import json


async def main():
    client = EdgarClient()
    filings = await client.get_company_filings('0000320193')  # Example CIK
    print(json.dumps(filings, indent=4))  # Handle the response as needed
    await client.close()


# Run the example
if __name__ == "__main__":
    import asyncio

    asyncio.run(main())
