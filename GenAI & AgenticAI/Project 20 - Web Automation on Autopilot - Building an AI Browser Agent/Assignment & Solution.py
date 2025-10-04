import asyncio
from browser_use import Agent

async def extract_search_results(agent):
    # Perform a Google search for 'what is browser automation' by navigating directly to Google
    search_url = 'https://www.google.com/search?q=what+is+browser+automation'
    
    # Navigate to Google Search page
    await agent.navigate(search_url)
    
    # Wait for the search results to load (you can adjust this delay)
    await asyncio.sleep(3)
    
    # Extract structured data (titles and URLs of the top 3 search results)
    results = await agent.extract_structured_data(
        query="Extract the URLs of the top 3 search results. For each result, extract the title and the URL."
    )
    
    # Process the results
    if results:
        print("Top 3 search results:")
        for index, result in enumerate(results, start=1):
            print(f"{index}. Title: {result['title']}, URL: {result['url']}")
    else:
        print("No results found.")
    
    return results

async def main():
    # Initialize the agent with a task
    task = "Search Google for 'what is browser automation' and extract top 3 results"
    agent = Agent(model="gemini-2.5-flash", task=task)
    
    # Extract search results
    search_results_urls = await extract_search_results(agent)

    # Optionally save results to a file
    if search_results_urls:
        with open('top_3_urls.txt', 'w') as f:
            for result in search_results_urls:
                f.write(f"Title: {result['title']}, URL: {result['url']}\n")
    
    print("Task completed.")

# Run the asyncio main function
if __name__ == "__main__":
    asyncio.run(main())