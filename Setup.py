#!/usr/bin/env python3
"""
Setup script for Secure RAG Researcher
Automates environment setup and dependency installation.
"""

import os
import sys
import subprocess
from pathlib import Path


def print_step(step_num, total_steps, message):
    """Print formatted step message."""
    print(f"\n[{step_num}/{total_steps}] {message}")
    print("-" * 60)


def check_python_version():
    """Verify Python version is 3.8+."""
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print("❌ Python 3.8+ is required")
        print(f"Current version: {version.major}.{version.minor}.{version.micro}")
        return False
    print(f"✅ Python {version.major}.{version.minor}.{version.micro}")
    return True


def create_virtual_environment():
    """Create Python virtual environment."""
    venv_path = Path("venv")
    
    if venv_path.exists():
        print("⚠️  Virtual environment already exists")
        response = input("Recreate it? (y/n): ").lower()
        if response != 'y':
            print("Skipping virtual environment creation")
            return True
        print("Removing old virtual environment...")
        import shutil
        shutil.rmtree(venv_path)
    
    print("Creating virtual environment...")
    try:
        subprocess.run([sys.executable, "-m", "venv", "venv"], check=True)
        print("✅ Virtual environment created")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to create virtual environment: {e}")
        return False


def get_pip_command():
    """Get the correct pip command for the platform."""
    if sys.platform == "win32":
        return str(Path("venv/Scripts/pip"))
    return str(Path("venv/bin/pip"))


def install_dependencies():
    """Install required packages."""
    pip_cmd = get_pip_command()
    
    print("Installing dependencies from requirements.txt...")
    try:
        subprocess.run(
            [pip_cmd, "install", "-r", "requirements.txt"],
            check=True,
            capture_output=False
        )
        print("✅ Dependencies installed")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to install dependencies: {e}")
        return False


def setup_env_file():
    """Create .env file from template."""
    env_path = Path(".env")
    env_example_path = Path(".env.example")
    
    if env_path.exists():
        print("⚠️  .env file already exists")
        return True
    
    if not env_example_path.exists():
        print("❌ .env.example not found")
        return False
    
    print("Creating .env file...")
    with open(env_example_path, 'r') as f:
        content = f.read()
    
    with open(env_path, 'w') as f:
        f.write(content)
    
    print("✅ .env file created")
    print("\n⚠️  IMPORTANT: Edit .env and add your OpenAI API key!")
    print("Get your API key from: https://platform.openai.com/api-keys\n")
    
    return True


def create_directories():
    """Create necessary directories."""
    directories = ['data', 'vectorstore']
    
    for dir_name in directories:
        dir_path = Path(dir_name)
        if not dir_path.exists():
            dir_path.mkdir(parents=True)
            print(f"✅ Created {dir_name}/ directory")
        else:
            print(f"⚠️  {dir_name}/ directory already exists")
    
    return True


def generate_sample_pdf():
    """Generate sample security policy PDF."""
    pdf_path = Path("data/sample_security_policy.pdf")
    
    if pdf_path.exists():
        print("⚠️  Sample PDF already exists")
        response = input("Regenerate it? (y/n): ").lower()
        if response != 'y':
            print("Skipping PDF generation")
            return True
    
    print("Generating sample security policy PDF...")
    try:
        python_cmd = get_pip_command().replace("/pip", "/python").replace("\\pip", "\\python")
        subprocess.run([python_cmd, "generate_sample_pdf.py"], check=True)
        print("✅ Sample PDF generated")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to generate PDF: {e}")
        return False


def print_next_steps():
    """Print instructions for next steps."""
    print("\n" + "=" * 70)
    print("🎉 Setup Complete!")
    print("=" * 70)
    print("\nNext steps:")
    print("1. Edit .env and add your OpenAI API key")
    print("2. Activate the virtual environment:")
    
    if sys.platform == "win32":
        print("   venv\\Scripts\\activate")
    else:
        print("   source venv/bin/activate")
    
    print("\n3. Run the application:")
    print("   python main.py              # Run with sample queries")
    print("   python interactive.py       # Interactive mode")
    print("   python test_rag.py          # Run tests")
    
    print("\n4. (Optional) Add your own PDF to data/ and update config.py")
    print("\nFor more information, see README.md")
    print("=" * 70 + "\n")


def main():
    """Run the complete setup process."""
    print("=" * 70)
    print("🔧 Secure RAG Researcher - Setup Script")
    print("=" * 70)
    
    total_steps = 7
    
    # Step 1: Check Python version
    print_step(1, total_steps, "Checking Python version")
    if not check_python_version():
        return False
    
    # Step 2: Create virtual environment
    print_step(2, total_steps, "Creating virtual environment")
    if not create_virtual_environment():
        return False
    
    # Step 3: Install dependencies
    print_step(3, total_steps, "Installing dependencies")
    if not install_dependencies():
        return False
    
    # Step 4: Create .env file
    print_step(4, total_steps, "Setting up environment variables")
    if not setup_env_file():
        return False
    
    # Step 5: Create directories
    print_step(5, total_steps, "Creating project directories")
    if not create_directories():
        return False
    
    # Step 6: Install reportlab for PDF generation
    print_step(6, total_steps, "Installing PDF generation tools")
    pip_cmd = get_pip_command()
    try:
        subprocess.run([pip_cmd, "install", "reportlab"], check=True, capture_output=True)
        print("✅ PDF tools installed")
    except subprocess.CalledProcessError:
        print("⚠️  Could not install reportlab, skipping PDF generation")
    
    # Step 7: Generate sample PDF
    print_step(7, total_steps, "Generating sample document")
    generate_sample_pdf()
    
    # Print next steps
    print_next_steps()
    
    return True


if __name__ == "__main__":
    try:
        success = main()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n\n⚠️  Setup cancelled by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        sys.exit(1)
