class Book(object):

    def __init__(self,name, description, section, quantity):
        self.name = name
        self.description = description
        self.section = section
        self.quantity = int(quantity)

    # def save(self):
    #     for x in Book.bookslist:
    #         if x.name == self.name:
    #             response = jsonify({'message':'Book already exists'})
    #             return make_response(response), 403
    #         else:
    #             Book.bookslist.append(self)
    #             response = jsonify({'message':'Book created  successfully'})
    #             return make_response(response), 201


    def __repr__(self):
        return '<Book {}>'.format(self.name)