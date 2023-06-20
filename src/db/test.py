from flask import Flask
from config import config
import pymysql

app = Flask(__name__)

cnx = pymysql.connect(
    host=config["host"],
    port=config["port"],
    user=config["user"],
    password=config["password"],
    cursorclass=pymysql.cursors.DictCursor
)

cursor = cnx.cursor()

# setup database and table with default words
# whenever the user edits the dictionary, we insert ignore the values into the dictionary
# same for dictionary uploads, it is treated as inserting into the dictionary 
# check for duplicates after insertion

with open('setup.sql', 'r') as setup_file:
    statements = setup_file.readlines()
for statement in statements:
    if statement.strip("/n"):
        cursor.execute(statement)
query = "SELECT * FROM dictionary;"
cursor.execute(query)
rows = cursor.fetchall()
for row in rows:
    print(row["custom_word"]) # key value hard coded here
cnx.commit()

cursor.close()
cnx.close()

if __name__ == '__main__':
    app.run()