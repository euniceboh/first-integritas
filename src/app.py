from flask import Flask, render_template

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

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0')