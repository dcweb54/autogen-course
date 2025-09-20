import requests
from bs4 import BeautifulSoup
import xml.etree.ElementTree as ET
import urllib.parse
import re

# --- Configuration ---
# The base domain
BASE_URL = "https://checkpost.parivahan.gov.in"
# The context path for the application
CONTEXT_PATH = "/checkpost"
# The specific page path
TAX_COLLECTION_PATH = "/faces/public/payment/TaxCollection.xhtml"
# Full initial URL would be BASE_URL + CONTEXT_PATH + TAX_COLLECTION_PATH

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Safari/537.36",
    "Accept-Language": "en-US,en;q=0.9",
    "Accept-Encoding": "gzip, deflate, br",
    "Connection": "keep-alive",
    "Upgrade-Insecure-Requests": "1",
}

# --- Helper Functions ---
def extract_viewstate(html_content):
    """Extracts the javax.faces.ViewState value from HTML."""
    soup = BeautifulSoup(html_content, 'html.parser')
    viewstate_input = soup.find("input", {"name": "javax.faces.ViewState"})
    if viewstate_input and viewstate_input.get('value'):
        return viewstate_input['value']
    else:
        return None

# --- Main Script ---
session = requests.Session()
session.headers.update(HEADERS)

try:
    # --- 1. Initial GET Request to TaxCollection.xhtml ---
    print("1. Fetching initial page...")
    # Correctly construct the initial URL
    initial_url = BASE_URL + CONTEXT_PATH + TAX_COLLECTION_PATH
    print(f"   Requesting URL: {initial_url}") # Debug print
    response = session.get(initial_url)
    response.raise_for_status() # Raise an exception for bad status codes (4xx or 5xx)

    # --- 2. Extract Initial ViewState ---
    initial_viewstate = extract_viewstate(response.text)
    if not initial_viewstate:
        print("Error: Could not extract initial ViewState. Aborting.")
        exit(1)
    print(f"   Initial ViewState: {initial_viewstate}")

    # --- 3. POST Request: Select State (KA) ---
    print("2. Sending State Selection POST request...")
    state_post_url = initial_url # Same URL for the POST
    state_data = {
        "javax.faces.partial.ajax": "true",
        "javax.faces.source": "ib_state",
        "javax.faces.partial.execute": "ib_state",
        "javax.faces.partial.render": "operation_code",
        "javax.faces.behavior.event": "change",
        "javax.faces.partial.event": "change",
        "master_Layout_form": "master_Layout_form",
        "ib_state_input": "KA",
        "operation_code_input": "-1",
        "javax.faces.ViewState": initial_viewstate
    }
    state_headers = {
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        "Faces-Request": "partial/ajax",
        "X-Requested-With": "XMLHttpRequest",
        "Referer": initial_url,
        "Accept": "application/xml, text/xml, */*; q=0.01",
    }

    response = session.post(state_post_url, data=state_data, headers=state_headers)
    response.raise_for_status()
    print("   State selection POST successful.")

    # --- 4. POST Request: Select Operation Code (5003) and Payment Type ---
    print("3. Sending Operation Selection POST request...")
    op_post_url = initial_url # Same URL again
    op_data = {
        "javax.faces.partial.ajax": "true",
        "javax.faces.source": "j_idt48", # Source component
        "javax.faces.partial.execute": "@all",
        "j_idt48": "j_idt48",
        "PAYMENT_TYPE": "ONLINE",
        "master_Layout_form": "master_Layout_form",
        "ib_state_input": "KA",
        "operation_code_input": "5003",
        "javax.faces.ViewState": initial_viewstate # Crucial!
    }
    op_headers = {
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        "Faces-Request": "partial/ajax",
        "X-Requested-With": "XMLHttpRequest",
        "Referer": initial_url,
        "Accept": "application/xml, text/xml, */*; q=0.01",
    }

    response = session.post(op_post_url, data=op_data, headers=op_headers)
    response.raise_for_status()
    print("   Operation selection POST successful.")

    # --- 5. Handle Final XML Response ---
    final_xml_content = response.text
    print("\n--- Parsing Final XML Response ---")

    # Parse the XML
    root = ET.fromstring(final_xml_content)

    # Look for the <redirect> element
    redirect_elem = root.find('.//redirect')
    if redirect_elem is not None:
        redirect_url = redirect_elem.get('url')
        if redirect_url:
            print(f"   Found redirect URL: {redirect_url}")
            # Handle relative URL correctly
            # The redirect URL from the XML is relative to the domain root
            if redirect_url.startswith('/'):
                # Correctly form the absolute URL
                redirect_url = BASE_URL + redirect_url
            print("   Following redirect...")
            # Make a GET request to the redirect URL
            final_page_response = session.get(redirect_url)
            final_page_response.raise_for_status()
            final_page_content = final_page_response.text
            print("   Successfully loaded redirected page.")
            # Now final_page_content holds the HTML of the final page
            # Extract ViewState from this HTML if needed for further actions
            final_page_viewstate = extract_viewstate(final_page_content)
            if final_page_viewstate:
                print(f"   Final Page ViewState: {final_page_viewstate}")
            else:
                 print("   No ViewState found on final page.")

            print("\n--- Process Completed ---")
            print("The final page HTML is in the 'final_page_content' variable.")
            # Example: soup = BeautifulSoup(final_page_content, 'html.parser')
            # You can now work with final_page_content

        else:
            print("Redirect element found but no URL attribute.")
    else:
        print("   No <redirect> element found in XML response.")
        print("   Inspect the 'final_xml_content' variable for details.")
        # print("Final XML Content:", final_xml_content) # Debug


except requests.exceptions.RequestException as e:
    print(f"An error occurred during the requests: {e}")
except ET.ParseError as e:
    print(f"An error occurred parsing the XML response: {e}")
    print("Raw XML content that failed to parse:")
    print(response.text[:1000] if 'response' in locals() else "Response not available")
except Exception as e:
    print(f"An unexpected error occurred: {e}")
