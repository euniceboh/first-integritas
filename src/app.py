from flask import Flask, render_template, url_for, request, redirect, jsonify, make_response
import ruamel.yaml
import json
import wordninja
from spellchecker import SpellChecker
import nltk
from nltk.corpus import wordnet as wn
from collections import defaultdict

nltk.download("wordnet")

app = Flask(__name__)

@app.route('/') 
def oasChecker():
    return render_template('API Exchange Developer Portal.html')

@app.route('/swaggeruipreview')
def swaggerUIPreview():
    return render_template('API Exchange Developer Portal2.html')

# @app.errorhandler(404)
@app.route('/', defaults={'my_path': ''})
@app.route('/<path:my_path>')
def errorPage(my_path):
    return render_template('404.html')

'''
Checks to do:
- Check subtier words not using short forms
    E.g., /api/IND/FRM_IND_GetMbrDPSInfo --> /api/IND/FRM_IND_GetMemberPolicyInformation
'''
def checkOpenapi(openapi):
    if openapi == "" or openapi == None:
        return False
    return True

def checkTitle(title):
    if title == "" or title == None:
        return False
    return True

def checkDescription(description):
    if description == "" or description == None:
        return False
    return True

def checkInfoVersion(infoVersion):
    if infoVersion == "" or infoVersion == None:
        return False
    return True

def checkXAuthor(x_author):
    if x_author == "" or x_author == None:
        return False
    return True

def checkXDate(x_date):
    if x_date == "" or x_date == None:
        return False
    return True

def checkPath(paths):
    if paths == None or len(paths) == 0:
        return False
    for path in paths:
        if path == "" or path == None:
            return False
    return True

# need to change to check response for each path
def checkResponse(doc):
    if isinstance(doc, dict):
        if "responses" in doc:
            return True
        for value in doc.values():
            if checkResponse(value):
                return True
    return False
    
def checkPathCharacters(path):
    # Check for whitespaces, underscores, or hyphens in path
    if ' ' in path or '_' in path or '-' in path:
        return False
    return True

def checkPathLeadingSlash(path):
    if path[0] != '/':
        return False
    return True

def checkPathLength(path):
    flag = 0
    subtiers = path.split("/")
    # Length only 5 and 6 allowed, including first index in list due to split
    if len(subtiers) < 5:
        flag = 1
    elif len(subtiers) > 6:
        flag = 2
    return flag

def checkPathVersion(path):
    pathVersion = None
    subtiers = path.split("/")
    # Assuming path version is determined through length of path
    if len(subtiers) == 5:
        pathVersion = subtiers[3]
    elif len(subtiers) == 6:
        pathVersion = subtiers[4]
    if pathVersion == "" or pathVersion == None or not pathVersion[1].isnumeric() or (pathVersion[0] != "v" and pathVersion[0] != "V"):
        return False
    return True
    
def checkMatchingVersion(infoVersion, path):
    subtiers = path.split("/")
    if len(subtiers) == 5:
        pathVersion = subtiers[3][1]
    elif len(subtiers) == 6:
        pathVersion = subtiers[4][1]
    if infoVersion.split('.')[0] != pathVersion:
        return False
    return True

def checkDuplicateDict(dictionary):
    seen = set()
    duplicateDictWords = set()
    for word in dictionary:
        if word.lower() not in seen:
            seen.add(word)
        else:
            duplicateDictWords.add(word)
            # dictionary.remove(word) # Can potentially help developer remove duplicate words automatically
    return duplicateDictWords

def checkPathWordsDict(path, dictionary):
    subtiers = path.split("/")
    dictionaryLower = [word.lower() for word in dictionary]
    wordsNotInDictionary = set()
    for subtier in subtiers[1:]:
        subtierWords = splitSubtierWords(subtier)
        for word in subtierWords:
            if ord(word[0]) < 65 or ord(word[0]) > 122 or len(word) == 1:
                continue
            if word.lower() not in dictionaryLower:
                wordsNotInDictionary.add(word)
    return wordsNotInDictionary

def checkSubtierVerb(path):
    subtiers = path.split("/")
    notVerbSubtiers = []
    if len(subtiers) == 5:
        firstSubtierPos = 4
    elif len(subtiers) == 6:
        firstSubtierPos = 5
    for subtier in subtiers[firstSubtierPos:]:
        subtierWords = splitSubtierWords(subtier)
        if not checkVerb(next(iter(subtierWords))):
            notVerbSubtiers.append(subtier)
    return notVerbSubtiers

def checkCamelCasing(path):
    subtiers = path.split("/")
    notCamelCasing = []
    flag = 0
    for subtier in subtiers[1:]:
        subtierWords = splitSubtierWords(subtier)
        if (len(subtierWords) > 1):
            if subtierWords[0][0] != subtierWords[0][0].lower():
                flag = 1
            else:
                for word in subtierWords[1:]:
                    if word[0] != word[0].upper():
                        flag = 1
                        break
        if flag == 1:
            notCamelCasing.append(subtier)
        flag = 0
    return notCamelCasing

# This function is included as the grammarly plugin cannot detect words that are joined together
def checkPathSpelling(path):
    wrongSubtierSpelling = []
    subtiers = path.split("/")
    for subtier in subtiers[1:]:
        subtierWords = splitSubtierWords(subtier)
        for word in subtierWords:
            if len(word) == 1:
                continue
            if correctSpelling(word) != word:
                wrongSubtierSpelling.append(subtier)
                break
    return wrongSubtierSpelling

# Needs more tests
def checkProperties(k, v, missingProperties):
    # Checks if required properties are not in "properties" list
    try:
        for key, value in v.items():
            checkProperties(key, value, missingProperties)
        if "required" in value.keys():
            requiredProperties = value["required"]
            for requiredProperty in requiredProperties:
                if requiredProperty not in value["properties"].keys():
                    missingProperties.append((key, requiredProperty))
    except (AttributeError):
        pass
    return missingProperties

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

@app.route('/checkOAS', methods=['GET', 'POST'])
def checkOAS():
    if request.method == 'POST':
        result = request.form
        listErrors = [] # storing tuple of (error_message, line number, column number (for non missing fields))
        yaml = ruamel.yaml.YAML()
        yaml.Constructor = MyConstructor

        doc = result.get("doc")
        dictionary = json.loads(result.get("dictionary"))["dictionary"]
        try:
            doc_json = yaml.load(doc)
        # going to remove the syntax error checks as it is not consistent with ace editor
        except (ruamel.yaml.parser.ParserError) as e: # Catches syntax errors that are not caught by ace editor
            # if hasattr(e, 'problem_mark'):
            #     line = e.problem_mark.line + 1
            #     column = e.problem_mark.column + 1
            #     listErrors.append(f'YAML parsing error at line {line}, column {column}: {e}')
            # else: # Catches any other errors that potentially breaks YAML
            #     listErrors.append(f'YAML parsing error: {e}')
            payload = {"message": "Has errors", "errors": [("Syntax error!", 0, 0)]}
            return make_response(jsonify(payload), 400)

        # Components of the YAML file that are checked; possibly to add more according to OAS 3.0
        # Possible to use Schemas to check with PYYAML, but then it will be one error caught at a time
        # Thus, we manually check each component
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
        
        # Check for missing OpenAPI version
        if not checkOpenapi(openapi):
            flag = 0
            for key in doc_json.keys():
                if key == "openapi":
                    flag = 1
                    line = key.lc.line
                    listErrors.append(("Missing openAPI version value", line, -1)) # col = -1 for missing value in field
            if flag == 0:
                listErrors.append(("Missing openAPI field", -1, -1)) # both = -1 for missing field

        # Check for null title
        if not checkTitle(title):
            flag = 0
            for key in doc_json["info"].keys():
                if key == "title":
                    flag = 1
                    line = key.lc.line
                    listErrors.append(("Missing title value", line, -1))
            if flag == 0:
                listErrors.append(("Missing title field", -1, -1))

        # Check for null description
        if not checkDescription(description):
            flag = 0
            for key in doc_json["info"].keys():
                if key == "description":
                    flag = 1
                    line = key.lc.line
                    listErrors.append(("Missing description value", line, -1))
            if flag == 0:
                listErrors.append(("Missing description field", -1, -1))

        # Check for null info version
        if not checkInfoVersion(infoVersion):
            flag = 0
            for key in doc_json["info"].keys():
                if key == "version":
                    flag = 1
                    line = key.lc.line
                    listErrors.append(("Missing version value", line, -1))
            if flag == 0:
                listErrors.append(("Missing version field", -1, -1))

        # Check for null x-author
        if not checkXAuthor(x_author):
            flag = 0
            for key in doc_json["info"].keys():
                if key == "x-author":
                    flag = 1
                    line = key.lc.line
                    listErrors.append(("Missing x-author value", line, -1))
            if flag == 0:
                listErrors.append(("Missing x-author field", -1, -1))

        # Check for null x_date
        if not checkXDate(x_date):
            flag = 0
            for key in doc_json["info"].keys():
                if key == "x-date":
                    flag = 1
                    line = key.lc.line
                    listErrors.append(("Missing x-date value", line, -1))
            if flag == 0:
                listErrors.append(("Missing x-date field", -1, -1))

        # Check for missing responses
        # if not checkResponse(doc_json):
        #     flag = 0
        #     for key in doc_json["info"].keys():
        #         if key == "title":
        #             flag = 1
        #             line = key.lc.line
        #             listErrors.append(("Missing title value", line, -1))
        #     if flag == 0:
        #         listErrors.append(("Missing title field", -1, -1))
        #     listErrors.append("Missing response in API request")

        # Check for null path
        # if not checkPath(paths):
        #     flag = 0
        #     for key in doc_json["paths"].keys():
        #         if key == "x-date":
        #             flag = 1
        #             line = key.lc.line
        #             listErrors.append(("Missing x-date value", line, -1))
        #     if flag == 0:
        #         listErrors.append(("Missing x-date field", -1, -1))
        #     listErrors.append("Missing path(s)")
        # else:
        #     for path in paths:
        #         # Check for illegal characters in path
        #         if not checkPathCharacters(path):
        #             listErrors.append("Illegal characters in path")
            
        #         # Check for leading slash in path
        #         if not checkPathLeadingSlash(path):
        #             listErrors.append("Path missing leading /")
                
        #         # Check for words in path that are not in dictionary
        #         wordsNotInDictionary = checkPathWordsDict(path, dictionary)
        #         if len(wordsNotInDictionary) > 0:
        #             listErrors.append("The following word(s) in subtiers are not in the dictionary: " + ", ".join(wordsNotInDictionary))

        #         # Check for camelCasing
        #         notCamelCasing = checkCamelCasing(path)
        #         if len(notCamelCasing) > 0:
        #             listErrors.append("The following subtier(s) is not using camel casing: " + ", ".join(notCamelCasing))

        #         # Check spelling of subtier words
        #         wrongSubtierSpelling = checkPathSpelling(path)
        #         if len(wrongSubtierSpelling) > 0:
        #             listErrors.append("The following subtier(s) has spelling errors: " + ", ".join(wrongSubtierSpelling))

        #         # Check for path length
        #         pathLengthFlag = checkPathLength(path)
        #         if pathLengthFlag == 1:
        #             listErrors.append("There needs to be at least one subtier in path")
        #         elif pathLengthFlag == 2:
        #             listErrors.append("Only two subtiers are allowed in path")
        #         else:
        #             # Check for null path version
        #             if not checkPathVersion(path):
        #                 listErrors.append("Missing path version")
        #             else:
        #                 # Check for matching info version and path version
        #                 if checkInfoVersion(infoVersion) and not checkMatchingVersion(infoVersion, path):
        #                     listErrors.append("Version numbers do not match")

        #             # Check if first word in subtier is a verb
        #             notVerbSubtiers = checkSubtierVerb(path)
        #             if len(notVerbSubtiers) > 0:
        #                 listErrors.append("The first word of the following subtier(s) is not a verb: " + ", ".join(notVerbSubtiers))


        # # Check for duplicate dictionary words
        # duplicateDictWords = checkDuplicateDict(dictionary)
        # if len(duplicateDictWords) > 0:
        #     listErrors.append("The following word(s) are repeated in the dictionary text box: " + ", ".join(duplicateDictWords)) 

        # # Check all required properties are present
        # missingProperties = []
        # try:
        #     for key, value in doc_json.items():
        #         missingProperties = checkProperties(key, value, missingProperties)
        # except (AttributeError):
        #     pass
        # if len(missingProperties) > 0:
        #     listErrors.append("The following properties are missing from your OAS: " + ", ".join([(missingProperty[1] + " in " + missingProperty[0] + " ==> properties") for missingProperty in missingProperties]))


        if len(listErrors) == 0:
            payload = {"message": "No errors"}
            return make_response(jsonify(payload), 201)
        else:
            payload = {"message": "Has errors", "errors": listErrors}
            return make_response(jsonify(payload), 400)
        return render_template('API Exchange Developer Portal.html', result=result, show_errors=True)
    
    else:
        render_template('404.html')

# Utils
def keysInNestedDictionary_recursive(d):
    keyList = []
    for key, value in d.items():
        keyList.append(key)
        if isinstance(value, dict):
            keyList.extend(keysInNestedDictionary_recursive(value))
    return keyList

def splitSubtierWords(subtier: str):
    words = wordninja.split(subtier)
    return words

def checkVerb(word: str):
    wn.ensure_loaded()
    if (wn.synsets(word, pos=wn.VERB)):
        return True
    return False

# For words in path since Grammarly cannot pick up on joined words
# WARNING: Not very accurate
def correctSpelling(word: str):
    spell = SpellChecker()
    return spell.correction(word)

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=80)