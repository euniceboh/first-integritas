# # White Box MVC Unit Testing

import yaml
import pytest
from src import app as flask_app

@pytest.fixture
def app():
    return flask_app.app

# View

class TestRoutes:
    def test_catchall_route(self, app):
        client = app.test_client()
        url = '/any/other/route'
        response = client.get(url)
        assert response.status_code == 200

    def test_oaschecker_route(self, app):
        client = app.test_client()
        url = '/'
        response = client.get(url)
        assert response.status_code == 200

    def test_swaggeruipreview_route(self, app):
        client = app.test_client()
        url = '/swaggeruipreview'
        response = client.get(url)
        assert response.status_code == 200

# Controller

# with open("../template1.yaml", 'r') as stream:
#             try:
#                 self.template1_json = yaml.safe_load(stream)
#                 self.template1_str = str(self.template1_json)
#             except yaml.YAMLError as exc:
#                 template1_json = {}

#         with open("../template2.yaml", 'r') as stream:
#             try:
#                 self.template2_json = yaml.safe_load(stream)
#             except yaml.YAMLError as exc:
#                 self.template2_json = {}

template1 = {
    "openapi": "3.0.0",
    "info": {
      "title": "Update Crediting Status of 55 WDL Application PayNow",
      "description": "This API is to update the crediting status of the member's 55 WDL Application for PayNow",
      "version": "1.0.0",
      "x-author": "Jennylyn Sze",
      "x-date": "2022-12-22"
    },
    "paths": {
      "/discretionaryWithdrawals/55Withdrawals/v1/updateMemberCreditStatusForPayNow": {
        "post": {
          "requestBody": {
            "content": {
              "application/json": {
                "schema": {
                  "type": "object",
                  "properties": {
                    "Section": {
                      "type": "object",
                      "description": "The main request body",
                      "properties": {
                        "programId": {
                          "type": "string",
                          "description": "Program ID of the consumer",
                          "example": "ESERVICE",
                          "minLength": 1,
                          "maxLength": 10
                        },
                        "userId": {
                          "type": "string",
                          "description": "User ID of the consumer",
                          "example": "RSD001"
                        },
                        "accountNumber": {
                          "type": "string",
                          "description": "Member's Account Number",
                          "example": "S1234567A",
                          "minLength": 9,
                          "maxLength": 9
                        },
                        "electronicFormTransactionNumber": {
                          "type": "string",
                          "description": "electronicForm Transaction Number",
                          "example": "1500142799903518",
                          "maxLength": 16
                        },
                        "creditStatusTag": {
                          "type": "string",
                          "description": "Credit Status Tag",
                          "example": "Y",
                          "maxLength": 1
                        },
                        "ocbcTransactionNumber": {
                          "type": "string",
                          "description": "OCBC Transaction Number",
                          "example": "20200928034440888853",
                          "maxLength": 20
                        },
                        "ocbcReturnCode": {
                          "type": "string",
                          "description": "OCBC Return Code",
                          "example": "",
                          "maxLength": 4
                        },
                        "guid": {
                          "type": "string",
                          "description": "The GUID of the API call",
                          "example": "123456789012345678901234567890123456",
                          "maxLength": 36
                        }
                      },
                      "required": [
                        "programId",
                        "accountNumber",
                        "electronicFormTransactionNumber",
                        "creditStatusTag",
                        "ocbcTransactionNumber",
                        "ocbcReturnCode",
                        "guid"
                      ]
                    }
                  },
                  "required": [
                    "Section"
                  ]
                }
              }
            }
          },
          "responses": {
            "200": {
              "description": "Successfully called the API to update credit status of Member's 55 WDL Application for PayNow. This can include application and data error.",
              "content": {
                "application/json": {
                  "schema": {
                    "type": "object",
                    "properties": {
                      "Section": {
                        "type": "object",
                        "description": "The main response body",
                        "properties": {
                          "programId": {
                            "type": "string",
                            "description": "Program ID of the consumer",
                            "example": "ESERVICE",
                            "minLength": 1,
                            "maxLength": 10
                          },
                          "userId": {
                            "type": "string",
                            "description": "User ID of the consumer",
                            "example": "RSD001"
                          },
                          "accountNumber": {
                            "type": "string",
                            "description": "Member's Account Number",
                            "example": "S1234567A",
                            "minLength": 9,
                            "maxLength": 9
                          },
                          "electronicFormTransactionNumber": {
                            "type": "string",
                            "description": "electronicForm Transaction Number",
                            "example": "1500142799903518",
                            "maxLength": 16
                          },
                          "creditStatusTag": {
                            "type": "string",
                            "description": "Credit Status Tag",
                            "example": "Y",
                            "maxLength": 1
                          },
                          "ocbcTransactionNumber": {
                            "type": "string",
                            "description": "OCBC Transaction Number",
                            "example": "20200928034440888853",
                            "maxLength": 20
                          },
                          "ocbcReturnCode": {
                            "type": "string",
                            "description": "OCBC Return COde",
                            "example": "",
                            "maxLength": 4
                          },
                          "returnCode": {
                            "type": "string",
                            "description": "Program Return Code",
                            "example": "0000",
                            "maxLength": 4
                          },
                          "returnMessage": {
                            "type": "string",
                            "description": "Program Return Message",
                            "example": "Successful",
                            "maxLength": 50
                          },
                          "guid": {
                            "type": "string",
                            "description": "The GUID of the API call",
                            "example": "123456789012345678901234567890123456",
                            "maxLength": 36
                          }
                        },
                        "required": [
                          "programId",
                          "accountNumber",
                          "electronicFormTransactionNumber",
                          "creditStatusTag",
                          "ocbcTransactionNumber",
                          "ocbcReturnCode",
                          "returnCode",
                          "returnMessage",
                          "guid"
                        ]
                      }
                    },
                    "required": [
                      "Section"
                    ]
                  }
                }
              }
            }
          }
        }
      }
    }
  }

template2 = {
  "openapi": "3.0.0",
  "info": {
    "title": "Agecheckfor55WDL",
    "description": "### To check age eligibility for 55 WDL.\nThe service shall validate member's CPF account number and Birth date.\nThis service shall retrieve the following information.\n1. 55 Eligibility Tag\n2. 55A eligibility Tag\n3. Return code\n4. Return message\n\n### Change log\n| version | Date      | Description                         |\n| ------- | --------- | ----------------------------------- |\n| 1.0.0   | 2021-10-09| First version                       |\n| 1.0.1   | 2021-12-01| change xxxxx for xxxxxxx            |\n| 1.0.2   | 2022-04-09| change xxxxx for xxxxxxx            |\n| 1.1.0   | 2022-07-04| change xxxxx for xxxxxxx            |\n| 1.1.1   | 2022-10-05| change xxxxx for xxxxxxx            |\n",
    "version": "1.1.1",
    "x-author": "MS1",
    "x-date": "2023-03-01T00:00:00.000Z",
    "x-searchKeywords": "55WDL"
  },
  "paths": {
    "/discretionaryWithdrawals/55Withdrawals/v2/checkMemberAgeEligibility": {
      "post": {
        "requestBody": {
          "content": {
            "application/json": {
              "schema": {
                "type": "object",
                "properties": {
                  "accountNumber": {
                    "type": "string",
                    "description": "Member Account Number",
                    "example": "S3120874B"
                  },
                  "birthdate": {
                    "type": "string",
                    "description": "Member Birthdate (CCYY-MM-DD)",
                    "example": "1965-03-04"
                  },
                  "guid": {
                    "type": "string",
                    "description": "Globally Unique Identifier for data integrity check",
                    "example": "abcab671-68e8-4096-8bbc-fe3e184ef72b"
                  }
                },
                "required": [
                  "accountNumber",
                  "startMonth",
                  "endMonth"
                ]
              }
            }
          }
        },
        "responses": {
          "200": {
            "description": "Successfully retrieved contribution history",
            "content": {
              "application/json": {
                "examples": {
                  "Return00": {
                    "summary": "normal return",
                    "value": {
                      "accountNumber": "S3120874B",
                      "birthdate": "1965-03-04",
                      "55EligibilityTag": "Y",
                      "55AEligibilityTag": "N",
                      "returnCode": "00",
                      "returnMessage": "SUCCESSFUL",
                      "guid": "abcab671-68e8-4096-8bbc-fe3e184ef72b"
                    }
                  },
                  "Return01": {
                    "summary": "error return",
                    "value": {
                      "accountNumber": "",
                      "birthdate": "1965-03-04",
                      "55EligibilityTag": "",
                      "55AEligibilityTag": "",
                      "returnCode": "01",
                      "returnMessage": "ACCOUNT NUMBER NOT PROVIDED",
                      "guid": "abcab671-68e8-4096-8bbc-fe3e184ef72b"
                    }
                  }
                },
                "schema": {
                  "type": "object",
                  "properties": {
                    "accountNumber": {
                      "type": "string",
                      "description": "Member Account Number"
                    },
                    "birthdate": {
                      "type": "string",
                      "description": "Member Birthdate (CCYY-MM-DD)"
                    },
                    "55EligibilityTag": {
                      "type": "string",
                      "enum": [
                        "Y",
                        "N"
                      ],
                      "description": "**The below table defines the value of 55EligibilityTag**\n| Value   | Description                         |\n| ------- | ----------------------------------- |\n| Y       | Eligible                            |\n| N       | Not Eligible                        |\n"
                    },
                    "55AEligibilityTag": {
                      "type": "string",
                      "enum": [
                        "N"
                      ],
                      "description": "**The below table defines the value of 55AEligibilityTag**\n| Value   | Description                         |\n| ------- | ----------------------------------- |\n| N       | Default value                       |\n"
                    },
                    "returnCode": {
                      "type": "string",
                      "description": "**The below table defines the value of returnCode**\n| Value   | Description                         |\n| ------- | ----------------------------------- |\n| 00      | Successful                          |\n| 01      | Account number not provided         |\n| 02      | Member's age unknown                |\n| 03      | Invalid birthdate - DD              |\n| 04      | Invalid birthdate - MM              |\n| 05      | Not a cpf member                    |\n| 06      | invalid pensionable tag             |\n| 07      | medisave table not found            |\n| 08      | last withdrawal age is not valid    |\n| 12      | Invalid birthdate - CCYY            |\n"
                    },
                    "returnMessage": {
                      "type": "string",
                      "description": "Return Message"
                    },
                    "guid": {
                      "type": "string",
                      "description": "Globally Unique Identifier for data integrity check"
                    }
                  },
                  "required": [
                    "accountNumber",
                    "birthdate",
                    "55EligibilityTag",
                    "55AEligibilityTag",
                    "returnCode",
                    "returnMessage",
                    "guid"
                  ]
                }
              }
            }
          }
        },
        "deprecated": 'false'
      }
    }
  }
}

class TestMissingKeys:
    def test_openapi_successful(self):
        assert flask_app.checkOpenapi("3.0.0") == True

    def test_openapi_unsuccessful(self):
        assert flask_app.checkOpenapi("") == False
        assert flask_app.checkOpenapi(None) == False

    def test_title_successful(self):
        assert flask_app.checkTitle("Update Crediting Status of 55 WDL Application PayNow") == True
    
    def test_title_unsuccessful(self):
        assert flask_app.checkTitle("") == False
        assert flask_app.checkTitle(None) == False
    
    def test_description_successful(self):
        assert flask_app.checkDescription("This API is to update the crediting status of the member's 55 WDL Application for PayNow") == True
    
    def test_description_unsuccessful(self):
        assert flask_app.checkDescription("") == False
        assert flask_app.checkDescription(None) == False

    def test_infoVersion_successful(self):
        assert flask_app.checkInfoVersion("1.0.0") == True
    
    def test_infoVersion_unsuccessful(self):
        assert flask_app.checkInfoVersion("") == False
        assert flask_app.checkInfoVersion(None) == False
    
    def test_xAuthor_successful(self):
        assert flask_app.checkXAuthor("Jennylyn Sze") == True
    
    def test_xAuthor_unsuccessful(self):
        assert flask_app.checkXAuthor("") == False
        assert flask_app.checkXAuthor(None) == False
    
    def test_xDate_successful(self):
        assert flask_app.checkXDate("2022-12-22") == True
    
    def test_xDate_unsuccessful(self):
        assert flask_app.checkXDate("") == False
        assert flask_app.checkXDate(None) == False
    
    def test_path_successful(self):
        assert flask_app.checkPath("/discretionaryWithdrawals/55Withdrawals/v1/updateMemberCreditStatusForPayNow") == True
    
    def test_path_unsuccessful(self):
        assert flask_app.checkPath("") == False
        assert flask_app.checkPath(None) == False
    
    def test_response_successful(self):
        assert flask_app.checkResponse(template1, 0) == 1
    
    def test_response_unsuccessful(self):
        template1_no_response = {
    "openapi": "3.0.0",
    "info": {
      "title": "Update Crediting Status of 55 WDL Application PayNow",
      "description": "This API is to update the crediting status of the member's 55 WDL Application for PayNow",
      "version": "1.0.0",
      "x-author": "Jennylyn Sze",
      "x-date": "2022-12-22"
    },
    "paths": {
      "/discretionaryWithdrawals/55Withdrawals/v1/updateMemberCreditStatusForPayNow": {
        "post": {
          "requestBody": {
            "content": {
              "application/json": {
                "schema": {
                  "type": "object",
                  "properties": {
                    "Section": {
                      "type": "object",
                      "description": "The main request body",
                      "properties": {
                        "programId": {
                          "type": "string",
                          "description": "Program ID of the consumer",
                          "example": "ESERVICE",
                          "minLength": 1,
                          "maxLength": 10
                        },
                        "userId": {
                          "type": "string",
                          "description": "User ID of the consumer",
                          "example": "RSD001"
                        },
                        "accountNumber": {
                          "type": "string",
                          "description": "Member's Account Number",
                          "example": "S1234567A",
                          "minLength": 9,
                          "maxLength": 9
                        },
                        "electronicFormTransactionNumber": {
                          "type": "string",
                          "description": "electronicForm Transaction Number",
                          "example": "1500142799903518",
                          "maxLength": 16
                        },
                        "creditStatusTag": {
                          "type": "string",
                          "description": "Credit Status Tag",
                          "example": "Y",
                          "maxLength": 1
                        },
                        "ocbcTransactionNumber": {
                          "type": "string",
                          "description": "OCBC Transaction Number",
                          "example": "20200928034440888853",
                          "maxLength": 20
                        },
                        "ocbcReturnCode": {
                          "type": "string",
                          "description": "OCBC Return Code",
                          "example": "",
                          "maxLength": 4
                        },
                        "guid": {
                          "type": "string",
                          "description": "The GUID of the API call",
                          "example": "123456789012345678901234567890123456",
                          "maxLength": 36
                        }
                      },
                      "required": [
                        "programId",
                        "accountNumber",
                        "electronicFormTransactionNumber",
                        "creditStatusTag",
                        "ocbcTransactionNumber",
                        "ocbcReturnCode",
                        "guid"
                      ]
                    }
                  },
                  "required": [
                    "Section"
                  ]
                }
              }
            }
          },
        }
      }
    }
  }
        assert flask_app.checkResponse(template1_no_response, 0) == 0

    def test_properties_successful(self):
        missingProperties = []
        for key, value in template1.items():
            missingProperties = flask_app.checkProperties(key, value, missingProperties)
        assert len(missingProperties) == 0
    
    def test_properties_unsuccessful(self):
        missingProperties = []
        for key, value in template2.items():
            missingProperties = flask_app.checkProperties(key, value, missingProperties)
        assert len(missingProperties) != 0

class TestPathFormat:
    def setup_method(self):
        self.path = "/discretionaryWithdrawals/55Withdrawals/v1/updateMemberCreditStatusForPayNow"
        self.path_with_spacing = "/discretionaryWithdrawals/55Withdrawals /v1/updateMemberCreditStatusForPayNow"
        self.path_with_underscore = "/discretionaryWithdrawals/55Withdrawals_/v1/updateMemberCreditStatusForPayNow"
        self.path_with_hyphen = "/discretionaryWithdrawals/55Withdrawals-/v1/updateMemberCreditStatusForPayNow"
        self.path_with_noleadingslash = "discretionaryWithdrawals/55Withdrawals-/v1/updateMemberCreditStatusForPayNow"
        self.path_with_wordnotindict = "discretionaryWithdrawals/55Withdrawals-/v1/updateMemberCreditStatusForPayNowThe"
        self.path_notcamelcasing = "/discretionaryWithdrawals/55Withdrawals/v1/updatememberCreditStatusForPayNow"
        self.path_wrongspelling = "/discretionaryWithdrawals/55Withdrawals/v1/updateMmberCreditStatusForPayNow"
        self.path_length4 = "/discretionaryWithdrawals/v1/updateMemberCreditStatusForPayNow"
        self.path_length5 = self.path
        self.path_length6 = "/discretionaryWithdrawals/55Withdrawals/v1/updateMemberCreditStatusForPayNow/userJohn"
        self.path_length7 = "/discretionaryWithdrawals/55Withdrawals/v1/updateMemberCreditStatusForPayNow/userJohn/wrongLength"
        self.path_notnumeric = "/discretionaryWithdrawals/55Withdrawals/vv/updateMemberCreditStatusForPayNow"
        self.path_notv = "/discretionaryWithdrawals/55Withdrawals/11/updateMemberCreditStatusForPayNow"
        self.path_notverb = "/discretionaryWithdrawals/55Withdrawals/v1/singaporeMemberCreditStatusForPayNow"
        self.dictionary = ["discretionary", "withdrawals", "update", "member", "credit", "status", "for", "pay", "now"]
    
    def test_pathCharacters_successful(self):
        assert flask_app.checkPathCharacters(self.path) == True
    
    def test_pathCharacters_unsuccessful(self):
        assert flask_app.checkPathCharacters(self.path_with_spacing) == False
        assert flask_app.checkPathCharacters(self.path_with_underscore) == False
        assert flask_app.checkPathCharacters(self.path_with_hyphen) == False
    
    def test_pathLeadingSlash_successful(self):
        assert flask_app.checkPathLeadingSlash(self.path) == True
    
    def test_pathLeadingSlash_unsuccessful(self):
        assert flask_app.checkPathLeadingSlash(self.path_with_noleadingslash) == False
    
    def test_pathWordsDict_successful(self):
        wordsNotInDictionary = flask_app.checkPathWordsDict(self.path, self.dictionary)
        assert len(wordsNotInDictionary) == 0
    
    def test_pathWordsDict_unsuccessful(self):
        wordsNotInDictionary = flask_app.checkPathWordsDict(self.path_with_wordnotindict, self.dictionary)
        assert len(wordsNotInDictionary) != 0
    
    def test_notCamelCasing_successful(self):
        notCamelCasing = flask_app.checkCamelCasing(self.path)
        assert len(notCamelCasing) == 0
    
    def test_notCamelCasing_unsuccessful(self):
        notCamelCasing = flask_app.checkCamelCasing(self.path_notcamelcasing)
        assert len(notCamelCasing) != 0
    
    def test_pathSpelling_successful(self):
        wrongSubtierSpelling = flask_app.checkPathSpelling(self.path)
        assert len(wrongSubtierSpelling) == 0
    
    def test_pathSpelling_unsuccessful(self):
        wrongSubtierSpelling = flask_app.checkPathSpelling(self.path_wrongspelling)
        assert len(wrongSubtierSpelling) != 0
    
    def test_pathLength_successful(self):
        pathLength5Flag = flask_app.checkPathLength(self.path_length5)
        pathLength6Flag = flask_app.checkPathLength(self.path_length6)
        assert pathLength5Flag == 0
        assert pathLength6Flag == 0
    
    def test_pathLength_unsuccessful(self):
        pathLength4Flag = flask_app.checkPathLength(self.path_length4)
        pathLength7Flag = flask_app.checkPathLength(self.path_length7)
        assert pathLength4Flag == 1
        assert pathLength7Flag == 2
    
    def test_pathVersion_successful(self):
        assert flask_app.checkPathVersion(self.path) == True
    
    def test_pathVersion_unsuccessful(self):
        assert flask_app.checkPathVersion("") == False
        assert flask_app.checkPathVersion(self.path_notnumeric) == False
        assert flask_app.checkPathVersion(self.path_notv) == False
    
    def test_subtierVerb_successful(self):
        notVerbSubtiers = flask_app.checkSubtierVerb(self.path)
        assert len(notVerbSubtiers) == 0
    
    def test_subtierVerb_unsuccessful(self):
        notVerbSubtiers = flask_app.checkSubtierVerb(self.path_notverb)
        assert len(notVerbSubtiers) != 0
    
class TestMatching:
    def setup_method(self):
        self.infoVersion = "1.0.0"
        self.infoVersion2 = "2.0.0"
        self.path = "/discretionaryWithdrawals/55Withdrawals/v1/updateMemberCreditStatusForPayNow"
        self.path_version2 = "/discretionaryWithdrawals/55Withdrawals/v2/updateMemberCreditStatusForPayNow"

    def test_matchingVersion_successful(self):
        assert flask_app.checkMatchingVersion(self.infoVersion, self.path) == True
    
    def test_matchingVersion_unsuccessful(self):
        assert flask_app.checkMatchingVersion(self.infoVersion, self.path_version2) == False
        assert flask_app.checkMatchingVersion(self.infoVersion2, self.path) == False


class TestDictionary:
    def setup_method(self):
        self.dictionary = ["discretionary", "withdrawals", "update", "member", "credit", "status", "for", "pay", "now"]
        self.dictionary_repeated = ["discretionary", "withdrawals", "update", "update", "member", "credit", "status", "for", "for", "pay", "now"]
    
    def test_duplicateDictionary_successful(self):
        duplicateDictWords = flask_app.checkDuplicateDict(self.dictionary)
        assert len(duplicateDictWords) == 0
    
    def test_duplicateDictionary_unsuccessful(self):
        duplicateDictWords = flask_app.checkDuplicateDict(self.dictionary_repeated)
        assert len(duplicateDictWords) != 0

