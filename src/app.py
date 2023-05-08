from flask import Flask, render_template, url_for, request, redirect, jsonify, make_response
import json
import wordninja
from spellchecker import SpellChecker
import nltk
from nltk.corpus import wordnet as wn

nltk.download("wordnet")

app = Flask(__name__)

@app.route('/')
def home():
    return '<h1>Hello, World!</h1>'

@app.route('/portal1') 
def portal1():
    return render_template('API Exchange Developer Portal.html')

@app.route('/portal2')
def portal2():
    return render_template('API Exchange Developer Portal2.html')

@app.route('/404')
def errorPage():
    return render_template('404.html')


'''
Checks to do:
- Check subtier words not using short forms
- Check all required properties are present
'''

@app.route('/checkOAS', methods=['GET', 'POST'])
def checkOAS():
    if request.method == 'POST':
        result = request.form
        listErrors = []

        # Check for null title
        if result.get("title") == "" or result.get("title") == None:
            listErrors.append("Missing title")
        # Check for null description
        if result.get("description") == "" or result.get("description") == None:
            listErrors.append("Missing description")
        # Check for null x-author
        if result.get("x_author") == "" or result.get("x_author") == None:
            listErrors.append("Missing x-author")
        # Check for null x_date
        if result.get("x_date") == "" or result.get("x_date") == None:
            listErrors.append("Missing x_date")

        path = result.get("path")
        pathVersionNumber = None
        # Check for null path
        if path == " " or path == None:
            listErrors.append("Missing path")
        else:
            # Check for whitespace in path
            if ' ' in path:
                listErrors.append("Whitespace in path")
            # Check for underscore in path
            if '_' in path:
                listErrors.append("Underscore in path")
            # Check for hyphen in path
            if '-' in path:
                listErrors.append("Hyphen in path")
            # Check for missing leading \/
            if path[0] != '/':
                listErrors.append("Path missing leading /")
            else:
                subtiers = path.split("/")
                # Check for length of subtiers in path and extract path version number
                if len(subtiers) < 5:
                    listErrors.append("There needs to be at least one subtier")
                elif len(subtiers) > 6:
                    listErrors.append("Only two subtiers are allowed")
                elif len(subtiers) == 5:
                    pathVersionNumber = subtiers[3]
                    firstSubtierPos = 4
                elif len(subtiers) == 6:
                    pathVersionNumber = subtiers[4]
                    firstSubtierPos = 5


                dictionaryWordsArray = json.loads(result.get("dictionary"))["dictionary"]
                dictionaryWordsArray = [word.lower() for word in dictionaryWordsArray]
                # Check duplicate words in dictionary
                seen = set()
                duplicates = set()
                for word in dictionaryWordsArray:
                    if word not in seen:
                        seen.add(word)
                    else:
                        duplicates.add(word)
                        dictionaryWordsArray.remove(word)
                if duplicates:
                    listErrors.append("The following words are repeated in the dictionary text box: " + ", ".join(duplicates))         

                flag = 0
                wordsNotInDictionary = set()
                for i in range(1, len(subtiers)):
                    subtierWords = wordninja.split(subtiers[i])
                    # Check for words in subtier not in dictionary
                    for word in subtierWords:
                        if ord(word[0]) < 65 or ord(word[0]) > 122 or len(word) == 1:
                            continue
                        if word.lower() not in dictionaryWordsArray:
                            wordsNotInDictionary.add(word)
                    # Check if first word in subtier is a verb
                    if i >= firstSubtierPos:
                        if not checkVerb(subtierWords[0]):
                            listErrors.append("The first word of the following subtier is not a verb: " + subtiers[i])
                    # Check for camelCasing
                    if (len(subtierWords) > 1):
                        if subtierWords[0][0] != subtierWords[0][0].lower():
                            flag = 1
                        else:
                            for word in subtierWords[1:]:
                                if word[0] != word[0].upper():
                                    flag = 1
                                    break
                    if flag == 1:
                        listErrors.append("The following subtier is not using camel casing: " + subtiers[i])
                    flag = 0
        if wordsNotInDictionary:
            listErrors.append("The following words in subtiers are not in the dictionary: " + ", ".join(wordsNotInDictionary))
        
        # Check for null version
        if result.get("version") == "" or result.get("version") == None:
            listErrors.append("Missing doc version")
        else:
            # Check if version numbers match
            docVersionNumber = result.get("version")
            if (pathVersionNumber != None and docVersionNumber.split('.')[0] != pathVersionNumber.replace('v', '')):
                listErrors.append("Version numbers do not match")

        if len(listErrors) == 0:
            payload = {"message": "Done"}
            return make_response(jsonify(payload), 201)
        else:
            payload = {"message": "Not done", "errors": listErrors}
            return make_response(jsonify(payload), 400)
        return render_template('API Exchange Developer Portal.html', result=result, show_errors=True)
    
    else:
        render_template('404.html')

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
    app.run(debug=True, host='0.0.0.0')