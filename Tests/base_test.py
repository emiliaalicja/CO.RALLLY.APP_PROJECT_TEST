import unittest
from selenium import webdriver
from Pages.home_page import HomePage


class BaseTest(unittest.TestCase):
    """
    Base class for each test in one class
    """

    def setUp(self):
        # Inicjalizacja przeglądarki
        self.driver = webdriver.Chrome()
        self.driver.maximize_window()
        self.driver.get("https://app.rallly.co/")
        self.home_page = HomePage(self.driver)

    def tearDown(self):
        try:
            if hasattr(self, "poll_page") and self.poll_page.poll_was_created:
                self.poll_page.delete_poll()
        finally:
            self.driver.quit()
