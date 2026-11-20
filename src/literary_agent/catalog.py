import httpx
from agents import function_tool

@function_tool
async def search_open_library(query: str, limit: int = 15) -> str:
    """Search Open Library for book title, author, subject and edition metadata."""
    params = {"q": query, "limit": max(1, min(limit, 30)),
              "fields": "key,title,author_name,first_publish_year,edition_count,subject,isbn,publisher,cover_i"}
    async with httpx.AsyncClient(timeout=25) as client:
        r = await client.get("https://openlibrary.org/search.json", params=params)
        r.raise_for_status()
    out = []
    for x in r.json().get("docs", []):
        out.append({"title": x.get("title"), "authors": x.get("author_name", [])[:4],
          "year": x.get("first_publish_year"), "editions": x.get("edition_count"),
          "subjects": x.get("subject", [])[:8], "isbn": x.get("isbn", [])[:3],
          "publisher": x.get("publisher", [])[:3],
          "url": "https://openlibrary.org" + x["key"] if x.get("key") else None})
    return str(out) if out else "No matching Open Library records."

@function_tool
async def search_google_books(query: str, limit: int = 12) -> str:
    """Search Google Books for descriptions, authors, categories and preview links."""
    async with httpx.AsyncClient(timeout=25) as client:
        r = await client.get("https://www.googleapis.com/books/v1/volumes",
            params={"q": query, "maxResults": max(1, min(limit, 20)), "printType": "books"})
        r.raise_for_status()
    out = []
    for x in r.json().get("items", []):
        v = x.get("volumeInfo", {})
        out.append({"title": v.get("title"), "authors": v.get("authors", []),
          "published": v.get("publishedDate"), "description": (v.get("description") or "")[:1200],
          "categories": v.get("categories", []), "rating": v.get("averageRating"),
          "ratings_count": v.get("ratingsCount"), "pages": v.get("pageCount"),
          "language": v.get("language"), "isbn": v.get("industryIdentifiers", []),
          "preview": v.get("previewLink"), "info": v.get("infoLink")})
    return str(out) if out else "No matching Google Books records."
