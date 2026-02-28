from flask import Flask

app = Flask(__name__)

@app.route("/other")
def other():
    return {"message": "Hello from other service"}

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8256)
