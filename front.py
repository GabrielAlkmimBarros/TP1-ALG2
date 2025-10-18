from flask import Flask, render_template, request

app = Flask(__name__)

@app.route("/")
def homepage():
    return render_template("index.html")

app.route("/search", methods=["POST"])
def buscar():
    termo = request.form["query"]

    ######################################################

    # AQUI VAI SER COLOCADO A CHAMADA DO PROGRAMA COM O PARAMETRO TERMO

    ######################################################


if __name__ == "__main__":
    app.run(debug=True)

    from front import app, render_template, request
