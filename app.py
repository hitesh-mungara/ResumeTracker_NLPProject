import base64
import streamlit as st
import os
import io
from PIL import Image
import pdf2image
import google.generativeai as genai

# Configure page
st.set_page_config(
    page_title="ATS Resume Expert",
    page_icon="📄",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS for premium styling
st.markdown("""
    <style>
        /* Main app styling */
        .stApp {
            background: linear-gradient(135deg, #f6f9fc 0%, #eef2f7 100%);
        }
        
        /* Header styling */
        .main-header {
            text-align: center;
            padding: 3rem 0;
            margin-bottom: 3rem;
            background: linear-gradient(135deg, #1a2980 0%, #26d0ce 100%);
            color: white;
            border-radius: 0 0 30px 30px;
            box-shadow: 0 4px 20px rgba(0,0,0,0.1);
        }
        
        .main-header h1 {
            color: white !important;
            font-size: 2.8rem !important;
            font-weight: 800 !important;
            margin: 0 !important;
            padding: 0 !important;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.2);
            letter-spacing: 1px;
        }
        
        .main-header .subtitle {
            color: rgba(255,255,255,0.9);
            font-size: 1.2rem;
            margin-top: 0.5rem;
            font-weight: 300;
        }
        
        /* Section styling */
        .content-section {
            background-color: white;
            padding: 2.5rem;
            border-radius: 20px;
            box-shadow: 0 8px 30px rgba(0,0,0,0.05);
            margin-bottom: 2rem;
            border: 1px solid rgba(255,255,255,0.8);
            backdrop-filter: blur(20px);
            transition: transform 0.3s ease, box-shadow 0.3s ease;
        }
        
        .content-section:hover {
            transform: translateY(-5px);
            box-shadow: 0 12px 40px rgba(0,0,0,0.08);
        }
        
        /* Custom container */
        .custom-container {
            max-width: 1400px;
            margin: 0 auto;
            padding: 0 2rem;
        }
        
        /* Button styling */
        .stButton button {
            background: linear-gradient(135deg, #1a2980 0%, #26d0ce 100%);
            color: white;
            border: none;
            padding: 0.8rem 1.5rem;
            border-radius: 12px;
            font-weight: 600;
            font-size: 1rem;
            transition: all 0.3s ease;
            text-transform: uppercase;
            letter-spacing: 0.5px;
            box-shadow: 0 4px 15px rgba(0,0,0,0.1);
        }
        
        .stButton button:hover {
            transform: translateY(-3px);
            box-shadow: 0 8px 25px rgba(0,0,0,0.15);
            background: linear-gradient(135deg, #26d0ce 0%, #1a2980 100%);
        }
        
        /* Enhanced Text Area Styling */
        .stTextArea textarea {
            border-radius: 12px;
            border: 2px solid #e0e6ed;
            padding: 1.2rem;
            font-size: 1rem;
            transition: all 0.3s ease;
            background-color: #ffffff;
            min-height: 300px !important;
            color: #1a2980 !important;
            font-family: 'Inter', sans-serif;
            line-height: 1.5;
            resize: vertical;
            white-space: pre-wrap;
            word-wrap: break-word;
            overflow-y: auto;
        }
        
        .stTextArea textarea:focus {
            border-color: #26d0ce;
            box-shadow: 0 0 0 2px rgba(38,208,206,0.1);
            background-color: #ffffff;
        }
        
        .stTextArea textarea::placeholder {
            color: #8e9aaf;
            opacity: 0.8;
        }
        
        /* File uploader styling */
        .uploadedFile {
            border-radius: 12px;
            padding: 1.5rem;
            background-color: #f8fafc;
            border: 2px dashed #e0e6ed;
            transition: all 0.3s ease;
        }
        
        .uploadedFile:hover {
            border-color: #26d0ce;
            background-color: #f0f4f8;
        }
        
        /* Success message styling */
        .success-message {
            padding: 1.2rem;
            background: linear-gradient(135deg, #26d0ce 0%, #1a2980 100%);
            color: white;
            border-radius: 12px;
            margin: 1rem 0;
            text-align: center;
            font-weight: 500;
            box-shadow: 0 4px 15px rgba(38,208,206,0.2);
            animation: slideIn 0.5s ease-out;
        }
        
        /* Updated Analysis Result Styling */
        .analysis-result {
            background-color: white;
            padding: 2rem;
            border-radius: 12px;
            margin-top: 1rem;
            border-left: 4px solid #1a2980;
            font-size: 1.1rem;
            line-height: 1.8;
            color: #334155;
            white-space: pre-line;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.05);
        }
        
        .analysis-result strong {
            color: #1a2980;
            font-weight: 600;
        }
        
        .analysis-result ul {
            list-style-type: disc;
            margin-left: 1.5rem;
            margin-top: 1rem;
            margin-bottom: 1rem;
        }
        
        .analysis-result li {
            margin-bottom: 0.5rem;
        }
        
        .analysis-section {
            margin-bottom: 1.5rem;
            padding-bottom: 1.5rem;
            border-bottom: 1px solid #e5e7eb;
        }
        
        .analysis-section:last-child {
            border-bottom: none;
            margin-bottom: 0;
            padding-bottom: 0;
        }
        
        .match-percentage {
            font-size: 2rem;
            font-weight: 700;
            color: #1a2980;
            text-align: center;
            padding: 1rem;
            margin-bottom: 1.5rem;
            background: linear-gradient(135deg, rgba(26,41,128,0.1) 0%, rgba(38,208,206,0.1) 100%);
            border-radius: 8px;
        }
        
        .keywords-missing {
            background-color: #fff1f2;
            padding: 1rem;
            border-radius: 8px;
            margin: 1rem 0;
            border-left: 4px solid #ef4444;
        }
        
        .final-thoughts {
            background-color: #f0f9ff;
            padding: 1rem;
            border-radius: 8px;
            margin: 1rem 0;
            border-left: 4px solid #0ea5e9;
        }
        
        /* Response section styling */
        .response-section {
            background: white;
            padding: 2.5rem;
            border-radius: 20px;
            box-shadow: 0 8px 30px rgba(0,0,0,0.05);
            margin-top: 2rem;
            border: 1px solid rgba(255,255,255,0.8);
            animation: fadeIn 0.5s ease-out;
        }
        
        /* Hide Streamlit branding */
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        
        /* Header styling */
        .section-header {
            color: #1a2980;
            font-size: 1.6rem;
            font-weight: 700;
            margin-bottom: 1.5rem;
            display: flex;
            align-items: center;
            gap: 0.5rem;
        }
        
        .section-header::before {
            content: '';
            display: inline-block;
            width: 4px;
            height: 24px;
            background: linear-gradient(to bottom, #1a2980, #26d0ce);
            border-radius: 4px;
            margin-right: 0.5rem;
        }
        
        /* Text counter */
        .text-counter {
            font-size: 0.8rem;
            color: #6b7280;
            text-align: right;
            margin-top: 0.5rem;
        }
        
        /* Animations */
        @keyframes slideIn {
            from {
                transform: translateY(-10px);
                opacity: 0;
            }
            to {
                transform: translateY(0);
                opacity: 1;
            }
        }
        
        @keyframes fadeIn {
            from {
                opacity: 0;
            }
            to {
                opacity: 1;
            }
        }
        
        /* Error message styling */
        .stAlert {
            background: linear-gradient(135deg, #ff6b6b 0%, #ff8e8e 100%);
            color: white;
            border: none;
            border-radius: 12px;
            padding: 1rem 1.5rem;
            box-shadow: 0 4px 15px rgba(255,107,107,0.2);
            animation: slideIn 0.5s ease-out;
        }
    </style>
""", unsafe_allow_html=True)


# Configure Gemini
genai.configure(api_key="AIzaSyBsTtGoCiG13nZqe5JZPK_HaYh14tnAkgw")

def get_gemini_response(input_text, pdf_content, prompt):
    model = genai.GenerativeModel('gemini-1.5-flash')
    response = model.generate_content([input_text, pdf_content[0], prompt])
    return response.text

def get_summary(pdf_content):
    summary_prompt = """
    Summarize this resume content in a few concise bullet points. Focus on key skills, experience, and any standout details.
    """
    summary_response = get_gemini_response("", pdf_content, summary_prompt)
    return summary_response

def input_pdf_setup(uploaded_file):
    if uploaded_file is not None:
        images = pdf2image.convert_from_bytes(uploaded_file.read())
        first_page = images[0]
        img_byte_arr = io.BytesIO()
        first_page.save(img_byte_arr, format='JPEG')
        img_byte_arr = img_byte_arr.getvalue()
        pdf_parts = [
            {
                "mime_type": "image/jpeg",
                "data": base64.b64encode(img_byte_arr).decode()
            }
        ]
        return pdf_parts
    else:
        raise FileNotFoundError("No file uploaded")

def format_analysis_response(response_text, is_match_analysis=False):
    """Format the analysis response for better display"""
    if is_match_analysis:
        sections = response_text.split('\n\n')
        formatted_text = ""
        
        for section in sections:
            section = section.strip()
            if "%" in section[:50]:
                formatted_text += f'<div class="match-percentage">{section}</div>'
            elif "missing" in section.lower() or "keyword" in section.lower():
                formatted_text += f'<div class="keywords-missing">{section}</div>'
            elif "thought" in section.lower() or "conclusion" in section.lower():
                formatted_text += f'<div class="final-thoughts">{section}</div>'
            else:
                formatted_text += f'<div class="analysis-section">{section}</div>'
        
        return formatted_text
    else:
        sections = response_text.split('\n\n')
        formatted_sections = []
        for section in sections:
            if section.strip():
                formatted_sections.append(f'<div class="analysis-section">{section.strip()}</div>')
        return ''.join(formatted_sections)

# Main App UI
st.markdown("""
    <div class='main-header'>
        <h1>📄 ATS Resume Expert</h1>
        <div class='subtitle'>AI-Powered Resume Analysis & Job Matching</div>
    </div>
""", unsafe_allow_html=True)

# Create container for content
st.markdown("<div class='custom-container'>", unsafe_allow_html=True)

# Create two columns for job description and resume upload
col1, col2 = st.columns([6, 4])

with col1:
    st.markdown("<div class='content-section'>", unsafe_allow_html=True)
    st.markdown("<div class='section-header'>📝 Job Description</div>", unsafe_allow_html=True)
    
    # Job Description Input
    input_text = st.text_area(
        "",
        value="",
        height=300,
        placeholder="Paste your job description here...",
        key="job_description_input_1234",
        help="Paste or type the job description here. The text will automatically wrap and scroll if needed."
    )
    
    # Character counter
    if input_text:
        st.markdown(f"<div class='text-counter'>{len(input_text)} characters</div>", unsafe_allow_html=True)
    
    st.markdown("</div>", unsafe_allow_html=True)

with col2:
    st.markdown("<div class='content-section'>", unsafe_allow_html=True)
    st.markdown("<div class='section-header'>📤 Upload Resume</div>", unsafe_allow_html=True)
    
    # File Upload
    uploaded_file = st.file_uploader(
        "",
        type=["pdf"],
        help="Upload your resume in PDF format"
    )
    
    if uploaded_file:
        st.markdown("""
            <div class='success-message'>
                ✨ Resume uploaded successfully!
            </div>
        """, unsafe_allow_html=True)
    
    # Action Buttons
    col_btn1, col_btn2, col_btn3 = st.columns(3)
    with col_btn1:
        submit1 = st.button("📋 Analyze", use_container_width=True)
    with col_btn2:
        submit3 = st.button("🎯 Match", use_container_width=True)
    with col_btn3:
        submit_summary = st.button("📝 Summarize", use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)

# Input prompts
input_prompt1 = """
You are an experienced Technical Human Resource Manager, your task is to review the provided resume against the job description.
Please share your professional evaluation on whether the candidate's profile aligns with the role.
Highlight the strengths and weaknesses of the applicant in relation to the specified job requirements.
"""

input_prompt3 = """
You are an skilled ATS (Applicant Tracking System) scanner with a deep understanding of data science and ATS functionality,
your task is to evaluate the resume against the provided job description. give me the percentage of match if the resume matches
the job description. First the output should come as percentage and then keywords missing and last final thoughts.
"""

# Handle button actions and display results
if submit1 or submit3 or submit_summary:
    if uploaded_file is None:
        st.error("⚠️ Please upload your resume to proceed!")
    elif not input_text and not submit_summary:
        st.error("⚠️ Please provide a job description!")
    else:
        with st.spinner("🔄 Processing..."):
            try:
                pdf_content = input_pdf_setup(uploaded_file)
                if submit_summary:
                    summary = get_summary(pdf_content)
                    st.markdown("<div class='response-section'>", unsafe_allow_html=True)
                    st.markdown("<div class='section-header'>📝 Summary</div>", unsafe_allow_html=True)
                    st.markdown(f"<div class='analysis-result'>{summary}</div>", unsafe_allow_html=True)
                    st.markdown("</div>", unsafe_allow_html=True)
                else:
                    prompt = input_prompt1 if submit1 else input_prompt3
                    response = get_gemini_response(input_text, pdf_content, prompt)
                    st.markdown("<div class='response-section'>", unsafe_allow_html=True)
                    st.markdown("<div class='section-header'>🎯 Analysis Results</div>", unsafe_allow_html=True)
                    st.markdown(f"<div class='analysis-result'>{response}</div>", unsafe_allow_html=True)
                    st.markdown("</div>", unsafe_allow_html=True)
            except Exception as e:
                st.error(f"⚠️ An error occurred: {str(e)}")

st.markdown("</div>", unsafe_allow_html=True)  # Close custom-container
