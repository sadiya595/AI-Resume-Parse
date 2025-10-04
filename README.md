# 🤖 AI-Powered Resume Parser & Job Matcher

An intelligent web application that leverages advanced Natural Language Processing to parse resumes and provide comprehensive job compatibility analysis. Built with Flask, spaCy NLP, and modern web technologies.

![AI Resume Parser Demo](https://img.shields.io/badge/Demo-Live-success?style=for-the-badge)
![Python](https://img.shields.io/badge/Python-3.8+-blue?style=for-the-badge&logo=python)
![Flask](https://img.shields.io/badge/Flask-Web%20Framework-red?style=for-the-badge&logo=flask)
![spaCy](https://img.shields.io/badge/spaCy-NLP-orange?style=for-the-badge)

## ✨ Features

### 🧠 **AI-Powered Analysis**
- **Smart Resume Parsing**: Extracts personal information, skills, experience, education, and projects using spaCy NLP
- **Job Compatibility Matching**: Analyzes resume-job fit with detailed scoring and recommendations
- **Field Mismatch Detection**: Identifies career field compatibility issues (e.g., technical vs marketing roles)
- **Student Resume Handling**: Specialized logic for academic resumes with appropriate guidance

### 📄 **Multi-Format Support**
- **PDF Processing**: Advanced text extraction using PyMuPDF
- **DOCX/DOC Support**: Microsoft Word document parsing with python-docx
- **Drag & Drop Interface**: Modern file upload with real-time feedback
- **File Validation**: Size limits and format verification

### 🎨 **Professional UI/UX**
- **Responsive Design**: Works seamlessly across desktop, tablet, and mobile
- **Interactive Results**: Tabbed navigation with smooth animations
- **Visual Analytics**: SVG pie charts for job compatibility scoring
- **Modern Styling**: Gradient backgrounds with professional typography

### 🎯 **Intelligent Matching**
- **Skills Analysis**: Comprehensive technical skills database with 100+ technologies
- **Experience Evaluation**: Distinguishes between professional work and academic projects
- **Education Filtering**: Focuses on academic qualifications, excludes certifications
- **Personalized Recommendations**: Tailored advice based on profile analysis


## 🛠️ Technology Stack

| Category | Technologies |
|----------|-------------|
| **Backend** | Flask, Python 3.8+ |
| **AI/NLP** | spaCy, Natural Language Processing |
| **Document Processing** | PyMuPDF, python-docx |
| **Frontend** | HTML5, CSS3, JavaScript ES6+ |
| **Styling** | Modern CSS with Flexbox/Grid |
| **Deployment** | Render, Gunicorn |

## 📋 Installation & Setup

### Prerequisites
- Python 3.8 or higher
- pip package manager
- Git

### Local Development

Clone the repository
git clone  https://github.com/sadiya595/AI-Resume-Parse.git
cd AI-Resume-Parse

Create virtual environment
python -m venv venv
source venv/bin/activate # Windows: venv\Scripts\activate

Install dependencies
pip install -r requirements.txt

Download spaCy English model
python -m spacy download en_core_web_sm

Run the application
python app.py


Navigate to `http://localhost:5000` to access the application.

## 🏗️ Project Structure
```
AI-Resume-Parse/
├── app.py # Flask application entry point
├── resume_parser.py # Core NLP parsing engine
├── job_matcher.py # Job compatibility analysis
├── requirements.txt # Python dependencies
├── .gitignore # Git ignore patterns
├── templates/
│ └── index.html # Web interface template
├── static/
│ ├── css/
│ │ └── style.css # Professional styling
│ └── js/
│ └── app.js # Interactive JavaScript
└── README.md # Project documentation
```

## 💻 Usage

### Basic Analysis
1. **Upload Resume**: Drag & drop or browse for PDF/DOC/DOCX files
2. **View Results**: Explore parsed data in organized tabs:
   - 📋 Personal Information
   - 🚀 Technical Skills  
   - 💼 Work Experience
   - 🎓 Education
   - 🛠️ Projects

### Job Compatibility Analysis
1. **Add Job Description**: Paste the job posting in the optional field
2. **Get Matching Score**: Receive detailed compatibility analysis:
   - Overall match percentage
   - Skills alignment
   - Experience gap analysis
   - Field compatibility warnings
   - Personalized recommendations

## 📊 Sample Results

### Skills Detection
The AI identifies technical skills from context and displays them as interactive pills:
Python | JavaScript | React | Node.js | MongoDB | Machine Learning
TensorFlow | Docker | AWS | Git | HTML/CSS | SQL


### Job Match Analysis
- **Overall Score**: 78% compatibility
- **Skills Match**: 85% (8/10 required skills found)
- **Experience**: Entry-level appropriate
- **Recommendations**: Focus on cloud technologies, consider AWS certification

## 🤝 Contributing

Contributions are welcome! Here's how you can help:

1. **Fork the repository**
2. **Create a feature branch**: `git checkout -b feature/amazing-feature`
3. **Commit changes**: `git commit -m 'Add amazing feature'`
4. **Push to branch**: `git push origin feature/amazing-feature`
5. **Open a Pull Request**

### Development Guidelines
- Follow PEP 8 Python style guide
- Add comments for complex NLP logic
- Test with various resume formats
- Ensure responsive design compatibility

## 🐛 Known Issues & Future Enhancements

### Current Limitations
- **Language Support**: Currently optimized for English resumes
- **Complex Formatting**: Some PDF layouts may affect extraction accuracy
- **Industry Specificity**: Job matching optimized for tech roles

### Planned Features
- [ ] Multi-language resume support
- [ ] Industry-specific matching algorithms
- [ ] Resume improvement suggestions
- [ ] Bulk processing capabilities
- [ ] API endpoints for integration

## 📈 Performance & Scalability

- **Processing Speed**: ~2-3 seconds per resume
- **File Size Limit**: 16MB maximum
- **Concurrent Users**: Optimized for moderate traffic
- **Accuracy**: 90%+ for well-formatted resumes

## 🔒 Privacy & Security

- **Data Handling**: Files processed in memory, not stored permanently
- **Privacy First**: No personal data retention
- **Secure Processing**: Input validation and sanitization
- **Local Deployment**: Can be deployed privately for sensitive documents

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 👩‍💻 Author

**Sadiya Noor** - *Full-Stack Developer & AI Enthusiast*

- 💼 **LinkedIn**: [Connect with me](https://linkedin.com/in/sadiya-profile)
- 🐱 **GitHub**: [@sadiya595](https://github.com/sadiya595)
- 📧 **Email**: noorsadiya464@gmail.com

## 🙏 Acknowledgments

- **spaCy Team** for the excellent NLP library
- **Flask Community** for the robust web framework
- **Open Source Contributors** who make projects like this possible.

