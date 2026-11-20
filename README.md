# Literary Agent — Top 5 Book Recommendations

Multi-agent book recommendation app using OpenAI Agents SDK, Open Library and Google Books.

## Agents
- Literary Recommendation Manager — orchestrates the workflow.
- Reader Intent Analyst — interprets topic, purpose and preferences.
- Genre Specialist — identifies genres, authors and diverse approaches.
- Book Catalog Researcher — searches book catalogs and verifies metadata.
- Top Five Selector — ranks exactly five suitable books.

## Setup (Windows PowerShell)
```powershell
py -m venv .venv
.venv\\Scripts\\Activate.ps1
pip install -r requirements.txt
Copy-Item .env.example .env
```
Add your OpenAI API key to `.env`.

## Run
```powershell
streamlit run app.py
```

CLI:
```powershell
python -m src.literary_agent.cli "Books on behavioral economics for beginners"
```

## Data sources
- Open Library: https://openlibrary.org/developers/api
- Google Books: https://developers.google.com/books/docs/v1/using

Catalog listings do not guarantee local purchase/borrowing availability. Verify edition, ISBN,
regional availability and publication details. Ratings are only included when supplied by a source.
The app does not sell books or reproduce copyrighted text.
