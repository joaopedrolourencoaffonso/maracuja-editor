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

    file = open("capitulos/data.json", "w")
    json.dump({"text": text}, file)
    file.close()

    return jsonify({"message": "ok"})

@app.route('/lista_projetos_recentes')
def lista_projetos_recentes():
    data = {"livro1":"1", "livro2":"2", "livro3":"3","livro4":"4","livro5":"5","livro6":"6","livro7":"7","livro8":"8","livro9":"9"}
    return jsonify(data)

@app.route('/project_page/<int:project_id>', methods=['GET'])
def project_page(project_id):
    print(project_id);
    return render_template('project_page.html',projectID=project_id)

@app.route('/project_info/<int:project_id>', methods=['GET'])
def project_info(project_id):
    data = {"name": "Saci e o Rei dos Ladrões","sinopse": "Humilhado e traído, o saci embarca numa jornada por justiça contra o terrível rei dos ladrões.", "capitulos":["capitulo 1","capitulo 2","capitulo 3","capitulo 4"], "capa":"https://images.unsplash.com/photo-1536895058696-a69b1c7ba34f?q=80&w=435&auto=format&fit=crop&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D"}
    return jsonify(data)

if __name__ == '__main__':
    app.run(debug=True)