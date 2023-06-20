import re
import json
import ruamel.yaml
import pymysql
from db.config import config
from flask import Flask, render_template, request, jsonify, make_response

app = Flask(__name__)

@app.after_request
def add_cors_headers(response):
    response.headers['Access-Control-Allow-Origin'] = 'http://127.0.0.1'
    return response

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

# Read database
@app.route('/db/get', methods=["GET", "POST"])
def getDictionary():
    dictionaryArray = []
    try:
        cnx = pymysql.connect(
            host=config["host"],
            port=config["port"],
            user=config["user"],
            password=config["password"],
            cursorclass=pymysql.cursors.DictCursor
        )
        cursor = cnx.cursor()

        with open('src/db/setup.sql', 'r') as setup_file:
            statements = setup_file.readlines()
        for statement in statements:
            if statement.strip("/n"):
                cursor.execute(statement)

        query = "SELECT * FROM dictionary;"
        cursor.execute(query)
        rows = cursor.fetchall()
        for row in rows:
            dictionaryArray.append(row["custom_word"]) # key value hard coded here
        cnx.commit()
        cursor.close()
        cnx.close()

        payload = {"dictionaryArray": dictionaryArray}
    except Exception as e:
        payload = {"dictionaryArray": []}
        return make_response(jsonify(payload), 400)
    return make_response(jsonify(payload), 200)

# Update database
@app.route('/db/edit', methods=["GET", "POST"])
def editDictionary():
    data = request.get_json()
    dictionaryArray = data.get("dictionaryArray")
    if len(dictionaryArray) > 0:
        try:
            cnx = pymysql.connect(
                host=config["host"],
                port=config["port"],
                user=config["user"],
                password=config["password"],
                database=config["database"],
                cursorclass=pymysql.cursors.DictCursor
            )
            cursor = cnx.cursor()
            
            # There is no way to know how much the user might erase or add to the dictionary
            # So we refresh the dictionary each time the user edits it then add all the words again
            # Handle duplicates afterwards
            query = "DELETE FROM dictionary;"
            cursor.execute(query)
            query = "INSERT INTO dictionary VALUES (%s);"
            for word in dictionaryArray:
                cursor.execute(query, (word,))
            query = "DELETE FROM dictionary WHERE custom_word IN (SELECT t1.word1 FROM (SELECT LOWER(custom_word) AS word1 FROM dictionary) t1 JOIN(SELECT LOWER(custom_word) AS word2 FROM dictionary GROUP BY LOWER(custom_word) HAVING COUNT(*) > 1) t2 ON t1.word1 = t2.word2);"
            cursor.execute()
            cnx.commit()
            cursor.close()
            cnx.close()
        except:
            return False
    return True


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
@app.route('/getLineNumber', methods=['POST', 'GET'])
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
            key = pathArray[i]
            try:
                key = float(key)
            except:
                pass
            docJson = docJson[key]
        for key in docJson.keys():
            if key == pathArray[-1]:
                return key.lc.line + 1 # because the first line is 0 and the first line in the editor is 1
    except:
        return -1 # path error somewhere that should not have happened
    

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=80)