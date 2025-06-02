from Pages.base_page import BasePage
from Locators.home_page_locators import HomePageLocators
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from Pages.create_page import CreatePage


class HomePage (BasePage):
    def click_create_group_poll(self):
        """
        1.Find button Create poll
        2.Click in the button
        return CreatePage (self.driver)
        """
        wait = WebDriverWait(self.driver, 15)
        button = wait.until(EC.element_to_be_clickable(HomePageLocators.CREATE_NEW_POLL))
        button.click()
        return CreatePage (self.driver)


    def get_welcome_message(self):

        welcome_message = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located(HomePageLocators.AFTER_DELETE_POLL_WELCOME_MESSAGE)
        )
        return welcome_message.text

