import subprocess
import sys
import nltk

def install_dependencies():
    print("Installing dependencies...")
    try:
        # Uninstall potentially conflicting packages
        subprocess.check_call([sys.executable, "-m", "pip", "uninstall", "-y", "newspaper3k"])
        subprocess.check_call([sys.executable, "-m", "pip", "uninstall", "-y", "lxml"])
        
        # Install lxml with HTML clean support
        subprocess.check_call([sys.executable, "-m", "pip", "install", "lxml-html-clean"])
        
        # Install other requirements
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        
        print("Dependencies installed successfully!")
    except Exception as e:
        print(f"Error installing dependencies: {str(e)}")
        sys.exit(1)

def download_nltk_data():
    print("Downloading NLTK data...")
    try:
        nltk.download('punkt')
        nltk.download('averaged_perceptron_tagger')
        print("NLTK data downloaded successfully!")
    except Exception as e:
        print(f"Error downloading NLTK data: {str(e)}")
        sys.exit(1)

def main():
    install_dependencies()
    download_nltk_data()

if __name__ == "__main__":
    main()