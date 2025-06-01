from Pages.base_page import BasePage
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from Pages.poll_page import PollPageLocators


class DeletePage(BasePage):



    def get_delete_poll_message(self):
        delete_alert = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located(PollPageLocators.DELETED_POLL_MESSAGE)
        )
        return delete_alert.text

