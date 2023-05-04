from flask import Flask, render_template, url_for, request, redirect, jsonify, make_response
import wordninja

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
- Spelling check - break up words in subtier
- Check subtier words not using short forms
- Check initial word in subtier is a verb?
- Check all required properties are present
'''

@app.route('/checkOAS', methods=['GET', 'POST'])
def checkOAS():
    if request.method == 'POST':
        result = request.form
        listErrors = []
        print(result.get("title"))

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
                elif len(subtiers) == 6:
                    pathVersionNumber = subtiers[4]
                
                flag = 0
                # Check for camelCasing
                for subtier in subtiers[1:]:
                    subtierWords = wordninja.split(subtier)
                    if (len(subtierWords) > 1):
                        if subtierWords[0][0] != subtierWords[0][0].lower():
                            flag = 1
                        else:
                            for word in subtierWords[1:]:
                                if word[0] != word[0].upper():
                                    flag = 1
                                    break
                    if flag == 1:
                        listErrors.append("The following subtier is not using camel casing: " + subtier)
                    flag = 0
        
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

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0')