class Database:
    def __init__(self):
        self.db = dict()

    # get the document
    def get(self, id):
        return self.db.get(id, None)

    # adds a document to the database
    def add(self, document):
        return self.db.update({document["id"]: document})

    # removes a document from database
    def remove(self, document):
        return self.db.pop(document["id"], None)

