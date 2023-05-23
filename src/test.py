import yaml
from collections import defaultdict

doc = '''
openapi:
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

# def process_yaml_string(yaml_string):
#     lines = yaml_string.split("\n")
#     line_mapping = defaultdict(list)

#     # Track positions of each line occurrence within the YAML string
#     position_mapping = {}
#     current_position = 0
#     for line_number, line in enumerate(lines, start=1):
#         line_mapping[line].append(line_number)
#         position_mapping[line_number] = current_position
#         current_position += len(line) + 1

#     print(line_mapping)
#     print(position_mapping)

#     try:
#         parsed_yaml = yaml.safe_load(yaml_string)
#     except yaml.YAMLError as e: # Syntax errors
#         if hasattr(e, 'problem_mark'):
#             mark = e.problem_mark
#             error_position = position_mapping[mark.line + 1] + mark.column
#             line_number = next( # keeps track of the next item to return in an iteratable without the use of index
#                 line_number for line_number, position in position_mapping.items() if position >= error_position
#             )
#             error_lines = line_mapping[lines[line_number - 1]]
#             print(f"YAML parsing error on line(s) {', '.join(map(str, error_lines))}: {lines[line_number - 1]}")
#         else: # uncaught errors by pyyaml
#             print("YAML parsing error:", e)
    
#     # Other checks
#     openapi = title = description = infoVersion = x_author = x_date = paths = None
#     try:
#         openapi = parsed_yaml["openapi"]
#         title = parsed_yaml["info"]["title"]
#         description = parsed_yaml["info"]["description"]
#         infoVersion = parsed_yaml["info"]["version"]
#         x_author = parsed_yaml["info"]["x-author"]
#         x_date = parsed_yaml["info"]["x-date"]
#         paths = list(parsed_yaml["paths"])
#     except (TypeError): # If the component is not found, it will be handled by the checkFunctions
#         pass
    
#     if openapi == "" or openapi == None:
        

# process_yaml_string(doc)






import ruamel.yaml

yaml_str = """
key1: 
  - key2: item2
  - key3: item3
  - key4:
    - key5: 'item5'
    - key6: |
        item6
"""

class Str(ruamel.yaml.scalarstring.ScalarString):
    __slots__ = ('lc')

    style = ""

    def __new__(cls, value):
        return ruamel.yaml.scalarstring.ScalarString.__new__(cls, value)

class MyPreservedScalarString(ruamel.yaml.scalarstring.PreservedScalarString):
    __slots__ = ('lc')

class MyDoubleQuotedScalarString(ruamel.yaml.scalarstring.DoubleQuotedScalarString):
    __slots__ = ('lc')

class MySingleQuotedScalarString(ruamel.yaml.scalarstring.SingleQuotedScalarString):
    __slots__ = ('lc')

class MyConstructor(ruamel.yaml.constructor.RoundTripConstructor):
    def construct_yaml_omap(self, node):
        omap = ruamel.yaml.comments.CommentedOrderedMap()
        self.construct_mapping(node, omap)
        return omap

    def construct_scalar(self, node):
        # type: (Any) -> Any
        if not isinstance(node, ruamel.yaml.nodes.ScalarNode):
            raise ruamel.yaml.constructor.ConstructorError(
                None, None,
                "expected a scalar node, but found %s" % node.id,
                node.start_mark)

        if node.style == '|' and isinstance(node.value, str):
            ret_val = MyPreservedScalarString(node.value)
        elif bool(self._preserve_quotes) and isinstance(node.value, str):
            if node.style == "'":
                ret_val = MySingleQuotedScalarString(node.value)
            elif node.style == '"':
                ret_val = MyDoubleQuotedScalarString(node.value)
            else:
                ret_val = Str(node.value)
        else:
            ret_val = Str(node.value)
        ret_val.lc = ruamel.yaml.comments.LineCol()
        ret_val.lc.line = node.start_mark.line
        ret_val.lc.col = node.start_mark.column
        return ret_val

def keysInNestedDictionary_recursive(d):
    keyList = []
    for key, value in d.items():
        keyList.append(key)
        if isinstance(value, dict):
            keyList.extend(keysInNestedDictionary_recursive(value))
    return keyList

def main():
  yaml = ruamel.yaml.YAML()
  yaml.Constructor = MyConstructor

  doc_json = yaml.load(doc)

  openapi = title = description = infoVersion = x_author = x_date = paths = None
  try:
      openapi = doc_json["openapi"]
      title = doc_json["info"]["title"]
      description = doc_json["info"]["description"]
      infoVersion = doc_json["info"]["version"]
      x_author = doc_json["info"]["x-author"]
      x_date = doc_json["info"]["x-date"]
      paths = list(doc_json["paths"])
  except (TypeError): # If the component is not found, it will be handled by the checkFunctions
      pass
  
  # keyList = keysInNestedDictionary_recursive(doc_json)
  # for key in keyList:
  #     if key == "post":
  #       print(doc_json[key])
  print(openapi)

  # if openapi == "" or openapi == None:
  #     for key, value in doc_json.items():
  #       print(key.lc.line)
  # else:
  #     print("missing openapi at line" + str(doc_json["openapi"].lc.line))

  # print(doc_json["openapi"].lc.line)
  # print(doc_json["openapi"].lc.col) # no col for omap keys

if __name__ == "__main__":
    main()
