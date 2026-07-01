import os
import time
import win32com.client
import re
from selenium.common.exceptions import TimeoutException
from selenium.common import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import config
import requests


class Functions:

    @staticmethod
    def check_response(config):
        response = requests.get(config.data)
        if response.status_code in [503, 404]:
            error_message = f"{response.status_code} error at {config.data}"
            print(error_message)
            Functions.append_to_notepad(config.file_path, error_message)
            return
    @staticmethod
    def clear_outlook_folder(folder_name, subfolder_name, email):
        outlook = win32com.client.Dispatch("Outlook.Application").GetNamespace("MAPI")
        folder = outlook.Folders(email).Folders(folder_name)
        subfolder = folder.Folders(subfolder_name)

        while subfolder.Items.Count > 0:
            try:
                item = subfolder.Items.GetFirst()
                item.Delete()
                time.sleep(.3)
            except Exception as e:
                print(f"An error occurred: {str(e)}")
                break

        print(f"The subfolder '{subfolder_name}' in folder '{folder_name}' has been cleared.")

    @staticmethod
    def wait_and_find_element_10(driver, xpath):
        try:
            wait = WebDriverWait(driver, 10)
            element = wait.until(EC.element_to_be_clickable((By.XPATH, xpath)))
            return element
        except (TimeoutException, NoSuchElementException) as e:
            print(f"Element not found: {xpath}")
            return None

    @staticmethod
    def wait_and_find_element_30(driver, xpath):
        try:
            wait = WebDriverWait(driver, 30)
            element = wait.until(EC.element_to_be_clickable((By.XPATH, xpath)))
            return element
        except (TimeoutException, NoSuchElementException) as e:
            print(f"Element not found: {xpath}")
            return None

    @staticmethod
    def wait_and_find_element_click_10(driver, xpath):
        try:
            wait = WebDriverWait(driver, 10)
            element = wait.until(EC.visibility_of_element_located((By.XPATH, xpath)))
            return element
        except (TimeoutException, NoSuchElementException) as e:
            print(f"Element not found: {xpath}")
            return None

    @staticmethod
    def wait_and_find_element_5(driver, xpath):
        try:
            wait = WebDriverWait(driver, 5)
            element = wait.until(EC.element_to_be_clickable((By.XPATH, xpath)))
            return element
        except (TimeoutException, NoSuchElementException) as e:
            print(f"Element not found: {xpath}")
            return None

    @staticmethod
    def error(driver, xpath):
        try:
            wait = WebDriverWait(driver, 3)
            element_click = wait.until(EC.element_to_be_clickable((By.XPATH, xpath)))
            return element_click
        except TimeoutException:
            print("No error found in this page")
            return None

    @staticmethod
    def otp(folder_name, subfolder_name, email, url_to_match, max_attempts=10, wait_time=10):
        for _ in range(max_attempts):
            outlook = win32com.client.Dispatch("Outlook.Application").GetNamespace("MAPI")

            folder = outlook.Folders(email).Folders(folder_name)
            subfolder = folder.Folders(subfolder_name)

            # Sort messages by received time in descending order
            messages = sorted(subfolder.Items, key=lambda x: x.ReceivedTime, reverse=True)

            for message in messages:
                body = message.Body
                match = re.search(r'\b\d{6}\b', body)
                if match:
                    six_digit_number = match.group()
                    #return six_digit_number
                    # Check if the body contains the specified URL
                    if f"{url_to_match}" in body:
                        return six_digit_number
            time.sleep(wait_time)
        return None

    @staticmethod
    def login(driver, auth_url):
        driver.get(auth_url)
        Functions.wait_and_find_element_30(driver, "//input[@id='username']").send_keys(config.username)
        Functions.wait_and_find_element_10(driver, "//input[@id='password']").send_keys(config.password)
        Functions.wait_and_find_element_10(driver, "//button[normalize-space()='Log in']").click()

    @staticmethod
    def login_and_verify_loop(driver, auth_url, full_url, outlookfolder, outlooksubfolder, email, max_attempts,
                              wait_time):
        """
        Logs in and verifies, handling invalid login attempts.
        Returns True if an invalid login was detected and skipped, False otherwise (successful login or other failure).
        """
        while True:
            # Calling the function to clear the Outlook box
            Functions.clear_outlook_folder(outlookfolder, outlooksubfolder, email)
            time.sleep(3)

            # Call the login function to log in
            Functions.login(driver, auth_url)

            # --- Check for "Invalid login attempt" ---
            if Functions.is_element_present(driver, "//li[text()='Invalid login attempt.']", timeout=3):
                print(f"Invalid login attempt detected for {auth_url}. Skipping this tenant.")
                time.sleep(2)  # Give a moment to register the message
                return True  # Indicate that an invalid login was detected and we should skip

            # Use the otp function to retrieve the OTP
            FA = Functions.otp(outlookfolder, outlooksubfolder, email, full_url, max_attempts=max_attempts,
                               wait_time=wait_time)

            # Check if FA is None
            if FA is None:
                print("FA is None. Retrying...")
                time.sleep(2)
            else:
                print(f"Six-digit number from the email with matching Tenant URL: {FA}")
                # Sleep for 1 second (if needed)
                time.sleep(1)
                try:
                    # Automating to enter 2FA
                    Functions.wait_and_find_element_10(driver, "//input[@id='TwoFactorCode']").send_keys(FA)
                    Functions.wait_and_find_element_10(driver, "//button[normalize-space()='Verify code']").click()
                    return False  # Successful login, exit loop and indicate no skip
                except (NoSuchElementException, TimeoutException) as e:
                    print(f"Error during 2FA entry: {e}. Retrying login process.")
                    time.sleep(2)
                    # continue to the next iteration of the while loop, don't return here yet
    @staticmethod
    def is_element_present(driver, xpath, timeout=3):
        """
        Checks if an element is present on the page within a given timeout.
        Returns True if found, False otherwise.
        """
        try:
            WebDriverWait(driver, timeout).until(
                EC.presence_of_element_located((By.XPATH, xpath))
            )
            return True
        except TimeoutException:
            return False
    @staticmethod
    def get_chrome_driver():
        chrome_options = Options()
        chrome_options.add_experimental_option("detach", True)
        return webdriver.Chrome(options=chrome_options)

    @staticmethod
    def create_folder(folder_name, folder_path):
        folder_path = os.path.join(folder_path, folder_name)
        try:
            os.makedirs(folder_path)
            print(f"Folder '{folder_name}' created successfully at '{folder_path}'")
        except FileExistsError:
            print(f"Folder '{folder_name}' already exists at '{folder_path}'")
        except Exception as e:
            print(f"An error occurred while creating the folder: {e}")

    @staticmethod
    def append_to_notepad(file_path, content):
        try:
            # Open the file in append mode
            with open(file_path, "a") as file:
                # Write the content to the file
                file.write(content + '\n')
            return True
        except Exception as e:
            print(f"An error occurred: {e}")
            return False

    @staticmethod
    def handle_error(driver):
        current_url = driver.current_url
        driver.execute_script(f"window.open('{current_url}', '_blank');")
        driver.switch_to.window(driver.window_handles[0])
        time.sleep(1)
