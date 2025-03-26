class ResumeAnalyzer:
    def __init__(self):
        """Initialize the resume analyzer with common patterns to look for"""
        # Common action verbs that make resumes more impactful
        self.action_verbs = {
            "achieved", "improved", "trained", "managed", "created", "resolved", "negotiated",
            "presented", "developed", "implemented", "designed", "launched", "increased",
            "decreased", "reduced", "expanded", "delivered", "generated", "led", "organized",
            "produced", "supervised", "streamlined", "strengthened", "transformed", "facilitated",
            "coordinated", "established", "executed", "formulated", "accelerated", "automated",
            "built", "boosted", "calculated", "captured", "centralized", "championed", "clarified",
            "compiled", "condensed", "conducted", "constructed", "counseled", "customized", "debugged",
            "directed", "doubled", "eliminated", "enabled", "engineered", "enhanced", "evaluated",
            "exceeded", "expedited", "founded", "guided", "identified", "illustrated", "initiated",
            "innovated", "installed", "instituted", "instructed", "integrated", "introduced",
            "invented", "leveraged", "maintained", "marketed", "maximized", "minimized", "modernized",
            "motivated", "navigated", "negotiated", "operated", "optimized", "orchestrated", "overhauled",
            "pioneered", "planned", "prepared", "programmed", "promoted", "provided", "re-engineered",
            "rebuilt", "redesigned", "refined", "remodeled", "repaired", "replaced", "restored",
            "restructured", "revamped", "reviewed", "revitalized", "saved", "secured", "selected",
            "simplified", "solved", "sorted", "spearheaded", "standardized", "stimulated", "synthesized",
            "systematized", "tested", "trained", "unified", "upgraded", "utilized", "validated", "won"
        }
        
        # Weak words that should be avoided or replaced
        self.weak_words = {
            "responsible for", "duties included", "helped", "worked on", "assisted with",
            "involved in", "participated in", "supported", "dealt with", "handled"
        }
        
        # Common resume sections
        self.resume_sections = {
            "summary": ["summary", "professional summary", "profile", "about me", "objective"],
            "experience": ["experience", "work experience", "employment history", "work history", "professional experience"],
            "education": ["education", "academic background", "academic history", "qualifications"],
            "skills": ["skills", "technical skills", "competencies", "abilities", "expertise"],
            "projects": ["projects", "personal projects", "key projects", "professional projects"],
            "certifications": ["certifications", "certificates", "licenses", "professional development"],
            "awards": ["awards", "honors", "achievements", "recognition"],
            "publications": ["publications", "papers", "research", "articles"],
            "languages": ["languages", "language proficiency", "language skills"],
            "interests": ["interests", "hobbies", "activities"]
        }
    
    def analyze_structure(self, text):
        """Analyze the structure of a resume and provide suggestions"""
        sections_found = self._detect_sections(text.lower())
        return {
            "content_suggestions": self._analyze_content(text),
            "structure_suggestions": self._analyze_structure(sections_found, text),
            "action_verb_suggestions": self._analyze_action_verbs(text),
            "length_suggestions": self._analyze_length(text),
            "bullet_point_suggestions": self._analyze_bullet_points(text),
            "weak_language_suggestions": self._analyze_weak_language(text),
            "quantification_suggestions": self._analyze_quantification(text)
        }
    
    def _detect_sections(self, text):
        """Detect which sections are present in the resume"""
        sections_found = {section_type: False for section_type in self.resume_sections}
        
        # Check for each section
        for section_type, keywords in self.resume_sections.items():
            for keyword in keywords:
                # Look for section headers (often followed by newlines or colons)
                if any(pattern in text for pattern in [
                    f"\n{keyword}\n", 
                    f"\n{keyword}:", 
                    f"\n{keyword.upper()}\n", 
                    f"\n{keyword.upper()}:",
                    f"\n{keyword.title()}\n",
                    f"\n{keyword.title()}:"
                ]):
                    sections_found[section_type] = True
                    break
        
        return sections_found
    
    def _analyze_structure(self, sections_found, text):
        """Analyze the structure based on sections found"""
        suggestions = []
        
        # Check for missing essential sections
        essential_sections = ["summary", "experience", "education", "skills"]
        missing_sections = [section for section in essential_sections if not sections_found[section]]
        
        if missing_sections:
            sections_str = ", ".join(missing_sections).title()
            suggestions.append(f"Your resume appears to be missing these key sections: {sections_str}.")
        
        # Check for order of sections
        if sections_found["summary"] and sections_found["experience"]:
            if text.lower().find("summary") > text.lower().find("experience"):
                suggestions.append("Consider placing your Professional Summary before your Work Experience section.")
        
        return suggestions
    
    def _analyze_content(self, text):
        """Analyze the overall content quality"""
        suggestions = []
        
        # Check for personal pronouns (should be avoided in resumes)
        personal_pronouns = ["i", "me", "my", "mine", "myself", "we", "us", "our", "ours", "ourselves"]
        if any(f" {pronoun} " in f" {text.lower()} " for pronoun in personal_pronouns):
            suggestions.append("Avoid using personal pronouns (I, me, my) in your resume. Use action verbs instead.")
        
        # Check for complete contact information
        contact_patterns = ["phone", "email", "linkedin", "@"]
        found_contacts = [pattern for pattern in contact_patterns if pattern in text.lower()]
        if len(found_contacts) < 2:
            suggestions.append("Make sure your resume includes complete contact information (phone, email, LinkedIn).")
        
        return suggestions
    
    def _analyze_action_verbs(self, text):
        """Analyze the use of action verbs"""
        suggestions = []
        
        # Count action verbs used
        words = set(text.lower().split())
        action_verbs_used = [word for word in self.action_verbs if word in words]
        
        if len(action_verbs_used) < 5:
            suggestions.append("Add more action verbs to strengthen your resume. Start bullet points with verbs like 'achieved', 'delivered', or 'implemented'.")
        
        return suggestions
    
    def _analyze_length(self, text):
        """Analyze the length of the resume"""
        suggestions = []
        
        # Count words
        words = text.split()
        word_count = len(words)
        
        if word_count < 300:
            suggestions.append("Your resume seems too short. Consider adding more details about your experience and achievements.")
        elif word_count > 800:
            suggestions.append("Your resume may be too long. Try to keep it concise and focused on the most relevant information.")
        
        # Count lines
        lines = text.split("\n")
        line_count = len(lines)
        
        if line_count > 60:
            suggestions.append("Your resume appears to exceed 2 pages. Consider condensing it to make it more focused.")
        
        return suggestions
    
    def _analyze_bullet_points(self, text):
        """Analyze the use of bullet points"""
        suggestions = []
        
        # Count bullet points (common bullet point characters)
        bullet_chars = ["•", "-", "*", "–", "—", ">"]
        bullet_count = sum(text.count(char) for char in bullet_chars)
        
        if bullet_count < 10:
            suggestions.append("Use more bullet points to make your achievements and responsibilities easy to scan.")
        elif bullet_count > 40:
            suggestions.append("You may have too many bullet points. Focus on the most important achievements.")
        
        return suggestions
    
    def _analyze_weak_language(self, text):
        """Analyze for weak language that should be avoided"""
        suggestions = []
        
        # Check for weak phrases
        text_lower = text.lower()
        found_weak_phrases = [phrase for phrase in self.weak_words if phrase in text_lower]
        
        if found_weak_phrases:
            phrases_str = ", ".join([f"'{phrase}'" for phrase in found_weak_phrases[:3]])
            if len(found_weak_phrases) > 3:
                phrases_str += ", and others"
            suggestions.append(f"Replace weak phrases like {phrases_str} with strong action verbs.")
        
        return suggestions
    
    def _analyze_quantification(self, text):
        """Analyze for quantifiable achievements"""
        suggestions = []
        
        # Look for numbers (indicates quantified achievements)
        import re
        numbers = re.findall(r'\b\d+%|\b\d+\b', text)
        
        if len(numbers) < 5:
            suggestions.append("Quantify your achievements with numbers where possible (e.g., 'increased sales by 20%', 'managed a team of 15').")
        
        return suggestions
    
    def get_top_suggestions(self, text, max_suggestions=5):
        """Get the top suggestions for improving the resume"""
        all_suggestions = []
        
        # Analyze the resume
        analysis = self.analyze_structure(text)
        
        # Collect all suggestions
        for category, suggestions in analysis.items():
            all_suggestions.extend(suggestions)
        
        # Return the top suggestions (limited to max_suggestions)
        return all_suggestions[:max_suggestions]