# doc = {
#     "openapi": "3.0.0",
#     "info": {
#       "title": "Update Crediting Status of 55 WDL Application PayNow",
#       "description": "This API is to update the crediting status of the member's 55 WDL Application for PayNow",
#       "version": "1.0.0",
#       "x-author": "Jennylyn Sze",
#       "x-date": "2022-12-22"
#     },
#     "paths": {
#       "/discretionaryWithdrawals/55Withdrawals/v1/updateMemberCreditStatusForPayNow": {
#         "post": {
#           "requestBody": {
#             "content": {
#               "application/json": {
#                 "schema": {
#                   "type": "object",
#                   "properties": {
#                     "Section": {
#                       "type": "object",
#                       "description": "The main request body",
#                       "properties": {
#                         "programId": {
#                           "type": "string",
#                           "description": "Program ID of the consumer",
#                           "example": "ESERVICE",
#                           "minLength": 1,
#                           "maxLength": 10
#                         },
#                         "userId": {
#                           "type": "string",
#                           "description": "User ID of the consumer",
#                           "example": "RSD001"
#                         },
#                         "accountNumber": {
#                           "type": "string",
#                           "description": "Member's Account Number",
#                           "example": "S1234567A",
#                           "minLength": 9,
#                           "maxLength": 9
#                         },
#                         "electronicFormTransactionNumber": {
#                           "type": "string",
#                           "description": "electronicForm Transaction Number",
#                           "example": "1500142799903518",
#                           "maxLength": 16
#                         },
#                         "creditStatusTag": {
#                           "type": "string",
#                           "description": "Credit Status Tag",
#                           "example": "Y",
#                           "maxLength": 1
#                         },
#                         "ocbcTransactionNumber": {
#                           "type": "string",
#                           "description": "OCBC Transaction Number",
#                           "example": "20200928034440888853",
#                           "maxLength": 20
#                         },
#                         "ocbcReturnCode": {
#                           "type": "string",
#                           "description": "OCBC Return Code",
#                           "example": "",
#                           "maxLength": 4
#                         },
#                         "guid": {
#                           "type": "string",
#                           "description": "The GUID of the API call",
#                           "example": "123456789012345678901234567890123456",
#                           "maxLength": 36
#                         }
#                       },
#                       "required": [
#                         "programId",
#                         "accountNumber",
#                         "electronicFormTransactionNumber",
#                         "creditStatusTag",
#                         "ocbcTransactionNumber",
#                         "ocbcReturnCode",
#                         "guid"
#                       ]
#                     }
#                   },
#                   "required": [
#                     "Section"
#                   ]
#                 }
#               }
#             }
#           },
#           "responses": {
#             "200": {
#               "description": "Successfully called the API to update credit status of Member's 55 WDL Application for PayNow. This can include application and data error.",
#               "content": {
#                 "application/json": {
#                   "schema": {
#                     "type": "object",
#                     "properties": {
#                       "Section": {
#                         "type": "object",
#                         "description": "The main response body",
#                         "properties": {
#                           "programId": {
#                             "type": "string",
#                             "description": "Program ID of the consumer",
#                             "example": "ESERVICE",
#                             "minLength": 1,
#                             "maxLength": 10
#                           },
#                           "userId": {
#                             "type": "string",
#                             "description": "User ID of the consumer",
#                             "example": "RSD001"
#                           },
#                           "accountNumber": {
#                             "type": "string",
#                             "description": "Member's Account Number",
#                             "example": "S1234567A",
#                             "minLength": 9,
#                             "maxLength": 9
#                           },
#                           "electronicFormTransactionNumber": {
#                             "type": "string",
#                             "description": "electronicForm Transaction Number",
#                             "example": "1500142799903518",
#                             "maxLength": 16
#                           },
#                           "creditStatusTag": {
#                             "type": "string",
#                             "description": "Credit Status Tag",
#                             "example": "Y",
#                             "maxLength": 1
#                           },
#                           "ocbcTransactionNumber": {
#                             "type": "string",
#                             "description": "OCBC Transaction Number",
#                             "example": "20200928034440888853",
#                             "maxLength": 20
#                           },
#                           "ocbcReturnCode": {
#                             "type": "string",
#                             "description": "OCBC Return COde",
#                             "example": "",
#                             "maxLength": 4
#                           },
#                           "returnCode": {
#                             "type": "string",
#                             "description": "Program Return Code",
#                             "example": "0000",
#                             "maxLength": 4
#                           },
#                           "returnMessage": {
#                             "type": "string",
#                             "description": "Program Return Message",
#                             "example": "Successful",
#                             "maxLength": 50
#                           },
#                           "guid": {
#                             "type": "string",
#                             "description": "The GUID of the API call",
#                             "example": "123456789012345678901234567890123456",
#                             "maxLength": 36
#                           }
#                         },
#                         "required": [
#                           "programId",
#                           "accountNumber",
#                           "electronicFormTransactionNumber",
#                           "creditStatusTag",
#                           "ocbcTransactionNumber",
#                           "ocbcReturnCode",
#                           "returnCode",
#                           "returnMessage",
#                           "guid"
#                         ]
#                       }
#                     },
#                     "required": [
#                       "Section"
#                     ]
#                   }
#                 }
#               }
#             }
#           }
#         }
#       },
#         "/discretionaryWithdrawals/55Withdrawals/v1/changeMemberCreditStatusForPayNow": {
#             "post": {
#             "requestBody": {
#                 "content": {
#                 "application/json": {
#                     "schema": {
#                     "type": "object",
#                     "properties": {
#                         "Section": {
#                         "type": "object",
#                         "description": "The main request body",
#                         "properties": {
#                             "programId": {
#                             "type": "string",
#                             "description": "Program ID of the consumer",
#                             "example": "ESERVICE",
#                             "minLength": 1,
#                             "maxLength": 10
#                             },
#                             "userId": {
#                             "type": "string",
#                             "description": "User ID of the consumer",
#                             "example": "RSD001"
#                             },
#                             "accountNumber": {
#                             "type": "string",
#                             "description": "Member's Account Number",
#                             "example": "S1234567A",
#                             "minLength": 9,
#                             "maxLength": 9
#                             },
#                             "electronicFormTransactionNumber": {
#                             "type": "string",
#                             "description": "electronicForm Transaction Number",
#                             "example": "1500142799903518",
#                             "maxLength": 16
#                             },
#                             "creditStatusTag": {
#                             "type": "string",
#                             "description": "Credit Status Tag",
#                             "example": "Y",
#                             "maxLength": 1
#                             },
#                             "ocbcTransactionNumber": {
#                             "type": "string",
#                             "description": "OCBC Transaction Number",
#                             "example": "20200928034440888853",
#                             "maxLength": 20
#                             },
#                             "ocbcReturnCode": {
#                             "type": "string",
#                             "description": "OCBC Return Code",
#                             "example": "",
#                             "maxLength": 4
#                             },
#                             "guid": {
#                             "type": "string",
#                             "description": "The GUID of the API call",
#                             "example": "123456789012345678901234567890123456",
#                             "maxLength": 36
#                             }
#                         },
#                         "required": [
#                             "programId",
#                             "accountNumber",
#                             "electronicFormTransactionNumber",
#                             "creditStatusTag",
#                             "ocbcTransactionNumber",
#                             "ocbcReturnCode",
#                             "guid"
#                         ]
#                         }
#                     },
#                     "required": [
#                         "Section"
#                     ]
#                     }
#                 }
#                 }
#             },
#             "responses": {
#                 "200": {
#                 "description": "Successfully called the API to update credit status of Member's 55 WDL Application for PayNow. This can include application and data error.",
#                 "content": {
#                     "application/json": {
#                     "schema": {
#                         "type": "object",
#                         "properties": {
#                         "Section": {
#                             "type": "object",
#                             "description": "The main response body",
#                             "properties": {
#                             "programId": {
#                                 "type": "string",
#                                 "description": "Program ID of the consumer",
#                                 "example": "ESERVICE",
#                                 "minLength": 1,
#                                 "maxLength": 10
#                             },
#                             "userId": {
#                                 "type": "string",
#                                 "description": "User ID of the consumer",
#                                 "example": "RSD001"
#                             },
#                             "accountNumber": {
#                                 "type": "string",
#                                 "description": "Member's Account Number",
#                                 "example": "S1234567A",
#                                 "minLength": 9,
#                                 "maxLength": 9
#                             },
#                             "electronicFormTransactionNumber": {
#                                 "type": "string",
#                                 "description": "electronicForm Transaction Number",
#                                 "example": "1500142799903518",
#                                 "maxLength": 16
#                             },
#                             "creditStatusTag": {
#                                 "type": "string",
#                                 "description": "Credit Status Tag",
#                                 "example": "Y",
#                                 "maxLength": 1
#                             },
#                             "ocbcTransactionNumber": {
#                                 "type": "string",
#                                 "description": "OCBC Transaction Number",
#                                 "example": "20200928034440888853",
#                                 "maxLength": 20
#                             },
#                             "ocbcReturnCode": {
#                                 "type": "string",
#                                 "description": "OCBC Return COde",
#                                 "example": "",
#                                 "maxLength": 4
#                             },
#                             "returnCode": {
#                                 "type": "string",
#                                 "description": "Program Return Code",
#                                 "example": "0000",
#                                 "maxLength": 4
#                             },
#                             "returnMessage": {
#                                 "type": "string",
#                                 "description": "Program Return Message",
#                                 "example": "Successful",
#                                 "maxLength": 50
#                             },
#                             "guid": {
#                                 "type": "string",
#                                 "description": "The GUID of the API call",
#                                 "example": "123456789012345678901234567890123456",
#                                 "maxLength": 36
#                             }
#                             },
#                             "required": [
#                             "programId",
#                             "accountNumber",
#                             "electronicFormTransactionNumber",
#                             "creditStatusTag",
#                             "ocbcTransactionNumber",
#                             "ocbcReturnCode",
#                             "returnCode",
#                             "returnMessage",
#                             "guid"
#                             ]
#                         }
#                         },
#                         "required": [
#                         "Section"
#                         ]
#                     }
#                     }
#                 }
#                 }
#             }
#             }
#         }
#     }
#   }

import yaml

doc = '''openapi: 3.0.0
info:
  title: Update Crediting Status of 55 WDL Application PayNow
  description: This API is to update the crediting status of the member's 55 WDL Application for PayNow
  version: 1.0.0
  x-author: Jennylyn Sze
  x-date: '2022-12-22'

paths:
  /discretionaryWithdrawals/55Withdrawals/v1/updateMemberCreditStatusForPayNow:
    post:
      requestBody:
        content:
          application/json:
            schema:
              type: object
              properties:
                Section:
                  type: object
                  description: The main request body
                  properties:
                    programId:
                      type: string
                      description: Program ID of the consumer
                      example: 'ESERVICE'
                      minLength: 1
                      maxLength: 10
                    userId:
                      type: string
                      description: User ID of the consumer
                      example: 'RSD001'
                    accountNumber:
                      type: string
                      description: Member's Account Number
                      example: 'S1234567A'
                      minLength: 9
                      maxLength: 9
                    electronicFormTransactionNumber:
                      type: string
                      description: electronicForm Transaction Number
                      example: '1500142799903518'
                      maxLength: 16
                    creditStatusTag:
                      type: string
                      description: Credit Status Tag
                      example: 'Y'
                      maxLength: 1
                    ocbcTransactionNumber:
                      type: string
                      description: OCBC Transaction Number
                      example: '20200928034440888853'
                      maxLength: 20
                    ocbcReturnCode:
                      type: string
                      description: OCBC Return Code
                      example: ''
                      maxLength: 4
                    guid:
                      type: string
                      description: The GUID of the API call
                      example: '123456789012345678901234567890123456'
                      maxLength: 36
                  required:
                    - programId
                    - accountNumber
                    - electronicFormTransactionNumber
                    - creditStatusTag
                    - ocbcTransactionNumber
                    - ocbcReturnCode
                    - guid
              required:
                - Section
      responses:
        '200':
          description: Successfully called the API to update credit status of Member's 55 WDL Application for PayNow. This can include application and data error.
          content:
            application/json:
              schema:
                type: object
                properties:
                  Section:
                    type: object
                    description: The main response body
                    properties:
                        programId:
                          type: string
                          description: Program ID of the consumer
                          example: 'ESERVICE'
                          minLength: 1
                          maxLength: 10
                        userId:
                          type: string
                          description: User ID of the consumer
                          example: 'RSD001'
                        accountNumber:
                          type: string
                          description: Member's Account Number
                          example: 'S1234567A'
                          minLength: 9
                          maxLength: 9
                        electronicFormTransactionNumber:
                          type: string
                          description: electronicForm Transaction Number
                          example: '1500142799903518'
                          maxLength: 16
                        creditStatusTag:
                          type: string
                          description: Credit Status Tag
                          example: 'Y'
                          maxLength: 1
                        ocbcTransactionNumber:
                          type: string
                          description: OCBC Transaction Number
                          example: '20200928034440888853'
                          maxLength: 20
                        ocbcReturnCode:
                          type: string
                          description: OCBC Return COde
                          example: ''
                          maxLength: 4
                        returnCode:
                          type: string
                          description: Program Return Code
                          example: '0000'
                          maxLength: 4
                        returnMessage:
                          type: string
                          description: Program Return Message
                          example: 'Successful'
                          maxLength: 50
                        guid:
                          type: string
                          description: The GUID of the API call
                          example: '123456789012345678901234567890123456'
                          maxLength: 36
                    required:
                        - programId
                        - accountNumber
                        - electronicFormTransactionNumber
                        - creditStatusTag
                        - ocbcTransactionNumber
                        - ocbcReturnCode
                        - returnCode
                        - returnMessage
                        - guid
                required:
                  - Section'''




# def parse_yaml_string_with_line_numbers(yaml_string):
#     lines = yaml_string.split("\n")

#     yaml_data = yaml.safe_load(yaml_string)

#     line_numbers = {}
#     find_line_numbers(yaml_data, lines, line_numbers)

#     return line_numbers


# def find_line_numbers(data, lines, line_numbers):
#     if isinstance(data, dict):
#         for key, value in data.items():
#             if isinstance(value, dict) or isinstance(value, list):
#                 find_line_numbers(value, lines, line_numbers)
#             else:
#                 line_number = find_line_number(str(value), lines)
#                 if line_number:
#                     if line_number not in line_numbers:
#                         line_numbers[line_number] = []

#                     line_numbers[line_number].append(value)
#     elif isinstance(data, list):
#         for item in data:
#             find_line_numbers(item, lines, line_numbers)


# def find_line_number(value, lines):
#     for i, line in enumerate(lines):
#         if value in line:
#             return i + 1

#     return None


# # Example usage
# yaml_string = '''
# name: John Smith
# age: 30
# address: 123 Main St
# '''

# result = parse_yaml_string_with_line_numbers(doc)
# for line_number, line_values in result.items():
#     print(f"Line {line_number}: {line_values}")


def parse_yaml_with_line_numbers(yaml_content):
    try:
        parsed_yaml = yaml.safe_load(yaml_content)
        print(parsed_yaml)
    except yaml.YAMLError as e:
        if hasattr(e, 'problem_mark'):
            line = e.problem_mark.line + 1
            column = e.problem_mark.column + 1
            print(f'YAML parsing error at line {line}, column {column}: {e}')
        else:
            print(f'YAML parsing error: {e}')

# Example usage
yaml_content = '''openapi: 3.0
info:
  title: My API
  version: 1.0.0 
paths:
  /users:
  get:
      summary: Get all users
      operationId: getUsers
      responses:
        200:
          description: Successful response'''

parse_yaml_with_line_numbers(yaml_content)