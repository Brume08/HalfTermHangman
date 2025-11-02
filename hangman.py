from flask import Flask, render_template, request, session, redirect
import csv
import random

app = Flask(__name__)
app.secret_key = "brume"  


def generate_word():
    wordlist = []

    with open("WordList.csv", "r") as file:
        for line in file:
            wordlist.append(line.strip())  

    selectedWord = random.choice(wordlist)
    return selectedWord.upper()  


def create_list_from_word(selectedWord):
    return list(selectedWord)


def check_letter(letter, wordlist):
    letter = letter.upper()
    positions = [i for i, char in enumerate(wordlist) if char == letter]
    return positions



@app.route("/", methods=["GET", "POST"])
def home():
    
    if "word" not in session:
        session["word"] = generate_word()

    if "guessed" not in session:
        session["guessed"] = []

    if "lives" not in session:
        session["lives"] = 6

    if "status" not in session:
        session["status"] = "playing"
    word = session["word"]
    guessed = session["guessed"]
    lives = session["lives"]
    status = session["status"]
    

    if request.method == "POST" and status == "playing":
        user_letter = request.form["letter"].upper()

       
        if user_letter and user_letter not in guessed:
            guessed.append(user_letter)

            
            if user_letter not in word:
                session["lives"] -= 1
                lives = session["lives"]

           
            if all(char in guessed for char in word):
                session["status"] = "won"
            elif session["lives"] <= 0:
                session["status"] = "lost"

        session["guessed"] = guessed

    
    display = [char if char in guessed else "_" for char in word]

    return render_template(
        "hangman.html",
        display=display,
        lives=session["lives"],
        status=session["status"],
        word=word if session["status"] != "playing" else None,
    )
@app.route("/reset")
def reset():
    session.clear()
    return redirect("/")

if __name__ == "__main__":
    app.run(debug=True)
