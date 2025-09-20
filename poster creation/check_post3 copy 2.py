import requests
from bs4 import BeautifulSoup
import xml.etree.ElementTree as ET
import urllib.parse
import time # Potentially useful for delays if needed

# --- Configuration ---
DOMAIN_BASE_URL = "https://checkpost.parivahan.gov.in"
CONTEXT_PATH = "/checkpost"
TAX_COLLECTION_PATH = "/faces/public/payment/TaxCollection.xhtml"
MAIN_ONLINE_PATH = "/faces/public/payment/TaxCollectionMainOnline.xhtml"
FINAL_OUTPUT_FILENAME = "final_page_result.html" # File to save the final HTML

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Safari/537.36",
    "Accept-Language": "en-US,en;q=0.9",
    "Accept-Encoding": "gzip, deflate, br",
    "Connection": "keep-alive",
    "Upgrade-Insecure-Requests": "1",
}

# --- Example Form Data for TaxCollectionMainOnline.xhtml ---
# YOU MUST UPDATE THESE VALUES, ESPECIALLY THE VEHICLE REGISTRATION NUMBER
FORM_DATA_TO_SUBMIT = {
    "j_idt198": "MH12TV2539",  # <-- CHANGE THIS
    "mobileno": "",
    "j_idt215_input": "-1",
    "district_input": "-1",
    "regn_dt_input": "",
    "cmb_service_type_input": "-1",
    "cmb_permit_type_input": "-1",
    "j_idt251": "",
    "txt_seat_cap": "",
    "cmb_payment_mode_input": "-1",
    "j_idt286_input": "-1",
    "purposeofjourney": "",
    "cal_tax_from_input": "",
}

# --- Helper Functions ---
def extract_viewstate(html_content):
    """Extracts the javax.faces.ViewState value from HTML."""
    soup = BeautifulSoup(html_content, 'html.parser')
    viewstate_input = soup.find("input", {"name": "javax.faces.ViewState"})
    if viewstate_input and viewstate_input.get('value'):
        return viewstate_input['value']
    else:
        print("Warning: ViewState not found in provided HTML.")
        return None

def save_content_to_file(content, filename):
    """Saves content to a file."""
    try:
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"Content successfully saved to '{filename}'")
    except Exception as e:
        print(f"Error saving content to file '{filename}': {e}")

# --- Main Script ---
session = requests.Session()
session.headers.update(HEADERS)

try:
    # --- STEP 1: Initial GET Request to TaxCollection.xhtml ---
    print("1. Fetching initial page (TaxCollection.xhtml)...")
    initial_url = DOMAIN_BASE_URL + CONTEXT_PATH + TAX_COLLECTION_PATH
    response = session.get(initial_url)
    response.raise_for_status()
    initial_html = response.text
    print("   Initial page loaded.")

    # --- STEP 2: Extract Initial ViewState ---
    initial_viewstate = extract_viewstate(initial_html)
    if not initial_viewstate:
        print("Error: Could not extract initial ViewState. Aborting.")
        exit(1)
    print("   Initial ViewState extracted.")

    # --- STEP 3: POST Request: Select State (KA) ---
    print("2. Sending State Selection POST request...")
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
    response = session.post(initial_url, data=state_data, headers=state_headers)
    response.raise_for_status()
    print("   State selection successful.")

    # --- STEP 4: POST Request: Select Operation Code (5003) and Payment Type ---
    print("3. Sending Operation Selection POST request...")
    op_data = {
        "javax.faces.partial.ajax": "true",
        "javax.faces.source": "j_idt48", # From fetch body
        "javax.faces.partial.execute": "@all",
        "j_idt48": "j_idt48",
        "PAYMENT_TYPE": "ONLINE",
        "master_Layout_form": "master_Layout_form",
        "ib_state_input": "KA",
        "operation_code_input": "5003",
        "javax.faces.ViewState": initial_viewstate # Reuse initial VS or extract from state response if it changes
    }
    op_headers = {
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        "Faces-Request": "partial/ajax",
        "X-Requested-With": "XMLHttpRequest",
        "Referer": initial_url,
        "Accept": "application/xml, text/xml, */*; q=0.01",
    }
    response = session.post(initial_url, data=op_data, headers=op_headers)
    response.raise_for_status()
    print("   Operation selection successful.")

    # --- STEP 5: Handle Redirect from Operation Selection ---
    final_xml_content = response.text
    print("4. Checking for redirect after operation selection...")
    root = ET.fromstring(final_xml_content)
    redirect_elem = root.find('.//redirect')

    main_online_url = DOMAIN_BASE_URL + CONTEXT_PATH + MAIN_ONLINE_PATH
    final_page_html = ""

    if redirect_elem is not None:
        redirect_url = redirect_elem.get('url')
        if redirect_url:
            print(f"   Found redirect URL: {redirect_url}")
            if redirect_url.startswith('/'):
                redirect_url = DOMAIN_BASE_URL + redirect_url
            print("   Following redirect to TaxCollectionMainOnline.xhtml...")
            final_page_response = session.get(redirect_url)
            final_page_response.raise_for_status()
            final_page_html = final_page_response.text
            print("   Redirected page loaded.")
        else:
            print("   Redirect element found but no URL attribute. Proceeding to main online page.")
            # Fallback: GET the main online page
            final_page_response = session.get(main_online_url)
            final_page_response.raise_for_status()
            final_page_html = final_page_response.text
    else:
        print("   No redirect found in XML response. Proceeding to main online page directly.")
        # Fallback: GET the main online page
        final_page_response = session.get(main_online_url)
        final_page_response.raise_for_status()
        final_page_html = final_page_response.text

    # --- STEP 6: Extract ViewState for Main Online Page ---
    print("5. Extracting ViewState from TaxCollectionMainOnline.xhtml...")
    main_online_viewstate = extract_viewstate(final_page_html)
    if not main_online_viewstate:
        print("Error: Could not extract ViewState for TaxCollectionMainOnline.xhtml. Using initial VS as fallback.")
        main_online_viewstate = initial_viewstate # Last resort fallback
        if not main_online_viewstate:
             print("Error: No ViewState available. Aborting form submission.")
             exit(1)
    print("   ViewState for main online page extracted.")

    # --- STEP 7: Submit Form on TaxCollectionMainOnline.xhtml ---
    print("6. Submitting form on TaxCollectionMainOnline.xhtml...")
    form_post_data = {
        "javax.faces.partial.ajax": "true",
        "javax.faces.source": "j_idt200", # From Pasted_Text_1756721532320.txt fetch body
        "javax.faces.partial.execute": "@all",
        "javax.faces.partial.render": "kataxcollection ConfirmationDialog popup ConfirmationDialogCash", # From fetch body
        "j_idt200": "j_idt200",
        "master_Layout_form": "master_Layout_form",
        **FORM_DATA_TO_SUBMIT, # Update this dict with your data
        "javax.faces.ViewState": main_online_viewstate
    }
    form_post_headers = {
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        "Faces-Request": "partial/ajax",
        "X-Requested-With": "XMLHttpRequest",
        "Referer": main_online_url, # Important for server-side checks
        "Accept": "application/xml, text/xml, */*; q=0.01",
    }
    response = session.post(main_online_url, data=form_post_data, headers=form_post_headers)
    response.raise_for_status()
    form_response_xml = response.text
    print("   Form submission successful.")

    # --- STEP 8: Determine Final State and Save HTML ---
    print("7. Determining final page state and saving HTML...")

    # The form submission was AJAX. The response is XML.
    # The page itself might have been updated via JavaScript in a real browser.
    # However, we can try to get the *current* state of the page by requesting it again.
    # This is a common approach in server-side scraping when dealing with AJAX updates
    # that don't result in a new page load/redirect.

    print("   Requesting the final state of TaxCollectionMainOnline.xhtml...")
    # Make a GET request to the main online page URL again to get its current state
    # after the AJAX update might have been processed server-side or just to get
    # the latest full HTML.
    final_state_response = session.get(main_online_url)
    final_state_response.raise_for_status()
    final_page_result_html = final_state_response.text

    # Save the final HTML content
    save_content_to_file(final_page_result_html, FINAL_OUTPUT_FILENAME)

    print("\n--- Process Completed ---")
    print(f"The final HTML page content is saved in '{FINAL_OUTPUT_FILENAME}'.")


except requests.exceptions.RequestException as e:
    print(f"An error occurred during the requests: {e}")
    if hasattr(e, 'request') and e.request:
        print(f"   Failed URL: {e.request.url}")
except ET.ParseError as e:
    print(f"An error occurred parsing an XML response: {e}")
except Exception as e:
    print(f"An unexpected error occurred: {e}")
