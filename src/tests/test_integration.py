import pytest
import unittest
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from src import app as flask_app

# class TestRoute:
#     def setup_method(self):
#         self.driver = webdriver.Chrome()

#     def test_search_in_python_org(self):
#         driver = self.driver
#         driver.get("http://www.python.org")
#         assert driver.title == "Welcome to Python.org"
#         elem = driver.find_element(By.NAME, "q")
#         elem.send_keys("pycon")
#         elem.send_keys(Keys.RETURN)
#         assert driver.page_source != "No results found"


#     def tearDown(self):
#         self.driver.close()

