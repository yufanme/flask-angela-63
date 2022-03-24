from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///books_collection.db'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)


class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(250), unique=True, nullable=False)
    author = db.Column(db.String(250), nullable=False)
    rating = db.Column(db.FLOAT, nullable=False)

    def __repr__(self):
        return '<User %r>' % self.title


# just create database after the Book table.
db.create_all()
print(1)


@app.route('/')
def home():
    # my code
    # all_books = []
    # books_in_db = db.session.query(Book).all()
    # for book in books_in_db:
    #     title = book.title
    #     author = book.author
    #     rating = book.rating
    #     new_book = {
    #         "title": title,
    #         "author": author,
    #         "rating": rating
    #     }
    #     all_books.append(new_book)

    # angela's code 👇
    all_books = db.session.query(Book).all()
    # angela's code 👆

    # delete book, my code. 👇
    # book_id = request.args.get("book_id")
    # if book_id:
    #     print(book_id)
    #     book_to_delete = Book.query.get(book_id)
    #     print(book_to_delete)
    #     db.session.delete(book_to_delete)
    #     db.session.commit()
    #     print(f"{book_to_delete} deleted")
    #     return redirect(url_for('home'))
    # delete book, my code. 👆

    return render_template("index.html", all_books=all_books)


@app.route("/add", methods=["GET", "POST"])
def add():
    if request.method == "POST":
        title = request.form["title"]
        author = request.form["author"]
        rating = request.form["rating"]
        new_book = Book(title=title, author=author, rating=rating)
        db.session.add(new_book)
        db.session.commit()
        print(db.session.query(Book).all())
        return redirect(url_for("home"))
    return render_template("add.html")

# parameter in url
# @app.route("/edit/<book_id>", methods=["GET", "POST"])
# def edit(book_id):
#     if request.method == "POST":
#         new_rating = request.form["new_rating"]
#         book = Book.query.get(book_id)
#         book.rating = new_rating
#         db.session.commit()
#         return redirect(url_for('home'))
#     book = Book.query.get(book_id)
#     return render_template("edit.html", book=book)


# parameter in URL query
@app.route("/edit", methods=["GET", "POST"])
def edit():
    if request.method == "POST":
        # my way
        # book_id = request.args.get("book_id")
        # angela's way  👇
        book_id = request.form["id"]
        # angela's way  👆

        new_rating = request.form["new_rating"]
        book = Book.query.get(book_id)
        book.rating = new_rating
        db.session.commit()
        return redirect(url_for('home'))
    book_id = request.args.get("book_id")
    book = Book.query.get(book_id)
    return render_template("edit.html", book=book)


@app.route("/delete")
def delete():
    book_id = request.args.get("book_id")
    book_to_delete = Book.query.get(book_id)
    db.session.delete(book_to_delete)
    db.session.commit()
    print(f"{book_to_delete} deleted")
    return redirect(url_for('home'))


if __name__ == "__main__":
    print(2)
    app.run(debug=True)

