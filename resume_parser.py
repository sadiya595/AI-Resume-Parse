import os
import re
import fitz  # PyMuPDF for PDF text extraction
import docx  # python-docx for DOCX files
from typing import Dict, List, Any, Optional
from datetime import datetime

# Load spaCy language model globally with enhanced error handling
try:
    import spacy
    nlp = spacy.load("en_core_web_sm")
    USE_SPACY = True
    print("✅ spaCy loaded successfully")
except ImportError:
    print("⚠️  spaCy not installed, using basic text processing")
    spacy = None
    nlp = None
    USE_SPACY = False
except OSError:
    print("⚠️  spaCy model 'en_core_web_sm' not found. Using basic text processing")
    print("   To install: python -m spacy download en_core_web_sm")
    spacy = None
    nlp = None
    USE_SPACY = False
except Exception as e:
    print(f"⚠️  spaCy initialization failed: {str(e)}. Using basic text processing")
    spacy = None
    nlp = None
    USE_SPACY = False

def extract_text_from_pdf(file_path: str) -> str:
    """Extract text from PDF file using PyMuPDF"""
    try:
        doc = fitz.open(file_path)
        text = ""
        for page in doc:
            text += page.get_text()
        doc.close()
        return text
    except Exception as e:
        raise Exception(f"Error extracting text from PDF: {str(e)}")

def extract_text_from_docx(file_path: str) -> str:
    """Extract text from DOCX file using python-docx"""
    try:
        doc = docx.Document(file_path)
        text = ""
        for paragraph in doc.paragraphs:
            text += paragraph.text + "\n"
        return text
    except Exception as e:
        raise Exception(f"Error extracting text from DOCX: {str(e)}")

def extract_personal_info(text: str) -> Dict[str, str]:
    """Extract personal information with enhanced clickable link detection"""
    personal_info = {
        "name": "",
        "email": "",
        "phone": "",
        "address": "",
        "linkedin": "",
        "github": "",
        "website": ""
    }
    
    lines = text.split('\n')
    clean_lines = [line.strip() for line in lines if line.strip()]
    
    # Enhanced name extraction with spaCy NLP or fallback
    if USE_SPACY and nlp:
        # Use spaCy for intelligent name extraction
        doc = nlp(text[:1000])
        persons = []
        locations = set()
        
        for ent in doc.ents:
            if ent.label_ == "GPE":
                locations.add(ent.text.lower())
        
        for ent in doc.ents:
            if ent.label_ == "PERSON":
                name_candidate = ent.text.strip()
                if (name_candidate.lower() not in locations and 
                    len(name_candidate.split()) >= 1 and
                    not any(loc in name_candidate.lower() for loc in ['bengaluru', 'bangalore', 'mumbai', 'delhi', 'chennai', 'hyderabad', 'pune', 'kolkata', 'karnataka', 'maharashtra', 'india'])):
                    persons.append(name_candidate)
        
        if persons:
            personal_info['name'] = persons[0]
        else:
            personal_info['name'] = "Name not clearly identified in resume"
    else:
        # Fallback name extraction
        for line in clean_lines[:5]:
            if any(keyword in line.lower() for keyword in ['email', 'phone', 'mobile', '@', 'linkedin', 'github', 'www']):
                continue
            if re.search(r'[0-9]', line):
                continue
            if len(line.split()) >= 2 and len(line.split()) <= 4:
                name_parts = []
                for part in line.split():
                    if part.lower() not in ['bengaluru', 'bangalore', 'mumbai', 'delhi', 'chennai', 'hyderabad', 'pune', 'kolkata', 'karnataka', 'maharashtra', 'india']:
                        name_parts.append(part)
                if len(name_parts) >= 1:
                    personal_info["name"] = " ".join(name_parts)
                    break
        
        if not personal_info["name"]:
            for line in clean_lines[:3]:
                line = line.strip()
                if (len(line) > 2 and len(line) < 50 and 
                    not any(char.isdigit() for char in line) and
                    not '@' in line and not 'phone' in line.lower()):
                    personal_info["name"] = line
                    break
            else:
                personal_info["name"] = "Name not clearly identified in resume"
    
    # Extract email
    email_pattern = re.compile(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b')
    emails = email_pattern.findall(text)
    if emails:
        personal_info["email"] = emails[0]
    else:
        personal_info["email"] = "Email address not found in resume"
    
    # Enhanced Indian phone number extraction
    phone_patterns = [
        r'\+91[\s-]?[6-9]\d{9}',
        r'91[\s-]?[6-9]\d{9}',
        r'[6-9]\d{9}'
    ]
    
    phone_found = False
    for pattern in phone_patterns:
        matches = re.findall(pattern, text)
        if matches:
            phone = matches[0]
            phone = re.sub(r'[\s-]', '', phone)
            if not phone.startswith('+91'):
                if phone.startswith('91'):
                    phone = '+' + phone
                else:
                    phone = '+91-' + phone
            else:
                phone = phone.replace('+91', '+91-')
            personal_info["phone"] = phone
            phone_found = True
            break
    
    if not phone_found:
        personal_info["phone"] = "Phone number not provided"
    
    # Extract address/location
    location_keywords = ['bengaluru', 'bangalore', 'mumbai', 'delhi', 'chennai', 'hyderabad', 'pune', 'kolkata', 'karnataka', 'maharashtra', 'india']
    for line in clean_lines:
        for keyword in location_keywords:
            if keyword in line.lower():
                personal_info["address"] = line
                break
        if personal_info["address"]:
            break
    
    if not personal_info["address"]:
        personal_info["address"] = "Location not specified"
    
    # ENHANCED LinkedIn Detection - Multiple Patterns
    linkedin_patterns = [
        r'https?://(?:www\.)?linkedin\.com/in/[\w-]+/?',      # Full URL
        r'linkedin\.com/in/[\w-]+/?',                         # Without protocol
        r'www\.linkedin\.com/in/[\w-]+/?',                    # With www
        r'(?:linkedin|LinkedIn):\s*([^\s\n]+)',               # "LinkedIn: username"
        r'(?:linkedin|LinkedIn)\s*-\s*([^\s\n]+)',            # "LinkedIn - username"
        r'(?:linkedin|LinkedIn)\s*:\s*linkedin\.com/in/([\w-]+)', # "LinkedIn: linkedin.com/in/username"
    ]
    
    linkedin_found = False
    for pattern in linkedin_patterns:
        matches = re.findall(pattern, text, re.IGNORECASE)
        if matches:
            match = matches[0]
            # Clean up the match
            if match.startswith('http'):
                personal_info["linkedin"] = match
            elif match.startswith('linkedin.com') or match.startswith('www.linkedin'):
                personal_info["linkedin"] = match
            else:
                # It's just a username, construct the full URL
                clean_username = match.strip('/')
                personal_info["linkedin"] = f"linkedin.com/in/{clean_username}"
            linkedin_found = True
            break
    
    if not linkedin_found:
        personal_info["linkedin"] = "LinkedIn profile not provided"
    
    # ENHANCED GitHub Detection - Multiple Patterns
    github_patterns = [
        r'https?://(?:www\.)?github\.com/[\w-]+/?',           # Full URL
        r'github\.com/[\w-]+/?',                              # Without protocol
        r'www\.github\.com/[\w-]+/?',                         # With www
        r'(?:github|GitHub):\s*([^\s\n]+)',                   # "GitHub: username"
        r'(?:github|GitHub)\s*-\s*([^\s\n]+)',                # "GitHub - username"
        r'(?:github|GitHub)\s*:\s*github\.com/([\w-]+)',      # "GitHub: github.com/username"
    ]
    
    github_found = False
    for pattern in github_patterns:
        matches = re.findall(pattern, text, re.IGNORECASE)
        if matches:
            match = matches[0]
            # Clean up the match
            if match.startswith('http'):
                personal_info["github"] = match
            elif match.startswith('github.com') or match.startswith('www.github'):
                personal_info["github"] = match
            else:
                # It's just a username, construct the full URL
                clean_username = match.strip('/')
                personal_info["github"] = f"github.com/{clean_username}"
            github_found = True
            break
    
    if not github_found:
        personal_info["github"] = "GitHub profile not found"
    
    # Extract website
    website_pattern = re.compile(r'www\.[\w.-]+\.[a-z]{2,}|https?://[\w.-]+\.[a-z]{2,}')
    website_matches = website_pattern.findall(text.lower())
    for match in website_matches:
        if 'linkedin' not in match and 'github' not in match:
            personal_info["website"] = match
            break
    else:
        personal_info["website"] = "Personal website not mentioned"
    
    return personal_info

def extract_skills(text: str) -> List[str]:
    """Extract technical skills from resume text with enhanced detection"""
    # Comprehensive skills database
    skills_database = [
        # Programming Languages
        'Python', 'Java', 'JavaScript', 'C++', 'C#', 'C', 'PHP', 'Ruby', 'Go', 'Swift', 
        'Kotlin', 'Scala', 'R', 'MATLAB', 'TypeScript', 'Dart', 'Rust', 'Perl',
        
        # Web Technologies
        'HTML', 'CSS', 'React', 'Angular', 'Vue', 'Node.js', 'Express', 'Django', 
        'Flask', 'Spring', 'Laravel', 'Bootstrap', 'jQuery', 'Sass', 'Less',
        
        # Databases
        'MySQL', 'PostgreSQL', 'MongoDB', 'SQLite', 'Redis', 'Oracle', 'SQL Server',
        'Firebase', 'DynamoDB', 'Cassandra', 'Neo4j', 'SQL',
        
        # Cloud & DevOps
        'AWS', 'Azure', 'Google Cloud', 'Docker', 'Kubernetes', 'Jenkins', 'Git',
        'GitHub', 'GitLab', 'CI/CD', 'Terraform', 'Ansible',
        
        # Data Science & ML
        'Machine Learning', 'Deep Learning', 'TensorFlow', 'PyTorch', 'Scikit-learn',
        'Pandas', 'NumPy', 'Matplotlib', 'Seaborn', 'Jupyter', 'Keras', 'OpenCV',
        'Data Science', 'Data Analysis', 'Statistics', 'Big Data', 'Hadoop', 'Spark',
        
        # Mobile Development
        'Android', 'iOS', 'React Native', 'Flutter', 'Xamarin',
        
        # Other Technologies
        'Linux', 'Windows', 'MacOS', 'REST API', 'GraphQL', 'Microservices',
        'Blockchain', 'Unity', 'Unreal Engine', 'AI', 'Artificial Intelligence',
        'Computer Vision', 'NLP', 'Natural Language Processing'
    ]
    
    found_skills = set()
    text_lower = text.lower()
    
    for skill in skills_database:
        # Check for exact match and common variations
        skill_variations = [skill, skill.lower(), skill.upper(), skill.replace(' ', '')]
        
        for variation in skill_variations:
            if variation.lower() in text_lower:
                found_skills.add(skill)
                break
    
    skills_list = sorted(list(found_skills))
    
    if not skills_list:
        return ["No technical skills clearly identified - consider adding a skills section"]
    
    return skills_list

def extract_experience(text: str) -> List[Dict[str, str]]:
    """Enhanced work experience extraction that completely avoids false positives"""
    experience = []
    lines = text.split('\n')
    clean_lines = [line.strip() for line in lines if line.strip()]
    
    # STRICT keywords that indicate actual work experience (not academic projects)
    work_keywords = [
        'employed', 'employee', 'intern at', 'internship at', 'worked at',
        'job title', 'position at', 'company:', 'employer:', 'workplace:',
        'full-time', 'part-time', 'freelance work', 'contract work',
        'professional experience', 'work experience', 'employment history'
    ]
    
    # Keywords that EXCLUDE work experience (academic/student projects)
    exclude_keywords = [
        'project', 'assignment', 'coursework', 'academic', 'college project',
        'university project', 'semester project', 'final year project',
        'mini project', 'major project', 'capstone', 'thesis', 'research',
        'student', 'course', 'study', 'developed a', 'built a', 'designed a'
    ]
    
    # Look for actual work experience
    has_real_work = False
    work_sections = []
    
    for line in clean_lines:
        line_lower = line.lower()
        
        # Must have work keywords AND not have exclude keywords
        has_work_indicators = any(keyword in line_lower for keyword in work_keywords)
        has_exclude_indicators = any(keyword in line_lower for keyword in exclude_keywords)
        
        if has_work_indicators and not has_exclude_indicators:
            has_real_work = True
            work_sections.append(line)
    
    # If no real work experience found, return student-appropriate message
    if not has_real_work:
        return [{
            'company': 'No professional work experience',
            'position': 'Student - No work history found',
            'duration': '0 years',
            'description': 'This is a student resume with academic projects only. Consider highlighting internships, part-time work, or volunteer experience.'
        }]
    
    # Process actual work experience (this won't execute for student resumes)
    for work_line in work_sections:
        experience.append({
            'company': 'Company from resume',
            'position': 'Position from resume', 
            'duration': work_line,
            'description': 'Professional work experience extracted from resume'
        })
    
    return experience

def extract_education(text: str) -> List[Dict[str, str]]:
    """Enhanced education extraction with summary exclusion and improved patterns"""
    education = []
    lines = text.split('\n')
    clean_lines = [line.strip() for line in lines if line.strip()]
    
    # Summary/objective exclusion keywords
    summary_keywords = [
        'results-driven', 'seeking', 'objective', 'summary', 'profile',
        'committed to', 'specializing in', 'passionate about', 'looking for',
        'dedicated', 'motivated', 'experienced in', 'skilled in'
    ]
    
    # ENHANCED academic education patterns - more comprehensive
    academic_patterns = [
        r'\b(?:b\.?e\.?|bachelor.*?engineering|be\s+computer)\b',
        r'\b(?:b\.?tech|bachelor.*?technology)\b', 
        r'\b(?:b\.?sc\.?|bachelor.*?science)\b',
        r'\b(?:b\.?a\.?|bachelor.*?arts)\b',
        r'\b(?:m\.?e\.?|master.*?engineering)\b',
        r'\b(?:m\.?tech|master.*?technology)\b',
        r'\b(?:m\.?sc\.?|master.*?science)\b',
        r'\b(?:m\.?a\.?|master.*?arts)\b',
        r'\b(?:mba|master.*?business)\b',
        r'\b(?:phd|ph\.d\.?|doctorate)\b',
        r'\b(?:computer science|electronics|mechanical|civil)\b',
        r'\b(?:engineering college|institute of technology)\b',
        r'\b(?:university|college|institute).*?(?:technology|engineering|science)\b',
        r'\b(?:kseeb|cbse|icse|state board).*?(?:12th|plus.*?two|intermediate|puc)\b',
        r'\b(?:10th|sslc|matriculation)\b',
        r'\b(?:high school|secondary school)\b'
    ]
    
    # Keywords to EXCLUDE (certifications, training, etc.)
    exclude_keywords = [
        'certification', 'certificate', 'certified', 'training', 'course',
        'workshop', 'seminar', 'bootcamp', 'online course', 'mooc',
        'udemy', 'coursera', 'edx', 'khan academy', 'pluralsight',
        'aws certified', 'google certified', 'microsoft certified',
        'oracle certified', 'cisco certified', 'comptia', 'pmp',
        'scrum master', 'agile', 'itil', 'six sigma', 'lean'
    ]
    
    in_education_section = False
    
    for i, line in enumerate(clean_lines):
        line_lower = line.lower()
        
        # Skip summary/objective lines
        if any(summary_word in line_lower for summary_word in summary_keywords):
            continue
            
        # Skip if it's clearly a summary (contains multiple summary indicators)
        summary_indicators = sum(1 for keyword in summary_keywords if keyword in line_lower)
        if summary_indicators >= 2:
            continue
        
        # Check if we're entering education section
        if 'education' in line_lower and len(line.split()) <= 3:
            in_education_section = True
            continue
        
        # Stop at projects, experience, or skills section
        if in_education_section and any(header in line_lower for header in ['project', 'experience', 'skill', 'certification', 'training']) and len(line.split()) <= 3:
            break
        
        # Skip lines with certification/training keywords
        if any(exclude_word in line_lower for exclude_word in exclude_keywords):
            continue
        
        # Look for ONLY academic education patterns
        if in_education_section or any(re.search(pattern, line_lower) for pattern in academic_patterns):
            # Check for academic degree patterns
            for pattern in academic_patterns:
                if re.search(pattern, line_lower):
                    # Skip if it contains certification keywords
                    if any(exclude_word in line_lower for exclude_word in exclude_keywords):
                        continue
                    
                    # Look for years
                    year_pattern = r'\b(20\d{2}|19\d{2})\b'
                    years = re.findall(year_pattern, line)
                    
                    # Check next few lines for institution context - ENHANCED
                    context_lines = clean_lines[i:i+5] if i+5 < len(clean_lines) else clean_lines[i:]
                    institution_match = None
                    
                    # Improved institution detection
                    for context_line in context_lines:
                        # Skip certification lines in context too
                        if any(exclude_word in context_line.lower() for exclude_word in exclude_keywords):
                            continue
                        
                        # Enhanced institution keywords
                        if any(keyword in context_line.lower() for keyword in 
                               ['college', 'university', 'institute', 'school', 'iit', 'nit', 
                                'technology', 'engineering', 'science']):
                            institution_match = context_line
                            break
                        
                        # Also look for years in context
                        context_years = re.findall(year_pattern, context_line)
                        years.extend(context_years)
                    
                    # Only create entry if it's clearly academic
                    if re.search(r'\b(?:engineering|science|arts|technology|bachelor|master|phd|school|college|university)\b', line_lower):
                        education_entry = {
                            'institution': institution_match if institution_match else 'Educational Institution',
                            'degree': line.strip()[:150] + ('...' if len(line) > 150 else ''),  # Increased length
                            'year': ' - '.join(years[:2]) if len(years) >= 2 else (years[0] if years else 'Year not specified'),
                            'gpa': 'Not provided'
                        }
                        
                        # Avoid duplicates and ensure it's academic
                        if not any(edu['degree'].lower() == education_entry['degree'].lower() for edu in education):
                            education.append(education_entry)
                    break
    
    # If no academic education found, provide helpful placeholder
    if not education:
        return [{
            'institution': 'Academic education information not clearly identified',
            'degree': 'Please ensure academic qualifications are clearly formatted in your resume',
            'year': 'N/A',
            'gpa': 'Not provided'
        }]
    
    return education

def extract_projects(text: str) -> List[Dict[str, Any]]:
    """Enhanced project extraction with duplicate prevention and better technology detection"""
    projects = []
    seen_projects = set()  # Track project names we've already added
    lines = text.split('\n')
    clean_lines = [line.strip() for line in lines if line.strip()]
    
    in_projects_section = False
    current_project = {}
    project_count = 0
    
    for i, line in enumerate(clean_lines):
        line_lower = line.lower()
        
        # Check if we're entering projects section
        if 'project' in line_lower and len(line.split()) <= 3:
            in_projects_section = True
            continue
        
        # Stop at education section to avoid mixing
        if in_projects_section and 'education' in line_lower and len(line.split()) <= 3:
            # Check for duplicate before adding the last project
            if current_project and current_project.get("name"):
                project_name_lower = current_project["name"].lower().strip()
                if project_name_lower not in seen_projects:
                    projects.append(current_project)
                    seen_projects.add(project_name_lower)
            break
        
        if in_projects_section and line.strip():
            # Enhanced project title detection
            is_title_line = (
                not line.startswith(('•', '-', 'o ', '▪', '●')) and 
                not re.search(r'^\d+\.', line) and  # Not numbered list
                len(line.split()) >= 3 and
                len(line.split()) <= 20 and
                'technologies' not in line_lower and
                'duration' not in line_lower and
                'description' not in line_lower and
                project_count < 10  # Limit projects
            )
            
            # Look for technology/project keywords
            tech_keywords = [
                'ai', 'ml', 'machine learning', 'deep learning', 'python', 'java', 'react', 
                'web', 'mobile', 'app', 'system', 'management', 'detection', 'chatbot',
                'analysis', 'prediction', 'classification', 'recognition', 'platform',
                'solution', 'tool', 'framework', 'algorithm', 'model', 'dashboard',
                'automation', 'optimization', 'monitoring', 'tracking', 'processing'
            ]
            has_tech_keywords = any(keyword in line_lower for keyword in tech_keywords)
            
            if is_title_line and has_tech_keywords:
                # Before adding the previous project, check for duplicates
                if current_project and current_project.get("name"):
                    project_name_lower = current_project["name"].lower().strip()
                    if project_name_lower not in seen_projects:
                        projects.append(current_project)
                        seen_projects.add(project_name_lower)
                        project_count += 1
                
                # Start new project
                current_project = {
                    "name": line,
                    "description": "",
                    "technologies": []
                }
            elif current_project and line.strip():
                # Add to description if we have a current project
                if len(line) > 20:  # Only add substantial lines to description
                    if current_project["description"]:
                        current_project["description"] += " " + line
                    else:
                        current_project["description"] = line
    
    # Add the last project with duplicate check
    if current_project and current_project.get("name"):
        project_name_lower = current_project["name"].lower().strip()
        if project_name_lower not in seen_projects:
            projects.append(current_project)
            seen_projects.add(project_name_lower)
    
    # Enhanced technology extraction and cleanup
    all_technologies = [
        'Python', 'Java', 'JavaScript', 'React', 'Node.js', 'MongoDB', 'MySQL', 
        'AI', 'ML', 'Machine Learning', 'Deep Learning', 'TensorFlow', 'PyTorch',
        'OpenCV', 'Flutter', 'Android', 'iOS', 'HTML', 'CSS', 'PHP', 'C++', 'C#',
        'Angular', 'Vue', 'Django', 'Flask', 'Spring', 'Docker', 'Kubernetes',
        'AWS', 'Azure', 'Git', 'GitHub', 'SQL', 'NoSQL', 'Redis', 'Firebase'
    ]
    
    for project in projects:
        if project["description"]:
            # Extract technologies from both name and description
            combined_text = (project["name"] + " " + project["description"]).lower()
            tech_found = []
            
            for tech in all_technologies:
                if tech.lower() in combined_text:
                    tech_found.append(tech)
            
            # Remove duplicates and limit
            project["technologies"] = list(set(tech_found))[:8]
            
            # Add placeholder if no technologies found
            if not project["technologies"]:
                project["technologies"] = ["Technologies not specified in resume"]
        else:
            project["technologies"] = ["Technologies not specified in resume"]
            if not project["description"]:
                project["description"] = "Project description not provided in resume"
    
    # If no projects found, provide helpful placeholder
    if not projects:
        return [{
            'name': 'No projects section found',
            'description': 'Consider adding academic or personal projects to strengthen your resume and demonstrate your technical abilities',
            'technologies': ['Project technologies not specified']
        }]
    
    return projects

def parse_resume_text(text: str) -> Dict[str, Any]:
    """Enhanced parsing with intelligent fallbacks and better error handling"""
    if not text or not text.strip():
        raise Exception("No text provided for parsing")
    
    try:
        # Extract different sections with enhanced algorithms
        personal_info = extract_personal_info(text)
        skills = extract_skills(text)
        experience = extract_experience(text)
        education = extract_education(text)
        projects = extract_projects(text)
        
        # Structure the parsed data
        parsed_data = {
            'personal_info': personal_info,
            'experience': experience,
            'education': education,
            'skills': skills,
            'projects': projects,
            'raw_text_length': len(text),
            'parsing_timestamp': datetime.now().isoformat(),
            'spacy_enabled': USE_SPACY
        }
        
        return parsed_data
        
    except Exception as e:
        raise Exception(f"Error parsing resume text: {str(e)}")

def process_resume_file(file_path: str) -> Dict[str, Any]:
    """Main function to process resume file with comprehensive error handling"""
    try:
        # Validate file exists
        if not os.path.exists(file_path):
            raise Exception(f"File not found: {file_path}")
        
        # Determine file type and extract text
        file_extension = os.path.splitext(file_path)[1].lower()
        
        if file_extension == '.pdf':
            text = extract_text_from_pdf(file_path)
        elif file_extension in ['.docx', '.doc']:
            text = extract_text_from_docx(file_path)
        else:
            raise Exception(f"Unsupported file type: {file_extension}")
        
        # Validate extracted text
        if not text or not text.strip():
            raise Exception("No text could be extracted from the file")
        
        if len(text.strip()) < 50:
            raise Exception("Extracted text is too short to be a valid resume")
        
        # Parse the extracted text
        parsed_data = parse_resume_text(text)
        
        # Add metadata
        parsed_data['file_info'] = {
            'filename': os.path.basename(file_path),
            'file_type': file_extension,
            'file_size': os.path.getsize(file_path),
            'text_length': len(text)
        }
        
        return parsed_data
    
    except Exception as e:
        raise Exception(f"Error processing resume file: {str(e)}")

# Export all functions
__all__ = [
    'extract_text_from_pdf',
    'extract_text_from_docx', 
    'parse_resume_text',
    'process_resume_file',
    'extract_personal_info',
    'extract_skills',
    'extract_experience',
    'extract_education',
    'extract_projects'
]
