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
    #print("form: ", request.form)
    print("images: ", request.files)

    titulo = request.form.get("titulo");
    sinopse = request.form.get("sinopse");
    
    image = request.files.get("image");
    image.filename = image.filename.replace(' ','_');
    filepath = os.path.join("localdata", image.filename)
    image.save(filepath)

    id_do_projeto = maracuja_funcs.insere_titulo_sinopse(sqlite3, titulo, sinopse, image.filename);

    resposta = {"msg":"ok","id":id_do_projeto}
    return jsonify(resposta)

@app.route('/project_info/<int:project_id>', methods=['GET'])
def project_info(project_id):
    titulo = maracuja_funcs.pega_titulo_por_id(sqlite3, project_id);
    sinopse = maracuja_funcs.pega_sinopse_por_id(sqlite3, project_id);
    capa = maracuja_funcs.pega_capa_por_id(sqlite3, project_id);
    print(titulo, sinopse, capa)
    data = {"name": titulo,"sinopse": sinopse, "capitulos":[[1,"capitulo_1"],[2,"capitulo_2"],[3,"capitulo_3"],[4,"capitulo_4"]], "capa":capa}
    return jsonify(data)

@app.route('/todos_projetos', methods=['GET'])
def todos_projetos():
    return render_template('todos_projetos.html')

@app.route('/img/<string:filename>', methods=['GET'])
def img(filename):
    if filename == "CAPA_DO_PROJETO":
        return send_file(".\\static\\under_contruction.png", mimetype='image/gif')
    return send_file(".\\localdata\\" + filename, mimetype='image/gif')

@app.route('/img_app/<int:image_id>', methods=['GET'])
def img_app(image_id):
    if (image_id == 1):
        image_id = "under_contruction.png";
    else:
        image_id = "alt_under_contruction.png";
    
    return send_file(".\\static\\" + image_id, mimetype='image/gif')

@app.route('/atualiza_projeto_info', methods=['POST'])
def atualiza_projeto_info():
    #print("form: ", request.form)
    print("images: ", request.files)

    project_id = request.form.get("project_id");
    titulo = request.form.get("titulo");
    sinopse = request.form.get("sinopse");
    nome_imagem = "qiwuqiwuqoeuwhewh,djhbfejhv";
    
    image = request.files.get("image");

    print(titulo, sinopse, image);

    if image != None:
        image.filename = image.filename.replace(' ','_');
        filepath = os.path.join("localdata", image.filename)
        image.save(filepath)
        nome_imagem = image.filename

    maracuja_funcs.atualiza_titulo_sinopse(sqlite3, project_id, titulo, sinopse, nome_imagem);

    resposta = {"msg":"ok"}
    return jsonify(resposta)

if __name__ == '__main__':
    maracuja_funcs.DB_start(sqlite3);
    app.run(debug=True)