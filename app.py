from flask import Flask, render_template, request, redirect
import sqlite3
import os
import fitz  # PyMuPDF for extracting text from PDFs
import re
import fitz  # PyMuPDF for extracting text from PDFs
import re
import random
import nltk
from nltk.tokenize import word_tokenize
from nltk import pos_tag
from nltk.corpus import wordnet, stopwords

nltk.download('averaged_perceptron_tagger')
nltk.download('punkt')
nltk.download('wordnet')
nltk.download('stopwords')


nltk.download('averaged_perceptron_tagger')
nltk.download('punkt')
nltk.download('wordnet')
nltk.download('stopwords')

app = Flask(__name__)
app.secret_key = os.urandom(24)

UPLOAD_FOLDER = "uploads"
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER


@app.route('/')
def login():
    return render_template('login.html')


@app.route('/login_validation', methods=['POST'])
def login_validation():
    username = request.form.get('username')
    password = request.form.get('password')

    conn = sqlite3.connect('Login_data.db')
    cursor = conn.cursor()

    try:
        user = cursor.execute(
            "SELECT * FROM USERS WHERE username=? AND password=?", (username, password)).fetchall()
    finally:
        conn.close()
        conn.close()

    if len(user) > 0:
        return render_template('home.html')
    else:
        return redirect('/')


@app.route('/signup')
def signup():
    return render_template('signup.html')


@app.route('/add_user', methods=['POST'])
def add_user():
    username = request.form.get('username')
    email_id = request.form.get('email_id')
    password = request.form.get('password')
    password = request.form.get('password')

    conn = sqlite3.connect('Login_data.db')
    cursor = conn.cursor()

    ans = cursor.execute(
        "SELECT * FROM USERS WHERE username=?", (username,)).fetchall()
    if len(ans) > 0:
        conn.close()
        return redirect('/')
        return redirect('/')
    else:
        cursor.execute("INSERT INTO USERS(username, email_id, password) VALUES (?, ?, ?)",
                       (username, email_id, password))
        conn.commit()
        conn.close()
        return redirect('/')


@app.route('/prompt1')
def prompt1():
    return render_template('prompt1.html')


@app.route('/upload_pdf', methods=['POST'])
def upload_pdf():
    if "pdf" not in request.files:
        return "No file found"

    pdf = request.files["pdf"]
    quiz_type = request.form.get('quiz_type')
    quiz_type = request.form.get('quiz_type')

    if pdf.filename == "":
        return "No file selected"

    file_path = os.path.join(app.config["UPLOAD_FOLDER"], pdf.filename)
    pdf.save(file_path)

    extracted_text = extract_text_from_pdf(file_path)
    questions = generate_questions(extracted_text, quiz_type)

    return render_template('quiz.html', questions=questions)


def extract_text_from_pdf(pdf_path):
    text = ""
    with fitz.open(pdf_path) as pdf_document:
        for page in pdf_document:
            text += page.get_text()
            text += page.get_text()
    return text


def generate_questions(text, quiz_type):
    questions = []
    sentences = re.split(r'(?<=[.?!])\s+', text.strip())

    for sentence in sentences:
        words = word_tokenize(sentence)
        tagged_words = pos_tag(words)

        # Keep only meaningful words (nouns, verbs, adjectives)
        important_words = [
            word for word, tag in tagged_words if tag.startswith(('NN', 'VB', 'JJ'))
        ]

        # Remove stopwords
        filtered_words = [
            word for word in important_words
            if word.lower() not in stopwords.words('english')
        ]

        if len(filtered_words) > 0:
            if quiz_type == "fill_in_the_blank":
                random_word = random.choice(filtered_words)
                fill_in_blank = sentence.replace(random_word, "_____")
                questions.append({
                    'text': f"Fill in the blank: {fill_in_blank}",
                    'type': 'fill',
                    'options': None,
                    'answer': random_word
                })

            elif quiz_type == "mcq":
                correct_answer = random.choice(filtered_words)
                # Make sure generate_distractors exists!
                wrong_options = generate_distractors(correct_answer)

                if len(wrong_options) < 3:
                    continue

                options = wrong_options + [correct_answer]
                random.shuffle(options)

                question_text = sentence.replace(correct_answer, "_____")
                questions.append({
                    'text': f"MCQ: {question_text}",
                    'type': 'mcq',
                    'options': options,
                    'answer': correct_answer
                })

            elif quiz_type == "subjective":
                questions.append({
                    'text': f"Subjective Question: {sentence}",
                    'type': 'subjective',
                    'options': None,
                    'answer': None
                })

            if len(questions) >= 5:
                break

    return questions


def generate_distractors(word):
    """Generate wrong answer options using synonyms."""
    synonyms = set()
    for syn in wordnet.synsets(word):
        for lemma in syn.lemmas():
            if lemma.name().lower() != word.lower():
                synonyms.add(lemma.name().replace("_", " "))

    return list(synonyms)[:3]  # Return up to 3 wrong options


@app.route('/submit_quiz', methods=['POST'])
def submit_quiz():
    answers = []
    for key in request.form:
        answers.append(request.form[key])

    return render_template('result.html', answers=answers)

    return render_template('result.html', answers=answers)


if __name__ == '__main__':
    app.run(debug=True)
