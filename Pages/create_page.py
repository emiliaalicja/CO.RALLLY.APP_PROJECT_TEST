from Pages.base_page import BasePage
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os
from Pages.poll_page import PollPage
from Locators.create_page_locators import CreatePageLocators


class CreatePage(BasePage):
    def enter_title(self, title):
        WebDriverWait(self.driver, 15).until(EC.presence_of_element_located(CreatePageLocators.TITLE_INPUT)).send_keys(
            title)

    def enter_location(self, location):
        self.driver.find_element(*CreatePageLocators.LOCATION_INPUT).send_keys(location)

    def enter_description(self, description):
        self.driver.find_element(*CreatePageLocators.DESCRIPTION_INPUT).send_keys(description)

    def enter_time(self):
        # Browser scroll
        self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        self.driver.find_element(*CreatePageLocators.DATE1_CLICK).click()
        self.driver.find_element(*CreatePageLocators.DATE2_CLICK).click()
        self.driver.find_element(*CreatePageLocators.DATE3_CLICK).click()

    def click_create_poll(self):
        # Browser scroll
        self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        self.driver.find_element(*CreatePageLocators.CREATEPOLL_CLICK).click()
        print("Button 'Create poll' clicked.")

    def save_modal_link_to_file(self, filename="copied_link.txt"):
        span_elem = WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located(CreatePageLocators.COPIED_LINK_SPAN)
        )
        # remove excess spaces
        link_text = span_elem.text.strip()
        # Path to the main directory of the project: co.rallly.app (one level above Test/)
        BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
        folder_path = os.path.join(BASE_DIR, "resources")
        os.makedirs(folder_path, exist_ok=True)
        file_path = os.path.join(folder_path, filename)
        with open(file_path, "w") as f:
            f.write(link_text)
        print(f"Link saved: {link_text} to the file: {file_path}")

    def close_modal_and_go_to_poll_page(self):
        close_btn = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable(CreatePageLocators.MODAL_CLOSE_BUTTON)
        )
        close_btn.click()
        return PollPage(self.driver)

    def turn_off_comments(self):
        toggle = self.driver.find_element(*CreatePageLocators.TOGGLE_COMMENTS)
        toggle.click()

    def get_error_date_message(self):
        element = self.driver.find_element(*CreatePageLocators.ERROR_DATE_MESSAGE)
        return element.text

    def get_error_title_message(self):
        element = self.driver.find_element(*CreatePageLocators.ERROR_TITLE_MESSAGE)
        # Scroll to element
        self.driver.execute_script("arguments[0].scrollIntoView({ behavior: 'smooth', block: 'center' });", element)
        return element.text
