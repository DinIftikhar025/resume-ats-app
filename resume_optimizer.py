import openai
import streamlit as st
from IPython.display import Markdown, display, update_display

# Access OpenAI API key from Streamlit Secrets
openai_api_key = st.secrets["openai"]["api_key"]

# Set up the OpenAI client
openai.api_key = openai_api_key
MODEL = 'gpt-4o-mini'
#openai = OpenAI()


def optimize_resume_for_ats(job_description, resume):
    # System prompt: Set the behavior of the assistant
    system_prompt = """
    You are an AI assistant that helps job seekers optimize their resumes for Applicant Tracking Systems (ATS).
    Your task is to analyze the given job description and the provided resume, and return an optimized resume that matches the job description.
    Ensure that the optimized resume:
    1. Uses relevant keywords and skills from the job description.
    2. Is concise and formatted to fit within one page.
    3. Excludes any irrelevant or unrelated content.
    4. Includes an ATS score that reflects how well the resume matches the job description based on keyword and skill relevance.
    5. Return the result in **Markdown** format (headers, bullet points, etc.).
    """
    
    # User prompt: This is the specific task the user wants to perform
    user_prompt = f"""
    Job Description:
    {job_description}
    
    Resume:
    {resume}
    
    Use this information to provide:
    - Optimized Resume: (The optimized resume content) in Markdown.
    - ATS Score: (A percentage that represents how well the resume matches the job description)
    ATS Score should be atleast 90%.

    Do not add stuff from your own side. Do not include addresses.
    keep the phone number, email, linkedin, github, portfolio website links to one line at the top.

    The optimized resume should be in the format of a professional CV fitted to 1 A4 Sheet of MS Word. Use this format:
    Name
    title
    contact, email, profiles etc
    Profession Summary
    Core skills
    Experience
    Education
    Projects/Certifications/Hobbies/languages/references, not necessary you include all these!
    """

    try:
        # Query OpenAI API to get the optimized resume and ATS score
        stream = openai.chat.completions.create(
            model=MODEL,  # You can also use "gpt-3.5-turbo" for cheaper alternatives
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
            max_tokens=1500,  # Adjust this to a larger value if needed
            stream=True
        )
        optimized_text = ""
        #display_handle = display(Markdown(""), display_id=True)
        for chunk in stream:
            optimized_text += chunk.choices[0].delta.content or ''
            optimized_text = optimized_text.replace("```","").replace("markdown", "")
            #update_display(Markdown(optimized_text), display_id=display_handle.display_id)
        # Extract the response (this will contain the optimized resume and ATS score)
        #optimized_text = response.choices[0].message.content.strip()

        # Debugging: Print the raw response to understand its structure
        #print("Raw Response from OpenAI:")
        #print(optimized_text)

        
        # Try to split the output into resume and ATS score
        if "ATS Score:" in optimized_text:
            optimized_resume, ats_score = optimized_text.split("ATS Score:")
            ats_score = int(ats_score.split(":")[-1].split("%")[0].strip())
            return optimized_resume.strip(), ats_score
        else:
            return optimized_text, "ATS score not found"

    except Exception as e:
        return f"An error occurred while processing: {e}"
