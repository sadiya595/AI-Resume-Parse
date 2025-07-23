const dropArea = document.getElementById('drop-area');
const fileInput = document.getElementById('fileInput');
const uploadBtn = document.getElementById('uploadBtn');
const statusDiv = document.getElementById('status');
const resultTabs = document.getElementById('resultTabs');
const jobDesc = document.getElementById('jobDescription');

dropArea.addEventListener('click', () => {
    fileInput.click();
});

fileInput.addEventListener('change', () => {
    handleFiles(fileInput.files);
});

dropArea.addEventListener('dragover', (event) => {
    event.preventDefault();
    dropArea.style.background = '#eee';
});
dropArea.addEventListener('dragleave', () => {
    dropArea.style.background = '';
});
dropArea.addEventListener('drop', (event) => {
    event.preventDefault();
    dropArea.style.background = '';
    handleFiles(event.dataTransfer.files);
});

function handleFiles(files) {
    if (files.length > 0) {
        // Show filename or feedback if needed
        alert(`Selected file: ${files[0].name}`);
    }
}

uploadBtn.addEventListener('click', () => {
    const files = fileInput.files;
    if (files.length === 0) {
        alert('Please select a resume file.');
        return;
    }
    const formData = new FormData();
    formData.append('resume', files[0]);
    formData.append('job_description', jobDesc.value);

    statusDiv.innerText = 'Uploading...';

    fetch('/upload', {
        method: 'POST',
        body: formData
    })
    .then(res => res.json())
    .then(data => {
        statusDiv.innerText = data.message;
        displayResults(data.parsed_data); // Future implementation
    })
    .catch(() => {
        statusDiv.innerText = 'Error uploading file.';
    });
});

function displayResults(data) {
    // For now, just show dummy tabbed interface
    resultTabs.innerHTML = `
        <div class="tabs">
            <div class="tab active" data-tab="overview">Overview</div>
            <div class="tab" data-tab="skills">Skills</div>
            <div class="tab" data-tab="experience">Experience</div>
        </div>
        <div class="tabContent active" id="overview">Parsed data will appear here.</div>
        <div class="tabContent" id="skills">Skills info will appear here.</div>
        <div class="tabContent" id="experience">Experience details will appear here.</div>
    `;

    document.querySelectorAll('.tab').forEach(tab => {
        tab.addEventListener('click', () => {
            document.querySelectorAll('.tab').forEach(t => t.classList.remove('active'));
            document.querySelectorAll('.tabContent').forEach(c => c.classList.remove('active'));
            tab.classList.add('active');
            document.getElementById(tab.dataset.tab).classList.add('active');
        });
    });
}
