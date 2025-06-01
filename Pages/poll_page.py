from Pages.base_page import BasePage
from Locators.poll_page_locators import PollPageLocators
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver import ActionChains #needed for double click
import time
from selenium.webdriver.common.keys import Keys #DO ZAZNACZENIA TEKSTU DO USUNIĘCIA
from selenium.common.exceptions import TimeoutException



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
        print(f"Opcje dat: {options.text}")
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
        #podwójne kliknięcie
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
        name_input.send_keys("Katarzyna")
        #self.driver.find_element(*PollPageLocators.NEW_PARTICIPANT_NAME).send_keys()

    def enter_participant_email(self, email):
        email_input = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located(PollPageLocators.NEW_PARTICIPANT_EMAIL)
        )
        email_input.send_keys("email@email.email")
        #self.driver.find_element(*PollPageLocators.NEW_PARTICIPANT_EMAIL).send_keys()

    def submit_participant_vote(self):
        self.driver.find_element(*PollPageLocators.NEW_PARTICIPANT_SUBMIT).click()

    def get_icon_counts(self):
        icons = self.driver.find_elements(*PollPageLocators.ICONS_NUMBER_OF_MEMBERS) #ELEMENTS BECAUSE LISTA
        span_locator = PollPageLocators.MEMBERS_ICON_SPAN
        return [int(icon.find_elements(*span_locator)[-1].text) for icon in icons]


    def change_participant(self):
        # Find svg, and next ".."
        button = self.driver.find_element(*PollPageLocators.DOTS_BUTTON).find_element(*PollPageLocators.GO_UP_ONE_LEVEL)

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
        #path_locator = (By.CSS_SELECTOR, "td.h-12 div.inline-flex svg path")

        path_element = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located(PollPageLocators.COLOR_OF_VOTED_ICON)
        )
        fill_color = path_element.get_attribute('fill')
        return fill_color

    def get_icon_fill_color_yes(self):
        #path_locator = (By.CSS_SELECTOR, "ul.flex.items-center li:nth-child(1) svg path")

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
        #path_locator = (By.CSS_SELECTOR, "ul.flex.items-center li:nth-child(3) svg path")

        path_element = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located(PollPageLocators.COLOR_OF_NO_VOTE_ICON_LEGEND))
        fill_colorno= path_element.get_attribute('fill')
        return fill_colorno

    def color_text(self, text, color_code):
        return f"\033[{color_code}m{text}\033[0m"



    def get_number_of_votes(self):
        element = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located(PollPageLocators.NUMBER_OF_VOTES_INITIAL)
        )
        text = self.driver.execute_script("return arguments[0].textContent;", element).strip()
        if not text.isdigit():
            raise ValueError(f"Oczekiwano liczby, ale otrzymano: '{text}'")
        return int(text)

    def get_initial_number_of_votes(self):
        return self.get_number_of_votes()

    def get_final_number_of_votes(self):
        return self.get_number_of_votes()


    def delete_participant(self):
        self.driver.find_element(*PollPageLocators.DELETE_PARTICIPANT).click()


    def confirm_delete_participant(self, timeout=10):
        # 1) Poczekaj na pojawienie się modalu
        modal = WebDriverWait(self.driver, timeout).until(
            EC.visibility_of_element_located(
                (PollPageLocators.MODAL_TO_DELETE_PARTICIPANT)))

        # 2) W modal znajdź przycisk "Delete"
        delete_btn = modal.find_element(*PollPageLocators.DELETE_PARTICIPANT_MODAL)
        # 3) Upewnij się, że jest klikalny, a potem kliknij
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
        #scroll bo nie widać
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


    # def get_all_comments(self):
    #     comments_elements = self.driver.find_elements(*PollPageLocators.COMMENTS)
    #     comments = []
    #     for elem in comments_elements:
    #         author = elem.find_element(*PollPageLocators.COMMENT_AUTHOR).text
    #         text = elem.find_element(*PollPageLocators.COMMENT_TEXT_INPUT).text
    #         comments.append({"author": author, "text": text})
    #     return comments

    def get_comment_count(self):
        comments = self.driver.find_elements(*PollPageLocators.COMMENT_ELEMENTS)
        count = len(comments)
        print(f"[INFO] Liczba widocznych komentarzy: {count}")
        return count

    def click_comment_ellipsis_by_you(self):

        try:
            # Poczekaj aż komentarz z trzema kropkami będzie widoczny
            comment = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located(PollPageLocators.COMMENTS)
            )

            # Find svg, and next ".."
            button = self.driver.find_element(*PollPageLocators.DOTS_BUTTON).find_element(*PollPageLocators.GO_UP_ONE_LEVEL)

            # svg = comment.find_element(*PollPageLocators.DOTS_BUTTON_COMMENTS)
            # button = svg.find_element(By.XPATH, "..")



            # Scroll do przycisku
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", button)

            # Kliknij przycisk
            button.click()

            print("✅ Kliknięto przycisk trzech kropek.")
        except Exception as e:
            raise Exception(f"❌ Nie udało się kliknąć przycisku: {str(e)}")



    def delete_comment(self):

        delete_menu_item = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable(PollPageLocators.DELETE_COMMENT_BUTTON)
        )

        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", delete_menu_item)
        time.sleep(0.3)

        try:
            delete_menu_item.click()
        except Exception:
            self.driver.execute_script("arguments[0].click();", delete_menu_item)



    def wait_for_comment_count_to_increase(self, previous_count, timeout=5):
        WebDriverWait(self.driver, timeout).until(
            lambda driver: self.get_comment_count() > previous_count,
            message=f"Liczba komentarzy nie wzrosła ponad {previous_count} w ciągu {timeout} sekund."
        )

    def wait_for_comment_count_to_decrease(self, previous_count, timeout=5):
        WebDriverWait(self.driver, timeout).until(
            lambda driver: self.get_comment_count() < previous_count,
            message=f"Liczba komentarzy nie zmieniła się poniżej {previous_count} w ciągu {timeout} sekund."
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





