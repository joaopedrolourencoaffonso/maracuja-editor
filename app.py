from flask import Flask, render_template, jsonify, request
import json
import os

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/editor')
def editor():
    return render_template('editor.html')

@app.route('/data')
def data():
    text = request.args.get("text", "")
    text = text.replace('<div class="ql-editor" contenteditable="true">', "");
    text = text.replace('</div><div class="ql-tooltip ql-hidden"><a class="ql-preview" rel="noopener noreferrer" target="_blank" href="about:blank"></a><input type="text" data-formula="e=mc^2" data-link="https://quilljs.com" data-video="Embed URL"><a class="ql-action"></a><a class="ql-remove"></a></div>', "");
    print(f"{text}");

    file = open("static/data.json", "w")
    json.dump({"text": text}, file)
    file.close()

    return jsonify({"message": "ok"})

if __name__ == '__main__':
    app.run(debug=True)