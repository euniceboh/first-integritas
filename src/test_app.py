import app
import pytest

class TestMissing:
    def setUp(self):
        self.title = "Update Crediting Status of 55 WDL Application PayNow"
        self.description = "This API is to update the crediting status of the member's 55 WDL Application for PayNow"
        self.version = "1.0.0"
        self.x_author = "Jennylyn Sze"
        self.x_date = "2022-12-22"

    def test_title(self):
        assert app.checkTitle(self.title)
    
    def test_description(self):
        assert app.checkDescription(self.description)
