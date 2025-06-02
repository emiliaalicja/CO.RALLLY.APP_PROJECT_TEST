from Pages.base_page import BasePage
from Locators.poll_page_locators import PollPageLocators
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver import ActionChains #needed for double click


class PollPage(BasePage):

    def __init__(self, driver):
        super().__init__(driver)
        self.poll_was_created = True  #False to delete the poll

    def get_page_header(self):
        header = WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located(PollPageLocators.HEADER)
        )
        return header.text

    def get_page_title(self):
        title = WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located(PollPageLocators.GET_TITLE)
        )
        return title.text


    def get_page_localization(self):
        localization = self.driver.find_element(*PollPageLocators.POLL_LOCALIZATION)
        return localization.text

    def get_page_description(self):
        description = self.driver.find_element(*PollPageLocators.POLL_DESCRIPTION)
        return description.text

    def get_page_dates_options(self):
        options = WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located(PollPageLocators.POLL_DATES_OPTIONS))
        print(f"Dat options: number: {options.text}")
        return options.text

    def get_page_active_comments(self):
        active_comments = self.driver.find_element(*PollPageLocators.POLL_COMMENTS_MESSAGE)
        return active_comments.text

    def get_page_disabled_comments(self):
        disabled_comments = self.driver.find_element(*PollPageLocators.POLL_DISABLED_COMMENTS_MESSAGE)
        return disabled_comments.text


    def add_new_participant(self):
        WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable(PollPageLocators.ADD_NEW_PARTICIPANT)).click()

    def add_vote_ifneed(self):
        #double click
        element = self.driver.find_element(*PollPageLocators.DATE1)
        actions = ActionChains(self.driver)
        actions.double_click(element).perform()


    def add_vote_yes(self):
        self.driver.find_element(*PollPageLocators.DATE2).click()

    def add_vote_yes1(self):
        self.driver.find_element(*PollPageLocators.DATE1).click()

    def confirm_votes(self):
        self.driver.find_element(*PollPageLocators.ADD_VOTE_CONTINUE_BUTTON).click()


    def enter_participant_name(self, name):
        name_input = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located(PollPageLocators.NEW_PARTICIPANT_NAME)
        )
        name_input.send_keys(name)


    def enter_participant_email(self, email):
        email_input = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located(PollPageLocators.NEW_PARTICIPANT_EMAIL)
        )
        email_input.send_keys(email)


    def submit_participant_vote(self):
        self.driver.find_element(*PollPageLocators.NEW_PARTICIPANT_SUBMIT).click()

    def get_icon_counts(self):
        # Wait up to 15 seconds until the first <span> in the member icon becomes visible
        # This ensures that the elements are loaded before interacting with them
        WebDriverWait(self.driver, 15).until(
            EC.visibility_of_element_located(PollPageLocators.MEMBERS_ICON_SPAN)
        )
        # Retrieve all elements that represent icons with the number of members: all icons
        icons = self.driver.find_elements(*PollPageLocators.ICONS_NUMBER_OF_MEMBERS)
        # Locator used to find the <span> that contains the member count within each icon.
        span_locator = PollPageLocators.MEMBERS_ICON_SPAN
        # List comprehension: for each icon, find all matching <span> elements, take the last one - contains the count,
        # extract its text, and convert it to an integer
        return [int(icon.find_elements(*span_locator)[-1].text) for icon in icons]


    def change_participant(self):
        wait = WebDriverWait(self.driver, 10)
        #waiting for the DOTS_BUTTON element to be clickable
        dots_button = wait.until(EC.element_to_be_clickable(PollPageLocators.DOTS_BUTTON))
        #Find the "go up one level" item inside it and click
        button = dots_button.find_element(*PollPageLocators.GO_UP_ONE_LEVEL)
        button.click()

    def edit_votes(self):
        self.driver.find_element(*PollPageLocators.EDIT_VOTES_BUTTON).click()


    def edit_vote_oneclick(self):
        self.driver.find_element(*PollPageLocators.CHOOSE_VOTE_EDIT_VOTE_BUTTON).click()

    def edit_vote_doubleclick(self):
        element = self.driver.find_element(*PollPageLocators.CHOOSE_VOTE_EDIT_VOTE_BUTTON)
        actions = ActionChains(self.driver)
        actions.double_click(element).perform()

    def save_edit_votes(self):
        WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable(PollPageLocators.SAVE_EDIT_VOTES_BUTTON)).click()


    def get_icon_fill_color(self):
        #custom wait: find element icon, find fill and check if its empty
        def wait_for_fill(driver):
            try:
                el = driver.find_element(*PollPageLocators.COLOR_OF_VOTED_ICON)
                fill = el.get_attribute('fill')
                return fill and fill != ''
            except:
                return False

        WebDriverWait(self.driver, 15).until(wait_for_fill)
        el = self.driver.find_element(*PollPageLocators.COLOR_OF_VOTED_ICON)
        return el.get_attribute('fill')


    def get_icon_fill_color_yes(self):
        path_element = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located(PollPageLocators.COLOR_OF_YES_VOTE_ICON_LEGEND)
        )
        fill_coloryes = path_element.get_attribute('fill')
        return fill_coloryes

    def get_icon_fill_color_ifneedbe(self):
        path_element = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located(PollPageLocators.COLOR_OF_IFNEEDBE_VOTE_ICON_LEGEND))
        fill_colorifneedbe = path_element.get_attribute('fill')
        return fill_colorifneedbe

    def get_icon_fill_color_no(self):
        path_element = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located(PollPageLocators.COLOR_OF_NO_VOTE_ICON_LEGEND))
        fill_colorno= path_element.get_attribute('fill')
        return fill_colorno


    def get_number_of_votes(self):
        element = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located(PollPageLocators.NUMBER_OF_VOTES_INITIAL)
        )
        text = self.driver.execute_script("return arguments[0].textContent;", element).strip()
        if not text.isdigit():
            raise ValueError(f"Expected the number but received: '{text}'")
        return int(text)


    def delete_participant(self):
        self.driver.find_element(*PollPageLocators.DELETE_PARTICIPANT).click()


    def confirm_delete_participant(self, timeout=10):
        # Wait for the modal to appear
        modal = WebDriverWait(self.driver, timeout).until(
            EC.visibility_of_element_located(
                (PollPageLocators.MODAL_TO_DELETE_PARTICIPANT)))

        # Find thr delete button inside the modal
        delete_btn = modal.find_element(*PollPageLocators.DELETE_PARTICIPANT_MODAL)
        # Firstly check if its clickable, then click
        WebDriverWait(self.driver, timeout).until(
            EC.element_to_be_clickable(PollPageLocators.DELETE_PARTICIPANT_MODAL)
        )
        delete_btn.click()


    def get_noparticipant_label(self):
        no_participant_label = WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located(PollPageLocators.NO_PARTICIPANT_LABEL)
        )
        return no_participant_label.text


    def enter_comment_text(self, text):
        self.driver.find_element(*PollPageLocators.COMMENT_BUTTON).click()
        self.driver.find_element(*PollPageLocators.COMMENT_TEXT_INPUT).send_keys(text)

    def enter_comment_author(self,author):
        #scroll - comment at the page bottom
        self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        self.driver.find_element(*PollPageLocators.COMMENT_AUTHOR_NAME).send_keys(author)


    def add_comment(self, expected_author=None, expected_text=None, timeout=10):
        self.driver.find_element(*PollPageLocators.ADD_COMMENT_BUTTON).click()

        if expected_author and expected_text:
            WebDriverWait(self.driver, timeout).until(
                lambda driver: any(
                    expected_author in comment.text and expected_text in comment.text
                    for comment in driver.find_elements(*PollPageLocators.COMMENTS)
                )
            )

    def get_comment_author(self, timeout=5):
        author_elem = WebDriverWait(self.driver, timeout).until(
            EC.presence_of_element_located(PollPageLocators.COMMENT_AUTHOR)
        )
        return author_elem.text

    def get_comment_text(self, timeout=5):
        text_elem = WebDriverWait(self.driver, timeout).until(
            EC.presence_of_element_located(PollPageLocators.COMMENT_TEXT_ADDED)
        )
        return text_elem.text


    def get_comment_count(self):
        comments = self.driver.find_elements(*PollPageLocators.COMMENT_ELEMENTS)
        count = len(comments)
        return count

    def click_comment_ellipsis_by_you(self):
        try:
            #Wait for the element with ".." to be present
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located(PollPageLocators.COMMENTS)
            )
            # Find svg : dots button, and next ".." - go up one level
            button = self.driver.find_element(*PollPageLocators.DOTS_BUTTON).find_element(*PollPageLocators.GO_UP_ONE_LEVEL)
            # Scroll to the button
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", button)
            button.click()
            print("Threee dots button next to the comment clicked.")
        except Exception as e:
            raise Exception(f"Could not click the button: {str(e)}")


    def delete_comment(self):
        delete_menu_item = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable(PollPageLocators.DELETE_COMMENT_BUTTON)
        )
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", delete_menu_item)
        try:
            delete_menu_item.click()
        except Exception:
            self.driver.execute_script("arguments[0].click();", delete_menu_item)


    def wait_for_comment_count_to_increase(self, previous_count, timeout=5):
        WebDriverWait(self.driver, timeout).until(
            lambda driver: self.get_comment_count() > previous_count,
            message=f"Number of comments does not increase from {previous_count} in time of{timeout} seconds."
        )

    def wait_for_comment_count_to_decrease(self, previous_count, timeout=5):
        WebDriverWait(self.driver, timeout).until(
            lambda driver: self.get_comment_count() < previous_count,
            message=f"Number of comments does not decrease from {previous_count} in time of {timeout} seconds"
        )

    def manage_poll(self):
        WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable(PollPageLocators.MANAGE_BUTTON)).click()

    def pause_poll(self):
        WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable(PollPageLocators.PAUSE_BUTTON)).click()

    def resume_poll(self):
        WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable(PollPageLocators.RESUME_BUTTON)).click()

    def get_pause_label(self):
        label = WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located(PollPageLocators.RESUME_LABEL)
        )
        return label.text

    def get_live_label(self):
        label = WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located(PollPageLocators.ACTIVE_LABEL)
        )
        return label.text

    def delete_poll(self):
        WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable(PollPageLocators.MANAGE_BUTTON)).click()
        WebDriverWait(self.driver, 15).until(EC.element_to_be_clickable(PollPageLocators.DELETE_BUTTON)).click()
        self.driver.find_element(*PollPageLocators.CONFIRM_DELETE_BUTTON).click()