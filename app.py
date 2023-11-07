import os
import streamlit as st
import PyPDF2
import openai


st.set_page_config(initial_sidebar_state="expanded")
st.title("PaperPilot")
st.subheader('''Turning Papers into Reviews, Seamlessly.''')
st.sidebar.header("Podcas Details:")
openai_api=st.sidebar.text_input("Your Open AI API:", type="password")
st.sidebar.write("")
st.sidebar.markdown("Drag and drop a Research Paper.")
pdf_file = st.sidebar.file_uploader("Upload a PDF file", type=["pdf"])

st.write('''literature review:''')

os.environ["OPENAI_API_KEY"]=openai_api

def get_data():
    reader = PyPDF2.PdfReader(pdf_file)
    n = [0, 1, -2, -1]
    text = ""
    for i in n:
        page = reader.pages[i]
        text = text + "\n" + page.extract_text()
    text = text.lower()
    ab_index = text.index("abstract")
    con_index = text.index("conclusions")
    data = text[ab_index:ab_index + 1200] + "\n" + text[con_index:con_index + 1000]
    prompt = "Please generate a literature review based on the abstract and conclusion of the research paper. The literature review should encapsulate the primary findings and contributions of the study, providing a comprehensive analysis and discussion of the results. It should follow a professional research-style format, with a clear structure and a non-plagiarized approach. Please make sure to use language appropriate for a scholarly audience.As one paragraph with no subheadings. Emphasis more on experiment conducted and result.should be between 200-250 words."
    chatOutput = openai.ChatCompletion.create(model="gpt-3.5-turbo",
                                              messages=[{"role": "system",
                                                         "content": "You are a experienced research scholar assistant."},
                                                        {"role": "user", "content": (prompt + data)}
                                                        ],
                                              temperature=0.1
                                              )
    response = chatOutput.choices[0].message.content
    st.write(response)


if st.sidebar.button("Generate"):
    if pdf_file is not None and openai_api is not None:
        get_data()
