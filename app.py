# import streamlit as st
# from dotenv import load_dotenv
# import base64
# import os
# import io
# from PIL import Image
# import pdf2image
# import google.generativeai as genai
# import matplotlib.pyplot as plt
# import pandas as pd
# import re
# import speech_recognition as sr
# import pyaudio


# # Load environment variables
# load_dotenv()

# # Configure the Google API Key
# genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# # Streamlit app configuration
# st.set_page_config(page_title="ATS Resume Expert", page_icon="📄", layout="wide")

# # Add custom CSS for styling
# st.markdown("""
#     <style>
#     body {
#         background-color: #f7f9fc;
#     }
#     .css-18ni7ap {
#         background-color: #ffffff;
#         border-radius: 10px;
#         box-shadow: 0px 4px 8px rgba(0, 0, 0, 0.1);
#         padding: 20px;
#     }
#     .css-1d391kg {
#         color: #0073e6;
#         font-weight: bold;
#         font-size: 24px;
#     }
#     .stButton>button {
#         background-color: #0073e6;
#         color: white;
#         border-radius: 8px;
#         padding: 10px 20px;
#         font-size: 16px;
#     }
#     .stTextInput {
#         border-radius: 10px;
#         border: 1px solid #ddd;
#     }
#     .css-145kmo2 {
#         border-radius: 8px;
#     }
#     </style>
# """, unsafe_allow_html=True)

# # Header Section
# st.title("📄 ATS Resume Expert")
# st.markdown("Evaluate and optimize your resume for job applications using ATS Resume Expert.")

# # Sidebar for instructions
# st.sidebar.header("📝 How It Works")
# st.sidebar.write("""
# 1. Enter or paste the job description.
# 2. Upload your resume (PDF format).
# 3. Select an action: Evaluation Summary or Percentage Match.
# 4. Get Candidate Email and Phone Number.
# 5. Get Candidate is Eligible Or Not.
# """)
# st.sidebar.info("Ensure your resume is in PDF format.")

# # Function to record speech and convert to text
# def record_speech():
#     recognizer = sr.Recognizer()
#     with sr.Microphone() as source:
#         st.info("Listening... Speak clearly into the microphone.")
#         try:
#             audio = recognizer.listen(source, timeout=10)
#             st.success("Audio recorded. Processing...")
#             text = recognizer.recognize_google(audio)
#             return text
#         except sr.UnknownValueError:
#             st.error("Sorry, I could not understand your speech. Please try again.")
#         except sr.RequestError as e:
#             st.error(f"Could not request results; {e}")
#         except Exception as e:
#             st.error(f"An error occurred: {e}")
#     return None

# # Job description input and file upload
# st.subheader("🔍 Job Description")
# input_text = st.text_area("Paste the Job Description here:", placeholder="Enter Job Description Here...", height=200)

# # Speech-to-Text Button
# if st.button("🎙️ Record Job Description"):
#     speech_text = record_speech()
#     if speech_text:
#         input_text += f"\n{speech_text}"  # Append speech result to input_text
#         st.success("Job description updated with your speech input!")

# uploaded_file = st.file_uploader("📤 Upload your resume (PDF only):", type=["pdf"])

# # The rest of your code continues here...



# # Function to process PDF input
# def input_pdf_setup(uploaded_file):
#     if uploaded_file:
#         images = pdf2image.convert_from_bytes(uploaded_file.read())
#         first_page = images[0]

#         img_byte_arr = io.BytesIO()
#         first_page.save(img_byte_arr, format='JPEG')
#         img_byte_arr = img_byte_arr.getvalue()

#         pdf_parts = [{"mime_type": "image/jpeg", "data": base64.b64encode(img_byte_arr).decode()}]
#         return pdf_parts
#     else:
#         raise FileNotFoundError("No file uploaded")

# # Function to get response from Gemini
# def get_gemini_response(input_text, pdf_content, prompt):
#     model = genai.GenerativeModel('gemini-1.5-flash')
#     response = model.generate_content([input_text, pdf_content[0], prompt])
#     return response.text

# # Enhanced prompts
# input_prompt1 = """
# You are an experienced Technical Human Resource Manager. Review the provided resume against the job description.
# Provide a professional evaluation, highlighting the strengths and weaknesses of the candidate for the specified role.
# """

# input_prompt3 = """
# You are a skilled ATS scanner. Evaluate the resume against the job description, and provide:
# 1. A match percentage.
# 2. Missing keywords.
# 3. Final thoughts on the resume's relevance.
# """

# # Function to extract email and phone number from resume text
# def extract_contact_info(resume_text):
#     # Regex pattern for email
#     email_pattern = r'[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+'
#     email = re.findall(email_pattern, resume_text)

#     # Regex pattern for phone number
#     phone_pattern = r'\+?\d{10,15}'
#     phone = re.findall(phone_pattern, resume_text)

#     # Extracting the first email and phone number (if available)
#     extracted_email = email[0] if email else "Not Found"
#     extracted_phone = phone[0] if phone else "Not Found"
    
#     return extracted_email, extracted_phone

# # Function to check eligibility based on user input
# def check_eligibility(resume_text, min_12_percentage, min_diploma_percentage):
#     # Check phone number
#     phone_number = re.search(r'\+?\d{10,15}', resume_text)
#     phone_valid = phone_number is not None

#     # Check email
#     email = re.search(r'@+', resume_text)
#     email_valid = email is not None

#     # Check for at least 3 projects
#     projects = len(re.findall(r'project', resume_text, re.IGNORECASE)) >= 3

#     # Check for internships
#     internships = "internship" in resume_text.lower()

#     # Check eligibility based on 12th or diploma percentage criteria
#     eligible = False
#     if "10th" in resume_text:
#         percentage = re.search(r'\d{2,3}%?', resume_text)
#         if percentage and int(percentage.group().replace('%', '')) >= min_10_percentage:
#             eligible = True
#     if "12th" in resume_text:
#         percentage = re.search(r'\d{2,3}%?', resume_text)
#         if percentage and int(percentage.group().replace('%', '')) >= min_12_percentage:
#             eligible = True
#     if not eligible and "diploma" in resume_text and projects:
#         percentage = re.search(r'\d{2,3}%?', resume_text)
#         if percentage and int(percentage.group().replace('%', '')) >= min_diploma_percentage:
#             eligible = True

#     return {
#         "phone_valid": phone_valid,
#         "email_valid": email_valid,
#         "projects": projects,
#         "internships": internships,
#         "eligible": eligible,
#     }

# # User input for eligibility criteria
# st.sidebar.header("Set Eligibility Criteria")
# min_10_percentage = st.sidebar.number_input("Minimum 10th Percentage (%)", min_value=0, max_value=100, value=60)
# min_12_percentage = st.sidebar.number_input("Minimum 12th Percentage (%)", min_value=0, max_value=100, value=60)
# min_diploma_percentage = st.sidebar.number_input("Minimum Diploma Percentage (%)", min_value=0, max_value=100, value=60)

# # Action buttons
# col1, col2 = st.columns(2)
# with col1:
#     submit1 = st.button("📋 Tell Me About the Resume")
# with col2:
#     submit3 = st.button("📊 Percentage Match")

# # Evaluation Section
# response = 'No evaluation performed.'  # Default response
# eligibility_results = None

# if submit1:
#     if uploaded_file:
#         pdf_content = input_pdf_setup(uploaded_file)
#         response = get_gemini_response(input_text, pdf_content, input_prompt1)
#         st.subheader("💬 Evaluation Summary")
#         st.success(response)
#     else:
#         st.warning("Please upload a resume.")

# if submit3:
#     if uploaded_file:
#         pdf_content = input_pdf_setup(uploaded_file)
#         response = get_gemini_response(input_text, pdf_content, input_prompt3)
#         st.subheader("📊 Match Analysis")
#         st.success(response)

#         # Visualization: Pie Chart
#         data = {"Matched": 70, "Missing": 30}  # Example data
#         fig, ax = plt.subplots(figsize=(4, 4))  # Adjusted smaller size
#         wedges, texts, autotexts = ax.pie(
#             data.values(), 
#             labels=data.keys(), 
#             autopct='%1.1f%%', 
#             startangle=90, 
#             colors=["#4CAF50", "#FF5722"], 
#             textprops=dict(color="w")
#         )
#         ax.legend(wedges, data.keys(), title="Legend", loc="center left", bbox_to_anchor=(1, 0, 0.5, 1))
#         ax.set_title("Resume Match Percentage", fontsize=12)  # Slightly smaller font size
#         st.pyplot(fig)

#         # Comparison Table
#         match_data = {
#             "Criteria": ["Python", "SQL", "Team Management"],
#             "Resume": ["Yes", "No", "Yes"],
#             "Job Requirement": ["Yes", "Yes", "Yes"]
#         }
#         df = pd.DataFrame(match_data)
#         st.write("🔎 **Skill Comparison Table**")
#         st.table(df)
#     else:
#         st.warning("Please upload a resume.")

# # Eligibility Check Button
# col1, col2 = st.columns(2)
# with col1:
#     check_eligibility_button = st.button("🔍 Check Eligibility")
# with col2:
#     candidate_info_button = st.button("👤 Candidate Info")

# # Candidate Info Extraction
# if candidate_info_button:
#     if uploaded_file:
#         pdf_content = input_pdf_setup(uploaded_file)
#         resume_text = get_gemini_response(input_text, pdf_content, "")
        
#         # Extract email and phone number from the resume text
#         extracted_email, extracted_phone = extract_contact_info(resume_text)

#         # Display the extracted information
#         st.subheader("📋 Candidate Info")
#         st.write(f"Email: {extracted_email}")
#         st.write(f"Phone: {extracted_phone}")
#     else:
#         st.warning("Please upload a resume.")

# # Eligibility Check Section
# if check_eligibility_button:
#     if uploaded_file:
#         pdf_content = input_pdf_setup(uploaded_file)
#         resume_text = get_gemini_response(input_text, pdf_content, "")

#         # Check eligibility based on the resume content
#         eligibility_results = check_eligibility(resume_text, min_12_percentage, min_diploma_percentage)

#         # Display eligibility results
#         st.subheader("📑 Eligibility Status")
#         st.write(f"Phone Valid: {eligibility_results['phone_valid']}")
#         st.write(f"Email Valid: {eligibility_results['email_valid']}")
#         st.write(f"Has at least 3 projects: {eligibility_results['projects']}")
#         st.write(f"Has internship: {eligibility_results['internships']}")
#         st.write(f"Eligible for the position: {eligibility_results['eligible']}")

#     else:
#         st.warning("Please upload a resume.")



import streamlit as st
from dotenv import load_dotenv
import base64
import os
import io
from PIL import Image
import pdf2image
import google.generativeai as genai
import matplotlib.pyplot as plt
import pandas as pd
import re
import speech_recognition as sr
import pyaudio

# Load environment variables
load_dotenv()

# Configure the Google API Key
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Streamlit app configuration
st.set_page_config(page_title="ATS Resume Expert", page_icon="📄", layout="wide")

# Add custom CSS for styling
st.markdown("""
    <style>
    body {
        background-color: #f7f9fc;
    }
    .css-18ni7ap {
        background-color: #ffffff;
        border-radius: 10px;
        box-shadow: 0px 4px 8px rgba(0, 0, 0, 0.1);
        padding: 20px;
    }
    .css-1d391kg {
        color: #0073e6;
        font-weight: bold;
        font-size: 24px;
    }
    .stButton>button {
        background-color: #0073e6;
        color: white;
        border-radius: 8px;
        padding: 10px 20px;
        font-size: 16px;
    }
    .stTextInput {
        border-radius: 10px;
        border: 1px solid #ddd;
    }
    .css-145kmo2 {
        border-radius: 8px;
    }
    </style>
""", unsafe_allow_html=True)

# Header Section
st.title("📄 ATS Resume Expert")
st.markdown("Evaluate and optimize your resume for job applications using ATS Resume Expert.")

# Sidebar for instructions
st.sidebar.header("📝 How It Works")
st.sidebar.write("""
1. Enter or paste the job description.
2. Upload your resume (PDF format).
3. Select an action: Evaluation Summary or Percentage Match.
4. Get Candidate Email and Phone Number.
5. Get Candidate is Eligible Or Not.
""")
st.sidebar.info("Ensure your resume is in PDF format.")

# Function to record speech and convert to text
def record_speech():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        st.info("Listening... Speak clearly into the microphone.")
        try:
            audio = recognizer.listen(source, timeout=10)
            st.success("Audio recorded. Processing...")
            text = recognizer.recognize_google(audio)
            return text
        except sr.UnknownValueError:
            st.error("Sorry, I could not understand your speech. Please try again.")
        except sr.RequestError as e:
            st.error(f"Could not request results; {e}")
        except Exception as e:
            st.error(f"An error occurred: {e}")
    return None

# Job description input and file upload
st.subheader("🔍 Job Description")
input_text = st.text_area("Paste the Job Description here:", placeholder="Enter Job Description Here...", height=100)

# Speech-to-Text Button
if st.button("🎙️ Record Job Description"):
    speech_text = record_speech()
    if speech_text:
        input_text += f"\n{speech_text}"  # Append speech result to input_text
        st.success("Job description updated with your speech input!")

uploaded_file = st.file_uploader("📤 Upload your resume (PDF only):", type=["pdf"])

# The rest of your code continues here...

# Function to process PDF input
def input_pdf_setup(uploaded_file):
    if uploaded_file:
        images = pdf2image.convert_from_bytes(uploaded_file.read())
        first_page = images[0]

        img_byte_arr = io.BytesIO()
        first_page.save(img_byte_arr, format='JPEG')
        img_byte_arr = img_byte_arr.getvalue()

        pdf_parts = [{"mime_type": "image/jpeg", "data": base64.b64encode(img_byte_arr).decode()}]
        return pdf_parts
    else:
        raise FileNotFoundError("No file uploaded")

# Function to get response from Gemini
def get_gemini_response(input_text, pdf_content, prompt):
    model = genai.GenerativeModel('gemini-1.5-flash')
    response = model.generate_content([input_text, pdf_content[0], prompt])
    return response.text

# Enhanced prompts
input_prompt1 = """
You are an experienced Technical Human Resource Manager. Review the provided resume against the job description.
Provide a professional evaluation, highlighting the strengths and weaknesses of the candidate for the specified role.
"""

input_prompt3 = """
You are a skilled ATS scanner. Evaluate the resume against the job description, and provide:
1. A match percentage.
2. Missing keywords.
3. Final thoughts on the resume's relevance.
"""

# Function to extract email and phone number from resume text
def extract_contact_info(resume_text):
    # Regex pattern for email
    email_pattern = r'[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+'
    email = re.findall(email_pattern, resume_text)

    # Regex pattern for phone number
    phone_pattern = r'\+?\d{10,15}'
    phone = re.findall(phone_pattern, resume_text)

    # Extracting the first email and phone number (if available)
    extracted_email = email[0] if email else "Not Found"
    extracted_phone = phone[0] if phone else "Not Found"
    
    return extracted_email, extracted_phone

# Function to check eligibility based on user input
def check_eligibility(resume_text, min_12_percentage, min_diploma_percentage):
    # Check phone number
    phone_number = re.search(r'\+?\d{10,15}', resume_text)
    phone_valid = phone_number is not None

    # Check email
    email = re.search(r'@+', resume_text)
    email_valid = email is not None

    # Check for at least 3 projects
    projects = len(re.findall(r'project', resume_text, re.IGNORECASE)) >= 3

    # Check for internships
    internships = "internship" in resume_text.lower()

    # Check eligibility based on 12th or diploma percentage criteria
    eligible = False
    if "10th" in resume_text:
        percentage = re.search(r'\d{2,3}%?', resume_text)
        if percentage and int(percentage.group().replace('%', '')) >= min_10_percentage:
            eligible = True
    if "12th" in resume_text:
        percentage = re.search(r'\d{2,3}%?', resume_text)
        if percentage and int(percentage.group().replace('%', '')) >= min_12_percentage:
            eligible = True
    if not eligible and "diploma" in resume_text and projects:
        percentage = re.search(r'\d{2,3}%?', resume_text)
        if percentage and int(percentage.group().replace('%', '')) >= min_diploma_percentage:
            eligible = True

    return {
        "phone_valid": phone_valid,
        "email_valid": email_valid,
        "projects": projects,
        "internships": internships,
        "eligible": eligible,
    }

# User input for eligibility criteria
st.sidebar.header("Set Eligibility Criteria")
min_10_percentage = st.sidebar.number_input("Minimum 10th Percentage (%)", min_value=0, max_value=100, value=60)
min_12_percentage = st.sidebar.number_input("Minimum 12th Percentage (%)", min_value=0, max_value=100, value=60)
min_diploma_percentage = st.sidebar.number_input("Minimum Diploma Percentage (%)", min_value=0, max_value=100, value=60)

# Action buttons
col1, col2 = st.columns(2)
with col1:
    submit1 = st.button("📋 Tell Me About the Resume")
with col2:
    submit3 = st.button("📊 Percentage Match")

# Evaluation Section
response = 'No evaluation performed.'  # Default response
eligibility_results = None

if submit1:
    if uploaded_file:
        pdf_content = input_pdf_setup(uploaded_file)
        response = get_gemini_response(input_text, pdf_content, input_prompt1)
        st.subheader("💬 Evaluation Summary")
        st.success(response)
    else:
        st.warning("Please upload a resume.")

if submit3:
    if uploaded_file:
        pdf_content = input_pdf_setup(uploaded_file)
        response = get_gemini_response(input_text, pdf_content, input_prompt3)
        st.subheader("📊 Match Analysis")
        st.success(response)

        # Visualization: Pie Chart
        data = {"Matched": 70, "Missing": 30}  # Example data
        fig, ax = plt.subplots(figsize=(4, 4))  # Adjusted smaller size
        wedges, texts, autotexts = ax.pie(
            data.values(), 
            labels=data.keys(), 
            autopct='%1.1f%%', 
            startangle=90, 
            colors=["#4CAF50", "#FF5722"], 
            textprops=dict(color="w")
        )
        ax.legend(wedges, data.keys(), title="Legend", loc="center left", bbox_to_anchor=(1, 0, 0.5, 1))
        plt.title('Resume Match Analysis')
        st.pyplot(fig)
    else:
        st.warning("Please upload a resume.")

# Display contact information if available
if uploaded_file:
    resume_text = uploaded_file.read().decode("utf-8")
    email, phone = extract_contact_info(resume_text)
    st.subheader("📧 Contact Information")
    st.write(f"Email: {email}")
    st.write(f"Phone: {phone}")

# Check eligibility
if uploaded_file:
    resume_text = uploaded_file.read().decode("utf-8")
    eligibility = check_eligibility(resume_text, min_12_percentage, min_diploma_percentage)
    st.subheader("🏅 Eligibility Check")
    st.write(f"Phone Valid: {eligibility['phone_valid']}")
    st.write(f"Email Valid: {eligibility['email_valid']}")
    st.write(f"Has 3+ Projects: {eligibility['projects']}")
    st.write(f"Has Internship Experience: {eligibility['internships']}")
    st.write(f"Eligible for the Role: {eligibility['eligible']}")

