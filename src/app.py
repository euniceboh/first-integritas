import re
import json
import ruamel.yaml
from flask import Flask, render_template, url_for, request, redirect, jsonify, make_response

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
Check subtier word not in short form
Duplicates in dictionary
'''

# Line number mapping on fields
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

# Called from NodeJS server to get line number
@app.route('/getLineNumber', methods=['POST', 'GET"'])
def getLineNumber():
    data = request.get_json()
    docString = data.get("docString")
    pathArray = data.get("pathArray")
    yaml = ruamel.yaml.YAML()
    yaml.Constructor = MyConstructor
    try:
        docJson = yaml.load(docString)
    except (ruamel.yaml.parser.ParserError) as e:
        payload = {"message": "Syntax error!"}
        return jsonify(payload)

    lineNumber = getLineNumberFromPathArray(docJson, pathArray)

    payload = {"lineNumber": lineNumber}
    return jsonify(payload)
    
# Utils

# For each key, iterate through the nested doc
# Edge case if number of keys is 0 or 1
def getLineNumberFromPathArray(docJson, pathArray):
    numKeys = len(pathArray)
    if numKeys == 0:
        return 0
    try:
        if numKeys == 1:
            for key in docJson.keys():
                if key == pathArray[-1]:
                    return key.lc.line + 1
        # Go down the JSON until the last key
        for i in range(numKeys - 1):
            docJson = docJson[pathArray[i]]
        for key in docJson.keys():
            if key == pathArray[-1]:
                return key.lc.line + 1 # because the first line is 0 and the first line in the editor is 1
    except:
        return -1 # path Error somewhere that should not have happened
    

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=80)