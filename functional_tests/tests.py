from django.test import LiveServerTestCase
from selenium.webdriver.common.keys import Keys
from selenium import webdriver
from selenium.common.exceptions import WebDriverException
import time

MAX_WAIT = 10


def wait_for(fn):
    start_time = time.time()
    while True:
        try:
            return fn()
        except (AssertionError, WebDriverException) as e:
            if time.time() - start_time > MAX_WAIT:
                raise e
            time.sleep(0.5)


class NewVisitorTest(LiveServerTestCase):

    def setUp(self):
        self.browser = webdriver.Firefox()

    def tearDown(self):
        self.browser.quit()

    def go_to_cv_page(self):
        self.browser.get(self.live_server_url + '/cv/')

    def test_can_view_cv_page(self):
        self.go_to_cv_page()
        self.assertIn('CV', self.browser.title)

        header_text = self.browser.find_element_by_tag_name('h1').text
        self.assertIn('CV', header_text)

    def test_can_edit_personal_details(self):
        self.go_to_cv_page()
        # personal details div
        personal_details = self.browser.find_element_by_id('id_personal_details').text
        self.assertIn('Personal Details', personal_details)

        edit_details = self.browser.find_element_by_id('id_edit_details')
        edit_details.click()

        # wait for new view
        wait_for(lambda: self.assertIn("Edit Personal Details", self.browser.find_element_by_tag_name('h2').text))

        edit_form = self.browser.find_element_by_tag_name('form')

        inputbox = edit_form.find_element_by_name('name')
        inputbox.send_keys('Ben Harper')

        inputbox = edit_form.find_element_by_name('dob')
        inputbox.clear()
        inputbox.send_keys('27/06/2000')

        inputbox = edit_form.find_element_by_name('email')
        inputbox.send_keys('blh898@student.bham.ac.uk')

        save = edit_form.find_element_by_tag_name('button')
        save.click()

        wait_for(lambda: self.assertIn("CV", self.browser.find_element_by_tag_name('h1').text))

        name = self.browser.find_element_by_id('name').text
        self.assertEqual(name, 'Name: Ben Harper')

        dob = self.browser.find_element_by_id('dob').text
        self.assertEqual(dob, 'D.O.B: 27 Jun 2000')

        email = self.browser.find_element_by_id('email').text
        self.assertEqual(email, 'Email: blh898@student.bham.ac.uk')

    def test_can_add_education(self):
        self.go_to_cv_page()
        # education div
        education = self.browser.find_element_by_id('id_education').text
        self.assertIn('Education', education)

        add_education = self.browser.find_element_by_id('id_add_education')
        add_education.click()

        wait_for(lambda: self.assertIn("New Education", self.browser.find_element_by_tag_name('h2').text))

        edit_form = self.browser.find_element_by_tag_name('form')

        inputbox = edit_form.find_element_by_name('institution')
        inputbox.send_keys('My School')

        inputbox = edit_form.find_element_by_name('grades')
        inputbox.send_keys('Maths - A')

        inputbox = edit_form.find_element_by_name('start_date')
        inputbox.clear()
        inputbox.send_keys('01/09/2016')

        inputbox = edit_form.find_element_by_name('end_date')
        inputbox.clear()
        inputbox.send_keys('01/07/2018')

        save = edit_form.find_element_by_tag_name('button')
        save.click()

        wait_for(lambda: self.assertIn("CV", self.browser.find_element_by_tag_name('h1').text))

        institution = self.browser.find_element_by_id('institution').text
        self.assertEqual(institution, 'My School')

        grades = self.browser.find_element_by_id('grades').text
        self.assertEqual(grades, 'Maths - A')

        start_date = self.browser.find_element_by_id('start_date').text
        self.assertEqual(start_date, 'Started: 1 Sep 2016')

        end_date = self.browser.find_element_by_id('end_date').text
        self.assertEqual(end_date, 'Left: 1 Jul 2018')
