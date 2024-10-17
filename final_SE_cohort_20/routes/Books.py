from flask import Blueprint, render_template, request, redirect, url_for, flash
from form.forms import BookForm
from models import db, Books
from sqlalchemy.exc import IntegrityError
from form.forms import UpdateBookForm

# Blueprint registration
book_bp = Blueprint('book', __name__)


@book_bp.route('/add_book', methods=['GET', 'POST'])
def add_book():
    form = BookForm()
    
    if form.validate_on_submit():
        new_book = Books(
            book_id=form.book_id.data,
            title=form.title.data,
            Rating=form.Rating.data,
            BookImages=form.BookImages.data,
            author=form.author.data,
            publication_year=form.publication_year.data,
            Description=form.Description.data,
            page=form.page.data,
            user_id=form.user_id.data  # Optional
        )
        
        try:
            # Try adding the book to the database
            db.session.add(new_book)
            db.session.commit()
            flash('Book added successfully!', 'success')
            return redirect(url_for('book.add_book'))
        
        except IntegrityError:
            # Handle any integrity errors such as duplicate primary key
            db.session.rollback()  # Rollback the session to avoid partial commits
            flash('Error: Book ID already exists. Please choose a different ID.', 'danger')
        
        except Exception as e:
            # Handle any other exception that might occur
            db.session.rollback()  # Rollback the session
            flash(f'An unexpected error occurred: {str(e)}', 'danger')
    
    return render_template('add_book.html', form=form)


# # CRUD for Books
# @book_bp.route('/add_book', methods=['GET', 'POST'])
# def add_book():
#     form = BookForm()
#     if form.validate_on_submit():
#         new_book = Books(
#             book_id=form.book_id.data,
#             title=form.title.data,
#             Rating=form.Rating.data,
#             BookImages=form.BookImages.data,
#             author=form.author.data,
#             publication_year=form.publication_year.data,
#             Description = form.Description.data,
#             page=form.page.data,
#             # book_status=form.book_status.data,
#             user_id=form.user_id.data
#         )
#         db.session.add(new_book)
#         db.session.commit()
#         flash('Book added successfully!', 'success')
#         return redirect(url_for('book.add_book'))
#     return render_template('add_book.html', form=form)

@book_bp.route('/update_book/<string:id>', methods=['GET', 'POST'])
def update_book(id):
    book = Books.query.get(id)
    form = UpdateBookForm(obj=book)
    
    if form.validate_on_submit():
        try:
            form.populate_obj(book)  # Update the book object with form data
            db.session.commit()
            flash('Book updated successfully!', 'success')
            return redirect(url_for('book.update_book', id=id))
        
        except IntegrityError:
            db.session.rollback()  # Rollback on any integrity errors
            flash('Error: Book ID already exists. Please choose a different ID.', 'danger')
        
        except Exception as e:
            db.session.rollback()  # Rollback on any other errors
            flash(f'An unexpected error occurred: {str(e)}', 'danger')
    
    return render_template('update_book.html', form=form, book=book)

# @book_bp.route('/update_book/<string:id>', methods=['GET', 'POST'])
# def update_book(id):
#     book = Books.query.get(id)
#     form = UpdateBookForm(obj=book)
#     if form.validate_on_submit():
#         form.populate_obj(book)
#         db.session.commit()
#         flash('Book updated successfully!', 'success')
#         return redirect(url_for('book.update_book', id=id))
#     return render_template('update_book.html', form=form, book=book)

@book_bp.route('/delete_book/<string:id>', methods=['POST'])
def delete_book(id):
    book = Books.query.get(id)
    if book:
        db.session.delete(book)
        db.session.commit()
        flash('Book deleted successfully!', 'success')
    else:
        flash('Book not found!', 'error')
    return redirect(url_for('book.view_all_books'))


@book_bp.route('/view_all_Books', methods=['GET'])
def view_all_books():
    books = Books.query.all()
    return render_template('view_all_Books.html', books=books)

@book_bp.route('/books')
def all_books():
    books = Books.query.all()
    return render_template('all_books.html', books=books)


@book_bp.route('/sorting_books', methods=['GET'])
def sorting_books():
    # Get the sort parameter from the request
    sort_by = request.args.get('sort', 'title')  # Default to sorting by title

    # Query books and apply sorting
    if sort_by == 'title':
        books = Books.query.order_by(Books.title.asc()).all()
    elif sort_by == 'author':
        books = Books.query.order_by(Books.author.asc()).all()
    elif sort_by == 'date':
        books = Books.query.order_by(Books.publication_year.desc()).all()
    elif sort_by == 'rating':
        books = Books.query.order_by(Books.Rating.desc()).all()
    else:
        books = Books.query.all()

    # Render the template with sorted books
    return render_template('all_books.html', books=books)

@book_bp.route('/search_books', methods=['GET'])
def search_books():
    query = request.args.get('query')  # Get the search query from the form input

    if query:
        # Filter books by title, author, or description
        books = Books.query.filter(
            (Books.title.ilike(f'%{query}%')) | 
            (Books.author.ilike(f'%{query}%')) | 
            (Books.Description.ilike(f'%{query}%'))
        ).all()
    else:
        books = Books.query.all()  # If no query, return all books

    return render_template('all_books.html', books=books)

