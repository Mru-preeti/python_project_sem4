from flask import Flask, render_template, request, redirect
import sqlite3
import os
import fitz # PyMuPDF for extracting text from PDF
import re  # Regular expressions for splitting text
import random
#import PyPDF2
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
        user = cursor.execute("SELECT * FROM USERS WHERE username=? AND password=?", (username, password)).fetchall()
    finally:
        conn.close()  

    if len(user) > 0:
        return render_template('home.html')
    else:
        return redirect('/')
    
@app.route('/signup')
def signup():
    return render_template('signup.html')  # Removed leading slash

@app.route('/add_user', methods=['POST'])
def add_user():
    username = request.form.get('username')
    email_id = request.form.get('email_id')
    password = request.form.get('password') 

    conn = sqlite3.connect('Login_data.db')
    cursor = conn.cursor()

    # Check if the username already exists
    ans = cursor.execute("SELECT * FROM USERS WHERE username=?", (username,)).fetchall()
    if len(ans) > 0:
        conn.close()
        return redirect('/')  # Redirect to login if user exists
    else:
        cursor.execute("INSERT INTO USERS(username, email_id, password) VALUES (?, ?, ?)", (username, email_id, password))
        conn.commit()
        conn.close()
        return redirect('/')  # Redirect to login after signup
@app.route('/prompt1')    
def prompt1():
    return render_template('prompt1.html')
    
@app.route('/upload_pdf', methods=['POST'])
def upload_pdf():
    if "pdf" not in request.files:
        return "No file found"
        
    pdf = request.files["pdf"]
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
            text += page.get_text()  # Correct and intended method
    return text
    
def generate_questions(text, quiz_type):
    questions = []
    sentences = re.split(r'(?<=[.?!])\s+', text.strip())  

    for sentence in sentences:
        words = sentence.split()
        if len(words) > 5:  
            if quiz_type == "fill_in_the_blank":  
                random_word = random.choice(words)
                fill_in_blank = sentence.replace(random_word, "_____")
                questions.append(f"Fill in the blank: {fill_in_blank}")
            elif quiz_type == "mcq":
                correct_answer = random.choice(words)
                wrong_options = random.sample(words, min(3, len(words) - 1))
                options = wrong_options + [correct_answer]
                random.shuffle(options)
                
                mcq = (
                    f"MCQ: {sentence.replace(correct_answer, '_____')}\n"
                    f"Options:\n"
                    f"A) {options[0]}\n"
                    f"B) {options[1]}\n"
                    f"C) {options[2]}\n"
                    f"D) {options[3]}"
                )
                questions.append(mcq)
            elif quiz_type == "subjective":
                questions.append(f"Subjective Question: {sentence}")    

        if len(questions) >= 5:  
            break

    return questions
@app.route('/submit_quiz', methods=['POST'])
def submit_quiz():
    answers = []
    for key in request.form:
        answers.append(request.form[key])  # Collect all submitted answers


if __name__ == '__main__':
    app.run(debug=True)