# ResumeTracker_NLPProject
![image](https://github.com/user-attachments/assets/47ea81ce-9a8d-4e2f-b7df-2235a2003778)


---

# ATS Resume Expert 📄

The **ATS Resume Expert** is a Streamlit-based web application that leverages AI to analyze resumes against job descriptions. It provides valuable insights, including skill matching, experience alignment, and an ATS compatibility score.

## Features
- **Job Description Input**: Paste job descriptions and compare them with resumes.
- **Resume Upload**: Upload a resume in PDF format to evaluate its fit for a given job.
- **ATS Analysis**: Get a match percentage between the job description and resume, along with keyword analysis.
- **Summary**: Automatically generate a concise summary of the resume highlighting key skills and experience.

## Demo
You can interact with the application through the live demo (provide link if available). Alternatively, follow the setup instructions below to run the app locally.

## Prerequisites

Before running this app, you’ll need:

- Python 3.6 or above
- `pip` for installing Python dependencies
- Poppler for PDF to image conversion (required by `pdf2image`)

## Setup Instructions

Follow these steps to set up the project locally:

### Step 1: Clone the Repository

```bash
git clone https://github.com/yourusername/ats-resume-expert.git
cd ats-resume-expert
```

### Step 2: Create a Virtual Environment (Optional but Recommended)

You can use `venv` or `conda` to create an isolated environment for the project:

#### Using `venv`:
```bash
python -m venv venv
source venv/bin/activate  # On macOS/Linux
.\venv\Scripts\activate  # On Windows
```

#### Using `conda` (optional):
```bash
conda create --name ats-resume-expert python=3.9
conda activate ats-resume-expert
```

### Step 3: Install Dependencies

Ensure you have the required dependencies installed by running:

```bash
pip install -r requirements.txt
```

**Note**: `pdf2image` requires **Poppler** to be installed on your system for PDF-to-image conversion.

#### For macOS:
Install Poppler using Homebrew:

```bash
brew install poppler
```

#### For Ubuntu/Linux:
```bash
sudo apt-get install poppler-utils
```

#### For Windows:
1. Download the Poppler binaries from [this link](http://blog.alivate.com.au/poppler-windows/).
2. Extract the files and add the path to the `bin` folder to your system’s `PATH` variable.

### Step 4: Run the Streamlit App

Once everything is set up, run the app with the following command:

```bash
streamlit run app.py
```

The app will start, and you can access it by navigating to `http://localhost:8501` in your web browser.

### Step 5: Using the App

1. **Job Description**: Paste the job description into the text area. The AI will compare this with the uploaded resume to provide feedback.
2. **Upload Resume**: Upload your resume in PDF format. The app will analyze it for skills, experience, and ATS compatibility.
3. **Actions**: You can choose between:
   - **Analyze**: Evaluate the match between the resume and job description.
   - **Match**: Get a percentage match and keyword analysis.
   - **Summarize**: Summarize the resume, focusing on key points like skills and experience.

## Example Usage

1. Paste a job description in the left column.
2. Upload a resume in PDF format in the right column.
3. Click **Analyze**, **Match**, or **Summarize** to get insights on how well the resume fits the job description.

## Requirements

The app requires the following Python libraries:

- `streamlit`: For building the web app interface.
- `pillow`: For image processing (used by `pdf2image`).
- `pdf2image`: For converting PDF pages to images.
- `google-generativeai`: For AI-based resume analysis.
- `base64`: For encoding image data (already part of Python's standard library).

You can install all the dependencies using:

```bash
pip install -r requirements.txt
```

## Troubleshooting

### Issue: `ModuleNotFoundError: No module named 'pdf2image'`

If you encounter this error, make sure `pdf2image` is installed and Poppler is available on your system.

1. **Install `pdf2image`**: 
    ```bash
    pip install pdf2image
    ```

2. **Install Poppler** (as described in Step 3 above).

### Issue: `No matching distribution found for base64`

This is because `base64` is a **built-in module** in Python, so you don't need to install it separately. Remove `base64` from the `requirements.txt` file.

### Issue: Poppler Installation

If Poppler is not installed or recognized, check the installation instructions for your operating system (macOS, Ubuntu, or Windows).

## Contributing

Feel free to open issues or pull requests if you have any improvements or bug fixes. This project is open for contributions!

### Steps to contribute:
1. Fork the repository.
2. Create a new branch for your feature or bugfix.
3. Commit your changes.
4. Open a pull request for review.
 your specific project structure, features, and usage scenarios. You may want to add screenshots or additional details about the app’s features for better clarity.
