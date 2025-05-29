import time
import random
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException

class FacebookReportBot:
    def __init__(self, email, password, headless=True):
        """
        Initialize the Facebook Report Bot
        
        :param email: Facebook login email
        :param password: Facebook login password
        :param headless: Run browser in headless mode (no GUI)
        """
        self.email = email
        self.password = password
        
        # Configure Chrome options
        options = webdriver.ChromeOptions()
        if headless:
            options.add_argument('--headless')
        options.add_argument('--disable-notifications')
        options.add_argument('--disable-infobars')
        options.add_argument('--disable-extensions')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--no-sandbox')
        
        # Initialize the WebDriver
        self.driver = webdriver.Chrome(options=options)
        self.wait = WebDriverWait(self.driver, 20)
        
    def login(self):
        """Log in to Facebook"""
        try:
            self.driver.get('https://www.facebook.com')
            
            # Wait for email field and enter credentials
            email_field = self.wait.until(EC.presence_of_element_located((By.ID, 'email')))
            email_field.send_keys(self.email)
            
            password_field = self.driver.find_element(By.ID, 'password')
            password_field.send_keys(self.password)
            password_field.send_keys(Keys.RETURN)
            
            # Wait for login to complete
            self.wait.until(EC.presence_of_element_located((By.XPATH, '//div[@role="navigation"]')))
            print("Login successful")
            return True
        except Exception as e:
            print(f"Login failed: {str(e)}")
            return False
    
    def report_account(self, profile_url, reason="spam", delay=5):
        """
        Report a Facebook account
        
        :param profile_url: URL of the profile to report
        :param reason: Reason for reporting (spam, fake, harassment, etc.)
        :param delay: Delay between actions to mimic human behavior
        :return: True if report was successful, False otherwise
        """
        try:
            self.driver.get(profile_url)
            time.sleep(delay)
            
            # Click on the three dots menu
            menu_button = self.wait.until(EC.element_to_be_clickable(
                (By.XPATH, '//div[@aria-label="Actions for this profile"]')))
            menu_button.click()
            time.sleep(delay/2)
            
            # Click on "Find support or report profile"
            report_option = self.wait.until(EC.element_to_be_clickable(
                (By.XPATH, '//span[contains(text(), "Find support or report profile")]')))
            report_option.click()
            time.sleep(delay/2)
            
            # Select reason for reporting
            reason_xpath = f'//span[contains(text(), "{reason.capitalize()}")]'
            reason_option = self.wait.until(EC.element_to_be_clickable((By.XPATH, reason_xpath)))
            reason_option.click()
            time.sleep(delay/2)
            
            # Click next
            next_button = self.wait.until(EC.element_to_be_clickable(
                (By.XPATH, '//span[contains(text(), "Next")]')))
            next_button.click()
            time.sleep(delay/2)
            
            # Submit the report
            submit_button = self.wait.until(EC.element_to_be_clickable(
                (By.XPATH, '//span[contains(text(), "Submit")]')))
            submit_button.click()
            time.sleep(delay)
            
            print(f"Successfully reported {profile_url} for {reason}")
            return True
            
        except Exception as e:
            print(f"Failed to report {profile_url}: {str(e)}")
            return False
    
    def mass_report(self, profile_urls, reasons=None, delay_range=(5, 15)):
        """
        Report multiple accounts
        
        :param profile_urls: List of profile URLs to report
        :param reasons: List of reasons corresponding to each profile
        :param delay_range: Range of random delays between reports (min, max)
        """
        if not reasons:
            reasons = ["spam"] * len(profile_urls)
            
        if len(profile_urls) != len(reasons):
            print("Error: Number of URLs must match number of reasons")
            return
            
        for i, (url, reason) in enumerate(zip(profile_urls, reasons)):
            print(f"Reporting account {i+1}/{len(profile_urls)}")
            self.report_account(url, reason)
            
            # Random delay to avoid detection
            delay = random.randint(*delay_range)
            time.sleep(delay)
    
    def close(self):
        """Close the browser"""
        self.driver.quit()

# Example usage
if __name__ == "__main__":
    # WARNING: Replace with your credentials if you want to test (not recommended)
    EMAIL = "your_email@example.com"
    PASSWORD = "your_password"
    
    # List of profile URLs to report (example only)
    PROFILES_TO_REPORT = [
        "https://www.facebook.com/profile1",
        "https://www.facebook.com/profile2",
        # Add more profiles here
    ]
    
    # Reasons for reporting (should match the number of profiles)
    REASONS = [
        "spam",
        "fake account",
        # Add more reasons here
    ]
    
    # Initialize and run the bot
    bot = FacebookReportBot(EMAIL, PASSWORD, headless=False)
    
    if bot.login():
        bot.mass_report(PROFILES_TO_REPORT, REASONS)
    else:
        print("Cannot proceed without login")
    
    bot.close()