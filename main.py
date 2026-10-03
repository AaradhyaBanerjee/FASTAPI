
from fastapi import FastAPI, Body, HTTPException

app = FastAPI()

books = [
    {"title": "Title one", "author": "author one", "category": "Programming", "description": "description one"},
    {"title": "Title two", "author": "author two", "category": "Science", "description": "description two"},
    {"title": "Title three", "author": "author three", "category": "Programming", "description": "description three"},
    {"title": "Title four", "author": "author four", "category": "Fiction", "description": "description four"},
    {"title": "Title five", "author": "author five", "category": "Science", "description": "description five"},
]

@app.get("/")
async def index():
    return {"web": "Welcome to FASTAPI tutorials"}

# Searching by category, author, or both
# Keep this route before /books/{book_title}
@app.get("/books/search")
async def search_books(
    category: str | None = None,
    author: str | None = None
):
    results = books

    if category:
        results = [
            book for book in results
            if category.casefold() in book["category"].casefold()
        ]

    if author:
        results = [
            book for book in results
            if author.casefold() in book["author"].casefold()
        ]

    return {
        "total_results": len(results),
        "books": results
    }

# Reading by title
@app.get("/books/{book_title}")
async def read_book_by_title(book_title: str):
    for book in books:
        if book["title"].casefold() == book_title.casefold():
            return book

    raise HTTPException(status_code=404, detail="Book not found")

# Reading by author
@app.get("/books/author/{book_author}")
async def read_book_by_author(book_author: str):
    results = [
        book for book in books
        if book["author"].casefold() == book_author.casefold()
    ]

    if not results:
        raise HTTPException(status_code=404, detail="Book not found")

    return results

# Creating a book
@app.post("/books/create")
async def create_book(new_book: dict = Body()):
    required = {"title", "author", "category", "description"}

    if not required.issubset(new_book):
        raise HTTPException(
            status_code=400,
            detail="All fields are required"
        )

    books.append(new_book)
    return {"message": "Book created successfully", "book": new_book}

# Deleting a book
@app.delete("/books/delete/{book_title}")
async def delete_book(book_title: str):
    for book in books:
        if book["title"].casefold() == book_title.casefold():
            books.remove(book)
            return {"message": "Book deleted successfully"}

    raise HTTPException(status_code=404, detail="Book not found")

# Updating a book by its current title
@app.put("/books/update/{book_title}")
async def update_book(book_title: str, updated_book: dict = Body()):
    for i, book in enumerate(books):
        if book["title"].casefold() == book_title.casefold():
            required = {"title", "author", "category", "description"}

            if not required.issubset(updated_book):
                raise HTTPException(
                    status_code=400,
                    detail="All fields are required"
                )

            books[i] = updated_book
            return {
                "message": "Book updated successfully",
                "book": books[i]
            }

    raise HTTPException(status_code=404, detail="Book not found")