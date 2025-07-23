import re
from typing import Dict, List, Any
from datetime import datetime

def extract_job_requirements(job_description: str) -> Dict[str, Any]:
    """Extract requirements from job description"""
    requirements = {
        'required_skills': [],
        'experience_years': 0,
        'education_level': '',
        'job_field': ''
    }
    
    text_lower = job_description.lower()
    
    # Detect job field
    if any(word in text_lower for word in ['marketing', 'brand', 'campaign', 'advertising']):
        requirements['job_field'] = 'marketing'
    elif any(word in text_lower for word in ['software', 'developer', 'programming', 'technical']):
        requirements['job_field'] = 'technical'
    elif any(word in text_lower for word in ['data', 'analytics', 'scientist']):
        requirements['job_field'] = 'data_science'
    
    # Extract skills
    common_skills = [
        'Python', 'Java', 'JavaScript', 'React', 'Node.js', 'SQL',
        'Marketing', 'Analytics', 'Branding', 'Campaign Management',
        'Data Analysis', 'Machine Learning', 'AI'
    ]
    
    for skill in common_skills:
        if skill.lower() in text_lower:
            requirements['required_skills'].append(skill)
    
    # Extract experience requirements
    exp_patterns = [
        r'(\d+)[\+\-\s]*years?\s*(?:of\s*)?experience',
        r'minimum\s*(\d+)\s*years?',
        r'at least\s*(\d+)\s*years?'
    ]
    
    for pattern in exp_patterns:
        matches = re.findall(pattern, text_lower)
        if matches:
            requirements['experience_years'] = int(matches[0])
            break
    
    return requirements

def analyze_job_match(resume_data: dict, job_description: str) -> dict:
    """Enhanced job matching with field compatibility detection"""
    
    # Extract job requirements
    job_requirements = extract_job_requirements(job_description)
    
    # Detect resume field vs job field mismatch
    resume_skills = [skill.lower() for skill in resume_data.get('skills', [])]
    job_text_lower = job_description.lower()
    
    # Define field categories
    tech_skills = ['python', 'java', 'javascript', 'ai', 'ml', 'programming', 'software', 'development', 'algorithm']
    marketing_skills = ['marketing', 'branding', 'campaign', 'analytics', 'lead generation', 'engagement', 'advertising']
    
    # Check resume field
    resume_tech_score = sum(1 for skill in resume_skills if any(tech in skill for tech in tech_skills))
    resume_marketing_score = sum(1 for skill in resume_skills if any(marketing in skill for marketing in marketing_skills))
    
    # Check job field
    job_tech_score = sum(1 for tech in tech_skills if tech in job_text_lower)
    job_marketing_score = sum(1 for marketing in marketing_skills if marketing in job_text_lower)
    
    # Determine field compatibility
    is_field_mismatch = False
    mismatch_message = ""
    
    if resume_tech_score > 3 and job_marketing_score > 2:
        is_field_mismatch = True
        mismatch_message = "Major field mismatch: Technical/Engineering resume vs Marketing position"
    elif resume_marketing_score > 3 and job_tech_score > 2:
        is_field_mismatch = True
        mismatch_message = "Major field mismatch: Marketing resume vs Technical position"
    
    # Check for student resume
    experience_data = resume_data.get('experience', [])
    is_student_resume = any(
        exp.get('company', '').lower().startswith('no professional') or
        exp.get('position', '').lower().startswith('student') or
        exp.get('description', '').lower().count('student') > 0
        for exp in experience_data
    )
    
    # Calculate experience match
    if is_student_resume:
        experience_match = {
            'match_percentage': 25,  # Low for student vs professional role
            'estimated_years': 0,
            'required_years': job_requirements.get('experience_years', 3),
            'experience_gap': job_requirements.get('experience_years', 3),
            'note': 'Student resume - No professional work experience'
        }
    else:
        experience_match = {
            'match_percentage': 75,
            'estimated_years': 2,
            'required_years': job_requirements.get('experience_years', 0),
            'experience_gap': 0
        }
    
    # Calculate skills match with field penalty
    resume_skill_set = set(skill.lower() for skill in resume_data.get('skills', []))
    job_skill_set = set(skill.lower() for skill in job_requirements.get('required_skills', []))
    
    if job_skill_set:
        matched_skills = resume_skill_set.intersection(job_skill_set)
        skills_percentage = (len(matched_skills) / len(job_skill_set)) * 100
    else:
        skills_percentage = 50  # Default when no specific skills listed
    
    skills_match = {
        'match_percentage': skills_percentage,
        'matched_skills': list(matched_skills) if job_skill_set else [],
        'missing_skills': list(job_skill_set - resume_skill_set) if job_skill_set else []
    }
    
    # Apply severe penalty for field mismatch
    if is_field_mismatch:
        skills_match['match_percentage'] = min(skills_match['match_percentage'], 20)
        skills_match['field_mismatch'] = True
        skills_match['mismatch_reason'] = mismatch_message
    
    # Calculate education match
    education_match = {
        'match_percentage': 80,
        'meets_requirement': True
    }
    
    # Calculate overall score with field mismatch penalty
    base_weights = {'skills': 0.5, 'experience': 0.3, 'education': 0.2}
    
    overall_score = (
        skills_match['match_percentage'] * base_weights['skills'] +
        experience_match['match_percentage'] * base_weights['experience'] +
        education_match['match_percentage'] * base_weights['education']
    )
    
    # Apply additional penalty for field mismatch
    if is_field_mismatch:
        overall_score = min(overall_score, 25)  # Cap at 25% for field mismatch
    
    # Generate appropriate recommendations
    recommendations = []
    if is_field_mismatch:
        recommendations = [
            f"⚠️  {mismatch_message}",
            "Consider applying to positions that match your technical background",
            "Look for software development, AI/ML, or engineering roles instead",
            "Your skills in programming and AI are valuable in tech companies"
        ]
    elif is_student_resume:
        recommendations = [
            "Focus on entry-level positions or internships in your field",
            "Highlight your academic projects and technical skills",
            "Consider roles like 'Junior Developer', 'ML Intern', or 'Software Engineer Trainee'",
            "Emphasize your learning ability and project experience"
        ]
    
    return {
        'overall_score': round(overall_score, 1),
        'skills_match': skills_match,
        'experience_match': experience_match,
        'education_match': education_match,
        'job_requirements': job_requirements,
        'recommendations': recommendations,
        'match_summary': get_realistic_match_summary(overall_score, is_field_mismatch, is_student_resume),
        'field_mismatch': is_field_mismatch,
        'analysis_timestamp': datetime.now().isoformat()
    }

def get_realistic_match_summary(score: float, is_mismatch: bool, is_student: bool) -> str:
    """Generate realistic match summary"""
    if is_mismatch:
        return "Poor match - Career field mismatch detected. Consider positions aligned with your technical background."
    elif is_student and score < 30:
        return "Limited match for this role. Focus on entry-level positions in your field of study."
    elif score >= 70:
        return "Good potential match for this position."
    elif score >= 50:
        return "Moderate match with room for skill development."
    else:
        return "Low compatibility. Consider developing relevant skills or pursuing different opportunities."

# Export functions
__all__ = ['analyze_job_match', 'extract_job_requirements']
