from selenium.webdriver.common.by import By

class HomePageLocators:
    """
    Home Page locators
    """
    CREATE_NEW_POLL = (By.LINK_TEXT, "Create Group Poll")
    AFTER_DELETE_POLL_WELCOME_MESSAGE = (By.XPATH, "//h1[text()='Welcome']")
