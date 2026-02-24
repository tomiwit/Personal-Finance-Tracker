# Personal-Finance-Tracker
A personal finance managment system that automates expense tracking - from bank CSV exports and receipt photos to an interactive Power BI dashboard

#Features
- CSV Import: Automatically loads transaction history exported from your bank account
- AI Categorization: Connects to Google Gemini API to classify each transaction into a spending category (food, transport, entertainment, etc.)
- Receipt OCR: Extracts date, amount, and merchant name from reccipt photos using Gemini's vision capabilites
- Data Storage: All transactions are restored in a local SQLite database
- Interactive Dashboard - Power BI report visualizing spending patterns, category breakdowns and monthly trends

  #Tech stack

| Area | Tools |
|---|---|
| Language | Python 3.x |
| AI / OCR | Google Gemini API |
| Database | SQLite |
| Visualization | Power BI |
| Environment | Anaconda / Spyder |
| Version Control | Git / GitHub |
---
