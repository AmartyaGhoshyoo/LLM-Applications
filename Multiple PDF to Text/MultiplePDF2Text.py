from dotenv import load_dotenv
load_dotenv() 
import streamlit as st 
from PyPDF2 import PdfReader # for reading pdf file
from langchain.text_splitter import RecursiveCharacterTextSplitter # Recursively breaks larger text into small chunk, one after another
import os
from langchain_google_genai import GoogleGenerativeAIEmbeddings,ChatGoogleGenerativeAI
import google.generativeai as genai
from langchain.vectorstores import FAISS # Vector database
from langchain.chains.question_answering import load_qa_chain
from langchain.prompts import PromptTemplate
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
model=ChatGoogleGenerativeAI(model= 'gemini-1.5-flash-8b-exp-0924',temperature=0.3)# temperature the more low we give the less productive it becomes and try to be obvious for the next word generation 

def get_pdf_text(pdf_docs):
    text=''
    for pdf in pdf_docs:
        pdf_reader=PdfReader(pdf) # contains in pages
        for page in pdf_reader.pages:
            text+=page.extract_text() # extracting text from the page and storing it in text variable
    return text
def break_text_into_chunks(text):
    text_splitter=RecursiveCharacterTextSplitter(chunk_size=10000,chunk_overlap=1000) # it's the class instance I have created, which will first created this empty object named text_splitter and implicitly passing the object in the constructor as a first argument and initialise it in specific memory particular for that instance
    chunks=text_splitter.split_text(text) # passing the text for chunking into the methodz
    return chunks
def converting_to_embedding():
    embedding=GoogleGenerativeAIEmbeddings(model='models/embedding-001') # Creating 'embedding' instance of this embedding model(embedding-001) class(GoogleGenerativeAIEmbeddings) which will convert chunks into a high dimensional vectors or embedding so we can store in vector database for later retrieval of most relevant chunks according to query
    return embedding
def storing_to_vectordatabase(text_chunks):
    vectorDB=FAISS.from_texts(texts=text_chunks,embedding=converting_to_embedding()) # converting each text_chunks with embedding and storing in vectorDB, direct memory mean in RAM , lost after if cancel it 
    vectorDB.save_local('FAISS_INDEX') # saving locally as it gets lost if stored in Memory
def get_conversational_chain():
    prompt_templates="""
    Answer the question as detailed as possible from the provided context ,make sure to provide all the details,if the answer is not present in the context just say 'Answer is not present in the context',Don't make up things
    Context:\n{context}?\n
    Question:\n{question}\n
    
    Answer:
    
    """
    
    prompt=PromptTemplate(template=prompt_templates,input_variables=['context','question'])
    chain=load_qa_chain(model,chain_type='stuff',prompt=prompt) # returning configured instance 
    return chain
    # Check below
def user_input(Query):
    storedDB=FAISS.load_local('FAISS_INDEX',embeddings=converting_to_embedding())
    # """
    # The error message you're seeing is a security warning related to the deserialization of pickle files.
    # Pickle files can potentially be modified to execute arbitrary code, which is why the library requires you to explicitly allow dangerous deserialization if you trust the source of the data.

    # To resolve this, you need to set the allow_dangerous_deserialization parameter to True when calling FAISS.load_local.
    # However, you should only do this if you are certain that the pickle file is from a trusted source.
    
    # in LeetCode py file in details pickle file 
    
    
    
    # """
    
    docs=storedDB.similarity_search(Query)
    chain=get_conversational_chain()
    response=chain({'input_documents':docs,'question':Query}, # chain as if it were a function because of the __call__ method
        return_only_outputs=True
    )
    
    print(response)
    st.write('Reply: ',response['output_text'])
def main():
    # st.set_page_config("MultiplePDF 🤖")
    st.title('Upload PDF files converts to Text')
    query=st.text_input('Write Query🗣️')
    if query:
        user_input(query)
    with st.sidebar: 
        st.title('Menu: ')
        pdf_docs=st.file_uploader('Upload PDF Files Here and Click on the submit button',type=['pdf'], accept_multiple_files=True)
        if st.button('Submit & Process'):
            with st.spinner("Processing..."):
                raw_text= get_pdf_text(pdf_docs)
                chunks=break_text_into_chunks(raw_text)
                storing_to_vectordatabase(chunks)
                st.success('Great Done') 
if __name__=='__main__': # name is a built in variable which automatically sets to main if we run the script directly
    main()
                
                
# """
# class Car:
#     def __init__(self, make, model, year):
#         self.make = make
#         self.model = model
#         self.year = year

#     def get_info(self):
#         return f"{self.year} {self.make} {self.model}"

# def create_car(make, model, year):
#     # This method configures and returns an instance of the Car class
#     car_instance = Car(make, model, year)
#     return car_instance
    

# This method takes make, model, and year as parameters, creates an instance of the Car class with these parameters, and returns the configured instance

# If you use the my_car object as a function, it means that the class Car (the class of which my_car is an instance) has a __call__ method defined. 
# The __call__ method allows an instance of the class to be called as if it were a function.

# class Car:
#     def __init__(self, make, model, year):
#         self.make = make
#         self.model = model
#         self.year = year

#     def get_info(self):
#         return f"{self.year} {self.make} {self.model}"

#     def __call__(self):
#         return self.get_info()

# def create_car(make, model, year):
#     car_instance = Car(make, model, year)
#     return car_instance

# # Example usage
# my_car = create_car("Toyota", "Corolla", 2020)

# # Using the my_car object as a function
# print(my_car())  # Output: 2020 Toyota Corolla
# By defining the __call__ method in the Car class, you can use instances of the class as if they were functions
# """
