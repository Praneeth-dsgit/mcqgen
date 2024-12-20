import os
import json
import pandas as pd
import traceback
from dotenv import load_dotenv
from src.mcqgenerator.utils import read_file,get_table_data
import streamlit as st
from PyPDF2 import PdfReader, PdfWriter
from langchain.callbacks import get_openai_callback
from langchain_community.callbacks.manager import get_openai_callback
from src.mcqgenerator.MCQGenerator import generate_evaluate_chain
from src.mcqgenerator.logger import logging 


with open(r'C:\Windows\System32\mcqgen\Response.json','r') as file:
    RESPONSE_JSON = json.load(file)
st.title("MCQ Generator with Langchian & HF")

with st.form("user_inputs"):
    uploaded_file = st.file_uploader("Upload a pdf or txt file")
    
    mcq_count = st.number_input("No of MCQs", min_value=3, max_value = 50)

    subject = st.text_input("Specify a subject on which you need MCQs",max_chars=20)

    tone = st.text_input("Complexity of Questions",max_chars=20,placeholder="Simple")

    button = st.form_submit_button("Generate MCQs")
    
    
    if button and uploaded_file is not None and mcq_count and subject and tone:
        with st.spinner("Loading..."):
            try:
                text = read_file(uploaded_file)
                
                with get_openai_callback() as cb:
                    response = generate_evaluate_chain.run({"text": text,
                                        "number": mcq_count,
                                        "subject": subject,
                                        "tone": tone,
                                        "response_json" : json.dumps(RESPONSE_JSON)})
                    
            except Exception as e:
                traceback.print_exception(type(e),e,e.__traceback__)
                st.error("Error")
                
                
            else:
                print(f"Total Tokens: {cb.total_tokens}")
                print(f"Prompt Tokens: {cb.prompt_tokens}")
                print(f"Completion Tokens: {cb.completion_tokens}")
                print(f"Total Cost:{cb.total_cost}")
                if isinstance(response, dict):
                #Extract the quiz data from the response quiz response.get("quiz", None)
                    quiz = response.get("quiz",None)
                    if quiz is not None:
                        table_data=get_table_data(quiz)
                        if table_data is not None:
                            df=pd.DataFrame(table_data)
                            df.index=df.index+1
                            st.table(df)
                            #Display the review in a text box as well
                            st.text_area(label="Review", value=response ["review"])

                        else:
                            st.error("Error in the table data")
                            
                else:
                    st.write(response)
