# Integration and e2e Testing on Deployed Web Apps

# Test 2 example YAML docs
    # Test successful and unsuccessful
    # Test accordion item line number exists

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
# options.add_argument("--headless")

chromeDriverPath = "/e2e_test/chromedriver"
frontendURL = "https://cpfdevportal.azurewebsites.net"
frontend404URL = "https://cpfdevportal.azurewebsites.net/404"
backendURL = "https://cpfdevportal-node.azurewebsites.net"
backend404URL = "https://cpfdevportal-node.azurewebsites.net/404"

class TestRoutes:
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

class TestRedirect:
    def setup_method(self):
        try: # in pipeline
            self.driver = webdriver.Chrome(service=ChromeService(chromeDriverPath), options=options)
        except Exception: # local
            self.driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=options)
        self.driver.get(frontend404URL)
    
    def test_frontend_catchall_redirect_button(self):
        try:
            button = WebDriverWait(self.driver, 10).until(
                EC.visibility_of_element_located((By.CLASS_NAME, "block"))
            )
        finally:
            button = self.driver.find_element(By.CLASS_NAME, "block").click()
        try:
            title_element = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.TAG_NAME, "title"))
            )
        finally:
            title = self.driver.title
            assert title == "API Exchange Developer Portal"
    
    def teardown_method(self):
        self.driver.close()

class TestValidator:
    def setup_method(self):
        try: # in pipeline
            with open("src/examples/example1.yaml", "r") as f:
                self.example1 = f.read()
            with open("src/examples/example2 .yaml", "r") as f:
                self.example2 = f.read()
        except (FileNotFoundError): # local
            with open("../examples/example1.yaml", "r") as f:
                self.example1 = f.read()
            with open("../examples/example2.yaml", "r") as f:
                self.example2 = f.read()
        try: # in pipeline
            self.driver = webdriver.Chrome(service=ChromeService(chromeDriverPath), options=options)
        except Exception: # local
            self.driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=options)
        self.driver.get(frontendURL)
    
    def test_validateYAML_noerror(self):
        try:
            doc_text_area = WebDriverWait(self.driver, 10).until(
                EC.visibility_of_element_located((By.CLASS_NAME, "ace_content"))
            )
        finally:
            self.driver.execute_script(f"editor.setValue(`{self.example1}`)")
            doc = self.driver.execute_script("editor.getValue()")
            assert (doc != "" or doc != None) == True
        try:
            preview_panel = WebDriverWait(self.driver, 10).until(
                EC.visibility_of_element_located((By.ID, "previewPanel"))
            )
        finally:
            class_attributes = preview_panel.get_attribute("class")
            assert "active" in class_attributes
    
    # def test_validateYAML_error(self):
    #     try:
    #         # WARNING: If screen minimized or screen too small, 
    #         # ace editor might not appear and thus this test will fail; fixed with fixed window size
    #         textarea = WebDriverWait(self.driver, 5).until(
    #             EC.visibility_of_element_located((By.CLASS_NAME, "ace_content"))
    #         )
    #     finally:
    #         self.driver.execute_script(f"editor.setValue(`{self.template2}`)")
    #         textareaContent = self.driver.execute_script("editor.getValue()")
    #         assert (textareaContent != "" or textareaContent != None) == True
    #     button = self.driver.find_element(By.ID, "checkOASButton").click()
    #     try:
    #         modal = WebDriverWait(self.driver, 20).until(
    #             EC.visibility_of_element_located((By.ID, "oasErrorsBody"))
    #         )
    #     finally:
    #         assert True

    def teardown_method(self):
            self.driver.close()


# class TestNavBarUtils:
#     def setup_method(self):
#         try: # in pipeline
#             self.driver = webdriver.Chrome(service=ChromeService(chromeDriverPath), options=options)
#         except Exception: # local
#             self.driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=options)
#         self.driver.get(frontend404URL)
    
#     def test_frontend_catchall_redirect_button(self):
#         try:
#             button = WebDriverWait(self.driver, 10).until(
#                 EC.visibility_of_element_located((By.CLASS_NAME, "block"))
#             )
#         finally:
#             button = self.driver.find_element(By.CLASS_NAME, "block").click()
#         try:
#             title_element = WebDriverWait(self.driver, 10).until(
#                 EC.presence_of_element_located((By.TAG_NAME, "title"))
#             )
#         finally:
#             title = self.driver.title
#             assert title == "API Exchange Developer Portal"
    
#     def teardown_method(self):
#         self.driver.close()

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