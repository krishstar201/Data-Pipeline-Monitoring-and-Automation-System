import requests
import time
from functions import Functions
import config

def orch_flow(driver):
    try:
        # Check for a 503 error before using the WebDriver
        response = requests.get(config.orch)
        if response.status_code in [503,404]:
            print(f"503 Service Unavailable error at {config.orch}")
            Functions.append_to_notepad(config.file_path, f"503 Service Unavailable error at {config.orch}")
            return

        # Navigate to the webpage
        driver.get(config.orch)
        time.sleep(2)

        # Check for 'No results found.' span
        orch_flow_no_streams = Functions.wait_and_find_element_10(driver, "//clr-dg-placeholder//span[contains(text(), 'No results')]")
        if orch_flow_no_streams is None:
            # Streams are present
            # function to open new tab
            Functions.handle_error(driver)
            print(f"Orch flow streams are present in {config.tenant}")
            Functions.append_to_notepad(config.file_path, f"Orch flow streams are present in {config.tenant}")
            Functions.append_to_notepad(config.file_path, f"Tenant URL: {config.orch}")  # Log the URL
        else:
            print(f"Orch flow streams are not present in {config.tenant}")
            Functions.append_to_notepad(config.file_path, f"Orch flow streams are not present in {config.tenant}")
    except Exception as e:
        print(f"An error occurred: {e}")
        Functions.append_to_notepad(config.file_path, f"An error occurred: {e}")
