from flask import Flask

app = Flask(__name__)

@app.route("/photos")
def photos():
    return {"message": "Hello from photos service"}

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8255)
