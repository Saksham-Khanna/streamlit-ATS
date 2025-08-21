from dotenv import load_dotenv
load_dotenv()

import base64
import streamlit as st
import os
import io
from PIL import Image 
import pdf2image
import google.generativeai as genai

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

def get_gemini_response(input, pdf_content, prompt):
    model = genai.GenerativeModel('gemini-2.5-pro')
    response = model.generate_content([input, *pdf_content, prompt])
    return response.text

def input_pdf_setup(uploaded_file):
    if uploaded_file is None:
        return None 

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

st.set_page_config(page_title="ATS Resume Expert")
st.header("ATS Tracking System")

input_text = st.text_area("Job Description", key="input")
uploaded_file = st.file_uploader("Upload Resume (PDF)", type=["pdf"])

submit1 = st.button("Tell me about this resume")
submit3 = st.button("Match Percentage")

input_prompt1 = """
You are an experienced HR with Tech Experience in the field of data science, full stack web development, Big Data, DevOps, and Data Analyst. 
Your task is to analyze the resume and provide a detailed analysis of the resume, including strengths, weaknesses, and areas for improvement. 
Please share your insights in a detailed manner on the candidate's suitability for the role from an HR perspective. 
Additionally offer advice for enhancing the resume to better align with the job description provided.
"""

input_prompt3 = """
You are a skilled ATS (Application Tracking System) scanner with a deep understanding of data science, full stack web development, Big Data, DevOps, and Data Analyst. 
Your task is to evaluate the resume against the job description and provide a match percentage. 
The match percentage should reflect how well the resume aligns with the job description, considering relevant skills, experience, and qualifications. 
Please provide a detailed explanation of the factors contributing to the match percentage.
"""

if submit1:
    if uploaded_file:
        pdf_content = input_pdf_setup(uploaded_file) 
        if pdf_content:
            response = get_gemini_response(input_prompt1, pdf_content, input_text)
            st.subheader("The response is:")
            st.write(response)
    else:
        st.warning("⚠️ Please upload a PDF before clicking this button.")

if submit3:
    if uploaded_file:
        pdf_content = input_pdf_setup(uploaded_file) 
        if pdf_content:
            response = get_gemini_response(input_prompt3, pdf_content, input_text)
            st.subheader("The response is:")
            st.write(response)
    else:
        st.warning("⚠️ Please upload a PDF before clicking this button.")
