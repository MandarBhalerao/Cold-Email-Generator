import streamlit as st
from langchain_community.document_loaders import WebBaseLoader

from chains import Chain
# from portfolio import Portfolio
from utils import clean_text, extract_text_from_pdf


def create_streamlit_app(llm, clean_text):
    st.title("📧 Welcome to Cold E-Mail Generator")
    
    # PDF upload section
    uploaded_file = st.file_uploader("Upload your resume as PDF", type=["pdf"])
    pdf_text = extract_text_from_pdf(uploaded_file)
    # if pdf_text:
    #     st.text_area("Extracted Text", value=pdf_text, height=300)
    
    
    url_input = st.text_input("Enter the URL of Job Posting:", value="https://careers.myntra.com/job-detail/?id=7431200002")
    submit_button = st.button("Generate E-mail")

    if submit_button:
        try:
            loader = WebBaseLoader([url_input])
            data = clean_text(loader.load().pop().page_content)   # cleans any unnecessary garbage text
            jobs = llm.extract_jobs(data)                         # create json objects for the job
            for job in jobs:                                      # this is for if one web page has multiple jobs
                # skills = job.get('skills', [])
                summarized_text = llm.summarize_pdf(pdf_text)
                # st.text_area(summarized_text)
                email = llm.write_mail(job, summarized_text)             # write the email
                # st.code(email, language='markdown')
                st.text_area("Email is as follows", value=email, height=500)

                # st.code('hello')
        except Exception as e:
            st.error(f"An Error Occurred: {e}")


if __name__ == "__main__":
    chain = Chain()
    # portfolio = Portfolio()
    st.set_page_config(layout="wide", page_title="Cold Email Generator", page_icon="📧")
    create_streamlit_app(chain, clean_text)


