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
        for para in a.splitlines():
            if "count" not in session:
                session["count"] = 0
            else:
                session["count"] += 1
            d = {}
            d["id"] = session["count"]
            d["text"] = para.lower()
            index1.index_document(d)
        return redirect(url_for("search"))


@app.route("/search", methods=["GET", "POST"])
def search():
    if request.method == "GET":
        return render_template("search.html")

    if request.method == "POST":
        a = request.form["word"].lower()
        result = index1.lookup_query(a)
        a = []
        for term in result.keys():
            for appearance in result[term]:
                # Belgium: { docId: 1, frequency: 1}
                document = db.get(appearance.docId)
                print(appearance.docId, ": ", document["text"])
                a.append((document["text"], appearance.frequency))
        a = sorted(a, key=lambda x: x[1])
        if a == []:
            a.append("Not Found")
        elif len(a) > 10:
            a = a[0:10]
        return render_template("final.html", ans=a)


if __name__ == "__main__":
    app.run(debug=True)
