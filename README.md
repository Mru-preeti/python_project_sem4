# EduExtract - AI-Powered Quiz Generation Platform

A Flask-based web application that automatically generates quizzes from PDF documents using Natural Language Processing and Machine Learning techniques.

## 🚀 Features

### Core Functionality

- **PDF Text Extraction**: Automatically extracts text content from uploaded PDF documents
- **AI-Powered Quiz Generation**: Creates three types of quizzes:
  - Multiple Choice Questions (MCQ)
  - Fill-in-the-blank questions
  - Subjective questions
- **Smart Answer Evaluation**: Uses semantic similarity for answer checking
- **Performance Analytics**: Visual charts showing quiz performance over time

### User Management

- User registration and authentication
- Password reset with OTP verification via email
- Session management
- Quiz history tracking

### Additional Features

- **PDF Result Export**: Download quiz results as formatted PDF
- **Email Notifications**: OTP-based password recovery
- **Performance Dashboard**: Graphical representation of quiz scores
- **Responsive Web Interface**: Modern HTML/CSS templates

## 🛠️ Technology Stack

### Backend

- **Flask**: Web framework
- **SQLite**: Database for user data and quiz results
- **PyMuPDF (fitz)**: PDF text extraction
- **NLTK**: Natural language processing
- **Transformers**: Hugging Face models for question generation
- **Sentence Transformers**: Semantic similarity checking
- **Flask-Mail**: Email functionality

### Frontend

- HTML5/CSS3
- JavaScript
- Responsive design

### AI/ML Components

- **Question Generation**: Valhalla T5-small model
- **Semantic Similarity**: SentenceTransformer all-MiniLM-L6-v2
- **NLP Processing**: NLTK for tokenization and POS tagging

## 📋 Prerequisites

- Python 3.8 or higher
- pip (Python package installer)
- Gmail account for email functionality (or modify email settings)

## 🔧 Installation

1. **Clone the repository**

   ```bash
   git clone https://github.com/Mru-preeti/python_project_sem4.git
   cd python_project_sem4-1
   ```

2. **Create a virtual environment**

   ```bash
   python -m venv venv

   # On Windows
   venv\Scripts\activate

   # On macOS/Linux
   source venv/bin/activate
   ```

3. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   ```

4. **Download NLTK data**

   ```python
   python -c "import nltk; nltk.download('averaged_perceptron_tagger'); nltk.download('punkt'); nltk.download('wordnet'); nltk.download('stopwords')"
   ```

5. **Configure email settings**

   - Update the email configuration in `app.py`:

   ```python
   app.config['MAIL_USERNAME'] = 'your-email@gmail.com'
   app.config['MAIL_PASSWORD'] = 'your-app-password'
   ```

6. **Initialize the database**
   ```bash
   python database.py
   ```

## 🚀 Running the Application

1. **Start the Flask application**

   ```bash
   python app.py
   ```

2. **Access the application**
   - Open your web browser and go to `http://localhost:5000`

## 🐳 Docker Deployment

### Quick Start with Docker

1. **Build the Docker image**

   ```bash
   docker build -t eduextract .
   ```

2. **Run the container**
   ```bash
   docker run -p 5000:5000 eduextract
   ```

### Advanced Docker Configuration

**With environment variables:**

```bash
docker run -p 5000:5000 \
  -e FLASK_ENV=production \
  -e MAIL_USERNAME=your-email@gmail.com \
  -e MAIL_PASSWORD=your-app-password \
  eduextract
```

**With volume mounting for persistent data:**

```bash
docker run -p 5000:5000 \
  -v $(pwd)/uploads:/app/uploads \
  -v $(pwd)/*.db:/app/ \
  eduextract
```

**Docker Compose (create docker-compose.yml):**

```yaml
version: "3.8"
services:
  eduextract:
    build: .
    ports:
      - "5000:5000"
    volumes:
      - ./uploads:/app/uploads
      - ./Login_data.db:/app/Login_data.db
    environment:
      - FLASK_ENV=production
      - MAIL_USERNAME=your-email@gmail.com
      - MAIL_PASSWORD=your-app-password
```

### Docker Features

- **Pre-built NLTK data**: NLTK datasets are downloaded during image build
- **System dependencies**: Includes necessary system packages for ML libraries
- **Optimized caching**: Dockerfile layers optimized for faster rebuilds
- **Production ready**: Configured for production deployment

## 📁 Project Structure

```
python_project_sem4-1/
├── app.py                 # Main Flask application
├── database.py            # Database initialization
├── requirements.txt       # Python dependencies
├── dockerfile            # Docker configuration
├── README.md             # Project documentation
├── static/               # CSS, JS, and image files
│   ├── styles.css
│   ├── quiz.css
│   ├── script.js
│   └── ...
├── templates/            # HTML templates
│   ├── login.html
│   ├── home.html
│   ├── quiz.html
│   ├── result.html
│   └── ...
├── uploads/              # PDF file storage
└── *.db                 # SQLite databases
```

## 🎯 Usage Guide

### 1. User Registration/Login

- Register with username, email, and password
- Login with your credentials
- Use forgot password feature if needed

### 2. Creating a Quiz

1. Navigate to the quiz creation page
2. Upload a PDF document
3. Select quiz type (MCQ, Fill-in-blank, or Subjective)
4. The system will automatically generate 5 questions

### 3. Taking a Quiz

1. Answer the generated questions
2. Submit your responses
3. View immediate results with detailed feedback

### 4. Performance Tracking

- View quiz history
- Check performance analytics
- Download results as PDF

## 🔧 Configuration

### Email Settings

Configure SMTP settings in `app.py`:

```python
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'your-email@gmail.com'
app.config['MAIL_PASSWORD'] = 'your-app-password'
```

### Database Configuration

The application uses SQLite by default. Database files:

- `Login_data.db`: User authentication and quiz results
- `quiz.db`: Quiz-specific data
- `your_database.db`: Additional data storage

## 🤖 AI Models Used

1. **Question Generation**: `valhalla/t5-small-qg-hl`

   - Generates questions from text passages
   - Optimized for educational content

2. **Semantic Similarity**: `all-MiniLM-L6-v2`
   - Evaluates answer correctness
   - Provides similarity scores for subjective answers

## 🛡️ Security Features

- Password validation with complexity requirements
- Session management
- OTP-based password recovery
- SQL injection prevention with parameterized queries

## 🐛 Troubleshooting

### Common Issues

1. **Model Download Errors**

   - Ensure stable internet connection
   - Models are downloaded automatically on first use

2. **Email Not Sending**

   - Check Gmail app password configuration
   - Verify SMTP settings

3. **PDF Processing Errors**
   - Ensure PDF is text-based (not scanned images)
   - Check file size limitations

### Error Logs

Check console output for detailed error messages and debugging information.

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 👥 Authors

- **Team Members**: Mru-preeti and contributors
- **Project**: Semester 4 Python Project

## 🙏 Acknowledgments

- Hugging Face for pre-trained models
- NLTK for natural language processing tools
- Flask community for excellent documentation
- PyMuPDF for PDF processing capabilities

## 📞 Support

For support and questions:

- Create an issue on GitHub
- Contact: srushtiprajakt.t@gmail.com

---

**Note**: Make sure to update email credentials and other sensitive configuration before deploying to production.
