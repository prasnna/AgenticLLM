

import streamlit as st
import dotenv
#from langchain.llms import OpenAI
from langchain_openai import OpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain, SequentialChain
from langchain_community.llms import OpenAI,Bedrock

from langchain_core.outputs.generation import Generation
import os
from dotenv import load_dotenv


load_dotenv()

# Set OpenAI API key as an environment variable
#os.environ["OPENAI_API_KEY"] = os.environ.get('OPENAI_API_KEY_v0')

llm = Bedrock(
    credentials_profile_name="saml", model_id="anthropic.claude-v2",
    model_kwargs={"temperature": 0}
)




code_prompt = PromptTemplate(
    input_variables=["task", "language"],
    template="Write a very short {language} function that will {task}"
)

test_prompt = PromptTemplate(
    input_variables=["language", "task", "code"],
    template="Write a test for the following {language} function, and check if it will {task} :\n{code}"
)

explain_prompt = PromptTemplate(
    input_variables=["language", "task", "code"],
    template="Explain very briefly how the following {language} function will {task} :\n{code}"
)

code_chain = LLMChain(llm=llm, prompt=code_prompt, output_key="code")
test_chain = LLMChain(llm=llm, prompt=test_prompt, output_key="test")
explain_chain = LLMChain(llm=llm, prompt=explain_prompt, output_key="explanation")

chain = SequentialChain(
    input_variables=["task", "language"],
    output_variables=["code", "test", "explanation"],
    chains=[code_chain, test_chain, explain_chain])
st.title('Code Generator')

task = st.text_input('Task', 'print hello world')
language = st.selectbox('Language', ['Python', 'Javascript', 'Java', 'C', 'C++'])

if st.button('Generate Code'):
    result = chain({"task": task, "language": language})
    st.subheader('Generated Code')
    st.code(result['code'], language=language.lower())

    st.subheader('Generated Test')
    st.code(result['test'], language=language.lower())

    st.subheader('Explanation of Code')
    st.markdown(result['explanation'])