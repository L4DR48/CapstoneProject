                                        STATYOURSQUAD
                                Architecture & Responsibilities



Architecture Overview

STATYOURSQUAD uses a layered architecture to separate UI, business logic, AI reasoning, and data storage, ensuring maintainability, scalability, and reliable AI-driven basketball analysis.


High-Level Architecture


Streamlit UI --> Application Logic --> Services/Tools --> AI Layer --> Data Layer


1. Layer Responsibilities

  1.1 UI Layer

  It handles user interaction, page navigation, file uploads, and displays insights and comparisons.

  1.2 Application Logic Layer
  
  This manages session state, validates inputs, routes pages, and coordinates workflows.

  1.3 Services/Tools Layer
 
  It performs boxscore extraction, team and player analytics, player comparison, and database read/write operations.

  1.4 AI Layer

  It extracts multimodal data, applies tactical basketball reasoning, generates insights, and ensures data-grounded analysis.

  1.5 Data Layer

  MongoDB: Stores team boxscores, player statistics, and enables historical analysis.
  SQLite: Handles user authentication and credential storage.



2. Analysis Responsibilities

Team Analysis: 
Aggregates team performance and identifies strengths and weaknesses.

Player Analysis: 
Tracks player contributions and measures consistency.

Player Comparison:
Compares MongoDB players and NBA players, generating contextual insights.


3. Observability

Langfuse:
Tracks prompts, monitors outputs, and aids debugging of AI responses.


4. Security

It manages environment variables, protects API keys, and ensures secure database access.


5. Scalability

This supports modular feature extension, handles dataset growth, and allows future analytics integration.




To sum up,the architecture separates responsibilities clearly, enables reliable AI reasoning, and remains modular and extensible for production-level and Capstone requirements.
