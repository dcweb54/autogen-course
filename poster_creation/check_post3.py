import requests
from bs4 import BeautifulSoup
import xml.etree.ElementTree as ET
import urllib.parse
import os

# --- Configuration ---
# The base domain
DOMAIN_BASE_URL = "https://checkpost.parivahan.gov.in"
# The context path for the application
CONTEXT_PATH = "/checkpost"
# Initial page path
TAX_COLLECTION_PATH = "/faces/public/payment/TaxCollection.xhtml"
# Main online page path
MAIN_ONLINE_PATH = "/faces/public/payment/TaxCollectionMainOnline.xhtml"
# Filename for final output
OUTPUT_FILENAME = "final_result_output.html"

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
    "j_idt198": "MH12TV2539",  # <-- CHANGE THIS TO THE ACTUAL VEHICLE REG NO
    "mobileno": "",
    "j_idt215_input": "-1", # District?
    "district_input": "-1", # District?
    "regn_dt_input": "", # Registration Date? Format?
    "cmb_service_type_input": "-1", # Service Type?
    "cmb_permit_type_input": "-1", # Permit Type?
    "j_idt251": "", # ???
    "txt_seat_cap": "", # Seat Capacity?
    "cmb_payment_mode_input": "-1", # Payment Mode?
    "j_idt286_input": "-1", # ???
    "purposeofjourney": "", # Purpose of Journey?
    "cal_tax_from_input": "", # Tax From Date? Format?
    # Add other fields as needed based on the form
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

def save_content_to_file(content, filename):
    """Saves content (HTML or XML) to a file."""
    try:
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"   Content saved to '{filename}'")
    except Exception as e:
        print(f"   Error saving content to file: {e}")

# --- Main Script ---
session = requests.Session()
session.headers.update(HEADERS)

try:
    # --- STEP 1: Initial GET Request to TaxCollection.xhtml ---
    print("1. Fetching initial page...")
    initial_url = DOMAIN_BASE_URL + CONTEXT_PATH + TAX_COLLECTION_PATH
    print(f"   Requesting URL: {initial_url}")
    response = session.get(initial_url)
    response.raise_for_status()

    # --- STEP 2: Extract Initial ViewState ---
    initial_viewstate = extract_viewstate(response.text)
    if not initial_viewstate:
        print("Error: Could not extract initial ViewState. Aborting.")
        exit(1)
    print(f"   Initial ViewState: {initial_viewstate}")

    # --- STEP 3: POST Request: Select State (KA) ---
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

    # --- STEP 4: POST Request: Select Operation Code (5003) and Payment Type ---
    print("3. Sending Operation Selection POST request...")
    op_post_url = initial_url
    op_data = {
        "javax.faces.partial.ajax": "true",
        "javax.faces.source": "j_idt48", # Source component from fetch body
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

    # --- STEP 5: Handle Final XML Response from Operation Selection ---
    final_xml_content = response.text
    print("\n--- Parsing Operation Selection XML Response ---")

    # Parse the XML
    root = ET.fromstring(final_xml_content)

    # Look for the <redirect> element
    redirect_elem = root.find('.//redirect')
    final_page_content = "" # Variable to hold the final HTML
    if redirect_elem is not None:
        redirect_url = redirect_elem.get('url')
        if redirect_url:
            print(f"   Found redirect URL: {redirect_url}")
            # Handle relative URL correctly using the domain base
            if redirect_url.startswith('/'):
                redirect_url = DOMAIN_BASE_URL + redirect_url

            print("   Following redirect...")
            # Make a GET request to the redirect URL
            final_page_response = session.get(redirect_url)
            final_page_response.raise_for_status()
            final_page_content = final_page_response.text
            print("   Successfully loaded redirected page (TaxCollectionMainOnline.xhtml).")
            # Extract ViewState from this HTML if needed (optional here)
            main_online_viewstate = extract_viewstate(final_page_content)
            if main_online_viewstate:
                print(f"   ViewState for Main Online page: {main_online_viewstate}")
            else:
                 print("   Warning: No ViewState found on TaxCollectionMainOnline.xhtml.")

        else:
            print("   Redirect element found but no URL attribute.")
    else:
        print("   No <redirect> element found in operation selection XML response.")
        print("   Saving the XML response as final content (fallback).")
        final_page_content = final_xml_content # Save the XML response

    # --- STEP 6: Save the Content After State/Op Selection ---
    print("\n--- Saving Content After State/Op Selection ---")
    if final_page_content:
         save_content_to_file(final_page_content, "after_state_op_selection.html")
    else:
         print("   No content to save after state/op selection.")

    # --- STEP 7: Extend - Submit Form on TaxCollectionMainOnline.xhtml ---
    print("\n--- Extending Process: Submitting Form on TaxCollectionMainOnline.xhtml ---")

    # Use the HTML content we just got (final_page_content) or fetch it again if needed.
    # Assuming final_page_content holds the HTML of TaxCollectionMainOnline.xhtml
    main_online_html = final_page_content
    main_online_url = DOMAIN_BASE_URL + CONTEXT_PATH + MAIN_ONLINE_PATH

    # If we didn't get the HTML content correctly, we might need to GET it.
    # This check is simplistic. A more robust way is to ensure final_page_content
    # is the HTML, perhaps by checking its start tag or content.
    if not main_online_html or not main_online_html.strip().startswith('<'):
        print("   HTML content for TaxCollectionMainOnline.xhtml not found. Fetching it...")
        main_online_response = session.get(main_online_url)
        main_online_response.raise_for_status()
        main_online_html = main_online_response.text
        print("   Fetched TaxCollectionMainOnline.xhtml successfully.")

    # Extract ViewState for the form submission
    main_online_viewstate = extract_viewstate(main_online_html)
    if not main_online_viewstate:
        # If not found in HTML, maybe it was in the previous XML response?
        # Let's assume it was extracted earlier or try to get it from the session/context
        # For now, let's error out as it's critical.
        print("Error: Could not extract ViewState from TaxCollectionMainOnline.xhtml. Aborting form submission.")
        # exit(1) # Or handle gracefully
        main_online_viewstate = initial_viewstate # Fallback - might not work
        print(f"   Using fallback ViewState: {main_online_viewstate}")

    if main_online_viewstate:
        print(f"   ViewState for form submission: {main_online_viewstate}")

        # --- Prepare Form Data for POST ---
        form_post_data = {
            "javax.faces.partial.ajax": "true",
            "javax.faces.source": "j_idt200", # Source button/component (from the fetch body in Pasted_Text_1756721532320.txt)
            "javax.faces.partial.execute": "@all", # Execute all (from fetch body)
            # Specify what parts to render/update (from fetch body)
            "javax.faces.partial.render": "kataxcollection ConfirmationDialog popup ConfirmationDialogCash",
            "j_idt200": "j_idt200", # Action trigger (value matches source)
            "master_Layout_form": "master_Layout_form", # Form ID
            # Add the actual form field values
            # ** IMPORTANT: Update FORM_DATA_TO_SUBMIT dictionary above **
            **FORM_DATA_TO_SUBMIT, # Unpack the example/user data
            # Include the ViewState
            "javax.faces.ViewState": main_online_viewstate
        }

        # --- POST Request: Submit Form Data ---
        print("4. Sending Form Submission POST request...")
        form_post_url = main_online_url # POST to the same URL
        form_post_headers = {
            "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
            "Faces-Request": "partial/ajax", # Crucial for JSF AJAX
            "X-Requested-With": "XMLHttpRequest", # Standard AJAX header
            "Referer": main_online_url, # Important
            "Accept": "application/xml, text/xml, */*; q=0.01", # Expecting XML response
        }

        response = session.post(form_post_url, data=form_post_data, headers=form_post_headers)
        response.raise_for_status()
        print("   Form submission POST successful.")

        # --- Handle Final XML Response (Form Submission Result) ---
        final_form_xml_content = response.text
        print("\n--- Parsing Form Submission XML Response ---")
        # print("Form Submission XML Content:", final_form_xml_content) # Debug

        # Save the final XML response
        save_content_to_file(final_form_xml_content, OUTPUT_FILENAME)
        print("\n--- Extended Process Completed ---")
        print(f"The final XML response from form submission is saved in '{OUTPUT_FILENAME}'.")
        print("Inspect this file for calculated tax, confirmation messages, errors, etc.")
        # Further parsing of final_form_xml_content (e.g., finding <update> tags)
        # would go here if needed.

    else:
        print("   Cannot proceed with form submission due to missing ViewState.")


except requests.exceptions.RequestException as e:
    print(f"An error occurred during the requests: {e}")
    if hasattr(e, 'request') and e.request:
        print(f"   Failed URL: {e.request.url}")
except ET.ParseError as e:
    print(f"An error occurred parsing an XML response: {e}")
    print("Raw XML content that failed to parse:")
    # print(response.text[:1000] if 'response' in locals() else "Response not available")
except Exception as e:
    print(f"An unexpected error occurred: {e}")
