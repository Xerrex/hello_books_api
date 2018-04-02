from _datetime import datetime, timedelta


class Borrow(object):
    """Borrow model

    This class defines the borrowing of a book by a user
    user_id, book_id, borrowed_at, due_at, is_returned
    """
    def __init__(self,user_id, book_id):
        self.user_id = user_id
        self.book_id = book_id
        self.borrowed_at = datetime.utcnow()
        self.due_at = datetime.utcnow() + timedelta(days=3)
        self.is_active = True

    def __repr__(self):
        """Define how Borrow is represented
        """
        return 'borrowed-{}-{}-{}'.format(self.book_id, self.borrowed_at, self.is_active)