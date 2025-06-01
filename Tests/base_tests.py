import unittest
from selenium import webdriver
from Pages.home_page import HomePage




class BaseTest(unittest.TestCase):
    """
    Base class for each test in one class
    """

    def setUp(self):
        #Inicjalizacja przeglądarki
        self.driver = webdriver.Chrome()
        self.driver.maximize_window()
        self.driver.get("https://app.rallly.co/")
        self.home_page = HomePage(self.driver)


    def test_open_homepage(self):
            #self.assertIn("Rallly", self.driver.title)
        return

    def tearDown(self):
        try:
            if hasattr(self, "poll_page") and self.poll_page.poll_was_created:
                self.poll_page.delete_poll()
        finally:
            self.driver.quit()


# BaseClassLevelTest — dla PollTest (raz driver i jedna ankieta)
# class BaseClassLevelTest(unittest.TestCase):
    """
       Base class for all tests in one class
       """

    # @classmethod
    # def setUpClass(cls):
    #     from selenium import webdriver
    #     cls.driver = webdriver.Chrome()
    #     cls.driver.maximize_window()
    #     cls.driver.get("https://app.rallly.co/")
    #     cls.home_page = HomePage(cls.driver)
    #
    # @classmethod
    # def tearDownClass(cls):
    #     try:
    #         if hasattr(cls, "poll_page") and cls.poll_page.poll_was_created:
    #             cls.poll_page.delete_poll()
    #     finally:
    #         cls.driver.quit()