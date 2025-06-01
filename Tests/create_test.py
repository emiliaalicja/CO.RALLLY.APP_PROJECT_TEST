from Tests.base_tests import BaseTest
from Pages.home_page import HomePage
from ddt import ddt, data, unpack
from Test_data.data_utilis import DataReader
from Test_data.fake_data import (
    random_meeting_name,
    random_location,
    random_description
)


@ddt
class CreateTest (BaseTest): #klasa dziedziczy po BaseTest: inicjalizacja przeglądarki itp.
    def setUp(self):
        #Wywołanie setUp z klasy bazowej
        super().setUp()
        #Dodatkowy warunek wstępny - wejście na stronę logowania??
        self.home_page = HomePage(self.driver)  # Stworzenie obiektu HomePage
        #wykonują akcje klikniecia, która przenosi mnie na stronę tworzenia ankiety
        self.create_page = self.home_page.click_create_group_poll()



# jest okej
    def test_valid_create(self):
        name = random_meeting_name()
        location = random_location()
        description = random_description()

        self.create_page.enter_title(name)
        self.create_page.enter_location(location)
        self.create_page.enter_description(description)
        self.create_page.enter_time()
        self.create_page.click_create_poll()
        #copy link from modal
        self.create_page.save_modal_link_to_file()
        #zamknięcie modala przejście na stronę ankiety
        self.poll_page = self.create_page.close_modal_and_go_to_poll_page()
        #UWAGA: DODANIE POLL_WAS_CREATED ŻEBY MI SIE USUNELA ANKIETA, MOZE POTEM DO OPTYMALIZACJI
        #DO SPRAWDZENIA RÓWNIEŻ CZY POWINNA BYĆ TUTAJ OPCJA SELF.POLL_PAGE I CZY TO JEST POPRAWNE
        self.poll_page.poll_was_created = True
        #sprawdzenie tytułu ankiety
        result_title = self.poll_page.get_page_title()
        self.assertEqual(result_title, name, "Tytuł spotkania nie jest zgodny z wprowadzonym w formularzu.")
        print(f"Tytuł spotkania: {result_title} - test passed!")

        #sprawdzenie opisu ankiety
        result_description = self.poll_page.get_page_description()

        self.assertEqual(result_description, description,  "Tytuł spotkania nie jest zgodny z wprowadzonym w formularzu.")
        print(f"Description: {result_description} - test passed!")


        result_localization = self.poll_page.get_page_localization()
        self.assertEqual(result_localization, location, "Localization is not equal to enter")
        print(f"Localization: {result_localization} - test passed!")


        #sprawdzenie 3 opcji dat
        options_text = self.poll_page.get_page_dates_options()
        self.assertEqual(options_text, "3 options", f"Expected '3 options' but got '{options_text}'")

        #comments - active
        active_comments = self.poll_page.get_page_active_comments()
        self.assertEqual(active_comments, "Leave a comment on this poll (visible to everyone)", "Unexpected message - comments")


    @data(*DataReader.get_csv_data("optional_attributes_for_poll.csv"))
    @unpack
    def test_valid_poll_optional_fields_combinations(self, title, location, description):

        self.create_page.enter_title(title)
        if location:
            self.create_page.enter_location(location)
            print(location)
        if description:
            self.create_page.enter_description(description)
        self.create_page.enter_time()
        self.create_page.click_create_poll()
        self.create_page.save_modal_link_to_file()
        self.poll_page = self.create_page.close_modal_and_go_to_poll_page()
        self.poll_page.poll_was_created = True
        result_title = self.poll_page.get_page_title()
        self.assertEqual(result_title, title,
                         "Tytuł spotkania nie jest zgodny z wprowadzonym w formularzu.")
        print(f"Tytuł spotkania: {result_title} - test passed!")



    def test_invalid_create_date(self): #działa
        name = random_meeting_name()

        self.create_page.enter_title(name)
        self.create_page.click_create_poll()
        error_text = self.create_page.get_error_date_message()
        self.assertEqual("You can't create a poll without any options. Add at least one option to continue.", error_text)


    def test_invalid_create_title(self):
        self.create_page.enter_title("")
        self.create_page.click_create_poll()
        error1_text = self.create_page.get_error_title_message()
        self.assertEqual("“Title” is required",
                          error1_text)

    def test_valid_create_without_comments(self):
        name = random_meeting_name()

        self.create_page.enter_title(name)
        self.create_page.enter_time()
        self.create_page.turn_off_comments()
        self.create_page.click_create_poll()
        self.create_page.save_modal_link_to_file()
        self.poll_page = self.create_page.close_modal_and_go_to_poll_page()
        self.poll_page.poll_was_created = True
        disabled_comments_message =self.poll_page.get_page_disabled_comments()
        self.assertEqual(disabled_comments_message, "Comments have been disabled", "Disabled comments message is not as expected")









