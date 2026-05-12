from flask import Flask, render_template
from routes.analyze import analyze_bp
from routes.compare import compare_bp

app = Flask(__name__)
app.register_blueprint(analyze_bp)
app.register_blueprint(compare_bp)

@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)