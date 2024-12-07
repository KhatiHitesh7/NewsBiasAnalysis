import subprocess
import sys

def run_app():
    try:
        # Run the Streamlit app
        subprocess.run([sys.executable, "-m", "streamlit", "run", "src/main.py"])
    except Exception as e:
        print(f"Error running the application: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    run_app()