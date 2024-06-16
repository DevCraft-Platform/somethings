from flask import Flask, request, jsonify, render_template

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/api', methods=['GET'])
def api():
    return jsonify({
        "message": "Hello, World!"
    })

@app.route('/editor', methods=['GET'])
def editor():
    return render_template('editor/index.html')    

if __name__ == '__main__':
    app.run(debug=True, port=3000)
    
