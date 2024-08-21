from edgarsec import EdgarClient
import json


async def main():
    client = EdgarClient()
    await client.connect()
    filings = await client.get_frames(period='CY2023Q2I', taxonomy='us-gaap', tag='AccountsPayableCurrent', currency='USD')
    print(json.dumps(filings, indent=4))
    await client.close()


# Run the example
if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
