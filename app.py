from flask import Flask, render_template, jsonify, request, send_file
import json
import os
import sqlite3
import maracuja_funcs;

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

@app.route('/lista_todos_projetos')
def lista_todos_projetos():
    tempFigura = "https://upload.wikimedia.org/wikipedia/commons/thumb/a/a9/Chaos%2C_of_Moss_K9%2C_as_a_Puppy.jpg/960px-Chaos%2C_of_Moss_K9%2C_as_a_Puppy.jpg?utm_source=commons.wikimedia.org&utm_campaign=imageinfo&utm_content=thumbnail"
    data = {"1": {"titulo":"Título 1","ncapitulos" : 12,"ntimelines":6,"src": tempFigura},"2": {"titulo":"Título 2","ncapitulos" : 5,"ntimelines":2,"src": tempFigura},"3": {"titulo":"Título 3","ncapitulos" : 5,"ntimelines":4,"src": tempFigura},"4": {"titulo":"Título 4","ncapitulos" : 5,"ntimelines":4,"src": tempFigura},"5": {"titulo":"Título 3","ncapitulos" : 5,"ntimelines":4,"src": tempFigura},"6": {"titulo":"Título 3","ncapitulos" : 5,"ntimelines":4,"src": tempFigura},"7": {"titulo":"Título 3","ncapitulos" : 5,"ntimelines":4,"src": tempFigura}}
    return jsonify(data)

@app.route('/project_page/<int:project_id>', methods=['GET'])
def project_page(project_id):
    print(project_id);
    return render_template('project_page.html',projectID=project_id)

@app.route('/criar_projeto', methods=['GET'])
def criar_projeto():
    return render_template('criar_projeto.html')

@app.route('/cadastraProjeto', methods=['POST'])
def cadastraProjeto():
    print("form: ", request.form)
    print("images: ", request.files)

    image = request.files.get("image");
    filepath = os.path.join("localdata", image.filename)
    image.save(filepath)

    resposta = {"msg":"ok"}
    return jsonify(resposta)

@app.route('/project_info/<int:project_id>', methods=['GET'])
def project_info(project_id):
    data = {"name": "Saci e o Rei dos Ladrões","sinopse": "Humilhado e traído, o saci embarca numa jornada por justiça contra o terrível rei dos ladrões.", "capitulos":["capitulo 1","capitulo 2","capitulo 3","capitulo 4"], "capa":"https://images.unsplash.com/photo-1536895058696-a69b1c7ba34f?q=80&w=435&auto=format&fit=crop&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D"}
    return jsonify(data)

@app.route('/todos_projetos', methods=['GET'])
def todos_projetos():
    return render_template('todos_projetos.html')

@app.route('/img/<int:image_id>', methods=['GET'])
def img(image_id):
    if (image_id == 1):
        image_id = "under_contruction.png";
    else:
        image_id = "alt_under_contruction.png";
    
    return send_file(".\\static\\" + image_id, mimetype='image/gif')

if __name__ == '__main__':
    maracuja_funcs.DB_start(sqlite3);
    app.run(debug=True)