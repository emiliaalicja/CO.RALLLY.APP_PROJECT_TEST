from Tests.base_test import BaseTest
from Pages.home_page import HomePage
from ddt import ddt, data, unpack
from Test_data.data_utilis import DataReader
from Test_data.fake_data import (
    random_meeting_name,
    random_location,
    random_description
)


@ddt
class CreateTest(BaseTest):  # Inherits from BaseTest
    def setUp(self):
        # Calling setUp from the base class
        super().setUp()
        # Additional prerequisite - entering the login page
        self.home_page = HomePage(self.driver)  # Creating a HomePage object
        # Perform a click action that takes me to the survey creation page from home page
        self.create_page = self.home_page.click_create_group_poll()

    def test_valid_create(self):
        name = random_meeting_name()
        location = random_location()
        description = random_description()
        self.create_page.enter_title(name)
        self.create_page.enter_location(location)
        self.create_page.enter_description(description)
        self.create_page.enter_time()
        self.create_page.click_create_poll()
        # copy link from modal
        self.create_page.save_modal_link_to_file()
        # Closing the modal going to the survey page
        self.poll_page = self.create_page.close_modal_and_go_to_poll_page()
        # condition required to delete surveys after the test
        self.poll_page.poll_was_created = True
        # Check the survey title
        result_title = self.poll_page.get_page_title()
        self.assertEqual(result_title, name, "The meeting title does not match the one entered in the form.")
        print(f"Tytuł spotkania: {result_title} - test passed!")

        # Check the survey description
        result_description = self.poll_page.get_page_description()
        self.assertEqual(result_description, description,
                         "The meeting description does not match the one entered in the form.")
        print(f"Description: {result_description} - test passed!")

        # Check the survey location
        result_localization = self.poll_page.get_page_localization()
        self.assertEqual(result_localization, location,
                         "The meeting location does not match the one entered in the form.")
        print(f"Localization: {result_localization} - test passed!")

        # Check dates options
        options_text = self.poll_page.get_page_dates_options()
        self.assertEqual(options_text, "3 options", f"Expected '3 options' but got '{options_text}'")

        # comments - active
        active_comments = self.poll_page.get_page_active_comments()
        self.assertEqual(active_comments, "Leave a comment on this poll (visible to everyone)",
                         "Unexpected message - comments")

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
                         "The meeting title does not match the one entered in the form.")
        print(f"Meeting title: {result_title} - test passed!")

    def test_invalid_create_date(self):
        name = random_meeting_name()
        self.create_page.enter_title(name)
        self.create_page.click_create_poll()
        error_text = self.create_page.get_error_date_message()
        self.assertEqual("You can't create a poll without any options. Add at least one option to continue.",
                         error_text)

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
        disabled_comments_message = self.poll_page.get_page_disabled_comments()
        self.assertEqual(disabled_comments_message, "Comments have been disabled",
                         "Disabled comments message is not as expected")
