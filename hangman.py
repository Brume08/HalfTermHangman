from flask import Flask, render_template
import csv

app = Flask(__name__)


@app.route("/")

def home():
    with open("templates/WordList.csv", newline='') as file:
        
        reader = csv.reader(file)
        data = list(reader)

        



    return render_template("hangman.html")

app.run(debug=True)
