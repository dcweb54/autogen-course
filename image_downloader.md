import asyncio
import json
import os
# from nodriver import Tab

from pydoll.browser import Chrome
from pydoll.constants import Key, By


async def save_to_json(data, query, filename=None):
    """Save data to JSON file"""
    try:
        # Create filename if not provided
        if filename is None:
            # Clean query for filename
            clean_query = "".join(c for c in query if c.isalnum() or c in (' ', '-', '_')).rstrip()
            clean_query = clean_query.replace(' ', '_')[:50]
          
            filename = f"amazon_{clean_query}.json"
        
        # Ensure the directory exists
        os.makedirs('scraped_data', exist_ok=True)
        filepath = os.path.join('scraped_data', filename)
        
        # Save data to JSON file
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump({
                'metadata': {
                    'query': query,
                    'total_products': len(data),
                    
                    'source': 'Amazon India'
                },
                'products': data
            }, f, indent=2, ensure_ascii=False)
        
        print(f"Data saved to {filepath}")
        return filepath
        
    except Exception as e:
        print(f"Error saving to JSON: {e}")
        return None


async def amazon_search(query: str, max_pages: int = 3):
    async with Chrome() as browser:
        tab = await browser.start()
        await tab.go_to('https://www.amazon.in/')
        await asyncio.sleep(3)
        
        # Search for the product
        search_box = await tab.query('//*[@id="twotabsearchtextbox"]')
        await search_box.type_text(query)
        await asyncio.sleep(2)
                
        submit_box = await tab.query('//*[@id="nav-search-submit-button"]')
        await submit_box.click()
        await asyncio.sleep(5)
    
        all_products = []
        
        for page in range(1, max_pages + 1):
            print(f"Scraping page {page}...")
            
            # Get product elements
            elements = await tab.query('div[data-component-type="s-search-result"]', find_all=True)
           
            
            for el in elements:
                try:
                    # Get ASIN
                    asin = el.get_attribute("data-asin")
                    if asin is None:
                        continue
                    
                    # Get title
                    title_elem = await el.find(tag_name='h2')
                    title = await title_elem.text if title_elem else "No title"
                    
                    # Get price - try multiple selectors
                    price = "Not available"
                    price_selectors = [
                        '.a-price-whole',
                        '.a-offscreen',
                        '.a-price > .a-offscreen'
                    ]
                    
                    for selector in price_selectors:
                        price_elem = await el.query(selector)
                        if price_elem:
                            price = await price_elem.text
                            break
                        
                    
                    image_url = "Not Available"
                    image_url_element = await el.query('div[data-cy="image-container"] > div > span > a > div > img')
                    if image_url_element:
                        image_url = image_url_element.get_attribute('src')
                    
                    all_products.append({
                        'asin': asin,
                        'title': title.strip(),
                        'price': price,
                        'page': page,
                        'image_url':image_url
                    })
                    
                    print(f"Page {page}: {title.strip()} - {price}")
                    
                except Exception as e:
                    print(f"Error processing product: {e}")
                    continue
            
            print(f"Finished page {page}. Found {len([p for p in all_products if p['page'] == page])} products.")
            
            # Try to go to next page if we haven't reached the max pages
            if page < max_pages:
                # next_page_found = await go_to_next_page(tab)
                # next_page = await tab.find(tag_name='a',text="Next")
                await asyncio.sleep(5)
               
                next_page = await tab.query('span[aria-label="pagination"] > ul > li:last-child')
                await next_page.click()
                await asyncio.sleep(5)
                
                if not next_page:
                    print("No more pages available.")
                    break
                await asyncio.sleep(5)  # Wait for the next page to load
        
        print(f"\nTotal products found: {len(all_products)}")
        
        await save_to_json(all_products,query)
        
        return all_products

# Run the search for multiple pages
asyncio.run(amazon_search('android', max_pages=10))