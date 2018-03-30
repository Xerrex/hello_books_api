class Book(object):

    def __init__(self, name, description, section, quantity):
        self.name = name
        self.description = description
        self.section = section
        self.quantity = int(quantity)

    def __repr__(self):
        return '<Book {}>'.format(self.name)
