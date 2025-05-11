from flask import Flask, request, render_template, jsonify
from parser import Parser

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/parse', methods=['POST'])
def parse_input():
    data = request.get_json(force=True)
    input_str = data.get('input', '')
    try:
        parser = Parser(input_str)
        parser.parse()
        dot = parser.to_dot()
        return jsonify(success=True, dot=dot, derivations=parser.get_derivations())
    except SyntaxError as e:
        return jsonify(success=False, error=str(e)), 200
    except Exception as e:
        return jsonify(success=False, error="Internal error: " + str(e)), 500

if __name__ == '__main__':
    app.run()

from werkzeug.middleware.dispatcher import DispatcherMiddleware
from werkzeug.serving import run_simple

application = DispatcherMiddleware(app.wsgi_app)