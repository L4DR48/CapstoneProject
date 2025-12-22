# StatYourSquad

Description:

StatYourSquad is an AI-powered tool that analyzes basketball-related data to help coaches make better decisions and players improve their performance. Currently, coaches and players heavily rely on intuition rather than data-driven insights, resulting in missed opportunities for performance improvement and strategic preparation. Our solution provides accessible and meaningful analytics that help teams better understand their strengths, weaknesses and areas for growth.
Our target users are athletes, coaches, youth teams, and even general fans looking to access advanced performance metrics, compare players, analyze past games, or receive guidance for future match strategies. 

## Features:

Interactive chatbot
- Answers basketball-related questions in a conversational, natural-language format.

Boxscore extractor and game analysis
- Extracts and processes information from image-based documents (.png, .jpg, .pdf) and stores the data in MongoDB (optional) for future queries. Provides game insights focused on the users’ wants (offense, defense,...) and suggests practice drills to improve weaknesses.

Team and player analysis and comparison
- Analyzes uploaded boxscores to generate data-driven insights and actionable advice for both coaches and players. Furthermore, it can compare two players against each other.

Practice Planner
- From the users selected specifics, such as team level, practice venue and available material, SYS can generate a practice plan on the go.

## Tech Stack:

Backend:
- Python
	- Selected due to the developers familiarity with Python
- Google Gemini API
	- Used to enable natural-language understanding, conversational responses, and basketball-specific analysis from both text and documents.

Frontend:
- Streamlit 
- Chosen for its simplicity and rapid development of interactive data-driven user interfaces.



Database:
- MongoDB
	- Selected for its flexible schema, making it suitable for storing extracted document data, chat history, and analysis results.


AI/ML:
- Langfuse
-Used for observability and error tracing



## Architecture:

[docs\architecure_diagram.png]



## Installation:
Python 3.10+


MongoDB Atlas account


Google Gemini API key


Langfuse account



## Usage:

Authentication

- Create an account or login

Boxscore Analysis

- Upload a boxscore image or PDF
- Enter team and opponent abbreviations
- Extract and review structured stats
- Save games to MongoDB
- Generate AI insights or practice drills

Insights 

-Enter any team name
-Select:
Entire Team
Individual Players
- Run player vs player comparisons

## Deployment 
Streamlit Community Cloud


## Structure
project-root/
├── app.py                    # Main Streamlit application
├── tools/
│   ├── boxscore2_0.py        # Boxscore extraction logic
│   ├── boxscore_analysis.py  # AI analysis & practice planning
│   └── mongotools.py         # MongoDB operations
├── utils/
│   └── mongo_utils.py        # MongoDB initialization & helpers
├── images/                  # UI assets
├── .env.example             # Environment template
├── users.db                 # SQLite user database
├── pyproject.toml           # Dependencies
└── README.md 


Team Information:

- João Patrício, 20231645, 20231645@novaims.unl.pt  
- Rodrigo Silva, 20231602, 20231602 @novaims.unl.pt 
- Srijan Dahal, 20230012, 20230012@novaims.unl.pt 
- Vasco Rodrigues, 20231676, 20231676 @novaims.unl.pt