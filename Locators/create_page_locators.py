from selenium.webdriver.common.by import By

class CreatePageLocators:
    """
    Create Page locators
    """
    TITLE_INPUT = (By.ID, "title")
    LOCATION_INPUT = (By.ID, "location")
    DESCRIPTION_INPUT = (By.ID, "description")
    DATE1_CLICK = (By.XPATH, "//button/span[text()='21']")
    DATE2_CLICK = (By.XPATH, "//button/span[text()='22']")
    DATE3_CLICK = (By.XPATH, "//button/span[text()='23']")
    CREATEPOLL_CLICK = (By.XPATH, "//button[@type='submit' and contains(normalize-space(), 'Create poll')]")
    ERROR_DATE_MESSAGE = (By.ID, "undefined-form-item-message")
    ERROR_TITLE_MESSAGE = (By.XPATH, "//p[contains(text(), 'Title') and contains(@class, 'text-destructive')]")
    MODAL_CLOSE_BUTTON = (By.CSS_SELECTOR, "button.absolute.right-4.top-4")
    COPIED_LINK_SPAN = (By.CSS_SELECTOR, "span.truncate")
    HEADER = (By.XPATH, "//h5[normalize-space()='Your administrator rights can be lost if you clear your cookies']")
    TITLE = (By.XPATH, '//*[@data-testid="poll-title"]')
    TOGGLE_COMMENTS = (By.ID, "disableComments")