# app.py

import os
import json
import google.generativeai as genai
from flask import Flask, render_template, request, send_file, jsonify
from werkzeug.utils import secure_filename
from resume_builder import generate_pdf, generate_cover_letter_pdf

# --- Configuration ---
try:
    genai.configure(api_key=os.environ.get("GOOGLE_API_KEY"))
except AttributeError:
    print("\nFATAL: GOOGLE_API_KEY environment variable not set.")

# --- Flask App Initialization ---
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads/'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)


# --- Routes ---
@app.route('/')
def index():
    return render_template('index.html')


@app.route('/generate-summary', methods=['POST'])
def generate_summary_route():
    if not request.json or 'experience' not in request.json or 'skills' not in request.json:
        return jsonify({"error": "Missing experience or skills data"}), 400
    experience = request.json['experience']
    skills = ", ".join(request.json['skills'])
    experience_text = ""
    for entry in experience:
        responsibilities = "; ".join(entry.get('responsibilities', []))
        experience_text += f"- Title: {entry.get('job_title', '')} at {entry.get('company', '')}. Responsibilities: {responsibilities}\n"

    prompt = f"""
    As a professional resume writer, create a concise professional summary of 3-4 sentences based on these skills and experiences.
    Use strong action verbs and highlight key achievements.
    Skills: {skills}
    Work Experience:\n{experience_text}
    Generated Summary:
    """
    try:
        model = genai.GenerativeModel('gemini-1.5-flash')
        response = model.generate_content(prompt)
        return jsonify({"summary": response.text.strip()})
    except Exception as e:
        return jsonify({"error": f"AI generation failed: {e}"}), 500


# <<< NEW ROUTE ADDED HERE >>>
@app.route('/improvise-section', methods=['POST'])
def improvise_section_route():
    data = request.json
    if not data or 'content' not in data:
        return jsonify({"error": "No content provided"}), 400

    content = data.get('content')
    prompt = f"""
    You are an expert resume editor. Rewrite the following resume bullet points to be more achievement-oriented and professional.
    - Start each point with a strong action verb.
    - Quantify results with numbers or metrics where possible.
    - Keep each point concise and impactful.
    - Return ONLY the rewritten bullet points, each on a new line. Do not add any extra commentary.

    Original points:
    {content}

    Rewritten points:
    """
    try:
        model = genai.GenerativeModel('gemini-1.5-flash')
        response = model.generate_content(prompt)
        improved_points = response.text.strip().split('\n')
        cleaned_points = [point.lstrip('-* ').strip() for point in improved_points if point.strip()]
        return jsonify({"improved_content": cleaned_points})
    except Exception as e:
        return jsonify({"error": f"AI improvisation failed: {e}"}), 500


# <<< MODIFIED ROUTE: Accepts 'tone' >>>
@app.route('/generate-cover-letter', methods=['POST'])
def generate_cover_letter_route():
    data = request.json
    # Added 'tone' to the check
    if not all(key in data for key in ['resumeData', 'jobDescription', 'companyName', 'tone']):
        return jsonify({"error": "Missing required data for cover letter"}), 400

    resume_data = data['resumeData']
    job_description = data['jobDescription']
    company_name = data['companyName']
    tone = data['tone'] # Get the tone from the request

    context = f"""
    My Name: {resume_data.get('name')}
    My Skills: {", ".join(resume_data.get('skills', []))}
    My Experience Summary:
    """
    for exp in resume_data.get('experience', []):
        context += f"- At {exp.get('company')}, I was responsible for: {'; '.join(exp.get('responsibilities', []))}\n"

    # Added the {tone} variable to the prompt
    prompt = f"""
    As a professional job applicant, write a formal and compelling three-paragraph cover letter for a position at {company_name}.
    Adopt a {tone} tone throughout the letter.
    Tailor the letter specifically to the provided job description, using my skills and experience as proof.
    - Paragraph 1: State the position and express genuine interest in the role and {company_name}.
    - Paragraph 2: Connect my skills and experience directly to the key requirements in the job description.
    - Paragraph 3: Reiterate my excitement and include a strong call to action.

    My Information for Context:
    {context}
    Job Description to Apply For:
    {job_description}
    Generated Cover Letter (start with 'Dear Hiring Manager,'):
    """
    try:
        model = genai.GenerativeModel('gemini-1.5-flash')
        response = model.generate_content(prompt)
        return jsonify({"cover_letter_text": response.text.strip()})
    except Exception as e:
        return jsonify({"error": f"AI cover letter generation failed: {e}"}), 500

# --- Unchanged Routes ---
@app.route('/download-cover-letter', methods=['POST'])
def download_cover_letter_route():
    data = request.json
    if not all(key in data for key in ['contactInfo', 'letterText']):
        return jsonify({"error": "Missing data for PDF generation"}), 400
    pdf_buffer = generate_cover_letter_pdf(data)
    return send_file(pdf_buffer, as_attachment=True, download_name='cover_letter.pdf', mimetype='application/pdf')

@app.route('/generate', methods=['POST'])
def generate_resume_route():
    try:
        form_data = json.loads(request.form.get('resumeData'))
        template_name = form_data.get('template', 'classic')
        profile_photo_path = None
        if 'profilePhoto' in request.files:
            file = request.files['profilePhoto']
            if file and file.filename != '':
                filename = secure_filename(file.filename)
                profile_photo_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                file.save(profile_photo_path)
        pdf_buffer = generate_pdf(form_data, template_name, profile_photo_path)
        if profile_photo_path:
            os.remove(profile_photo_path)
        return send_file(pdf_buffer, as_attachment=True, download_name='resume.pdf', mimetype='application/pdf')
    except Exception as e:
        return "An error occurred while generating the resume.", 500

if __name__ == '__main__':
    app.run(debug=True)