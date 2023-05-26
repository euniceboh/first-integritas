import re
import yaml
from collections import defaultdict
from pykwalify.core import Core
from pykwalify.errors import SchemaError

doc = '''openapi: 3.0.0
info:
  title: grvrws
  description: This API is to update the crediting status of the member's 55 WDL Application for PayNow
  version: 1.0.0
  x-author: 
  x-date: '2022-12-22'

paths:
  dummy:
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

def flattenDict(d):
    keyValueList = []
    for key, value in d.items():
        if value == None:
            keyValueList.append((key, None))
        else:
            keyValueList.append((key, value))
        if isinstance(value, dict):
            keyValueList.extend(flattenDict(value))
    return keyValueList

def is_key_nested(dictionary, parent_key, nested_key):
    if parent_key in dictionary and nested_key in dictionary[parent_key]:
        return True
    
    for value in dictionary.values():
        if isinstance(value, dict):
            if is_key_nested(value, parent_key, nested_key):
                return True
            elif nested_key in value:
                return True
    
    return False


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
    
def getLineNumberFromPath(doc, path):
    if path == "":
        return True
    keysArray = path.split("/")

    for i in range(len(keysArray)):
        for j in range(i, len(keysArray)):
            key = "/".join([keysArray[x] for x in range(i, j + 1)])
            try:
                new_doc = doc[key]
            except:
                continue
            new_keysArray = keysArray.copy()
            new_keysArray = new_keysArray[:i] + new_keysArray[(j + 1):]
            new_path = "/".join(new_keysArray)
            res = getLineNumberFromPath(new_doc, new_path)
            if res == True:
                try:
                    return doc[key].lc.line
                except:
                    return doc.lc.line
            elif res != False:
                return res
    return False

def parse_error(error):
    # Extract the error path using regular expression
    path_regex = r": '([^']*)'"
    path_match = re.search(path_regex, error)
    if path_match:
        error_path = path_match.group(1)
    else:
        error_path = ""

    # Extract the error message by removing the path from the error and some additional processing
    error_message = re.sub(path_regex, "", error).strip()

    # Check if the error message contains enum information
    enum_values = None
    enum_regex = r"Enum: \[(.+)\]"
    enum_match = re.search(enum_regex, error_message)
    if enum_match:
        enum_values = enum_match.group(1)
        error_message = re.sub(enum_regex, "", error_message).strip()


    # Check if the error message contains regex validation error
    regex_string = None
    regex_error_regex = r"Key '(.+)' does not match any regex '(.+)'\."
    regex_error_match = re.search(regex_error_regex, error_message)
    if regex_error_match:
        key = regex_error_match.group(1)
        regex_string = regex_error_match.group(2)
        error_message = f"Key '{key}' invalid value."
    
    # Additional processing
    if "Path ." in error_message:
      error_message = error_message.replace("Path .", "")
    if "Path." in error_message:
      error_message = error_message.replace("Path.", "")
    if "required.novalue" in error_message:
      property = error_path.split("/")[-1]
      error_message = f"Should have required value '{property}'"
    
    # Additional properties that should not be in the doc
    property_match = re.findall(r"Key '([^']*)' was not defined", error_message)
    if property_match:
        additional_property = property_match[0]
        error_message = f"Should not have additional key '{additional_property}'"



    return error_path, error_message, enum_values, regex_string


def main():
  yaml = ruamel.yaml.YAML()
  yaml.Constructor = MyConstructor

  doc_json = yaml.load(doc)

  # openapi = title = description = infoVersion = x_author = x_date = paths = None
  # try:
  #     openapi = doc_json["openapi"]
  #     title = doc_json["info"]["title"]
  #     description = doc_json["info"]["description"]
  #     infoVersion = doc_json["info"]["version"]
  #     x_author = doc_json["info"]["x-author"]
  #     x_date = doc_json["info"]["x-date"]
  #     paths = list(doc_json["paths"])
  # except (TypeError): # If the component is not found, it will be handled by the checkFunctions
  #     pass
  
  # keyList = keysInNestedDictionary_recursive(doc_json)
  # for key in keyList:
  #     if key == "post":
  #       print(doc_json[key])
  # print(flattenDict(doc_json))

  # if openapi == "" or openapi == None:
  #     for key, value in doc_json.items():
  #       print(key.lc.line)
  # else:
  #     print("missing openapi at line" + str(doc_json["openapi"].lc.line))

  # print(doc_json["openapi"].lc.line)
  # print(doc_json["openapi"].lc.col) # no col for omap keys


  try:
    c = Core(source_data=doc_json, schema_files=["schema1.yaml"])
    c.validate()
  except SchemaError as e:
      errors = e.msg
      for error in errors.split("\n")[1:]:
          error_path, error_message, enum_values, regex_string = parse_error(error)
          if regex_string == "^/":
              print(error_path)
          print("Error Path:", error_path)
          print("Error line", getLineNumberFromPath(doc_json, error_path))
          print("Error Message:", error_message)
          print("Enum values:", enum_values)
          print("Error regex string:", regex_string)
          print()
  
  # try:
  #     paths = list(doc_json["paths"])
  #     for path in paths:
  #         # check 
  # except:
  #     pass


if __name__ == "__main__":
    main()
