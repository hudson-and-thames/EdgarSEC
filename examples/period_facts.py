from edgarsec import EdgarClient
import json


async def main():
    client = EdgarClient()
    filings = await client.get_frames('CY2024Q2I')
    print(json.dumps(filings, indent=4))
    await client.close()


# Run the example
if __name__ == "__main__":
    import asyncio

    asyncio.run(main())
