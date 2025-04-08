from flask import Flask, render_template, request, redirect,send_file
import sqlite3
import os
import fitz  # PyMuPDF for extracting text from PDFs
import re
import random
import nltk
import io
import json
from nltk.tokenize import word_tokenize
from nltk import pos_tag
from nltk.corpus import wordnet, stopwords
from flask import session
from fpdf import FPDF
from flask import send_file
from io import BytesIO
from fpdf import FPDF
from flask import send_file, session, redirect



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
        user = cursor.execute("SELECT * FROM USERS WHERE username=? AND password=?", (username, password)).fetchone()
    finally:
        conn.close()

    if user:
        session['username'] = username  # ✅ Store username in session
        return render_template('home.html', username=username)
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

    conn = sqlite3.connect('Login_data.db')
    cursor = conn.cursor()

    ans = cursor.execute("SELECT * FROM USERS WHERE username=?", (username,)).fetchall()
    if len(ans) > 0:
        conn.close()
        return redirect('/')
    else:
        cursor.execute("INSERT INTO USERS(username, email_id, password) VALUES (?, ?, ?)", (username, email_id, password))
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

    if pdf.filename == "":
        return "No file selected"

    file_path = os.path.join(app.config["UPLOAD_FOLDER"], pdf.filename)
    pdf.save(file_path)

    extracted_text = extract_text_from_pdf(file_path)
    questions, correct_answers = generate_questions(extracted_text, quiz_type)
    session['questions'] = questions
    session['correct_answers'] = correct_answers

    return render_template('quiz.html', questions=questions)

def extract_text_from_pdf(pdf_path):
    text = ""
    with fitz.open(pdf_path) as pdf_document:
        for page in pdf_document:
            text += page.get_text()
    return text

def generate_questions(text, quiz_type):
    questions = []
    correct_answers = []
    sentences = re.split(r'(?<=[.?!])\s+', text.strip())

    for sentence in sentences:
        words = word_tokenize(sentence)
        tagged_words = pos_tag(words)

        # Keep only meaningful words (nouns, verbs, adjectives)
        important_words = [word for word, tag in tagged_words if tag.startswith(('NN', 'VB', 'JJ'))]
        
        # Remove stopwords
        filtered_words = [word for word in important_words if word.lower() not in stopwords.words('english')]

        if len(filtered_words) > 0:
            if quiz_type == "fill_in_the_blank":
                random_word = random.choice(filtered_words)
                fill_in_blank = sentence.replace(random_word, "_____")
                questions.append(f"Fill in the blank: {fill_in_blank}")
                correct_answers.append(random_word)


            elif quiz_type == "mcq":
                correct_answer = random.choice(filtered_words)
                wrong_options = generate_distractors(correct_answer)
                
                if len(wrong_options) < 3:
                    continue  # Skip this question if we don't have enough distractors

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
                correct_answers.append(correct_answer.strip())  # ✅ Ensure it's clean

            elif quiz_type == "subjective":
                questions.append(f"Subjective Question: {sentence}")
                correct_answers.append(correct_answer)


        if len(questions) >= 5:
            break

    return questions, correct_answers



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
    import json  # make sure you have this at the top of your file
    questions = session.get('questions',[])
    correct_answers = session.get('correct_answers', [])
    user_answers = []
    detailed_results = []
    score = 0

    for i in range(len(correct_answers)):
        user_answer = request.form.get(f'q{i+1}', '').strip().lower()
        correct_answer = correct_answers[i].strip().lower()
        user_answers.append(user_answer)

        is_correct = user_answer == correct_answer
        if is_correct:
            score += 1

        detailed_results.append({
            'qnum': i + 1,
            'user_answer': user_answer,
            'correct_answer': correct_answer,
            'is_correct': is_correct
        })

    # Store results in the database
    username = session.get('username')  # make sure the user is logged in
    quiz_type = 'mcq'  # optionally change this dynamically
    questions = json.dumps(session.get('questions', []))
    useranswers = json.dumps(user_answers)
    correctanswers = json.dumps(correct_answers)
    score_value = score

    conn = sqlite3.connect('Login_data.db')
    cursor = conn.cursor()

    cursor.execute('''
        INSERT INTO results (username, quiz_type, questions, user_answers, Correctanswer, score)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', (username, quiz_type, questions, useranswers, correctanswers, score_value))

    conn.commit()
    quiz_id = cursor.lastrowid  # Get the ID of the newly inserted quiz
    session['last_quiz_id'] = quiz_id  # ✅ Store it in session
    conn.close()

    return render_template('result.html', score=score, total=len(correct_answers), results=detailed_results)



def remove_unicode(text):
    # Remove any character not supported by latin-1
    return re.sub(r'[^\x00-\xFF]', '', text)

def generate_explanation(question, correct_answer):
    # Dummy explanation
    return f"The answer '{correct_answer}' is correct because it fits the context of the question."

@app.route('/download_result/pdf')
def download_result_pdf():
    if 'username' not in session or 'last_quiz_id' not in session:
        return redirect('/login')
    quiz_id = session['last_quiz_id']
    username = session['username']

    # Fetch from DB
    conn = sqlite3.connect('Login_data.db')
    cursor = conn.cursor()
    results = cursor.execute("""
        SELECT quiz_type, questions, user_answers, Correctanswer, score, timestamp 
        FROM results WHERE username=? and id=?
    """, (username,quiz_id)).fetchall()
    conn.close()

    # Create PDF
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font('Arial', 'B', 14)
    pdf.cell(0, 10, f'Quiz Results for {username}', ln=True, align='C')
    pdf.ln(10)

    for idx, (quiz_type, questions, user_answers, correct_answers, score, timestamp) in enumerate(results, start=1):
        pdf.set_font('Arial', 'B', 12)
        pdf.set_fill_color(230, 230, 230)
        pdf.cell(0, 8, f'Result #{idx} - {timestamp}', ln=True, fill=True)
        pdf.ln(3)

        try:
            q_list = json.loads(questions)
            a_list = json.loads(user_answers)
            c_list = json.loads(correct_answers)
        except:
            q_list = [questions]
            a_list = [user_answers]
            c_list = [correct_answers]

        pdf.set_font('Arial', '', 11)
        for i in range(len(q_list)):
            q = remove_unicode(q_list[i])
            a = remove_unicode(a_list[i])
            c = remove_unicode(c_list[i])
            expl = remove_unicode(generate_explanation(q, c))

            pdf.multi_cell(0, 8, f"Q{i+1}: {q}")
            pdf.multi_cell(0, 8, f"Your Answer: {a}")
            pdf.multi_cell(0, 8, f"Correct Answer: {c}")
            pdf.set_text_color(100, 100, 100)
            pdf.multi_cell(0, 8, f"Explanation: {expl}")
            pdf.set_text_color(0, 0, 0)
            pdf.ln(3)

        pdf.set_font('Arial', 'B', 11)
        pdf.cell(0, 10, f"Total Score: {score}/{len(q_list)}", ln=True)
        pdf.ln(5)

    # Output to BytesIO using dest='S'
    pdf_bytes = BytesIO()
    pdf_output_str = pdf.output(dest='S').encode('latin1')  # Important: encode to latin1
    pdf_bytes.write(pdf_output_str)
    pdf_bytes.seek(0)

    return send_file(pdf_bytes, download_name='quiz_results_clean.pdf', as_attachment=True)




if __name__ == '__main__':
    app.run(debug=True)
