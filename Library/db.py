books = [
    {"id": 1, "title": "The Whispering Shadows", "author": "Alice Green", "year": 2021, "slug": "the-whispering-shadows"},
    {"id": 2, "title": "Journey to the Unknown", "author": "John Smith", "year": 2020, "slug": "journey-to-the-unknown"},
    {"id": 3, "title": "The Last Light", "author": "Emily White", "year": 2019, "slug": "the-last-light"},
    {"id": 4, "title": "Echoes of the Past", "author": "Michael Brown", "year": 2022, "slug": "echoes-of-the-past"},
    {"id": 5, "title": "Beneath the Surface", "author": "Sarah Johnson", "year": 2023, "slug": "beneath-the-surface"},
    {"id": 6, "title": "The Forgotten Realm", "author": "David Lee", "year": 2021, "slug": "the-forgotten-realm"},
    {"id": 7, "title": "A Dance with Time", "author": "Laura Wilson", "year": 2020, "slug": "a-dance-with-time"},
    {"id": 8, "title": "The Secret Garden", "author": "James Taylor", "year": 2018, "slug": "the-secret-garden"},
    {"id": 9, "title": "Whispers in the Wind", "author": "Jessica Martin", "year": 2022, "slug": "whispers-in-the-wind"},
    {"id": 10, "title": "The Edge of Tomorrow", "author": "Daniel Harris", "year": 2023, "slug": "the-edge-of-tomorrow"},
    {"id": 11, "title": "Fragments of Reality", "author": "Sophia Clark", "year": 2021, "slug": "fragments-of-reality"},
    {"id": 12, "title": "The Hidden Path", "author": "Matthew Lewis", "year": 2020, "slug": "the-hidden-path"},
    {"id": 13, "title": "Chasing Dreams", "author": "Olivia Hall", "year": 2019, "slug": "chasing-dreams"},
    {"id": 14, "title": "The Silent Echo", "author": "William Young", "year": 2022, "slug": "the-silent-echo"},
    {"id": 15, "title": "A World Apart", "author": "Isabella King", "year": 2023, "slug": "a-world-apart"},
    {"id": 16, "title": "The Color of Hope", "author": "Ethan Wright", "year": 2021, "slug": "the-color-of-hope"},
    {"id": 17, "title": "Beyond the Horizon", "author": "Mia Scott", "year": 2020, "slug": "beyond-the-horizon"},
    {"id": 18, "title": "The Timekeeper's Daughter", "author": "Alexander Green", "year": 2019, "slug": "the-timekeepers-daughter"},
    {"id": 19, "title": "The Last Voyage", "author": "Charlotte Adams", "year": 2022, "slug": "the-last-voyage"},
    {"id": 20, "title": "The Dreamer's Journey", "author": "Henry Baker", "year": 2023, "slug": "the-dreamers-journey"},
    {"id": 21, "title": "The Art of Letting Go", "author": "Grace Nelson", "year": 2021, "slug": "the-art-of-letting-go"},
]

def get_book(slug):
    for book in books:
        if book["slug"] == slug:
            return book
    return None

def get_books():   
    return books

def get_book_by_id(id):
    for book in books:
        if book["id"] == id:
            return book 
    return None
