
from Tests.base_tests import BaseTest
from Pages.home_page import HomePage


from time import sleep



import logging
logging.basicConfig(level=logging.INFO)

from faker import Faker



class PollTest(BaseTest):


    def setUp(self):
        super().setUp()
        print("Tworzę ankietę przed testem...")
        self.home_page = HomePage(self.driver)
        self.create_page = self.home_page.click_create_group_poll()
        self.create_page.enter_title("Spotkanie")
        self.create_page.enter_location("Warszawa")
        self.create_page.enter_time()
        self.create_page.click_create_poll()
        self.create_page.save_modal_link_to_file()
        self.poll_page = self.create_page.close_modal_and_go_to_poll_page()
        self.poll_page.poll_was_created = True
        print("Ankieta została stworzona")





    def test_add_vote(self):
        #tutaj użyć fakera do generowania danych takich jak imię oraz email
        self.poll_page.add_new_participant()
        before = self.poll_page.get_icon_counts()

        self.poll_page.add_vote_ifneed()
        self.poll_page.add_vote_yes()
        self.poll_page.confirm_votes()
        self.poll_page.enter_participant_name("Katarzyna")
        self.poll_page.enter_participant_email("blabla@notifiactions.pl")
        self.poll_page.submit_participant_vote()
        sleep(5)

        after = self.poll_page.get_icon_counts()

        assert after[0] == before[0] + 1
        assert after[1] == before[1] + 1
        assert after[2] == before[2]  # bez zmian

    def test_edit_vote_member_no_toyes(self):
        #one click
        self.poll_page.add_new_participant()

        self.poll_page.confirm_votes()
        self.poll_page.enter_participant_name("Katarzyna")
        self.poll_page.submit_participant_vote()
        sleep(2)

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
        self.poll_page.add_new_participant()

        self.poll_page.confirm_votes()
        self.poll_page.enter_participant_name("Katarzyna")
        self.poll_page.submit_participant_vote()
        sleep(2)

        icon_color_before = self.poll_page.get_icon_fill_color()
        print(icon_color_before)
        expected_color_before = self.poll_page.get_icon_fill_color_no()

        self.poll_page.change_participant()
        self.poll_page.edit_votes()
        self.poll_page.edit_vote_doubleclick()
        self.poll_page.save_edit_votes()
        sleep(5)

        icon_color_after = self.poll_page.get_icon_fill_color()
        expected_color_after = self.poll_page.get_icon_fill_color_ifneedbe()

        assert icon_color_before == expected_color_before, f"Oczekiwano koloru przed zmianą: {expected_color_before}, a było: {icon_color_before}"
        assert icon_color_after == expected_color_after, f"Oczekiwano koloru po zmianie: {expected_color_after}, a było: {icon_color_after}"

        print("Test przebiegł pomyślnie: kolorprzedi po zmianie są zgodne z oczekiwaniami.")


    def test_edit_vote_member_maybetoyes(self):
        #double click
        self.poll_page.add_new_participant()
        self.poll_page.add_vote_ifneed()
        self.poll_page.confirm_votes()
        self.poll_page.enter_participant_name("Katarzyna")
        self.poll_page.submit_participant_vote()
        sleep(5)


        icon_color_before = self.poll_page.get_icon_fill_color()
        print(icon_color_before)
        expected_color_before = self.poll_page.get_icon_fill_color_ifneedbe()


        self.poll_page.change_participant()
        self.poll_page.edit_votes()
        #sleep(2)
        self.poll_page.edit_vote_doubleclick()
        self.poll_page.save_edit_votes()
        sleep(2)
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
        self.poll_page.add_new_participant()
        self.poll_page.add_vote_ifneed()
        self.poll_page.confirm_votes()
        self.poll_page.enter_participant_name("Katarzyna")
        self.poll_page.submit_participant_vote()
        sleep(2)

        icon_color_before = self.poll_page.get_icon_fill_color()
        print(icon_color_before)
        expected_color_before = self.poll_page.get_icon_fill_color_ifneedbe()



        self.poll_page.change_participant()
        self.poll_page.edit_votes()
        self.poll_page.edit_vote_oneclick()
        self.poll_page.save_edit_votes()

        sleep(2)

        icon_color_after = self.poll_page.get_icon_fill_color()
        expected_color_after = self.poll_page.get_icon_fill_color_no()

        assert icon_color_before == expected_color_before, f"Oczekiwano koloru przed zmianą: {expected_color_before}, a było: {icon_color_before}"
        assert icon_color_after == expected_color_after, f"Oczekiwano koloru po zmianie: {expected_color_after}, a było: {icon_color_after}"

        print("Test przebiegł pomyślnie: kolorprzedi po zmianie są zgodne z oczekiwaniami.")

    def test_edit_vote_member_yestono(self):
        #double click
        self.poll_page.add_new_participant()
        self.poll_page.add_vote_yes1()
        self.poll_page.confirm_votes()
        self.poll_page.enter_participant_name("Katarzyna")
        self.poll_page.submit_participant_vote()
        sleep(1)


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
        self.poll_page.add_new_participant()
        self.poll_page.add_vote_yes1()
        self.poll_page.confirm_votes()
        self.poll_page.enter_participant_name("Katarzyna")
        self.poll_page.submit_participant_vote()
        sleep(1)

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
        self.poll_page.add_new_participant()
        self.poll_page.confirm_votes()
        self.poll_page.enter_participant_name("Katarzyna")
        self.poll_page.submit_participant_vote()
        sleep(5)
        self.poll_page.change_participant()
        self.poll_page.delete_participant()
        self.poll_page.confirm_delete_participant()
        #asercja no participant
        label_text = self.poll_page.get_noparticipant_label()
        print(f"label_text: {repr(label_text)}")
        assert label_text == "No participants", f"Oczekiwano tekstu 'No participants', ale otrzymano: '{label_text}'"

    def test_add_new_comment(self):
        previous_count = self.poll_page.get_comment_count()
        print(f"[INFO] Liczba komentarzy PRZED: {previous_count}")
        fake = Faker()
        random_author = fake.first_name()
        random_text = fake.sentence(nb_words=8)

        self.poll_page.enter_comment_text(random_text)
        self.poll_page.enter_comment_author(random_author)
        self.poll_page.add_comment()

        # Czekaj, aż liczba komentarzy wzrośnie, jak nie pojdzie to dodanie metodau
        self.poll_page.wait_for_comment_count_to_increase(previous_count)

        new_count = self.poll_page.get_comment_count()
        print(f"[INFO] Liczba komentarzy PO: {new_count}")
        self.assertEqual(new_count, previous_count + 1)
        print("[TEST] ✅ Dodanie komentarza zwiększyło licznik o 1")

        found_author = self.poll_page.get_comment_author()
        found_text = self.poll_page.get_comment_text()

        logging.info(f"[INFO] Oczekiwany autor: '{random_author}', znaleziony: '{found_author}'")
        logging.info(f"[INFO] Oczekiwana treść: '{random_text}', znaleziona: '{found_text}'")

        self.assertEqual(found_author, random_author)
        self.assertEqual(found_text, random_text)


    def test_delete_comment(self):


        previous_count = self.poll_page.get_comment_count()
        print(f"[INFO] Liczba komentarzy PRZED: {previous_count}")

        fake = Faker()
        random_author = fake.first_name()
        random_text = fake.sentence(nb_words=10)

        self.poll_page.enter_comment_text(random_text)
        self.poll_page.enter_comment_author(random_author)
        self.poll_page.add_comment()

        # Czekaj aż liczba komentarzy będzie większa niż wcześniej
        self.poll_page.wait_for_comment_count_to_increase(previous_count)

        new_count = self.poll_page.get_comment_count()
        print(f"[INFO] Liczba komentarzy PO dodaniu: {new_count}")

        assert new_count == previous_count + 1, f"Liczba komentarzy powinna wzrosnąć o 1, ale jest {new_count}"

        self.poll_page.click_comment_ellipsis_by_you()
        self.poll_page.delete_comment()

        # Czekaj aż liczba komentarzy wróci do poprzedniej wartości
        self.poll_page.wait_for_comment_count_to_decrease(new_count)

        final_count = self.poll_page.get_comment_count()
        print(f"[INFO] Liczba komentarzy PO usunięciu: {final_count}")

        assert final_count == previous_count, f"Liczba komentarzy po usunięciu powinna być {previous_count}, ale jest {final_count}"


    def test_pause(self):
        self.poll_page.manage_poll()
        self.poll_page.pause_poll()

        label_text = self.poll_page.get_pause_label()
        assert label_text == "Paused", f"Oczekiwano tekstu 'Pause', ale otrzymano: '{label_text}'"

    def test_resume_poll(self):
        self.poll_page.manage_poll()
        self.poll_page.pause_poll()

        self.poll_page.manage_poll()
        self.poll_page.resume_poll()

        label_text = self.poll_page.get_live_label()
        assert label_text == "Live", f"Oczekiwano tekstu 'Live', ale otrzymano: '{label_text}"





    def test_delete_poll(self): #DO POPRAWY
        self.poll_page.delete_poll()
        self.poll_page.poll_was_created = False

        #Go to home page
        self.home_page.get_welcome_message()
        welcome_message = self.home_page.get_welcome_message()
        print(welcome_message)

        self.assertEqual(welcome_message, "Welcome",
                         "Deleted alert not as expected")

        #Adding new page - chyba nie trzeba zobaczymy czy będzie dalej to działać
        # self.delete_page = DeletePage(self.driver)
        # # sleep(6)
        # #
        # # #Download the alert
        # deleted_poll_message = self.delete_page.get_delete_poll_message()
        # print(deleted_poll_message)
        # #
        # self.assertEqual(deleted_poll_message, "Deleted poll",
        #                   "Deleted alert not as expected")



