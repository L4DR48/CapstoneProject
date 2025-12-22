Clear Documentaion on how to run the Application Locally  

To get the environment and libraries: 

Open Terminal 

Write: 

1st : py -m venv venv 

2nd :venv\Scripts\activate 

3rd : pip install . 

 

Create a .env file that includes Google Api Key , Langfuse Secret Key, Langfuse Public key, Langfuse host/base url, Mongo URI, Mongo database name and Mongo Collection name. 

 

Go to main_app.py , go to terminal and write: streamlit run .\main_app.py 

When you want to deactivate the streamlit page click these buttons in the terminal: ctrl+c 

If you wish to deactivate the environment write deactivate in the terminal. 
