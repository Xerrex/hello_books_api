class Book(object):
    """This defines the Book data model

    name, description, section, quantity
    """
    def __init__(self, name, description, section, quantity):
        self.name = name
        self.description = description
        self.section = section
        self.quantity = int(quantity)

    def __repr__(self):
        """
        Defines how to print the User model
        """

        return 'Book:{}-{}'.format(self.name, self.quantity)
