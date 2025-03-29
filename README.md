1. Install Python
If you don't have Python installed, download the latest version from the official Python website (python.org) and install it. Make sure to add Python to your system's PATH during installation.
2. Create a Virtual Environment (Recommended)
Creating a virtual environment is highly recommended to isolate the dependencies of this project from your global Python environment. This prevents conflicts and keeps your system organized.
Open your terminal or command prompt and navigate to the directory where you want to store your project.
Create a virtual environment using venv (recommended for Python 3.3+):
 
python -m venv .venv
Use code with caution
Activate the virtual environment:
Windows:
 
.venv\Scripts\activate
Use code with caution
macOS/Linux:
 
source .venv/bin/activate
Use code with caution
3. Install Dependencies
Create a file named requirements.txt in your project directory and add the following lines:
 
chromadb
pypdf
groq
gradio
langchain-community
sentence-transformers
Use code with caution
Install the dependencies using pip:
 
pip install -r requirements.txt
Use code with caution
4. Download the HR Policy PDF
Download the Nestlé HR Policy PDF file (nestle_hr_policy.pdf) and place it in the same directory as your Python code.
5. Obtain a Groq API Key
To use the Groq API, you need to obtain an API key. You can sign up for an account on the Groq website and generate an API key.
Replace "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" in the code with your actual API key.
6. Run the Code
Save the provided Python code as a .py file (e.g., hr_chatbot.py).
In your terminal (with the virtual environment activated), execute the code using the following command:
 
python hr_chatbot.py
Use code with caution
7. Access the Chatbot Interface
Once the code is running, it will launch a Gradio interface. It might display a local URL (e.g., http://127.0.0.1:7860/) in your terminal.
Open this URL in your web browser to access the chatbot interface and start asking questions.
Important Considerations
Firewall/Antivirus: Make sure your firewall or antivirus software is not blocking the Gradio interface from running or accessing the internet.
Troubleshooting: If you encounter errors during installation or execution, carefully review the error messages. Check if all dependencies are installed correctly and if the required files are in the correct locations.
By following these steps, you should be able to run the Nestlé HR Assistant Chatbot code on your PC. Let me know if you have any other questions.
