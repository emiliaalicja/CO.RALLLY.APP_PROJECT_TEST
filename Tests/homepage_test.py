from Tests.base_test import BaseTest
from Pages.home_page import HomePage

class PollTest(BaseTest):

    def setUp(self):
        super().setUp()
        self.home_page = HomePage(self.driver)

    def test_get_welcome_text(self):
        self.home_page.get_welcome_message()
        welcome_message = self.home_page.get_welcome_message()
        print(welcome_message)
        self.assertEqual(welcome_message, "Welcome", "Should receive home page and text 'Welcome'")