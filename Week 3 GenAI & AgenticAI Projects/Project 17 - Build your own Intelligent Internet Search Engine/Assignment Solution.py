import asyncio
import json
import zipfile
import os
from crawl4ai import AsyncWebCrawler, CrawlerRunConfig
from crawl4ai.deep_crawling import BFSDeepCrawlStrategy
from crawl4ai.content_scraping_strategy import LXMLWebScrapingStrategy

async def main():
    # Configure crawl with depth=2 and page limit
    config = CrawlerRunConfig(
        deep_crawl_strategy=BFSDeepCrawlStrategy(
            max_depth=2,
            include_external=False,
            max_pages=20   # ✅ Stop after 20 pages
        ),
        scraping_strategy=LXMLWebScrapingStrategy(),
        verbose=True
    )

    async with AsyncWebCrawler() as crawler:
        results = await crawler.arun("https://www.wikipedia.org", config=config)

        print(f"Crawled {len(results)} pages in total")

        # Collect data
        data = []
        for result in results:
            data.append({
                "url": result.url,
                "depth": result.metadata.get("depth", 0),
                "content": result.markdown[:500]  # truncate to first 500 chars
            })

        # Save JSON in the current folder
        json_filename = "crawl_results.json"
        with open(json_filename, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

        # Always save the zip to Desktop
        desktop = os.path.join(os.path.expanduser("~"), "Desktop")
        zip_path = os.path.join(desktop, "crawl_results.zip")

        with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zipf:
            zipf.write(json_filename)

        print(f"✅ Results saved to {zip_path}")

if __name__ == "__main__":
    asyncio.run(main())