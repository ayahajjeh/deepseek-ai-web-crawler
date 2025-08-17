import asyncio
import random

from crawl4ai import AsyncWebCrawler
from dotenv import load_dotenv

from config import BASE_URL, CSS_SELECTOR, REQUIRED_KEYS
from utils.data_utils import (
    save_venues_to_csv,
)
from utils.scraper_utils import (
    fetch_and_process_page,
    get_browser_config,
    get_llm_strategy,
)

load_dotenv()


async def crawl_venues():
    """
    Main function to crawl venue data from the website.
    """
    # Clean up any existing output files to start fresh
    import os
    if os.path.exists("complete_venues.csv"):
        os.remove("complete_venues.csv")
        print("🧹 Cleaned up previous output file to start fresh")
    
    # Initialize configurations
    browser_config = get_browser_config()
    llm_strategy = get_llm_strategy()
    session_id = "venue_crawl_session"

    # Initialize state variables
    page_number = 1
    all_venues = []
    seen_names = set()
    max_pages = 50  # Safety limit to prevent infinite crawling
    consecutive_duplicate_pages = 0  # Track consecutive pages with only duplicates
    max_consecutive_duplicates = 5  # Stop after 5 consecutive duplicate pages

    # Start the web crawler context
    # https://docs.crawl4ai.com/api/async-webcrawler/#asyncwebcrawler
    async with AsyncWebCrawler(config=browser_config) as crawler:
        # Add initial delay before first page to reset Groq rate limit
        initial_delay = random.uniform(60, 90)  # Same delay as between pages for Groq rate limit
        print(f"⏳ Initial delay: {initial_delay:.1f} seconds before starting to reset Groq rate limit...")
        await asyncio.sleep(initial_delay)
        
        while page_number <= max_pages:
            # Fetch and process data from the current page
            venues, no_results_found = await fetch_and_process_page(
                crawler,
                page_number,
                BASE_URL,
                CSS_SELECTOR,
                llm_strategy,
                session_id,
                REQUIRED_KEYS,
                seen_names,
            )

            if no_results_found:
                print("No more venues found. Ending crawl.")
                break  # Stop crawling when "No Results Found" message appears

            if not venues:
                print(f"No venues extracted from page {page_number}.")
                break  # Stop if no venues are extracted
            
            # Check for duplicate venues to detect when we're repeating
            # Skip duplicate checking on page 1 since seen_names starts empty
            if page_number > 1:
                new_venues = []
                duplicate_count = 0
                
                for venue in venues:
                    if venue["name"] not in seen_names:
                        new_venues.append(venue)
                    else:
                        duplicate_count += 1
                        print(f"Duplicate venue '{venue['name']}' found on page {page_number}")
                
                # Check if this page is all duplicates
                if duplicate_count == len(venues):
                    consecutive_duplicate_pages += 1
                    print(f"Page {page_number} only contains duplicate venues. Consecutive duplicate pages: {consecutive_duplicate_pages}")
                    
                    # Stop after max consecutive duplicate pages
                    if consecutive_duplicate_pages >= max_consecutive_duplicates:
                        print(f"Stopping crawl after {max_consecutive_duplicates} consecutive duplicate pages.")
                        break
                else:
                    # Reset counter if we found new venues
                    consecutive_duplicate_pages = 0
                    print(f"Page {page_number} has {len(venues) - duplicate_count} new venues. Resetting duplicate counter.")
                
                # Use only the new, non-duplicate venues
                venues = new_venues
            # Page 1: process all venues without duplicate checking

            # Add the venues from this page to the total list
            all_venues.extend(venues)
            
            # Add venue names to seen_names AFTER processing them
            for venue in venues:
                seen_names.add(venue["name"])
            
            page_number += 1  # Move to the next page
            
            # Check if we've reached the maximum page limit
            if page_number > max_pages:
                print(f"Reached maximum page limit ({max_pages}). Ending crawl.")
                break

            # Pause between requests to be polite and avoid rate limits
            # Groq has 6000 tokens per minute limit, so wait longer to reset
            delay = random.uniform(60, 90)  # Random delay between 60-90 seconds (1-1.5 minutes)
            print(f"Waiting {delay:.1f} seconds before next request to reset Groq rate limit...")
            await asyncio.sleep(delay)

    # Save the collected venues to a CSV file
    if all_venues:
        save_venues_to_csv(all_venues, "complete_venues.csv")
        print(f"Saved {len(all_venues)} venues to 'complete_venues.csv'.")
    else:
        print("No venues were found during the crawl.")

    # Display usage statistics for the LLM strategy
    llm_strategy.show_usage()


async def main():
    """
    Entry point of the script.
    """
    await crawl_venues()


if __name__ == "__main__":
    asyncio.run(main())
