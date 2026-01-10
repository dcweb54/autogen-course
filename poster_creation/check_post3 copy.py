import requests
from bs4 import BeautifulSoup, XMLParsedAsHTMLWarning # Import the warning class
import xml.etree.ElementTree as ET
import re
import json
import warnings # To handle warnings

# --- Suppress the BeautifulSoup XML/HTML parser warning ---
# As the content inside CDATA is often HTML meant for browser parsing,
# using the HTML parser is acceptable, and we suppress the warning.
warnings.filterwarnings("ignore", category=XMLParsedAsHTMLWarning)

# --- Configuration ---
DOMAIN_BASE_URL = "https://checkpost.parivahan.gov.in"
CONTEXT_PATH = "/checkpost"
TAX_COLLECTION_PATH = "/faces/public/payment/TaxCollection.xhtml"
MAIN_ONLINE_PATH = "/faces/public/payment/TaxCollectionMainOnline.xhtml"
OUTPUT_FILENAME = "final_result_output.xml"
EXTRACTED_DATA_JSON_FILENAME = "extracted_result_data.json"
EXTRACTED_DATA_TXT_FILENAME = "extracted_result_data.txt"

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
        return None

def save_content_to_file(content, filename):
    """Saves content to a file."""
    try:
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"   Content saved to '{filename}'")
    except Exception as e:
        print(f"   Error saving content to file: {e}")

def to_camel_case(label_text):
    """Converts a label string to camelCase."""
    if not label_text:
        return ""
    words = re.sub(r'[^\w\s]', '', label_text).split()
    if not words:
        return ""
    camel_case_words = [words[0].lower()] + [word.capitalize() for word in words[1:]]
    return "".join(camel_case_words)

def extract_data_from_html(html_content, source_description=""):
    """
    Extracts label-value pairs from HTML, mimicking the Dart logic.
    """
    print(f"  [Debug] Attempting to extract data from HTML source: {source_description}")
    extracted_data = {}
    try:
        # Use html.parser as intended, warning is suppressed
        soup = BeautifulSoup(html_content, 'html.parser')

        rows = soup.find_all(class_='ui-grid-row')
        print(f"  [Debug] Found {len(rows)} .ui-grid-row(s) in {source_description}")

        if len(rows) == 0:
            # Debug: Check if the main structure classes exist at all
            grid_cols = soup.find_all(class_=['ui-grid-col-3', 'ui-grid-col-6'])
            output_labels = soup.find_all(class_='ui-outputlabel')
            input_fields = soup.find_all('input', class_='ui-inputfield')
            print(f"  [Debug] Fallback search in {source_description}:")
            print(f"    Found {len(grid_cols)} .ui-grid-col-3/.ui-grid-col-6 elements")
            print(f"    Found {len(output_labels)} .ui-outputlabel elements")
            print(f"    Found {len(input_fields)} input.ui-inputfield elements")

        for i, row in enumerate(rows):
            print(f"  [Debug] Processing row {i+1}/{len(rows)}")
            columns = row.find_all(class_=['ui-grid-col-3', 'ui-grid-col-6'])
            print(f"    [Debug] Row {i+1} has {len(columns)} matching column(s)")

            for j, element in enumerate(columns):
                print(f"    [Debug] Processing column {j+1}/{len(columns)}")
                label_element = element.find(class_='ui-outputlabel')
                label_text = label_element.get_text(strip=True) if label_element else None
                print(f"      [Debug] Found label element: {label_element is not None}, text: '{label_text}'")

                value_text = None
                if label_text:
                    input_field = element.find('input', class_='ui-inputfield')
                    if input_field and input_field.get('value'):
                        value_text = input_field.get('value', '').strip()
                        print(f"      [Debug] Value from input field: '{value_text}'")
                    elif element.find('option', selected='selected'):
                        selected_option = element.find('option', selected='selected')
                        value_text = selected_option.get_text(strip=True) if selected_option else ''
                        print(f"      [Debug] Value from selected option: '{value_text}'")
                    elif element.find('span'):
                         span_text = element.find('span').get_text(strip=True)
                         value_text = span_text
                         print(f"      [Debug] Value from span: '{value_text}'")
                    else:
                         element_text = element.get_text(strip=True)
                         if element_text and element_text != label_text and element_text not in ['---Select Service Name---']:
                             value_text = element_text
                             print(f"      [Debug] Value from element text: '{value_text}'")
                         else:
                             print(f"      [Debug] Discarded element text: '{element_text}'")

                    if label_text and value_text and value_text.strip() and value_text != '---Select Service Name---':
                        clean_label = to_camel_case(label_text)
                        extracted_data[clean_label] = value_text.strip()
                        print(f"      [Extracted] {clean_label} = {value_text.strip()}")
                    else:
                         print(f"      [Debug] Skipping - Incomplete label/value pair.")

    except Exception as e:
        print(f"Error during HTML data extraction from {source_description}: {e}")

    print(f"  [Debug] Finished extracting data from {source_description}. Found {len(extracted_data)} items.")
    return extracted_data

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
    
    main_online_url = DOMAIN_BASE_URL + CONTEXT_PATH + MAIN_ONLINE_PATH

    # This part would normally use `final_page_content` from Steps 1-6.
    # If it's not available or not HTML, fetch it:
    try:
        if 'final_page_content' not in locals() or not final_page_content.strip().startswith('<'):
            print("   Fetching TaxCollectionMainOnline.xhtml (fallback)...")
            main_online_response = session.get(main_online_url)
            main_online_response.raise_for_status()
            final_page_content = main_online_response.text
            print("   Fetched TaxCollectionMainOnline.xhtml successfully.")
        else:
            print("   Using HTML content from previous step (redirect).")
    except NameError:
        print("   final_page_content not found, fetching TaxCollectionMainOnline.xhtml...")
        main_online_response = session.get(main_online_url)
        main_online_response.raise_for_status()
        final_page_content = main_online_response.text
        print("   Fetched TaxCollectionMainOnline.xhtml successfully.")
    except Exception as e:
        print(f"   Error fetching TaxCollectionMainOnline.xhtml: {e}")
        final_page_content = ""

    # Save the main page HTML for inspection if needed
    save_content_to_file(final_page_content, "TaxCollectionMainOnline_fetched.html")

    # Extract ViewState for form submission
    main_online_viewstate = extract_viewstate(final_page_content)
    if not main_online_viewstate:
        print("Error: Could not extract ViewState for TaxCollectionMainOnline.xhtml.")
        # Try using the initial one as a last resort (might not work)
        main_online_viewstate = initial_viewstate if 'initial_viewstate' in locals() else None
        if main_online_viewstate:
            print(f"   Using fallback ViewState: {main_online_viewstate}")
        else:
            print("   No ViewState available. Aborting form submission.")
            exit(1) # Stop if no ViewState

    print(f"   ViewState for form submission: {main_online_viewstate}")

    # Prepare and send form submission POST
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

    print("4. Sending Form Submission POST request...")
    form_post_url = main_online_url
    form_post_headers = {
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        "Faces-Request": "partial/ajax",
        "X-Requested-With": "XMLHttpRequest",
        "Referer": main_online_url, # Important for server-side checks
        "Accept": "application/xml, text/xml, */*; q=0.01",
    }

    try:
        response = session.post(form_post_url, data=form_post_data, headers=form_post_headers)
        response.raise_for_status()
        print("   Form submission POST successful.")
    except requests.exceptions.RequestException as e:
        print(f"   Error during form submission POST: {e}")
        if hasattr(e, 'request') and e.request:
            print(f"     Failed URL: {e.request.url}")
        exit(1)

    final_form_xml_content = response.text
    print("\n--- Parsing Form Submission XML Response ---")
    save_content_to_file(final_form_xml_content, OUTPUT_FILENAME)

    # --- EXTRACT RESULTS FROM XML RESPONSE ---
    print("\n--- Extracting Data from XML Response ---")
    extracted_data_dict = {}

    try:
        root = ET.fromstring(final_form_xml_content)
        print("   XML parsed successfully.")

        # --- Strategy 1: Look in the specific 'kataxcollection' update ---
        target_update_id = "kataxcollection"
        target_update_elem = root.find(f".//update[@id='{target_update_id}']")
        print(f"   Searching for <update id='{target_update_id}'>...")

        if target_update_elem is not None and target_update_elem.text:
            html_fragment = target_update_elem.text
            print(f"   Found <update id='{target_update_id}'>. Extracting data from its HTML content...")
            save_content_to_file(html_fragment, f"{target_update_id}_fragment.html") # Save for inspection
            extracted_data_dict = extract_data_from_html(html_fragment, source_description=f"<update id='{target_update_id}'> CDATA")

        # --- Strategy 2: If Strategy 1 fails, check other relevant updates ---
        if not extracted_data_dict:
            print("   No data found in 'kataxcollection'. Checking other <update> elements...")
            other_update_ids = ["ConfirmationDialog", "popup", "ConfirmationDialogCash"]
            for update_id in other_update_ids:
                update_elem = root.find(f".//update[@id='{update_id}']")
                if update_elem is not None and update_elem.text:
                    html_fragment = update_elem.text
                    print(f"   Found <update id='{update_id}'>. Extracting data...")
                    save_content_to_file(html_fragment, f"{update_id}_fragment.html")
                    temp_data = extract_data_from_html(html_fragment, source_description=f"<update id='{update_id}'> CDATA")
                    if temp_data:
                        extracted_data_dict.update(temp_data) # Merge found data
                        print(f"   Data found in <update id='{update_id}'>. Continuing...")
                        # You might want to break here if you only need data from the first relevant source found
                        # break

        # --- Strategy 3: Ultimate fallback - parse the main page HTML again ---
        # This is less likely if the POST was successful and meant to update a section.
        if not extracted_data_dict:
            print("   No data found in XML updates. Trying to extract from the main page HTML again...")
            extracted_data_dict = extract_data_from_html(final_page_content, source_description="Main Page HTML (Fallback)")


        # --- SAVE EXTRACTED DATA ---
        if extracted_data_dict:
            print(f"\n--- Data Extraction Completed ---")
            print(f"Extracted {len(extracted_data_dict)} key-value pairs.")

            try:
                with open(EXTRACTED_DATA_JSON_FILENAME, 'w', encoding='utf-8') as f:
                    json.dump(extracted_data_dict, f, indent=4, ensure_ascii=False)
                print(f"   Extracted data saved to '{EXTRACTED_DATA_JSON_FILENAME}' (JSON format).")
            except Exception as e:
                print(f"   Error saving JSON data: {e}")

            try:
                with open(EXTRACTED_DATA_TXT_FILENAME, 'w', encoding='utf-8') as f:
                    f.write("{\n")
                    for key, value in extracted_data_dict.items():
                        escaped_value = value.replace('"', '\\"')
                        f.write(f'  "{key}": "{escaped_value}",\n')
                    f.write("}\n")
                print(f"   Extracted data saved to '{EXTRACTED_DATA_TXT_FILENAME}' (Text map format).")
            except Exception as e:
                print(f"   Error saving text data: {e}")

            print("   Sample of extracted data:")
            count = 0
            for key, value in extracted_data_dict.items():
                print(f"     {key}: {value}")
                count += 1
                if count >= 5:
                    if len(extracted_data_dict) > 5:
                        print("     ... (see full output in files)")
                    break
        else:
            print("   *** No data was extracted from any source. ***")
            print("   - Check the saved HTML/XML files (especially the _fragment.html files) to see the actual structure returned by the server.")
            print("   - The server might have returned an error message instead of the expected data table.")
            print("   - The structure of the result table might be different from what the extraction function expects.")
            print("   - Ensure the vehicle registration number and other form data are correct.")


    except ET.ParseError as e:
        print(f"   Error parsing XML response: {e}")
        print("   Raw XML content (first 1000 chars):")
        print(final_form_xml_content[:1000])
    except Exception as e:
        print(f"   Unexpected error during data extraction process: {e}")

    print("\n--- Process Finished ---")



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
