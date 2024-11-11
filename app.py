import streamlit as st
from resume_optimizer import optimize_resume_for_ats
from file_handler import read_job_description, read_docx
import time
import base64
import io

class ResumeATSApp:
    def __init__(self):
        # Initialize variables
        self.job_description = ""
        self.uploaded_file_content = None
        self.uploaded_file_name = None
        self.optimized_resume = ""
        self.ats_score = ""

    def setup_layout(self):
        # Title for the page
        st.title("Job Application Assistant")
        st.markdown("""
            Use this app to optimize your resume for ATS compatibility. 
            Upload your resume and paste the job description to get an ATS-optimized resume.
        """)

        # Apply custom CSS for 100% height text area in the "Optimized Resume" section
        st.markdown(
            """
            <style>
                /* Set the height of the optimized resume text area to 100% of the viewport height */
                
                .resume-heading {
                    font-size: 24px;
                    font-weight: bold;
                    color: #28a745;
                    margin-bottom: 10px;
                }
                .resume-section {
                    margin-top: 15px;
                    margin-bottom: 20px;
                }
                .resume-text {
                    font-size: 16px;
                    line-height: 1.6;
                    font-family: 'Arial', sans-serif;
                }
                .ats-score {
                    font-size: 18px;
                    font-weight: bold;
                    color: green;
                    margin-top: 20px;
                }
            </style>
            """, 
            unsafe_allow_html=True
        )

        # Job Description Section
        self.job_description = st.text_area("Paste the Job Description here...", height=150)
        if st.button("Submit Job Description"):
            if self.job_description:
                st.success("Job description submitted successfully!")
                # Save the job description to a file
                with open("uploads/job_description.txt", "w", encoding="utf-8") as f:
                    f.write(self.job_description)
            else:
                st.error("Please provide a valid job description.")

        # File Upload Section
        uploaded_file = st.file_uploader("Upload Your Resume", type=["pdf", "docx", "txt"])
        if uploaded_file is not None:
            self.uploaded_file_name = uploaded_file.name
            self.uploaded_file_content = uploaded_file.read()
            st.success(f"File '{self.uploaded_file_name}' uploaded successfully!")

        # ATS Optimization Button
        if st.button("Generate ATS Optimized Resume"):
            if self.job_description and self.uploaded_file_content:
                with st.spinner("Optimizing resume..."):
                    # Simulate processing time
                    time.sleep(2)
                    # Process job description and resume
                    jd = read_job_description()  # Reads the job description from a file or variable
                    if self.uploaded_file_name.endswith(".docx"):
                        text = read_docx(uploaded_file)  # Reads the docx file
                    else:
                        text = uploaded_file.getvalue().decode("utf-8")  # For text files or other formats

                    optimized_resume, ats_score = optimize_resume_for_ats(jd, text)
                    self.optimized_resume = optimized_resume
                    self.ats_score = ats_score

                    # Display the ATS score in green and the optimized resume
                    st.markdown(f"<div class='ats-score'>ATS Score: {ats_score}%</div>", unsafe_allow_html=True)
                    st.markdown(self.optimized_resume, unsafe_allow_html=True)
            else:
                st.error("Please provide both Job Description and Resume to generate the optimized resume.")

if __name__ == "__main__":
    app = ResumeATSApp()
    app.setup_layout()
