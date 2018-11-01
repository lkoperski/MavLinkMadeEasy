from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select

class UITests(StaticLiveServerTestCase):
    '''
    @UITests contain all of the classes that relate to performing actions on UI elements (i.e. buttons)
    param: StaticLiveServerTestCase allows for automated testing
    at execution time by launching a server in the background &
    shuts it down on teardown
    '''

    @classmethod
    def setUpClass(cls):
        cls.selenium = WebDriver()
        cls.selenium.implicitly_wait(10)

    @classmethod
    def tearDownClass(cls):
        cls.selenium.quit()

    def test_createuser_form(self):
        selenium = self.selenium
        selenium.get('http://127.0.0.1:8000/landing/createuser/')
        self.selenium.find_element_by_name("e-email").send_keys("test@test.com")
        Select(self.selenium.find_element_by_name('d-degree')).select_by_value("Bachelor of Science")
        Select(self.selenium.find_element_by_name('d-major')).select_by_value("Computer Science")
        self.selenium.find_element_by_name("submit").click()
        self.assertIn("MavLink", selenium.title)

    def test_selectcourses_form(self):
        selenium = self.selenium
        selenium.get('http://127.0.0.1:8000/landing/selectcourses/1')
        self.selenium.find_element_by_name("submit").click()
        self.assertIn("MavLink", selenium.title)

    def test_addclasses_form(self):
        selenium = self.selenium
        selenium.get('http://127.0.0.1:8000/landing/schedule/1')
        self.selenium.find_element_by_name("updateCourses").click()
        self.assertIn("MavLink", selenium.title)

    # this UI test is for a link from schedule to have the user change major...
    # right now, there isn't enough functionality to state the the user should be
    # updated (as opposed to creating a new one) so this test doesn't make sense to
    # write yet, although it would be helpful eventually :)
    #def test_changemajor_form(self):
        #selenium = self.selenium
        #selenium.get('http://127.0.0.1:8000/landing/schedule/')
        #self.selenium.find_element_by_name("changemajor").click()
        #assert 'Landing Page' in selenium.page_source