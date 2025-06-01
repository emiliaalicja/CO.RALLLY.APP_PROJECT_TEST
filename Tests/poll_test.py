from Tests.base_tests import BaseTest
from Pages.home_page import HomePage
from time import sleep
import logging
logging.basicConfig(level=logging.INFO)
from faker import Faker
from Test_data.fake_data import (
    random_meeting_name,
    random_location,
    random_participant,
    random_email,
    random_comment_author,
    random_description
)



class PollTest(BaseTest):


    def setUp(self):
        super().setUp()
        title = random_meeting_name()
        location = random_location()
        self.home_page = HomePage(self.driver)
        self.create_page = self.home_page.click_create_group_poll()
        self.create_page.enter_title(title)
        self.create_page.enter_location(location)
        self.create_page.enter_time()
        self.create_page.click_create_poll()
        self.create_page.save_modal_link_to_file()
        self.poll_page = self.create_page.close_modal_and_go_to_poll_page()
        self.poll_page.poll_was_created = True
        print("Poll is created")


    def test_add_vote(self):
        member = random_participant()
        email = random_email()
        self.poll_page.add_new_participant()
        before = self.poll_page.get_icon_counts()
        self.poll_page.add_vote_ifneed()
        self.poll_page.add_vote_yes()
        self.poll_page.confirm_votes()
        self.poll_page.enter_participant_name(member)
        self.poll_page.enter_participant_email(email)
        self.poll_page.submit_participant_vote()

        after = self.poll_page.get_icon_counts()

        assert after[0] == before[0] + 1
        assert after[1] == before[1] + 1
        assert after[2] == before[2]  # bez zmian

    def test_edit_vote_member_no_toyes(self):
        #one click
        member = random_participant()
        self.poll_page.add_new_participant()
        self.poll_page.confirm_votes()
        self.poll_page.enter_participant_name(member)
        self.poll_page.submit_participant_vote()


        icon_color_before = self.poll_page.get_icon_fill_color()
        print(icon_color_before)
        expected_color_before = self.poll_page.get_icon_fill_color_no()

        self.poll_page.change_participant()
        self.poll_page.edit_votes()
        self.poll_page.edit_vote_oneclick()
        self.poll_page.save_edit_votes()

        icon_color_after = self.poll_page.get_icon_fill_color()
        expected_color_after = self.poll_page.get_icon_fill_color_yes()

        assert icon_color_before == expected_color_before, f"Oczekiwano koloru przed zmianą: {expected_color_before}, a było: {icon_color_before}"
        assert icon_color_after == expected_color_after, f"Oczekiwano koloru po zmianie: {expected_color_after}, a było: {icon_color_after}"

        print("Test przebiegł pomyślnie: kolorprzedi po zmianie są zgodne z oczekiwaniami.")

    def test_edit_vote_member_no_tomaybe(self):
        #double click
        member = random_participant()
        self.poll_page.add_new_participant()
        self.poll_page.confirm_votes()
        self.poll_page.enter_participant_name(member)
        self.poll_page.submit_participant_vote()
        #sleep(1)

        icon_color_before = self.poll_page.get_icon_fill_color()
        print(icon_color_before)
        expected_color_before = self.poll_page.get_icon_fill_color_no()

        self.poll_page.change_participant()
        self.poll_page.edit_votes()
        self.poll_page.edit_vote_doubleclick()
        self.poll_page.save_edit_votes()


        icon_color_after = self.poll_page.get_icon_fill_color()
        print(icon_color_after)
        expected_color_after = self.poll_page.get_icon_fill_color_ifneedbe()

        assert icon_color_before == expected_color_before, f"Oczekiwano koloru przed zmianą: {expected_color_before}, a było: {icon_color_before}"
        assert icon_color_after == expected_color_after, f"Oczekiwano koloru po zmianie: {expected_color_after}, a było: {icon_color_after}"

        print("Test przebiegł pomyślnie: kolorprzedi po zmianie są zgodne z oczekiwaniami.")


    def test_edit_vote_member_maybetoyes(self):
        #double click
        member = random_participant()
        self.poll_page.add_new_participant()
        self.poll_page.add_vote_ifneed()
        self.poll_page.confirm_votes()
        self.poll_page.enter_participant_name(member)
        self.poll_page.submit_participant_vote()

        icon_color_before = self.poll_page.get_icon_fill_color()
        print(icon_color_before)
        expected_color_before = self.poll_page.get_icon_fill_color_ifneedbe()


        self.poll_page.change_participant()
        self.poll_page.edit_votes()
        #sleep(2)
        self.poll_page.edit_vote_doubleclick()
        self.poll_page.save_edit_votes()

        icon_color_after = self.poll_page.get_icon_fill_color()
        expected_color_after =  self.poll_page.get_icon_fill_color_yes()

        # Kolorowanie tekstu w terminalu (zielony=32, czerwony=31)
        assert icon_color_before == expected_color_before, (
            f"Oczekiwano koloru ikonki przed zmianą: {self.poll_page.color_text(expected_color_before, 32)}, "
            f"ale było: {self.poll_page.color_text(icon_color_before, 31)}"
        )
        assert icon_color_after == expected_color_after, (
            f"Oczekiwano koloru ikonki po zmianie: {self.poll_page.color_text(expected_color_after, 32)}, "
            f"ale było: {self.poll_page.color_text(icon_color_after, 31)}"
        )


        print(self.poll_page.color_text("Test przebiegł pomyślnie: kolory ikonek przed i po zmianie są zgodne z oczekiwaniami.", 32))


    def test_edit_vote_member_maybetono(self):
        #oneclick
        member = random_participant()
        self.poll_page.add_new_participant()
        self.poll_page.add_vote_ifneed()
        self.poll_page.confirm_votes()
        self.poll_page.enter_participant_name(member)
        self.poll_page.submit_participant_vote()
        #sleep(2)

        icon_color_before = self.poll_page.get_icon_fill_color()
        print(icon_color_before)
        expected_color_before = self.poll_page.get_icon_fill_color_ifneedbe()



        self.poll_page.change_participant()
        self.poll_page.edit_votes()
        self.poll_page.edit_vote_oneclick()
        self.poll_page.save_edit_votes()

        #sleep(2)

        icon_color_after = self.poll_page.get_icon_fill_color()
        expected_color_after = self.poll_page.get_icon_fill_color_no()

        assert icon_color_before == expected_color_before, f"Oczekiwano koloru przed zmianą: {expected_color_before}, a było: {icon_color_before}"
        assert icon_color_after == expected_color_after, f"Oczekiwano koloru po zmianie: {expected_color_after}, a było: {icon_color_after}"

        print("Test przebiegł pomyślnie: kolorprzedi po zmianie są zgodne z oczekiwaniami.")

    def test_edit_vote_member_yestono(self):
        #double click
        member = random_participant()
        self.poll_page.add_new_participant()
        self.poll_page.add_vote_yes1()
        self.poll_page.confirm_votes()
        self.poll_page.enter_participant_name(member)
        self.poll_page.submit_participant_vote()

        icon_color_before = self.poll_page.get_icon_fill_color()
        print(icon_color_before)
        expected_color_before = self.poll_page.get_icon_fill_color_yes()

        self.poll_page.change_participant()
        self.poll_page.edit_votes()
        self.poll_page.edit_vote_doubleclick()
        self.poll_page.save_edit_votes()

        icon_color_after = self.poll_page.get_icon_fill_color()
        expected_color_after = self.poll_page.get_icon_fill_color_no()

        assert icon_color_before == expected_color_before, f"Oczekiwano koloru przed zmianą: {expected_color_before}, a było: {icon_color_before}"
        assert icon_color_after == expected_color_after, f"Oczekiwano koloru po zmianie: {expected_color_after}, a było: {icon_color_after}"

        print("Test przebiegł pomyślnie: kolorprzedi po zmianie są zgodne z oczekiwaniami.")


    def test_edit_vote_member_yestomaybe(self):
        #oneclick
        member = random_participant()
        self.poll_page.add_new_participant()
        self.poll_page.add_vote_yes1()
        self.poll_page.confirm_votes()
        self.poll_page.enter_participant_name(member)
        self.poll_page.submit_participant_vote()

        icon_color_before = self.poll_page.get_icon_fill_color()
        print(icon_color_before)
        expected_color_before = self.poll_page.get_icon_fill_color_yes()

        self.poll_page.change_participant()
        self.poll_page.edit_votes()
        self.poll_page.edit_vote_oneclick()
        self.poll_page.save_edit_votes()

        icon_color_after = self.poll_page.get_icon_fill_color()
        expected_color_after = self.poll_page.get_icon_fill_color_ifneedbe()

        assert icon_color_before == expected_color_before, f"Oczekiwano koloru przed zmianą: {expected_color_before}, a było: {icon_color_before}"
        assert icon_color_after == expected_color_after, f"Oczekiwano koloru po zmianie: {expected_color_after}, a było: {icon_color_after}"

        print("Test przebiegł pomyślnie: kolorprzedi po zmianie są zgodne z oczekiwaniami.")



    def test_delete_member(self):
        member = random_participant()
        self.poll_page.add_new_participant()
        self.poll_page.confirm_votes()
        self.poll_page.enter_participant_name(member)
        self.poll_page.submit_participant_vote()
        #sleep(0.5)
        self.poll_page.change_participant()
        self.poll_page.delete_participant()
        self.poll_page.confirm_delete_participant()
        #asercja no participant
        label_text = self.poll_page.get_noparticipant_label()
        print(f"label_text: {repr(label_text)}")
        assert label_text == "No participants", f"Expected label 'No participants', but received: '{label_text}'"

    def test_add_new_comment(self):
        previous_count = self.poll_page.get_comment_count()
        author = random_comment_author()
        description = random_description()
        self.poll_page.enter_comment_text(description)
        self.poll_page.enter_comment_author(author)
        self.poll_page.add_comment()
        #Wait for comment increase
        self.poll_page.wait_for_comment_count_to_increase(previous_count)
        new_count = self.poll_page.get_comment_count()
        self.assertEqual(new_count, previous_count + 1, "One comment should be added")
        found_author = self.poll_page.get_comment_author()
        found_text = self.poll_page.get_comment_text()
        logging.info(f"[INFO] Expected author: '{author}', founded: '{found_author}'")
        logging.info(f"[INFO] Expected description: '{description}', founded: '{found_text}'")
        self.assertEqual(found_author, author, f"The actual author is {found_author}, but expected is {author}")
        self.assertEqual(found_text, description, f"The actual description is {found_text}. but expected is {description}")


    def test_delete_comment(self):
        previous_count = self.poll_page.get_comment_count()
        author_comment = random_comment_author()
        description_comment = random_description()

        self.poll_page.enter_comment_text(description_comment)
        self.poll_page.enter_comment_author(author_comment)

        self.poll_page.add_comment()

        #Wait for comments to increase
        self.poll_page.wait_for_comment_count_to_increase(previous_count)

        new_count = self.poll_page.get_comment_count()
        assert new_count == previous_count + 1, f"Number of comments should increase by 1, actual value is {new_count}"

        self.poll_page.click_comment_ellipsis_by_you()
        self.poll_page.delete_comment()

        #Wait for number of comments to decrease
        self.poll_page.wait_for_comment_count_to_decrease(new_count)

        final_count = self.poll_page.get_comment_count()
        assert final_count == previous_count, f"Number of comments should be {previous_count}, abut the actual number is{final_count}"


    def test_pause(self):
        self.poll_page.manage_poll()
        self.poll_page.pause_poll()
        label_text = self.poll_page.get_pause_label()
        assert label_text == "Paused", f"Should receive label 'Pause', but received: '{label_text}'"

    def test_resume_poll(self):
        self.poll_page.manage_poll()
        self.poll_page.pause_poll()
        self.poll_page.manage_poll()
        self.poll_page.resume_poll()
        label_text = self.poll_page.get_live_label()
        assert label_text == "Live", f"Should receive label 'Live', but received: '{label_text}"


    def test_delete_poll(self):
        self.poll_page.delete_poll()
        self.poll_page.poll_was_created = False

        #Go to home page
        self.home_page.get_welcome_message()
        welcome_message = self.home_page.get_welcome_message()
        print(welcome_message)

        self.assertEqual(welcome_message, "Welcome","Should receive home page and text 'Welcome'")


