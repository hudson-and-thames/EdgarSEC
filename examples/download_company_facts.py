from edgarsec import EdgarClient


async def main():
    client = EdgarClient()
    await client.download_company_facts(file_path='../data/companyfacts.zip')
    await client.download_filing_history(file_path='../data/submissions.zip')
    await client.close()


# Run the example
if __name__ == "__main__":
    import asyncio

    asyncio.run(main())
