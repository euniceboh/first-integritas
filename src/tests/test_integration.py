# Integration Testing on Deployed App

import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class TestRoute:
    def setup_method(self):
        self.driver = webdriver.Chrome()
        
    def test_oasChecker_route(self):
        self.driver.get("http://127.0.0.1:80/")
        try:
            route_identifier = WebDriverWait(self.driver, 5).until(
                EC.presence_of_element_located((By.CLASS_NAME, "route-identifier"))
            )
        finally:
            route_identifier = self.driver.find_element(By.CLASS_NAME, "route-identifier").text
            assert route_identifier == "CPF OAS Validator Tool"
    
    def test_swaggeruipreview_route(self):
        self.driver.get("http://127.0.0.1:80/swaggeruipreview")
        try:
            route_identifier = WebDriverWait(self.driver, 5).until(
                EC.presence_of_element_located((By.CLASS_NAME, "route-identifier"))
            )
        finally:
            route_identifier = self.driver.find_element(By.CLASS_NAME, "route-identifier").text
            assert route_identifier == "OAS Preview Tool"
    
    def test_catchall_route(self):
        self.driver.get("http://127.0.0.1:80/404")
        try:
            route_identifier = WebDriverWait(self.driver, 5).until(
                    EC.presence_of_element_located((By.CLASS_NAME, "route-identifier"))
                )
        finally:
            route_identifier = self.driver.find_element(By.CLASS_NAME, "route-identifier").text
            assert route_identifier == "Not Found"

    def teardown_method(self):
        self.driver.close()

class TestRedirect:
    def setup_method(self):
        self.driver = webdriver.Chrome()
        self.driver.get("http://127.0.0.1:80/404")
    
    def test_catchall_redirect_button(self):
        try:
            button = WebDriverWait(self.driver, 5).until(
                EC.visibility_of_element_located((By.CLASS_NAME, "block"))
            )
        finally:
            button = self.driver.find_element(By.CLASS_NAME, "block").click()
        try:
            route_identifier = WebDriverWait(self.driver, 5).until(
                EC.presence_of_element_located((By.CLASS_NAME, "route-identifier"))
            )
        finally:
            route_identifier = self.driver.find_element(By.CLASS_NAME, "route-identifier").text
            assert route_identifier == "CPF OAS Validator Tool"

class TestOASValidator:
    def setup_method(self):
        with open("../template1.yaml", "r") as f:
            self.template1 = f.read()
        with open("../template2.yaml", "r") as f:
            self.template2 = f.read()
        self.driver = webdriver.Chrome()
        self.driver.get("http://127.0.0.1:80/")
    
    def test_checkOAS_noerror(self):
        try:
            # WARNING: If screen minimized or screen too small, ace editor might not appear and thus this test will fail
            textarea = WebDriverWait(self.driver, 5).until(
                EC.visibility_of_element_located((By.CLASS_NAME, "ace_content"))
            )
        finally:
            self.driver.execute_script(f"editor.setValue(`{self.template1}`)")
            textareaContent = self.driver.execute_script("editor.getValue()")
            assert (textareaContent != "" or textareaContent != None) == True
        button = self.driver.find_element(By.ID, "checkOASButton").click()
        try:
            modal = WebDriverWait(self.driver, 20).until(
                EC.visibility_of_element_located((By.ID, "oasSuccessBody"))
            )
        finally:
            # Two ways to check if an element exists 
                # (1) Use find_elements to find all appearances of the element then compare with 0; will be more costly
                # (2) Use try except finally statements; more code and more confusing if test case not simple
            # tick = self.driver.find_elements(By.TAG_NAME, "svg")
            # assert len(tick) != 0
            assert True
    
    def test_checkOAS_error(self):
        try:
            # WARNING: If screen minimized or screen too small, ace editor might not appear and thus this test will fail
            textarea = WebDriverWait(self.driver, 5).until(
                EC.visibility_of_element_located((By.CLASS_NAME, "ace_content"))
            )
        finally:
            self.driver.execute_script(f"editor.setValue(`{self.template2}`)")
            textareaContent = self.driver.execute_script("editor.getValue()")
            assert (textareaContent != "" or textareaContent != None) == True
        button = self.driver.find_element(By.ID, "checkOASButton").click()
        try:
            modal = WebDriverWait(self.driver, 20).until(
                EC.visibility_of_element_located((By.ID, "oasErrorsBody"))
            )
        finally:
            assert True
    
    def test_uploadFile(self):
        pass

    def test_saveFile(self):
        pass

    def teardown_method(self):
        self.driver.close()

