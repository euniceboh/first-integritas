#========================================================================================================
#                                               Dependencies
#========================================================================================================

import re
import json
import ruamel.yaml
from flask_cors import CORS
from flask import Flask, render_template, request, jsonify, make_response

#========================================================================================================
#                                               Routes
#========================================================================================================

app = Flask(__name__)
CORS(app)

@app.route('/') 
def oasChecker():
    return render_template('API Exchange Developer Portal.html')

@app.route('/', defaults={'my_path': ''})
@app.route('/<path:my_path>')
def errorPage(my_path):
    return render_template('404.html')

@app.route('/getLineNumber', methods=['POST', 'GET'])
def getLineNumber():
    '''
    Receives the YAML/JSON document and maps line numbers onto each key value pair - docString
    Receives the path to error identified by Ajv - pathArray
    Calls utility function getLineNumberFromPathArray(docString, pathArray)
    Returns a JSON response with the line number
    '''
    data = request.get_json()
    docString = data.get("doc")
    pathArray = data.get("path")
    yaml = ruamel.yaml.YAML()
    yaml.Constructor = MyConstructor
    try:
        docJson = yaml.load(docString)
    except (ruamel.yaml.parser.ParserError):
        payload = {"message": "Syntax error!"}
        return jsonify(payload)

    lineNumber = getLineNumberFromPathArray(docJson, pathArray)

    payload = {"lineNumber": lineNumber}
    return jsonify(payload)

#========================================================================================================
#                                               Utils
#========================================================================================================

# Modifying subclasses in ruamel.yaml library to map line numbers to each string
class Str(ruamel.yaml.scalarstring.ScalarString):
    '''
    Wrapper around ScalarString constructor overriding __new__ method to create a custom instance of Str
    '''
    __slots__ = ('lc')

    style = ""

    def __new__(cls, value):
        return ruamel.yaml.scalarstring.ScalarString.__new__(cls, value)

class MyPreservedScalarString(ruamel.yaml.scalarstring.PreservedScalarString):
    '''
    Custom subclass of PreservedScalarString to represent a YAML scalar string should preserve line breaks and formatting
    '''
    __slots__ = ('lc')

class MyDoubleQuotedScalarString(ruamel.yaml.scalarstring.DoubleQuotedScalarString):
    '''
    Custom subclass of DoubleQuotedScalarString to represent a YAML scalar string that should be enclosed in double quotes
    '''
    __slots__ = ('lc')

class MySingleQuotedScalarString(ruamel.yaml.scalarstring.SingleQuotedScalarString):
    '''
    Custom subclass of SingleQuotedScalarString to represent a YAML scalar string that should be enclosed in single quotes
    '''
    __slots__ = ('lc')

class MyConstructor(ruamel.yaml.constructor.RoundTripConstructor):
    '''
    Wrapper around RoundTripConstructor overriding construct_yaml_omap() and construct_scalar()
    '''
    def construct_yaml_omap(self, node):
        '''
        Constructs a CommentedOrderedMap based on given YAML for ruamel.yaml to parse
        '''
        omap = ruamel.yaml.comments.CommentedOrderedMap()
        self.construct_mapping(node, omap)
        return omap

    def construct_scalar(self, node):
        '''
        Maps line numbers on top of the constructed CommentedOrderedMap based on the type of strings they are
        '''
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


def getLineNumberFromPathArray(docJson, pathArray):
    '''
    Iterates mapped JSON document based on pathArray
    Returns line number
    '''
    numKeys = len(pathArray)
    if numKeys == 0:
        return 0
    try:
        if numKeys == 1:
            for key in docJson.keys():
                if key == pathArray[-1]:
                    return key.lc.line + 1
        for i in range(numKeys - 1):
            key = pathArray[i]
            try: 
                docJson = docJson[key]    
            except Exception:
                key = float(key) # handle integers or decimals as keys
                docJson = docJson[key]
        for key in docJson.keys():
            if key == pathArray[-1]:
                return key.lc.line + 1
    except Exception:
        return -1 # unexpected error
    

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=80)