import requests
import time
from functions import Functions
import config

def stream_flow(driver):
    try:
        response = requests.get(config.stream)
        if response.status_code in [503,404]:
            print(f"503 Service Unavailable error at {config.stream}")
            Functions.append_to_notepad(config.file_path, f"503 Service Unavailable error at {config.stream}")
            return

        driver.get(config.stream)
        time.sleep(2)

        sf_no_streams = Functions.wait_and_find_element_10(driver, "//clr-dg-placeholder//span[contains(text(), 'No results')]")
        if sf_no_streams is None:
            Functions.handle_error(driver)
            print(f"Stream flow streams are present in {config.tenant}")
            Functions.append_to_notepad(config.file_path, f"Stream flow streams are present in {config.tenant}")
            Functions.append_to_notepad(config.file_path, f"Tenant URL: {config.stream}")  # Log the URL
        else:
            print(f"Stream flow streams are not present in {config.tenant}")
            Functions.append_to_notepad(config.file_path, f"Stream flow streams are not present in {config.tenant}")
    except Exception as e:
        print(f"An error occurred: {e}")
        Functions.append_to_notepad(config.file_path, f"An error occurred: {e}")
