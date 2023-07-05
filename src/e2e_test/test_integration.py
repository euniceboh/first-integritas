# Integration Testing on Deployed Web Apps

# Test routes
# Test redirect button in 404 page
# Test 2 example YAML docs
    # Test successful and unsuccessful
    # Test accordion item line number exists

import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


options = Options()
options.add_argument("--start-maximized")
options.add_argument("--window-size=2560,1440")
options.add_argument("--headless")

chromeDriverPath = "/e2e_test/chromedriver"
frontendURL = "https://cpfdevportal.azurewebsites.net"
frontend404URL = "https://cpfdevportal.azurewebsites.net/404"
backendURL = "https://cpfdevportal-node.azurewebsites.net"
backend404URL = "https://cpfdevportal-node.azurewebsites.net/404"

class TestRoute:
    def setup_method(self):
        try: # in pipeline
            self.driver = webdriver.Chrome(service=ChromeService(chromeDriverPath), options=options)
        except Exception: # local
            self.driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=options)

    def test_frontend_route(self):
        self.driver.get(frontendURL)
        try:
            title_element = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.TAG_NAME, "title"))
            )
        finally:
            title = self.driver.title
            assert title == "API Exchange Developer Portal"
    
    def test_frontend_catchall_route(self):
        self.driver.get(frontend404URL)
        try:
            title_element = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.TAG_NAME, "title"))
            )
        finally:
            title = self.driver.title
            assert title == "404 Not Found"
    
    def test_backend_route(self):
        self.driver.get(backendURL)
        try:
            title_element = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.TAG_NAME, "title"))
            )
        finally:
            title = self.driver.title
            assert title == "API Exchange Developer Portal Backend"

    def test_backend_catchall_route(self):
        self.driver.get(backend404URL)
        try:
            title_element = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.TAG_NAME, "title"))
            )
        finally:
            title = self.driver.title
            assert title == "404 Not Found"

    def teardown_method(self):
        self.driver.close()

# class TestRedirect:
#     def setup_method(self):
#         # self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
#         self.driver = webdriver.Chrome('/src/tests/chromedriver', options=options)
#         self.driver.get("https://cpfdevportal.azurewebsites.net/404")
    
#     def test_catchall_redirect_button(self):
#         try:
#             button = WebDriverWait(self.driver, 5).until(
#                 EC.visibility_of_element_located((By.CLASS_NAME, "block"))
#             )
#         finally:
#             button = self.driver.find_element(By.CLASS_NAME, "block").click()
#         try:
#             route_identifier = WebDriverWait(self.driver, 5).until(
#                 EC.presence_of_element_located((By.CLASS_NAME, "route-identifier"))
#             )
#         finally:
#             route_identifier = self.driver.find_element(By.CLASS_NAME, "route-identifier").text
#             assert route_identifier == "CPF OAS Validator Tool"
    
#     def teardown_method(self):
#         self.driver.close()

# class TestOASValidator:
#     def setup_method(self):
#         try:
#             with open("src/template1.yaml", "r") as f:
#                 self.template1 = f.read()
#             with open("src/template2.yaml", "r") as f:
#                 self.template2 = f.read()
#         except (FileNotFoundError):
#             with open("../template1.yaml", "r") as f:
#                 self.template1 = f.read()
#             with open("../template2.yaml", "r") as f:
#                 self.template2 = f.read()
#         # self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
#         self.driver = webdriver.Chrome('/src/tests/chromedriver', options=options)
#         self.driver.get("https://cpfdevportal.azurewebsites.net/")
    
#     def test_checkOAS_noerror(self):
#         try:
#             # WARNING: If screen minimized or screen too small, ace editor might not appear and thus this test will fail
#             textarea = WebDriverWait(self.driver, 20).until(
#                 EC.visibility_of_element_located((By.CLASS_NAME, "ace_content"))
#             )
#         finally:
#             self.driver.execute_script(f"editor.setValue(`{self.template1}`)")
#             textareaContent = self.driver.execute_script("editor.getValue()")
#             assert (textareaContent != "" or textareaContent != None) == True
#         button = self.driver.find_element(By.ID, "checkOASButton")
#         self.driver.execute_script("arguments[0].scrollIntoView(false);", button)
#         button.click()
#         try:
#             modal = WebDriverWait(self.driver, 5).until(
#                 EC.visibility_of_element_located((By.ID, "oasSuccessBody"))
#             )
#         finally:
#             # Two ways to check if an element exists 
#                 # (1) Use find_elements to find all appearances of the element then compare with 0; will be more costly
#                 # (2) Use try except finally statements; more code and more confusing if test case not simple
#             # tick = self.driver.find_elements(By.TAG_NAME, "svg")
#             # assert len(tick) != 0
#             assert True
    
#     def test_checkOAS_error(self):
#         try:
#             # WARNING: If screen minimized or screen too small, 
#             # ace editor might not appear and thus this test will fail; fixed with fixed window size
#             textarea = WebDriverWait(self.driver, 5).until(
#                 EC.visibility_of_element_located((By.CLASS_NAME, "ace_content"))
#             )
#         finally:
#             self.driver.execute_script(f"editor.setValue(`{self.template2}`)")
#             textareaContent = self.driver.execute_script("editor.getValue()")
#             assert (textareaContent != "" or textareaContent != None) == True
#         button = self.driver.find_element(By.ID, "checkOASButton").click()
#         try:
#             modal = WebDriverWait(self.driver, 20).until(
#                 EC.visibility_of_element_located((By.ID, "oasErrorsBody"))
#             )
#         finally:
#             assert True

#     def teardown_method(self):
#             self.driver.close()

# Manual Testing or external libraries can support
# class TestFileUploadSave:
#     def setup_method(self):
#         # self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
#         self.driver = webdriver.Chrome('/src/tests/chromedriver', options=options)
#         self.driver.get("https://cpfdevportal.azurewebsites.net/")

#     def test_uploadFile(self):
#         try:
#             buttonChooseFile = WebDriverWait(self.driver, 5).until(
#                 EC.visibility_of_element_located((By.ID, "fileUpload"))
#             )
#             buttonChooseFile.send_keys(os.getcwd()+"../template1.yaml")
#         finally:
#             self.driver.find_element(By.ID, "fileUploadButton").click()
#             textareaContent = self.driver.execute_script("editor.getValue()")
#             assert (textareaContent != "" or textareaContent != None) == True
            
    # def test_saveFile(self):
    #     try:
    #         buttonChooseFile = WebDriverWait(self.driver, 5).until(
    #             EC.visibility_of_element_located((By.ID, "fileUpload"))
    #         )
    #         buttonChooseFile.send_keys("C:/Users/danie/Documents/CPF Validator Tool/CPF-Dev-Portal/src/template1.yaml")
    #     finally:
    #         self.driver.find_element(By.ID, "fileUploadButton").click()
    #         buttonSaveFile = self.driver.find_element(By.ID, "savefile").click()
    #         textareaContent = self.driver.execute_script("editor.getValue()")
    #         assert (textareaContent != "" or textareaContent != None) == True

    # def teardown_method(self):
    #     self.driver.close()

# Dictionary Input

