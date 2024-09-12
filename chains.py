import os
from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.exceptions import OutputParserException
from dotenv import load_dotenv

import streamlit as st

GROQ_API_KEY = st.secrets["default"]["GROQ_API_KEY"]

# using this we can have a file called .env in your root folder where you can keep your API key. 
# load_dotenv()   # This will find the .env file and it will set the things in that file as your environment variable

# print(os.getenv("GROQ_API_KEY"))        # just for testing

class Chain:
    def __init__(self):
        self.llm = ChatGroq(temperature=0, groq_api_key=GROQ_API_KEY, model_name="llama-3.1-70b-versatile")
        # self.llm = ChatGroq(temperature=0, groq_api_key=os.getenv("GROQ_API_KEY"), model_name="llama-3.1-70b-versatile")
        

    # function for extracting the job description and then passing it to a json parser to convert it to json
    def extract_jobs(self, cleaned_text):
        prompt_extract = PromptTemplate.from_template(
            """
            ### SCRAPED TEXT FROM WEBSITE:
            {page_data}
            ### INSTRUCTION:
            The scraped text is from the career's page of a website.
            Your job is to extract the job postings and return them in JSON format containing the following keys: `role`, `experience`, `skills` and `description`.
            Only return the valid JSON.
            ### VALID JSON (NO PREAMBLE):
            """
        )
        chain_extract = prompt_extract | self.llm
        res = chain_extract.invoke(input={"page_data": cleaned_text})
        try:
            json_parser = JsonOutputParser()
            res = json_parser.parse(res.content)
            # Check if the result is a list and extract the first dictionary
            # if isinstance(json_res, list):
            #     json_res = json_res[0]
            
        except OutputParserException:
            raise OutputParserException("Context too big. Unable to parse jobs.")
        return res if isinstance(res, list) else [res]

    
    def summarize_pdf(self, pdf_data):
        prompt_extract = PromptTemplate.from_template(
        """
        ### PDF DATA OBTAINED FROM RESUME:
        {pdf_data}
        ### INSTRUCTION:
        The data is from the resume of a person.
        Your job is to extract all the details of this person and summarize it in 200 words, which includes name, education, experience, projects, skills.
        ### (NO PREAMBLE):    
        """
        )
        chain_extract = prompt_extract | self.llm    # this will form a langchain chain ie you are getting a prompt and passing it to LLM 
        res2 = chain_extract.invoke(input={'pdf_data':pdf_data})
        # print(res.content)
        summary = res2.content
        return summary
        
    def write_mail(self, job_description, summary):
        prompt_email = PromptTemplate.from_template(
        """
        ### JOB DESCRIPTION:
        This is a job description
        
        {job_description}

        ### INSTRUCTION:
        These are the person's details.
        {summary}
        Consider yourself as this person. 
        
        Introduce yourself in an engaging way from above with your name from the above details and your current designation.  
        
        Try to find some things in the job description which are similar with your details. Mention those things which are similar. 
        Do not mention anything which is not present in the details.
        
        Your job is to write a cold email of about 250 words to the hiring manager regarding the job mentioned above describing the capability of you 
        in fulfilling their needs. The cold email must be engaging to read. 
        End the email with Name and Current place where your are working or studying. 
        Do not provide a preamble.
        ### EMAIL (NO PREAMBLE):

        """
        )
        chain_email = prompt_email | self.llm
        res = chain_email.invoke({"job_description": str(job_description), "summary": summary})
        return res.content

# if __name__ == "__main__":
#     print(os.getenv("GROQ_API_KEY"))