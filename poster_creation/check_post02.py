import requests
from bs4 import BeautifulSoup
import xml.etree.ElementTree as ET
import urllib.parse
import os # To handle file paths

# --- Configuration ---
# The base URL including the context path '/checkpost'
BASE_URL_WITH_CONTEXT = "https://checkpost.parivahan.gov.in/checkpost"
# The specific initial page path
TAX_COLLECTION_PATH = "/faces/public/payment/TaxCollection.xhtml"
# The filename to save the final HTML
OUTPUT_FILENAME = "final_page_output.html"

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
        # print("Warning: ViewState not found in HTML.")
        return None

def save_html_to_file(html_content, filename):
    """Saves HTML content to a file."""
    try:
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(html_content)
        print(f"   Final HTML content saved to '{filename}'")
    except Exception as e:
        print(f"   Error saving HTML to file: {e}")

# --- Main Script ---
session = requests.Session()
session.headers.update(HEADERS)

try:
    # --- 1. Initial GET Request to TaxCollection.xhtml ---
    print("1. Fetching initial page...")
    # Construct the initial URL correctly based on the file content
    initial_url = BASE_URL_WITH_CONTEXT + TAX_COLLECTION_PATH
    print(f"   Requesting URL: {initial_url}")
    response = session.get(initial_url)
    response.raise_for_status()

    # --- 2. Extract Initial ViewState ---
    initial_viewstate = extract_viewstate(response.text)
    if not initial_viewstate:
        print("Error: Could not extract initial ViewState. Aborting.")
        exit(1)
    print(f"   Initial ViewState: {initial_viewstate}")

    # --- 3. POST Request: Select State (KA) ---
    print("2. Sending State Selection POST request...")
    state_post_url = initial_url
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
    op_post_url = initial_url
    op_data = {
        "javax.faces.partial.ajax": "true",
        "javax.faces.source": "j_idt48", # Source component (from the file's POST body)
        "javax.faces.partial.execute": "@all", # Execute all (from the file's POST body)
        "j_idt48": "j_idt48", # Action trigger (from the file's POST body)
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
    final_page_content = "" # Variable to hold the final HTML
    if redirect_elem is not None:
        redirect_url = redirect_elem.get('url')
        if redirect_url:
            print(f"   Found redirect URL: {redirect_url}")
            # Handle relative URL correctly
            # The redirect URL from the XML is relative to the domain root
            # The base for constructing the full URL should be the domain root
            # The redirect URL '/checkpost/faces/public/payment/TaxCollectionMainOnline.xhtml'
            # combined with 'https://checkpost.parivahan.gov.in' should give the correct full URL.
            # The BASE_URL_WITH_CONTEXT already includes '/checkpost', so we should use the domain root.
            # Let's define the domain root separately for clarity.
            DOMAIN_BASE_URL = "https://checkpost.parivahan.gov.in" # Domain root

            if redirect_url.startswith('/'):
                # Correctly form the absolute URL using the domain root
                redirect_url = DOMAIN_BASE_URL + redirect_url

            print("   Following redirect...")
            # Make a GET request to the redirect URL
            final_page_response = session.get(redirect_url)
            final_page_response.raise_for_status()
            final_page_content = final_page_response.text
            print("   Successfully loaded redirected page.")
            # Extract ViewState from this HTML if needed (optional here)
            final_page_viewstate = extract_viewstate(final_page_content)
            if final_page_viewstate:
                print(f"   Final Page ViewState: {final_page_viewstate}")
            else:
                 print("   No ViewState found on final page (this is okay).")

        else:
            print("   Redirect element found but no URL attribute.")
    else:
        print("   No <redirect> element found in XML response.")
        print("   The response might contain partial updates or scripts.")
        # In this case, the final content is likely the XML itself or parts of it.
        # It's less likely to be the full HTML page we want.
        # Let's try to see if there's an <update> containing HTML.
        # This is more complex and depends on the specific XML structure.
        # For now, we'll save the XML response as a fallback.
        # A better approach might be to inspect the XML manually or
        # make a subsequent GET request to TaxCollectionMainOnline.xhtml
        # if we know that's the expected next page.
        print("   Saving the XML response as final content (fallback).")
        final_page_content = final_xml_content # Save the XML response

    # --- 6. Save the Final Content ---
    print("\n--- Saving Final Content ---")
    if final_page_content:
         save_html_to_file(final_page_content, OUTPUT_FILENAME)
    else:
         print("   No final content to save.")

    print("\n--- Process Completed ---")


except requests.exceptions.RequestException as e:
    print(f"An error occurred during the requests: {e}")
    # Print the specific URL that failed, if available
    if hasattr(e, 'request') and e.request:
        print(f"   Failed URL: {e.request.url}")
except ET.ParseError as e:
    print(f"An error occurred parsing the XML response: {e}")
    print("Raw XML content that failed to parse:")
    print(response.text[:1000] if 'response' in locals() else "Response not available")
except Exception as e:
    print(f"An unexpected error occurred: {e}")
