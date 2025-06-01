from Pages.base_page import BasePage
from Locators.home_page_locators import HomePageLocators
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from Pages.create_page import CreatePage
from Pages.poll_page import PollPageLocators


# class HomePageLocators:
#     """
#     Home Page locators
#     """
#     CREATE_NEW_POLL = (By.LINK_TEXT, "Create Group Poll")


class HomePage (BasePage):
    def click_create_group_poll(self):
        wait = WebDriverWait(self.driver, 10)  # Czekaj max 10 sek
        button = wait.until(EC.element_to_be_clickable(HomePageLocators.CREATE_NEW_POLL))
        button.click()
        return CreatePage (self.driver)
       # """
       # Click Create group poll
      #  :return: CreatePoll page
      #  """
        #1. Find button Create poll
        #2.Click in the button
        #return CreatePage (self.driver)

    def get_welcome_message(self):

        welcome_message = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located(HomePageLocators.AFTER_DELETE_POLL_WELCOME_MESSAGE)
        )
        return welcome_message.text

