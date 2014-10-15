from flask import Flask, render_template
app = Flask(__name__)

@app.route('/test')
def index():
  return 'Hello, World!'

@app.route('/route')
def route():
  return 'Route page'

if __name__ == '__main__':
  app.run(debug=True)
