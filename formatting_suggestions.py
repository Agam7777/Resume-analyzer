import re

class FormattingAnalyzer:
    def __init__(self):
        """Initialize the formatting analyzer"""
        # Common resume formatting issues
        self.formatting_checks = {
            "inconsistent_spacing": self._check_inconsistent_spacing,
            "irregular_capitalization": self._check_irregular_capitalization,
            "font_consistency": self._check_font_consistency,
            "non_standard_sections": self._check_non_standard_sections,
            "bullets_formatting": self._check_bullets_formatting,
            "date_consistency": self._check_date_consistency
        }
    
    def analyze_formatting(self, text):
        """Analyze the formatting of a resume and provide suggestions"""
        suggestions = []
        
        for check_name, check_function in self.formatting_checks.items():
            result = check_function(text)
            if result:
                suggestions.append(result)
        
        return suggestions
    
    def _check_inconsistent_spacing(self, text):
        """Check for inconsistent spacing in the resume"""
        # Check for multiple consecutive blank lines
        if re.search(r'\n{3,}', text):
            return "Be consistent with spacing between sections. Avoid having multiple blank lines."
        
        # Check for inconsistent line breaks after section headers
        section_headers = ["experience", "education", "skills", "summary", "profile", "projects"]
        inconsistent_spacing = False
        
        for header in section_headers:
            pattern = f'(?i)^{header}.*?\n'
            matches = re.findall(pattern, text, re.MULTILINE)
            
            if matches:
                # Check the lines following each match
                following_lines = [text[text.find(match) + len(match):].split('\n', 1)[0] for match in matches]
                if any(line.strip() for line in following_lines) and any(not line.strip() for line in following_lines):
                    inconsistent_spacing = True
                    break
        
        if inconsistent_spacing:
            return "Maintain consistent spacing after section headers throughout your resume."
        
        return None
    
    def _check_irregular_capitalization(self, text):
        """Check for inconsistent capitalization"""
        # Check for inconsistent capitalization in section headers
        section_headers = ["experience", "education", "skills", "summary", "profile", "projects"]
        capitals = []
        
        for header in section_headers:
            pattern = f'(?:^|\n)({header}.*?)(?:\n|$)'
            matches = re.findall(pattern, text, re.IGNORECASE)
            
            for match in matches:
                # Check if all caps or title case
                if match.isupper():
                    capitals.append("upper")
                elif match.istitle():
                    capitals.append("title")
                else:
                    capitals.append("other")
        
        if len(set(capitals)) > 1 and len(capitals) > 1:
            return "Be consistent with capitalization in section headers. Stick to either ALL CAPS or Title Case."
        
        return None
    
    def _check_font_consistency(self, text):
        """Check for font consistency clues"""
        # This is a heuristic since we can't directly detect fonts from plain text
        # Look for markdown or unusual formatting characters that might indicate font changes
        formatting_chars = ["*", "_", "#", "==", "--", "++", "~~"]
        
        if any(char in text for char in formatting_chars):
            return "Ensure consistent font usage throughout your resume. Use at most 2 font families."
        
        return None
    
    def _check_non_standard_sections(self, text):
        """Check for non-standard section names"""
        standard_sections = {
            "summary", "profile", "objective", "experience", "work experience", "employment history", 
            "education", "skills", "technical skills", "certifications", "projects", "publications", 
            "awards", "honors", "activities", "interests", "languages", "references"
        }
        
        # Try to identify section headers
        potential_sections = re.findall(r'(?:^|\n)([A-Z][A-Za-z\s]+):?(?:\n|$)', text)
        
        non_standard = [section.lower().strip() for section in potential_sections 
                        if section.lower().strip() not in standard_sections 
                        and len(section.strip()) > 3]
        
        if non_standard:
            return "Consider using standard section headers that ATS systems can easily recognize."
        
        return None
    
    def _check_bullets_formatting(self, text):
        """Check for consistent bullet formatting"""
        # Common bullet characters
        bullet_chars = ["•", "-", "*", "–", "—", ">"]
        used_bullets = [char for char in bullet_chars if char in text]
        
        if len(used_bullets) > 1:
            return "Use consistent bullet point styles throughout your resume. Stick to one bullet character."
        
        return None
    
    def _check_date_consistency(self, text):
        """Check for consistent date formatting"""
        # Common date patterns
        date_patterns = [
            r'\b\d{1,2}/\d{1,2}/\d{2,4}\b',              # MM/DD/YYYY or DD/MM/YYYY
            r'\b\d{1,2}-\d{1,2}-\d{2,4}\b',              # MM-DD-YYYY or DD-MM-YYYY
            r'\b[A-Z][a-z]{2,8}\s+\d{4}\b',              # Month YYYY
            r'\b\d{4}\s+to\s+\d{4}\b',                   # YYYY to YYYY
            r'\b\d{4}\s*-\s*\d{4}\b',                    # YYYY-YYYY
            r'\b\d{4}\s*–\s*(?:\d{4}|present)\b',        # YYYY–YYYY or YYYY–present
            r'\b[A-Z][a-z]{2,8}\s+\d{4}\s*-\s*[A-Z][a-z]{2,8}\s+\d{4}\b',  # Month YYYY - Month YYYY
            r'\b[A-Z][a-z]{2,8}\s+\d{4}\s*-\s*present\b'  # Month YYYY - present
        ]
        
        found_patterns = []
        for pattern in date_patterns:
            matches = re.findall(pattern, text)
            if matches:
                found_patterns.append(pattern)
        
        if len(found_patterns) > 1:
            return "Use a consistent date format throughout your resume. For example, use either 'MM/YYYY' or 'Month YYYY' format everywhere."
        
        return None
    
    def get_top_formatting_suggestions(self, text, max_suggestions=3):
        """Get the top formatting suggestions for the resume"""
        suggestions = self.analyze_formatting(text)
        return suggestions[:max_suggestions]