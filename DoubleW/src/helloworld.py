from flask import Flask
app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello World!'

@app.route('/user/<username>')
def test(username):
    return 'Welcome %s!' % username

if __name__ == '__main__':

    app.run(debug=True)
