**AI Resume & Cover Letter Generator ✨**
This web application leverages the power of Google's Gemini AI to help you create professional, tailored resumes and cover letters in minutes. The app provides a user-friendly interface to input your professional details, select a template, and generate high-quality PDF documents.

**Key Features �**�
1. AI-Powered Summary: Automatically generate a concise, professional summary based on your work experience and skills.

2. AI Content Improvisation: Enhance your work experience and project descriptions with a click. The AI rewrites your bullet points to be more achievement-oriented.

3. Tailored Cover Letters: Generate a unique cover letter for any job by simply providing the job description. You can even guide the AI's writing style by selecting a tone (e.g., Professional, Enthusiastic).

4. Multiple PDF Templates: Choose from several professional resume templates to match your style.

5. Dynamic Form: Easily add multiple entries for work experience, education, projects, certifications, and achievements.

6. PDF Downloads: Download both your final resume and cover letter as high-quality PDF files.

**Tech Stack 🛠️**
Backend: Python with Flask

AI Integration: Google Generative AI (Gemini)

PDF Generation: ReportLab

Frontend: HTML, CSS, JavaScript (no complex frameworks)

**Setup and Installation**
Follow these steps to get the project running on your local machine.

1. Clone the Repository
First, clone this repository to your local machine.

Bash

git clone https://github.com/your-username/ai-resume-generator.git
cd ai-resume-generator
2. Create a Virtual Environment (Recommended)
It's best practice to create a virtual environment to manage project dependencies.

Bash

# For Windows
python -m venv venv
venv\Scripts\activate

# For macOS/Linux
python3 -m venv venv
source venv/bin/activate
3. Install Dependencies
Install all the required Python libraries using the following command:

Bash

pip install Flask google-generativeai reportlab Pillow
4. Set Your API Key
This project requires a Google AI API key to function.

Get your free API key from Google AI Studio.

Set it as an environment variable in your terminal. This is a secure way to handle your key without hardcoding it.

On Windows (Command Prompt):

DOS

set GOOGLE_API_KEY="YOUR_API_KEY_HERE"
On macOS/Linux:

Bash

export GOOGLE_API_KEY="YOUR_API_KEY_HERE"
Note: You must set this variable every time you open a new terminal session, or add it to your shell's startup file (e.g., .bashrc, .zshrc).

5. Run the Application
With your environment set up and the API key configured, run the Flask app:

Bash

python app.py
The application will start, and you'll see a message in the terminal indicating it's running, usually on http://127.0.0.1:5000.

Open this URL in your web browser to start using the generator!

Project Structure
The project is organized into a standard Flask application structure:

/
├── app.py                  # Main Flask application, handles routing and AI logic
├── resume_builder.py       # Handles all PDF generation logic with ReportLab
├── static/
│   └── styles.css          # All frontend styling
└── templates/
    └── index.html          # The main HTML file with the user interface and JavaScript
How to Use
Fill in Your Details: Start by filling in your personal information, work experience, education, skills, and any other relevant sections.

**Generate AI Content:**
Click ✨ Generate AI Summary to create your professional summary.

Inside each work or project entry, click ✨ Improvise to enhance your bullet points.

Create a Cover Letter:

Scroll down to the Cover Letter section.

Enter the company name and paste the job description.

Select a writing tone.

Click ✨ Generate AI Cover Letter.

Download: Click the Download Resume PDF or Download Cover Letter PDF buttons to get your final documents.
