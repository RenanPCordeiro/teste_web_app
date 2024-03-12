import openai
import streamlit as st
import pandasai
import pandas as pd
from dotenv import load_dotenv
from pandasai import SmartDataframe
from pandasai.llm.openai import OpenAI
import matplotlib.pyplot as plt
import openpyxl 
import os

load_dotenv()

#openai.api_key = os.getenv('OPENAI_API_KEY')

openai_api_key = st.sidebar.text_input("OpenAI API Key",
                                        type="password",
                                        placeholder="Paste your OpenAI API key here (sk-...)")

#os.environ["OPENAI_API_KEY"]

mylist = ["grafico", "gráfico", "GRAFICO", "GRÁFICO", "barras", "chart", "graph", "bar chart", "line chart", "plot", "PLOT", "plote", "PLOTE"]

def clear_submit():
    """
    Clear the Submit Button State
    Returns:

    """
    st.session_state["submit"] = False




llm = OpenAI(api_token=openai_api_key)


lista_arquivo = ['Excel', 'CSV']

st.title("ANÁLISE DE DADOS COM I.A.")

with st.sidebar:


    st.title("Submeta seus dados")
     
    arquivo = st.radio(
            label= 'Escolha um tipo de arquivo:',
            options= lista_arquivo,
            horizontal=True
            )

if arquivo=='Excel':
    with st.sidebar:
         uploaded_excel_file = st.file_uploader("Submeta seu arquivo Excel", 
                                             type=['xlsx'],  
                                              on_change=clear_submit,)
         
    if uploaded_excel_file is not None:

        wb = openpyxl.load_workbook(uploaded_excel_file)
        sheet_selector = st.sidebar.selectbox("Selecione uma planilha do Excel escolhido:",wb.sheetnames)
        df = pd.read_excel(uploaded_excel_file, sheet_selector)
        with st.expander("Prévia das primeiras 20 linhas dos dados"):
            st.write(df.head(20))


      
elif arquivo=='CSV':

    with st.sidebar:
        uploaded_csv_file = st.file_uploader("Submeta seu arquivo csv", 
                                             type=['csv'],  
                                              on_change=clear_submit,)
    if uploaded_csv_file is not None:
        df = pd.read_csv(uploaded_csv_file)
        with st.expander("Prévia das primeiras 20 linhas dos dados"):
             st.write(df.head(20))
             



if "messages" not in st.session_state or st.sidebar.button("Limpar histórico de conversação"):
    st.session_state["messages"] = [{"role": "assistant", "content": "Olá, submeta seu arquivo ao lado e faça suas perguntas!"}]

for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])


if prompt := st.chat_input(placeholder="Pergunte aqui!"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)

    
    sdf = SmartDataframe(df, config={"llm":llm})

    with st.chat_message("assistant"):
        
        if not any(x in prompt for x in mylist):

            response=sdf.chat(prompt)
            st.session_state.messages.append({"role": "assistant", "content": response})
            st.success(response)
            #st.write(response)
            #st.set_option('deprecation.showPyplotGlobalUse', False)
            #st.pyplot()
        else:
            response=sdf.chat(prompt)
            st.session_state.messages.append({"role": "assistant", "content": response})
            st.success(response)
            #st.write(response)
            st.set_option('deprecation.showPyplotGlobalUse', False)
            st.pyplot()

        
                    
                    



