/* -------------------------------------------------
   AI Resume Parser – Professional UI Controller
   (Complete working version with all features)
--------------------------------------------------*/
class ResumeParserUI {
  constructor() {
    /* ---------- DOM refs ---------- */
    this.dropArea = document.getElementById('drop-area');
    this.fileInput = document.getElementById('fileInput');
    this.uploadBtn = document.getElementById('uploadBtn');
    this.statusDiv = document.getElementById('status');
    this.resultTabs = document.getElementById('resultTabs');
    this.jobDesc = document.getElementById('jobDescription');

    this.currentFile = null;
    this.initializeEventListeners();
  }

  initializeEventListeners() {
    // File selection events
    this.dropArea.addEventListener('click', (e) => {
      if (e.target.classList.contains('browse-btn') || 
          e.target.classList.contains('change-file-btn') ||
          this.dropArea.dataset.state === 'initial') {
        this.fileInput.click();
      }
    });

    this.fileInput.addEventListener('change', () => {
      this.handleFileSelection(this.fileInput.files);
    });

    // Drag and drop events
    this.dropArea.addEventListener('dragover', this.handleDragOver.bind(this));
    this.dropArea.addEventListener('dragleave', this.handleDragLeave.bind(this));
    this.dropArea.addEventListener('drop', this.handleDrop.bind(this));

    // Upload button
    this.uploadBtn.addEventListener('click', this.handleUpload.bind(this));

    // Upload new resume button
    this.dropArea.addEventListener('click', (e) => {
      if (e.target.classList.contains('upload-new-btn')) {
        this.resetToInitialState();
      }
    });
  }

  handleDragOver(event) {
    event.preventDefault();
    if (this.dropArea.dataset.state === 'initial' || 
        this.dropArea.dataset.state === 'file-selected') {
      this.dropArea.classList.add('dragover');
    }
  }

  handleDragLeave() {
    this.dropArea.classList.remove('dragover');
  }

  handleDrop(event) {
    event.preventDefault();
    this.dropArea.classList.remove('dragover');
    
    if (this.dropArea.dataset.state === 'initial' || 
        this.dropArea.dataset.state === 'file-selected') {
      this.handleFileSelection(event.dataTransfer.files);
    }
  }

  handleFileSelection(files) {
    if (files.length > 0) {
      const file = files[0];
      
      // Validate file type
      const allowedTypes = ['application/pdf', 'application/msword', 
                          'application/vnd.openxmlformats-officedocument.wordprocessingml.document'];
      
      if (!allowedTypes.includes(file.type) && !file.name.match(/\.(pdf|doc|docx)$/i)) {
        this.showMessage('❌ Please select a PDF, DOC, or DOCX file', 'error');
        return;
      }

      // Validate file size (16MB limit)
      if (file.size > 16 * 1024 * 1024) {
        this.showMessage('❌ File size must be less than 16MB', 'error');
        return;
      }

      this.currentFile = file;
      this.setUIState('file-selected');
      this.updateFileInfo(file);
      this.enableUploadButton();
    }
  }

  setUIState(state) {
    this.dropArea.dataset.state = state;
    
    // Hide all content states
    const contentStates = this.dropArea.querySelectorAll('.upload-content');
    contentStates.forEach(content => content.style.display = 'none');
    
    // Show current state
    const activeState = this.dropArea.querySelector(`.${state}-state`);
    if (activeState) {
      activeState.style.display = 'block';
    }

    // Handle upload button state
    if (state === 'processing' || state === 'success') {
      this.uploadBtn.disabled = true;
      this.uploadBtn.classList.add('disabled');
    } else if (state === 'file-selected') {
      this.uploadBtn.disabled = false;
      this.uploadBtn.classList.remove('disabled');
    } else {
      this.uploadBtn.disabled = true;
      this.uploadBtn.classList.add('disabled');
    }
  }

  updateFileInfo(file) {
    const fileName = this.dropArea.querySelector('.file-name');
    const fileSize = this.dropArea.querySelector('.file-size');
    
    if (fileName && fileSize) {
      fileName.textContent = file.name;
      fileSize.textContent = `(${(file.size / 1024 / 1024).toFixed(2)} MB)`;
    }
  }

  enableUploadButton() {
    this.uploadBtn.disabled = false;
    this.uploadBtn.classList.remove('disabled');
    this.clearMessage();
  }

  async handleUpload() {
    if (!this.currentFile) {
      this.showMessage('❌ Please select a resume file first', 'error');
      return;
    }

    // Set processing state
    this.setUIState('processing');
    this.startProgressAnimation();

    // Prepare form data
    const formData = new FormData();
    formData.append('resume', this.currentFile);
    formData.append('job_description', this.jobDesc.value);

    try {
      const response = await fetch('/upload', {
        method: 'POST',
        body: formData
      });

      const data = await response.json();

      if (data.success && data.results) {
        // Success state
        this.setUIState('success');
        this.showMessage('🎉 Resume analysis completed successfully!', 'success', true);
        this.displayResults(data.results);
      } else {
        throw new Error(data.error || 'Unknown error occurred');
      }
    } catch (error) {
      console.error('Upload error:', error);
      this.showMessage(`❌ Error: ${error.message}`, 'error');
      this.setUIState('file-selected'); // Return to file selected state
    }
  }

  startProgressAnimation() {
    const progressFill = document.querySelector('.progress-fill');
    if (progressFill) {
      progressFill.style.width = '0%';
      
      // Simulate progress
      let progress = 0;
      const interval = setInterval(() => {
        progress += Math.random() * 15;
        if (progress > 90) progress = 90;
        progressFill.style.width = progress + '%';
      }, 200);

      // Complete progress when upload finishes
      setTimeout(() => {
        clearInterval(interval);
        progressFill.style.width = '100%';
      }, 2000);
    }
  }

  showMessage(message, type, persistent = false) {
    this.statusDiv.innerHTML = `<span class="message ${type}">${message}</span>`;
    this.statusDiv.className = `status-message ${type}`;
    
    if (!persistent) {
      setTimeout(() => {
        this.clearMessage();
      }, 5000);
    }
  }

  clearMessage() {
    this.statusDiv.innerHTML = '';
    this.statusDiv.className = 'status-message';
  }

  resetToInitialState() {
    this.currentFile = null;
    this.fileInput.value = '';
    this.setUIState('initial');
    this.clearMessage();
    this.resultTabs.style.display = 'none';
    this.jobDesc.value = '';
  }

  // Helper function for skill formatting
  prettifySkill(skill) {
    return skill.replace(/([a-z])([A-Z])/g, '$1 $2');
  }

  // Helper function for pie chart segments
  calculateSegment(percentage) {
    return 440 * percentage / 100;
  }

  // Generate SVG pie chart
  generatePieChart(jobMatch) {
    const skillsPercent = jobMatch.skills_match?.match_percentage || 0;
    const experiencePercent = jobMatch.experience_match?.match_percentage || 0;
    const educationPercent = jobMatch.education_match?.match_percentage || 0;

    return `
      <svg width="140" height="140" viewBox="0 0 140 140">
        <circle r="66" cx="70" cy="70" fill="none" stroke="#e5e7eb" stroke-width="12"/>
        <circle r="66" cx="70" cy="70" fill="none" stroke="#10b981" stroke-width="12"
                stroke-dasharray="${this.calculateSegment(skillsPercent)} 440"
                transform="rotate(-90 70 70)"/>
        <circle r="66" cx="70" cy="70" fill="none" stroke="#3b82f6" stroke-width="12"
                stroke-dasharray="${this.calculateSegment(experiencePercent)} 440"
                transform="rotate(${this.calculateSegment(skillsPercent)-90} 70 70)"/>
        <circle r="66" cx="70" cy="70" fill="none" stroke="#f59e0b" stroke-width="12"
                stroke-dasharray="${this.calculateSegment(educationPercent)} 440"
                transform="rotate(${this.calculateSegment(skillsPercent)+this.calculateSegment(experiencePercent)-90} 70 70)"/>
      </svg>
    `;
  }

  displayResults(data) {
    console.log('Displaying results:', data);
    
    // Create comprehensive tabs based on available data
    let tabsHTML = '<div class="tabs">';
    let contentHTML = '';
    
    // Personal Info Tab
    if (data.personal_info) {
      tabsHTML += '<div class="tab active" data-tab="personal"><i class="fas fa-user"></i> Personal Info</div>';
      contentHTML += this.createPersonalInfoTab(data.personal_info);
    }
    
    // Skills Tab
    if (data.skills && data.skills.length > 0) {
      tabsHTML += '<div class="tab" data-tab="skills"><i class="fas fa-cogs"></i> Skills</div>';
      contentHTML += this.createSkillsTab(data.skills);
    }
    
    // Experience Tab
    if (data.experience && data.experience.length > 0) {
      tabsHTML += '<div class="tab" data-tab="experience"><i class="fas fa-briefcase"></i> Experience</div>';
      contentHTML += this.createExperienceTab(data.experience);
    }
    
    // Education Tab
    if (data.education && data.education.length > 0) {
      tabsHTML += '<div class="tab" data-tab="education"><i class="fas fa-graduation-cap"></i> Education</div>';
      contentHTML += this.createEducationTab(data.education);
    }
    
    // Projects Tab
    if (data.projects && data.projects.length > 0) {
      tabsHTML += '<div class="tab" data-tab="projects"><i class="fas fa-project-diagram"></i> Projects</div>';
      contentHTML += this.createProjectsTab(data.projects);
    }
    
    // Job Match Tab
    if (data.job_match) {
      tabsHTML += '<div class="tab" data-tab="jobmatch"><i class="fas fa-bullseye"></i> Job Match</div>';
      contentHTML += this.createJobMatchTab(data.job_match);
    }
    
    tabsHTML += '</div>';
    
    // Set the complete HTML
    this.resultTabs.innerHTML = tabsHTML + contentHTML;
    this.resultTabs.style.display = 'block';
    this.resultTabs.scrollIntoView({ behavior: 'smooth' });
    
    // Add tab switching functionality
    document.querySelectorAll('.tab').forEach(tab => {
      tab.addEventListener('click', () => {
        document.querySelectorAll('.tab').forEach(t => t.classList.remove('active'));
        document.querySelectorAll('.tabContent').forEach(c => c.classList.remove('active'));
        
        tab.classList.add('active');
        const targetTab = document.getElementById(tab.dataset.tab);
        if (targetTab) {
          targetTab.classList.add('active');
        }
      });
    });
  }

  createPersonalInfoTab(personalInfo) {
    const createInfoItem = (label, value) => {
      if (!value || value.includes('not found') || value.includes('not provided') || value.includes('not specified')) {
        return `<div class="info-item placeholder-content">
          <strong>${label}:</strong> 
          <span class="placeholder-text">${value || `${label} not provided`}</span>
        </div>`;
      }
      return `<div class="info-item">
        <strong>${label}:</strong> ${value}
      </div>`;
    };

    return `
      <div class="tabContent active" id="personal">
        <h3>📋 Personal Information</h3>
        <div class="info-grid">
          ${createInfoItem('Name', personalInfo.name)}
          ${createInfoItem('Email', personalInfo.email)}
          ${createInfoItem('Phone', personalInfo.phone)}
          ${createInfoItem('Address', personalInfo.address)}
          ${createInfoItem('LinkedIn', personalInfo.linkedin)}
          ${createInfoItem('GitHub', personalInfo.github)}
        </div>
      </div>
    `;
  }

  createSkillsTab(skills) {
    const skillsHTML = skills.map(skill => {
      const isPlaceholder = skill.includes('not clearly identified') || skill.includes('consider adding');
      return `<span class="skill-badge ${isPlaceholder ? 'placeholder' : ''}">${this.prettifySkill(skill)}</span>`;
    }).join('');
    
    return `
      <div class="tabContent" id="skills">
        <h3>🚀 Technical Skills</h3>
        <div class="skills-container">
          ${skillsHTML}
        </div>
        <p class="skill-count">Total Skills Detected: <strong>${skills.length}</strong></p>
      </div>
    `;
  }

  createExperienceTab(experience) {
    const experienceHTML = experience.map(exp => {
      const isPlaceholder = exp.company && (exp.company.includes('No work experience') || exp.company.includes('student resume'));
      
      return `
        <div class="experience-item ${isPlaceholder ? 'placeholder-content' : ''}">
          <h4>${exp.position || 'Position'}</h4>
          <div class="company-duration">
            <span class="company">${exp.company || 'Company'}</span>
            <span class="duration">${exp.duration || 'Duration not specified'}</span>
          </div>
          ${exp.description ? `<p class="description ${isPlaceholder ? 'placeholder-text' : ''}">${exp.description}</p>` : ''}
        </div>
      `;
    }).join('');
    
    return `
      <div class="tabContent" id="experience">
        <h3>💼 Work Experience</h3>
        <div class="experience-container">
          ${experienceHTML}
        </div>
      </div>
    `;
  }

  createEducationTab(education) {
    const educationHTML = education.map(edu => {
      const isPlaceholder = edu.institution && edu.institution.includes('not clearly identified');
      
      return `
        <div class="education-item ${isPlaceholder ? 'placeholder-content' : ''}">
          <h4>${edu.degree || 'Degree'}</h4>
          <div class="institution-year">
            <span class="institution">${edu.institution || 'Institution'}</span>
            <span class="year">${edu.year || 'Year not specified'}</span>
          </div>
          ${edu.gpa && edu.gpa !== 'N/A' && edu.gpa !== 'Not provided' ? `<p class="gpa">GPA: ${edu.gpa}</p>` : ''}
        </div>
      `;
    }).join('');
    
    return `
      <div class="tabContent" id="education">
        <h3>🎓 Education</h3>
        <div class="education-container">
          ${educationHTML}
        </div>
      </div>
    `;
  }

  createProjectsTab(projects) {
    const projectsHTML = projects.map(project => {
      const isPlaceholder = project.name && project.name.includes('No projects');
      
      const techsHTML = project.technologies && project.technologies.length > 0
        ? project.technologies.map(tech => {
            const isTechPlaceholder = tech.includes('not specified') || tech.includes('not found') || tech.includes('not listed');
            return `<span class="tech-badge ${isTechPlaceholder ? 'placeholder' : ''}">${this.prettifySkill(tech)}</span>`;
          }).join('')
        : '<span class="tech-badge placeholder">Tech not listed in resume</span>';
      
      return `
        <div class="project-item ${isPlaceholder ? 'placeholder-content' : ''}">
          <h4>${project.name || 'Project Name Not Specified'}</h4>
          <p class="description ${project.description && project.description.includes('not provided') ? 'placeholder-text' : ''}">${
            project.description || 'Project description not provided. Consider adding detailed descriptions to showcase your technical abilities and achievements.'
          }</p>
          <div class="technologies"><strong>Technologies:</strong> ${techsHTML}</div>
        </div>
      `;
    }).join('');
    
    return `
      <div class="tabContent" id="projects">
        <h3>🛠️ Projects</h3>
        <div class="projects-container">
          ${projectsHTML}
        </div>
      </div>
    `;
  }

  createJobMatchTab(jobMatch) {
    const skillsMatch = jobMatch.skills_match || {};
    const experienceMatch = jobMatch.experience_match || {};
    const educationMatch = jobMatch.education_match || {};
    
    return `
      <div class="tabContent" id="jobmatch">
        <h3>🎯 Job Compatibility Analysis</h3>
        
        <div class="match-summary">
          ${this.generatePieChart(jobMatch)}
          <div class="overall-score-text">
            <h4>${Math.round(jobMatch.overall_score || 0)}% overall match</h4>
          </div>
        </div>
        
        <div class="detailed-analysis">
          <div class="match-section">
            <h5>📊 Skills Match: ${Math.round(skillsMatch.match_percentage || 0)}%</h5>
            ${skillsMatch.matched_skills && skillsMatch.matched_skills.length > 0 ? `
              <p><strong>Matched Skills:</strong> ${skillsMatch.matched_skills.join(', ')}</p>
            ` : ''}
            ${skillsMatch.missing_skills && skillsMatch.missing_skills.length > 0 ? `
              <p><strong>Missing Skills:</strong> ${skillsMatch.missing_skills.join(', ')}</p>
            ` : ''}
          </div>
          
          <div class="match-section">
            <h5>💼 Experience Match: ${Math.round(experienceMatch.match_percentage || 0)}%</h5>
            ${experienceMatch.estimated_years ? `
              <p><strong>Your Experience:</strong> ${experienceMatch.estimated_years} years</p>
            ` : ''}
          </div>
          
          <div class="match-section">
            <h5>🎓 Education Match: ${Math.round(educationMatch.match_percentage || 0)}%</h5>
            <p><strong>Requirement Met:</strong> ${educationMatch.meets_requirement ? 'Yes' : 'No'}</p>
          </div>
        </div>
        
        ${jobMatch.recommendations && jobMatch.recommendations.length > 0 ? `
          <div class="recommendations">
            <h5>💡 Recommendations</h5>
            <ul>
              ${jobMatch.recommendations.map(rec => `<li>${rec}</li>`).join('')}
            </ul>
          </div>
        ` : ''}
      </div>
    `;
  }
}

// Initialize the application
document.addEventListener('DOMContentLoaded', () => {
  new ResumeParserUI();
});
