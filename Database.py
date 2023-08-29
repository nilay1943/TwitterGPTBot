import sqlite3

DB_NAME = 'articles.db'


def setup_db():
    cursor = get_cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS seen_articles (
            id INTEGER PRIMARY KEY,
            url TEXT UNIQUE
        )
        """)

    cursor.connection.commit()
    cursor.connection.close()


def has_seen_article(url):
    cursor = get_cursor()
    cursor.execute("SELECT 1 FROM seen_articles WHERE url=?", (url,))

    exists = cursor.fetchone()

    cursor.connection.close()
    return exists is not None


def mark_article_as_seen(url):
    cursor = get_cursor()
    cursor.execute("INSERT INTO seen_articles (url) VALUES (?)", (url,))

    cursor.connection.commit()
    cursor.connection.close()


def get_cursor():
    return sqlite3.connect(DB_NAME).cursor()

def clear_database():
    cursor = get_cursor()
    cursor.execute("DELETE FROM seen_articles")
    cursor.connection.commit()
    cursor.connection.close()

def see_DB():
    cursor = get_cursor()

    cursor.execute('SELECT url FROM seen_articles')
    articles = cursor.fetchall()

    for article in articles:
        print(article[0])

    cursor.connection.close()

if __name__ == "__main__":
    clear_database()



