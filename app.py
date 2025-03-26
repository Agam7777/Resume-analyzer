from flask import Flask, request, render_template, jsonify, redirect, url_for
import os
import docx2txt
import PyPDF2
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import spacy
import re
from collections import Counter

# Initialize Flask app
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads/'

# Load NLP model
nlp = spacy.load("en_core_web_sm")

# Define domain-specific keywords for software engineering
SOFTWARE_ENGINEERING_DOMAIN = {
    'software', 'developer', 'engineer', 'programming', 'code', 'java', 'python', 'c++',
    'algorithm', 'data structure', 'backend', 'frontend', 'full stack', 'api', 'cloud',
    'devops', 'agile', 'scrum', 'version control', 'git', 'database', 'sql', 'nosql',
    'machine learning', 'ai', 'computer vision', 'nlp', 'web development', 'mobile development'
}

def extract_text_from_pdf(file_path):
    text = ""
    with open(file_path, 'rb') as file:
        reader = PyPDF2.PdfReader(file)
        for page in reader.pages:
            text += page.extract_text()
        
    return text

def extract_text_from_docx(file_path):
    return docx2txt.process(file_path)

def extract_text_from_txt(file_path):
    with open(file_path, 'r', encoding='utf-8', errors='ignore') as file:
        return file.read()

def extract_text(file_path):
    if file_path.endswith('.pdf'):
        return extract_text_from_pdf(file_path)
    elif file_path.endswith('.docx'):
        return extract_text_from_docx(file_path)
    elif file_path.endswith('.txt'):
        return extract_text_from_txt(file_path)
    else:
        return ""

def extract_keywords(text, top_n=20):
    """Extract important keywords from text using spaCy"""
    doc = nlp(text)
    
    # Enhanced filtering
    keywords = [
        token.lemma_.lower() for token in doc
        if token.pos_ in ["NOUN", "PROPN"]
        and not token.is_stop
        and len(token.text) > 2
        and token.text.lower() not in {'resume', 'cv', 'improvement'}
    ]
    
    # Add multi-word phrases
    keywords += [
        chunk.text.lower() for chunk in doc.noun_chunks
        if len(chunk.text.split()) > 1
    ]
    
    keyword_freq = Counter(keywords)
    return keyword_freq.most_common(top_n)

def extract_skills(text):
    """Extract skills from text by matching against common skills list"""
    doc = nlp(text.lower())
    found_skills = set()
    
    # Extract single-word skills
    for token in doc:
        if token.text.lower() in COMMON_SKILLS:
            found_skills.add(token.text.lower())
    
    # Extract multi-word skills using regex patterns
    for skill in MULTI_WORD_SKILLS:
        if re.search(r'\b' + re.escape(skill) + r'\b', text.lower()):
            found_skills.add(skill)
            
    return list(found_skills)

def analyze_resume_structure(text):
    """Analyze resume structure and provide suggestions"""
    suggestions = []
    
    # Check length
    words = text.split()
    if len(words) < 300:
        suggestions.append("Your resume seems short. Consider adding more details about your experience and skills.")
    elif len(words) > 1000:
        suggestions.append("Your resume is quite lengthy. Consider condensing it to highlight your most relevant experiences.")
    
    # Check for bullet points
    if text.count('•') < 5 and text.count('-') < 5:
        suggestions.append("Consider using bullet points to make your achievements and responsibilities more readable.")
    
    # Check for action verbs
    action_verbs_count = sum(1 for word in words if word.lower() in ACTION_VERBS)
    if action_verbs_count < 10:
        suggestions.append("Add more action verbs (like 'achieved', 'managed', 'developed') to make your accomplishments stand out.")
    
    # Check for quantifiable achievements
    numbers = re.findall(r'\b\d+%|\b\d+\b', text)
    if len(numbers) < 5:
        suggestions.append("Try to quantify your achievements with numbers (e.g., 'increased sales by 20%').")
    
    return suggestions

def calculate_weighted_similarity(job_text, resume_text):
    """Calculate a weighted similarity score based on skills, domain, experience, and education"""
    # Extract skills from job description and resume
    job_skills = extract_skills(job_text)
    resume_skills = extract_skills(resume_text)
    
    # Calculate skill overlap (partial matching)
    skill_overlap = len(set(job_skills).intersection(resume_skills)) / len(job_skills) if job_skills else 0
    
    # Check domain alignment (less strict)
    domain_alignment = 1 if is_domain_aligned(resume_text, SOFTWARE_ENGINEERING_DOMAIN) else 0
    
    # Check experience and education alignment (new factor)
    experience_alignment = 1 if "intern" in resume_text.lower() or "experience" in resume_text.lower() else 0
    education_alignment = 1 if "computer science" in resume_text.lower() or "software engineering" in resume_text.lower() else 0
    
    # Weighted similarity score
    weighted_similarity = (
        0.5 * skill_overlap + 
        0.2 * domain_alignment + 
        0.2 * experience_alignment +  
        0.1 * education_alignment 
    )

    # to do: currenly, if num experience > required experience, then domain relevance is not accounted for, 
    # domain alignment comes before the num years experience check, change hierarchy of analysis 
    
    return round(weighted_similarity * 100, 2)

def is_domain_aligned(resume_text, domain_keywords):
    """Check if the resume aligns with the job domain (less strict)"""
    resume_tokens = set(resume_text.lower().split())
    domain_overlap = resume_tokens.intersection(domain_keywords)
    return len(domain_overlap) >= 1  # At least 1 domain-specific keyword

def generate_improvement_suggestions(job_text, resume_text):
    """Generate suggestions to improve resume based on job description"""
    suggestions = []
    
    # Extract job skills
    job_skills = extract_skills(job_text)
    
    # Extract resume skills
    resume_skills = extract_skills(resume_text)
    
    # Identify missing skills
    missing_skills = [skill for skill in job_skills if skill not in resume_skills]
    
    # Generate skill suggestions
    if missing_skills:
        if len(missing_skills) > 5:
            suggestions.append(f"Consider adding these key skills: {', '.join(missing_skills[:5])}, and others.")
        else:
            suggestions.append(f"Consider adding these key skills: {', '.join(missing_skills)}.")
    
    # Check domain alignment
    if not is_domain_aligned(resume_text, SOFTWARE_ENGINEERING_DOMAIN):
        suggestions.append("Your resume could better align with the software engineering domain. Consider highlighting relevant technical experience.")
    
    # Add structure suggestions
    structure_suggestions = analyze_resume_structure(resume_text)
    suggestions.extend(structure_suggestions)
    
    return suggestions
    
@app.route("/")
def home():
    return render_template('home.html')

@app.route("/batch-analysis")
def batch_analysis():
    return render_template('batch_analysis.html')

@app.route("/single-analysis")
def single_analysis():
    return render_template('single_analysis.html')

@app.route('/matcher', methods=['POST'])
def matcher():
    if request.method == 'POST':
        job_description = request.form['job_description']
        resume_files = request.files.getlist('resumes')
        
        if not resume_files or not job_description or resume_files[0].filename == '':
            return redirect(url_for('home'))  # Redirect to home page
        
        # Create upload folder if it doesn't exist
        if not os.path.exists(app.config['UPLOAD_FOLDER']):
            os.makedirs(app.config['UPLOAD_FOLDER'])
        
        resumes = []
        resume_texts = []
        for resume_file in resume_files:
            filename = os.path.join(app.config['UPLOAD_FOLDER'], resume_file.filename)
            resume_file.save(filename)
            
            # Extract text
            text = extract_text(filename)
            resumes.append({
                'filename': resume_file.filename,
                'text': text
            })
            resume_texts.append(text)
        
        # Calculate similarities
        results = []
        for i, resume in enumerate(resumes):
            similarity = calculate_weighted_similarity(job_description, resume['text'])
            suggestions = generate_improvement_suggestions(job_description, resume['text'])
            
            results.append({
                'filename': resume['filename'],
                'similarity': similarity,
                'suggestions': suggestions
            })
        
        # Sort results by similarity
        results.sort(key=lambda x: x['similarity'], reverse=True)
        
        return render_template('results.html', 
                              job_description=job_description, 
                              results=results[:10])
    
    return redirect(url_for('home'))

@app.route('/analyze', methods=['POST'])
def analyze_single_resume():
    if request.method == 'POST':
        job_description = request.form['job_description']
        
        # Check if file is uploaded
        if 'resume' not in request.files or request.files['resume'].filename == '':
            return redirect(url_for('home'))  # Redirect to home page
        
        resume_file = request.files['resume']
        
        # Create upload folder if it doesn't exist
        if not os.path.exists(app.config['UPLOAD_FOLDER']):
            os.makedirs(app.config['UPLOAD_FOLDER'])
        
        # Save file
        filename = os.path.join(app.config['UPLOAD_FOLDER'], resume_file.filename)
        resume_file.save(filename)
        
        # Extract text
        resume_text = extract_text(filename)
        
        # Generate suggestions
        suggestions = generate_improvement_suggestions(job_description, resume_text)
        
        # Calculate similarity
        similarity = calculate_weighted_similarity(job_description, resume_text)
        
        result = {
            'filename': resume_file.filename,
            'similarity': similarity,
            'suggestions': suggestions
        }
        
        return render_template('analyze.html', 
                               job_description=job_description, 
                               result=result)
    
    return redirect(url_for('home'))

# Common skills database (simplified version)
COMMON_SKILLS = {
    'python', 'java', 'javascript', 'html', 'css', 'sql', 'nosql', 'react', 'angular', 'vue', 
    'node', 'django', 'flask', 'spring', 'docker', 'kubernetes', 'aws', 'azure', 'gcp', 
    'machine learning', 'data analysis', 'statistics', 'ai', 'nlp', 'computer vision',
    'leadership', 'communication', 'teamwork', 'project management', 'agile', 'scrum',
    'testing', 'ci/cd', 'git', 'github', 'gitlab', 'jira', 'excel', 'powerpoint', 'word',
    'research', 'analysis', 'design', 'marketing', 'sales', 'customer service', 'operations',
    'finance', 'accounting', 'hr', 'recruitment', 'training'
}

MULTI_WORD_SKILLS = {
    'machine learning', 'data science', 'artificial intelligence', 'project management',
    'business intelligence', 'data analysis', 'natural language processing', 'computer vision',
    'user experience', 'user interface', 'front end', 'back end', 'full stack',
    'continuous integration', 'continuous deployment', 'version control'
}

ACTION_VERBS = {
    'achieved', 'improved', 'trained', 'managed', 'created', 'resolved', 'negotiated',
    'presented', 'developed', 'implemented', 'designed', 'launched', 'increased',
    'decreased', 'reduced', 'expanded', 'delivered', 'generated', 'led', 'organized',
    'produced', 'supervised', 'streamlined', 'strengthened', 'transformed'
}

if __name__ == '__main__':
    app.run(debug=True)