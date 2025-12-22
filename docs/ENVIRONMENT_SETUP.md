Environment Setup Guide
This document explains how to configure the environment required to run STATYOURSQUAD locally or in deployment.

1. Python Environment:
Required Version -Python 3.10 or higher

2. Dependency Installation
This project uses uv for dependency management.
   -Install project dependencies:
         [uv sync] will install all required packages listed in pyproject.toml

3. Environment Variables
The application relies on several external services that require API keys.

    Step 1: Create .env file
    Step 2: Fill in the required values

              # Google Gemini API
              GOOGLE_API_KEY=your_gemini_api_key_here
              
              # MongoDB
              MONGO_URI=your_mongodb_connection_string
              MONGO_DB=statyoursquad
              MONGO_COLLECTION=boxscores
              
              # Langfuse (LLM Observability)
              LANGFUSE_PUBLIC_KEY=your_langfuse_public_key
              LANGFUSE_SECRET_KEY=your_langfuse_secret_key
              LANGFUSE_HOST=https://cloud.langfuse.com

4. MongoDB Setup
      Option 1: MongoDB Atlas (Recommended)
                  Create a MongoDB Atlas cluster 
                  Create a database (e.g. statyoursquad)
                  Create a collection (e.g. boxscores)
                  Copy the connection string into MONGO_URI
        
      Option 2: Local MongoDB
           - Make sure mongodb is running before you start the app.


5. Google Gemini API Setup
        1. Visit: https://aistudio.google.com/
        2. Create an API key
        3. Enable Gemini models
        4. Paste the key into GOOGLE_API_KEY

     Used models:
              gemini-2.5-flash-lite

6. Langfuse Setup (Optional but Recommended)
         - Create an account at https://langfuse.com/
         - Create a new project
         - Copy public & secret keys into .env

7. Running the Application
        Once setup is complete:
             [uv run streamlit run app.py]
   
8. Security Notes
        1. Never commit .env
        2. Rotate API keys if exposed
        3. Use environment variables in deployment platforms

9. Deployment Notes
          - When deploying (Streamlit Cloud, Render, etc.)   
          - Add environment variables directly in the platform dashboard
          - Do not upload .env files
