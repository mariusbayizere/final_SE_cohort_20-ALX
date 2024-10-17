from flask import Blueprint, render_template, request, redirect, url_for, flash
from form.forms import BorrowForm, UpdateBorrowForm, ReturnForm
from models import db, Borrow, Books
from datetime import datetime, timedelta

borrow_bp = Blueprint('borrow', __name__)

# @borrow_bp.route('/add_borrow', methods=['GET', 'POST'])
# def add_borrow():
#     form = BorrowForm()
#     if form.validate_on_submit():
#         new_borrow = Borrow(
#             book_id=form.book_id.data,
#             user_id=form.user_id.data,
#             borrow_date=form.borrow_date.data,
#             return_date=form.return_date.data,
#             fine=form.fine.data,
#             status=form.status.data
#         )
#         db.session.add(new_borrow)
#         db.session.commit()
#         flash('Borrow record added successfully!', 'success')
#         return redirect(url_for('borrow.add_borrow'))
#     return render_template('add_borrow.html', form=form)

# @borrow_bp.route('/add_borrow/<string:book_id>', methods=['GET', 'POST'])
# def add_borrow(book_id):
#     form = BorrowForm()

#     # Pre-fill the book_id in the form
#     form.book_id.data = str(book_id)

#     if form.validate_on_submit():
#         # Create a new Borrow record
#         new_borrow = Borrow(
#             book_id=form.book_id.data,
#             user_id=form.user_id.data,
#             borrow_date=form.borrow_date.data,
#             return_date=form.return_date.data,
#             fine=form.fine.data,
#             status=form.status.data
#         )
#         db.session.add(new_borrow)

#         # Update the book's status to 'Borrowed'
#         book = Books.query.filter_by(book_id=book_id).first()
#         if book:
#             book.book_status = 'Borrowed'

#         db.session.commit()  # Commit both the new borrow and the book status update

#         flash('Borrow record added successfully, and book status updated to Borrowed!', 'success')
#         return redirect(url_for('borrow.add_borrow', book_id=book_id))
    
#     return render_template('add_borrow.html', form=form)


# borrow.py
from flask import Blueprint, redirect, url_for, flash, render_template
from form.forms import BorrowForm
from models import db, Books, Borrow

borrow_bp = Blueprint('borrow', __name__)

@borrow_bp.route('/add_borrow/<string:book_id>', methods=['GET', 'POST'])
def add_borrow(book_id):
    form = BorrowForm()

    # Fetch the book to check its status
    book = Books.query.filter_by(book_id=book_id).first()

    if book is None:
        flash('Book not found!', 'danger')
        return redirect(url_for('book.all_books'))  # Corrected

    # Check if the book is already borrowed
    if book.book_status == 'Borrowed':
        flash('This book is already borrowed and cannot be borrowed again until returned.', 'danger')
        return redirect(url_for('book.all_books'))  # Corrected

    # Pre-fill the book_id in the form
    form.book_id.data = str(book_id)

    if form.validate_on_submit():
        # Create a new Borrow record
        new_borrow = Borrow(
            book_id=form.book_id.data,
            user_id=form.user_id.data,
            borrow_date=form.borrow_date.data,
            return_date=form.return_date.data,
            fine=form.fine.data,
            status=form.status.data
        )
        db.session.add(new_borrow)

        # Update the book's status to 'Borrowed'
        book.book_status = 'Borrowed'
        db.session.commit()  # Commit both the new borrow and the book status update

        flash('Borrow record added successfully, and book status updated to Borrowed!', 'success')
        return redirect(url_for('borrow.add_borrow', book_id=book_id))
    
    return render_template('add_borrow.html', form=form)




@borrow_bp.route('/update_borrow/<string:id>', methods=['GET', 'POST'])
def update_borrow(id):
    borrow = Borrow.query.get(id)
    form = UpdateBorrowForm(obj=borrow)
    if form.validate_on_submit():
        form.populate_obj(borrow)
        db.session.commit()
        flash('Borrow updated successfully!', 'success')
        return redirect(url_for('borrow.update_borrow', id=id))
    return render_template('Update_Borrow.html', form=form, borrow=borrow)

@borrow_bp.route('/delete_borrow/<string:id>')
def delete_borrow(id):
    borrow = Borrow.query.get(id)
    db.session.delete(borrow)
    db.session.commit()
    flash('Borrow record deleted successfully!', 'success')
    return redirect(url_for('borrow.view_all_borrow'))


@borrow_bp.route('/view_all_borrow')
def view_all_borrow():
    borrow_records = Borrow.query.all()
    return render_template('view_all_Borrow.html', borrow_records=borrow_records)


@borrow_bp.route('/return_book', methods=['GET', 'POST'])
def return_book():
    form = ReturnForm()
    borrow_records = None

    if request.method == 'POST':
        user_id = request.form.get('user_id')  # Retrieve user ID from the form
        selected_books = request.form.getlist('books_to_return')  # Retrieve list of selected book_ids
        
        if not selected_books:
            flash('No books selected for return.', 'warning')
            return redirect(url_for('borrow.return_book', user_id=user_id))

        # Fetch all borrow records for the user that are pending (not yet returned) and match the selected book_ids
        borrow_records = Borrow.query.filter_by(user_id=user_id, status='Pending').filter(Borrow.book_id.in_(selected_books)).all()

        if not borrow_records:
            flash('No borrowed books found for the provided User ID.', 'warning')
            return redirect(url_for('borrow.return_book', user_id=user_id))

        fine = 0  # Initialize the fine
        for record in borrow_records:
            record.actual_return_date = datetime.utcnow()

            expected_return_date = record.return_date
            actual_return_date = record.actual_return_date
            if actual_return_date > expected_return_date:
                delta = actual_return_date - expected_return_date
                late_days = delta.days
                fine += late_days * 10000

            record.fine = fine
            record.status = 'Returned'

            # Optionally, update the book's availability
            book = Books.query.filter_by(book_id=record.book_id).first()
            if book:
                book.book_status = "Available"

        db.session.commit()
        flash(f'Books returned successfully! Total fine: {fine} RWF', 'success')
        return redirect(url_for('borrow.return_book', user_id=user_id))

    if request.method == 'GET':
        user_id = request.args.get('user_id')
        if user_id:
            borrow_records = Borrow.query.filter_by(user_id=user_id, status='Pending').all()
            if borrow_records:
                form.books_to_return.choices = [(record.book_id, record.books.title) for record in borrow_records]
            else:
                flash('No borrowed books found for the provided User ID.', 'warning')

    return render_template('return_books.html', form=form, borrow_records=borrow_records)

# @borrow_bp.route('/return_book', methods=['GET', 'POST'])
# def return_book():
#     form = ReturnForm()
#     borrow_records = None

#     if request.method == 'POST':
#         user_id = request.form.get('user_id')  # Retrieve user ID from the form
#         selected_books = request.form.getlist('books_to_return')  # Retrieve list of selected book_ids
        
#         if not selected_books:
#             flash('No books selected for return.', 'warning')
#             return redirect(url_for('borrow.return_book', user_id=user_id))

#         # Fetch all borrow records for the user that are pending (not yet returned) and match the selected book_ids
#         borrow_records = Borrow.query.filter_by(user_id=user_id, status='Pending').filter(Borrow.book_id.in_(selected_books)).all()

#         if not borrow_records:
#             flash('No borrowed books found for the provided User ID.', 'warning')
#             return redirect(url_for('borrow.return_book', user_id=user_id))

#         fine = 0  # Initialize the fine
#         for record in borrow_records:
#             record.actual_return_date = datetime.utcnow()

#             # Calculate the number of late days
#             expected_return_date = record.return_date
#             actual_return_date = record.actual_return_date

#             # If returned after the expected date, calculate fine
#             if actual_return_date > expected_return_date:
#                 delta = actual_return_date - expected_return_date
#                 late_days = delta.days
#                 fine += late_days * 10000  # Add fine based on 10,000 per day

#             record.fine = fine
#             record.status = 'Returned'

#             # Update the book's availability if its status is 'Borrowed'
#             book = Books.query.filter_by(book_id=record.book_id).first()
#             if book and book.book_status == "Borrowed":
#                 book.book_status = "Available"

#         # Commit all changes (borrow records and book statuses)
#         db.session.commit()
#         flash(f'Books returned successfully! Total fine: {fine} RWF', 'success')
#         return redirect(url_for('borrow.return_book', user_id=user_id))

#     if request.method == 'GET':
#         user_id = request.args.get('user_id')
#         if user_id:
#             borrow_records = Borrow.query.filter_by(user_id=user_id, status='Pending').all()
#             if borrow_records:
#                 form.books_to_return.choices = [(record.book_id, record.books.title) for record in borrow_records]
#             else:
#                 flash('No borrowed books found for the provided User ID.', 'warning')

#     return render_template('return_books.html', form=form, borrow_records=borrow_records)
