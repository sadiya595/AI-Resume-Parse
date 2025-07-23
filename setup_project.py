#!/usr/bin/env python3
"""
Setup script for AI Resume Parser project
Creates the initial folder structure and placeholder files
"""

import os

def create_folder_structure():
    """Create the complete folder structure for the project"""

    folders = [
        'utils',
        'static/css',
        'static/js', 
        'static/uploads',
        'static/images',
        'templates',
        'tests/sample_resumes',
        'data/models',
        'docs'
    ]

    for folder in folders:
        os.makedirs(folder, exist_ok=True)
        print(f"✅ Created folder: {folder}")

    # Create placeholder files
    placeholder_files = [
        'utils/__init__.py',
        'tests/__init__.py',
        'static/uploads/.gitkeep',
        'tests/sample_resumes/.gitkeep',
        'data/models/.gitkeep'
    ]

    for file_path in placeholder_files:
        with open(file_path, 'w') as f:
            f.write('# Placeholder file\n')
        print(f"✅ Created placeholder: {file_path}")

if __name__ == "__main__":
    print("🚀 Setting up AI Resume Parser project structure...")
    create_folder_structure()
    print("\n✅ Project structure created successfully!")
    print("\nNext steps:")
    print("1. Create virtual environment: python -m venv venv")
    print("2. Activate virtual environment:")
    print("   - Windows: venv\\Scripts\\activate")
    print("   - Mac/Linux: source venv/bin/activate")
    print("3. Install dependencies: pip install -r requirements.txt")