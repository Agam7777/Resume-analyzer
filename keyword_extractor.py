import spacy
import re
from collections import Counter
from itertools import combinations
import string

class KeywordExtractor:
    def __init__(self, nlp_model="en_core_web_sm"):
        """Initialize the keyword extractor with a spaCy language model"""
        self.nlp = spacy.load(nlp_model)
        
        # Load skill data
        self.technical_skills = self._load_technical_skills()
        self.soft_skills = self._load_soft_skills()
        self.all_skills = self.technical_skills.union(self.soft_skills)
        
        # Common phrases that indicate experience
        self.experience_phrases = [
            "years of experience", "year experience", "years experience",
            "experienced in", "expertise in", "proficient in", "skilled in",
            "background in", "knowledge of", "familiarity with"
        ]
        
    def _load_technical_skills(self):
        """Load technical skills from a predefined list"""
        # This is a simplified list; in a real application, this could be loaded from a database or file
        skills = {
            # Programming languages
            "python", "java", "javascript", "typescript", "c++", "c#", "ruby", "php", "golang", "swift",
            "kotlin", "rust", "scala", "perl", "r", "matlab", "sql", "nosql", "bash", "powershell",
            
            # Web development
            "html", "css", "react", "angular", "vue", "jquery", "sass", "less", "bootstrap", "tailwind",
            "node.js", "express", "django", "flask", "spring", "laravel", "asp.net", "rails",
            
            # Data science & AI
            "machine learning", "deep learning", "data science", "artificial intelligence", "neural networks",
            "nlp", "computer vision", "data mining", "big data", "statistics", "data analysis",
            "tensorflow", "pytorch", "keras", "scikit-learn", "pandas", "numpy", "tableau", "power bi",
            
            # DevOps & Infrastructure
            "aws", "azure", "gcp", "cloud computing", "docker", "kubernetes", "terraform", "jenkins",
            "ci/cd", "devops", "git", "github", "gitlab", "jira", "agile", "scrum", "linux", "unix",
            
            # Database
            "sql", "mysql", "postgresql", "mongodb", "oracle", "sql server", "redis", "elasticsearch",
            "dynamodb", "cassandra", "neo4j", "graphql", "database design", "data modeling",
            
            # Mobile
            "android", "ios", "react native", "flutter", "xamarin", "swift", "objective-c", "mobile development",
            
            # Other technical
            "rest api", "graphql", "microservices", "serverless", "system architecture", "cybersecurity",
            "blockchain", "networking", "testing", "qa", "seo", "ui/ux", "responsive design"
        }
        return set(skills)
        
    def _load_soft_skills(self):
        """Load soft skills from a predefined list"""
        skills = {
            # Leadership & Management
            "leadership", "management", "team lead", "project management", "strategic planning",
            "decision making", "mentoring", "coaching", "team building", "conflict resolution",
            
            # Communication
            "communication", "presentation", "public speaking", "technical writing", "documentation",
            "interpersonal skills", "negotiation", "client relations", "customer service",
            
            # Collaboration
            "teamwork", "collaboration", "cross-functional", "remote work", "distributed teams",
            
            # Problem solving
            "problem solving", "critical thinking", "analytical skills", "research", "innovation",
            "creativity", "troubleshooting", "debugging",
            
            # Work habits
            "time management", "organization", "multitasking", "attention to detail", "adaptability",
            "flexibility", "self-motivated", "independent", "initiative", "fast learner"
        }
        return set(skills)
    
    def extract_keywords(self, text, top_n=30):
        """Extract important keywords from text using NLP techniques"""
        # Clean and process text
        text = text.lower()
        doc = self.nlp(text)
        
        # Extract potential keywords (nouns, proper nouns, adjectives)
        keywords = []
        for token in doc:
            if token.pos_ in ["NOUN", "PROPN", "ADJ"]:
                # Filter out stopwords and short words
                if not token.is_stop and len(token.text) > 2:
                    keywords.append(token.text)
        
        # Extract noun phrases (for multi-word terms)
        for chunk in doc.noun_chunks:
            clean_chunk = " ".join([token.text for token in chunk if not token.is_stop and len(token.text) > 2])
            if clean_chunk and len(clean_chunk.split()) > 1:
                keywords.append(clean_chunk)
        
        # Count frequencies
        keyword_freq = Counter(keywords)
        
        # Boost frequencies for skills
        for word, count in list(keyword_freq.items()):
            if word in self.all_skills:
                keyword_freq[word] = count * 2  # Give higher weight to recognized skills
        
        return keyword_freq.most_common(top_n)
    
    def extract_skills(self, text):
        """Extract skills from text by matching against skill lists"""
        text = text.lower()
        found_skills = {
            "technical": set(),
            "soft": set()
        }
        
        # Check for direct matches
        words = re.findall(r'\b\w+\b', text)
        for word in words:
            if word in self.technical_skills:
                found_skills["technical"].add(word)
            if word in self.soft_skills:
                found_skills["soft"].add(word)
        
        # Check for multi-word skills
        doc = self.nlp(text)
        for skill in self.all_skills:
            if " " in skill and skill in text:
                if skill in self.technical_skills:
                    found_skills["technical"].add(skill)
                else:
                    found_skills["soft"].add(skill)
        
        return found_skills
    
    def extract_experience_requirements(self, text):
        """Extract experience requirements from job descriptions"""
        text = text.lower()
        experience_reqs = []
        
        # Look for patterns kinda like "X years of experience in Y"
        year_patterns = [
            r'(\d+\+?\s*(?:year|yr)s?\s*(?:of)?\s*experience\s*(?:in|with)?\s*([^,.;]+))',
            r'(\d+\+?\s*(?:to|-)\s*\d+\s*(?:year|yr)s?\s*(?:of)?\s*experience\s*(?:in|with)?\s*([^,.;]+))'
        ]
        
        for pattern in year_patterns:
            matches = re.findall(pattern, text)
            for match in matches:
                full_match = match[0]
                experience_reqs.append(full_match.strip())
        
        # Look for general experience phrases
        for phrase in self.experience_phrases:
            if phrase in text:
                # Get the context around the phrase
                start_idx = text.find(phrase)
                # Get surrounding text (reasonable context)
                start = max(0, start_idx - 30)
                end = min(len(text), start_idx + len(phrase) + 50)
                context = text[start:end]
                # Clean up the context
                context = re.sub(r'\s+', ' ', context).strip()
                if context not in experience_reqs:
                    experience_reqs.append(context)
        
        return experience_reqs
    
    def compare_skills(self, job_skills, resume_skills):
        """Compare job skills against resume skills"""
        job_technical = set(job_skills["technical"])
        job_soft = set(job_skills["soft"])
        resume_technical = set(resume_skills["technical"])
        resume_soft = set(resume_skills["soft"])
        
        results = {
            "technical": {
                "matched": list(job_technical.intersection(resume_technical)),
                "missing": list(job_technical - resume_technical)
            },
            "soft": {
                "matched": list(job_soft.intersection(resume_soft)),
                "missing": list(job_soft - resume_soft)
            }
        }
        
        return results
    
    def get_skill_suggestions(self, missing_skills, max_suggestions=5):
        """Generate suggestions based on missing skills"""
        suggestions = []
        
        # Handle technical skills
        if missing_skills["technical"]:
            tech_skills = missing_skills["technical"][:max_suggestions]
            if len(tech_skills) > 0:
                suggestions.append(f"Add these technical skills to your resume: {', '.join(tech_skills)}")
                
        # Handle soft skills
        if missing_skills["soft"]:
            soft_skills = missing_skills["soft"][:max_suggestions]
            if len(soft_skills) > 0:
                suggestions.append(f"Include these soft skills: {', '.join(soft_skills)}")
        
        return suggestions