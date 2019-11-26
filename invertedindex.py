from apperance import Appearance
import re


class InvertedIndex:
    # Inverted Index class.

    def __init__(self, db):
        self.index = dict()
        self.db = db

    # save text to the database
    def index_document(self, document):
        # Remove punctuation from the text.
        clean_text = re.sub(r"[^\w\s]", "", document["text"])
        terms = clean_text.split(" ")
        appearances_dict = dict()
        # Dictionary with each term and the frequency it appears in the text.
        for term in terms:
            term_frequency = (
                appearances_dict[term].frequency if term in appearances_dict else 0
            )
            appearances_dict[term] = Appearance(document["id"], term_frequency + 1)

        # Update the inverted index
        update_dict = {
            key: [appearance]
            if key not in self.index
            else self.index[key] + [appearance]
            for (key, appearance) in appearances_dict.items()
        }
        self.index.update(update_dict)
        # Add the document into the database
        self.db.add(document)
        return document

    # returns the dictionary with the corresponding appearance
    def lookup_query(self, query):
        return {
            term: self.index[term] for term in query.split(" ") if term in self.index
        }

