from database import Database
from invertedindex import InvertedIndex
from flask import Flask, redirect, render_template, request, session, url_for

app = Flask(__name__)

# Secret key for sessions
app.secret_key = "secret"
db = Database()
index1 = InvertedIndex(db)


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "GET":
        return render_template("index.html")

    if request.method == "POST":
        a = request.form["para"]
        for para in a.split("\n"):
            if "count" not in session:
                session["count"] = 0
            else:
                session["count"] += 1
            d = {}
            d["id"] = session["count"]
            d["text"] = para
            index1.index_document(d)
        return redirect(url_for("search"))


@app.route("/search", methods=["GET", "POST"])
def search():
    if request.method == "GET":
        return render_template("search.html")


def main():
    db = Database()
    index = InvertedIndex(db)
    document1 = {"id": "1", "text": "The big sharks of Belgium drink beer."}
    document2 = {
        "id": "2",
        "text": "Belgium has great beer. They drink beer all the time.",
    }
    index.index_document(document1)
    index.index_document(document2)

    search_term = input("Enter term(s) to search: ")
    result = index.lookup_query(search_term)

    for term in result.keys():
        for appearance in result[term]:
            # Belgium: { docId: 1, frequency: 1}
            document = db.get(appearance.docId)
            print(appearance.docId, ": ", document["text"])
        print("-----------------------------")


if __name__ == "__main__":
    app.run(debug=True)
