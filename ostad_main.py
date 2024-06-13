from sqlalchemy import select

from ostad_data_model import *
from sqlalchemy.orm import Session

with Session(engine) as session:
    # spongebob = session.get(User, 1)
    spongebob = User(name="spongebob")
    print(spongebob.name)

    print("adding many-to-many relationship data...")
    author1 = Author(email_address="x1@x.com")
    author2 = Author(email_address="x2@x.com")
    book1 = Book(name="book1")
    book2 = Book(name="book2")
    book3 = Book(name="book3")
    author1.publishes.append(Publish(extra_data="some extra data", book=book1))
    author1.publishes.append(Publish(extra_data="some extra data", book=book2))
    author1.publishes.append(Publish(extra_data="some extra data", book=book3))
    author2.publishes.append(Publish(extra_data="some extra data", book=book1))
    author2.publishes.append(Publish(extra_data="some extra data", book=book2))
    author2.publishes.append(Publish(extra_data="some extra data", book=book3))
    print("done adding many-to-many relationship data...")
    session.add_all([author1, author2, book1, book2, book3])
    session.commit()

    for author in session.scalars(select(Author)):
        print(f"--------------------------------------------:")
        print(f"listing all publishes of {author!r}:")
        for publish in author.publishes:
            print(f"\t{publish.extra_data}")
            print(f"\t{publish.book}")

