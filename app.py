from flask import Flask, render_template, jsonify, request, send_file
import json
import os
from time import time;
import sqlite3
from pathlib import Path
import maracuja_funcs;

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/editor')
def editor():
    return render_template('editor.html')

@app.route('/editarCapitulo/', methods=['GET'])
def editarCapitulo():
    # CONTINUAR DAQUI!
    project_id = request.args.getlist('project_id')[0];
    chapter_id = request.args.getlist('chapter_id')[0];
    version_id = request.args.getlist('version_id')[0];
    # PLACEHOLDER
    #version_id = str(1);
    print(project_id, chapter_id);
    if chapter_id == "Novo":
        chapter_id = maracuja_funcs.retorna_novo_chapter_id(sqlite3, project_id, chapter_id)
        file = open("capitulos/" + project_id + "-" + chapter_id + "-" + version_id + ".json", "w")
        json.dump({"text": '{"text": "<p>Era uma vez...</p>"}'}, file)
        file.close()
    
    file = open("capitulos/" + project_id + "-" + chapter_id + "-" + version_id  + ".json", "r")
    rawChapterData = file.read();
    file.close();

    chapterData = json.loads(rawChapterData);

    titulo_capitulo = maracuja_funcs.retorna_titulo_capitulo(sqlite3, project_id, chapter_id, version_id);

    return render_template('editor.html',projectID=project_id, chapterID=chapter_id,chapterData=chapterData,versionID=version_id,tituloCapitulo=titulo_capitulo);

@app.route('/data', methods=['POST'])
def data():
    data = request.get_json()

    project_id = data["project_id"]
    chapter_id = data["chapter_id"]
    version_id = data["version_id"]
    contents = data["contents"]
    chapter_title = data["chapter_title"]

    file = open("capitulos/" + project_id + "-" + chapter_id + "-" + version_id + ".json", "w")
    json.dump(contents, file)
    file.close()

    maracuja_funcs.atualiza_titulo_capitulo(sqlite3, project_id, chapter_id, version_id, chapter_title)

    maracuja_funcs.atualiza_projeto_mais_recente(sqlite3, time, project_id);

    return jsonify({"message": "ok"})

@app.route('/nova_versao_capitulo', methods=['POST'])
def nova_versao_capitulo():
    data = request.get_json()

    print(data);

    project_id = data["project_id"]
    chapter_id = data["chapter_id"]
    #version_id = data["version_id"]
    contents = data["contents"]
    chapter_title = data["chapter_title"]
    nome_nova_versao = data["nome_nova_versao"]

    version_id = maracuja_funcs.registra_nova_versao(sqlite3, project_id, chapter_id, chapter_title, nome_nova_versao);

    file = open("capitulos/" + str(project_id) + "-" + str(chapter_id) + "-" + str(version_id) + ".json", "w")
    json.dump(contents, file)
    file.close()

    maracuja_funcs.atualiza_titulo_capitulo(sqlite3, project_id, chapter_id, version_id, chapter_title)

    maracuja_funcs.atualiza_projeto_mais_recente(sqlite3, time, project_id);

    return jsonify({"message": "ok","version_id":version_id})

@app.route('/chapterData', methods=['POST'])
def chapterData():
    chapter_id = request.args.getlist("chapter_id")[0];
    project_id = request.args.getlist("project_id")[0];

    file = open("capitulos/" + project_id + "-" + chapter_id + "-" + version_id + ".json", "r")
    data = file.read();
    file.close()

    return jsonify({"chapterData": data})

@app.route('/lista_projetos_recentes')
def lista_projetos_recentes():
    order_desc = maracuja_funcs.retorna_projetos_recentes(sqlite3);
    print(order_desc)
    data = {}
    for projeto in order_desc:
        titulo = maracuja_funcs.pega_titulo_por_id(sqlite3, projeto[0]);
        data[titulo] = projeto[0];
        
    print(data);
    
    return jsonify(data)

@app.route('/lista_todos_projetos')
def lista_todos_projetos():
    rows = maracuja_funcs.todos_projetos(sqlite3);
    return jsonify(rows)

@app.route('/project_page/<int:project_id>', methods=['GET'])
def project_page(project_id):
    print(project_id);
    return render_template('project_page.html',projectID=project_id)

@app.route('/criar_projeto', methods=['GET'])
def criar_projeto():
    return render_template('criar_projeto.html')

@app.route('/cadastraProjeto', methods=['POST'])
def cadastraProjeto():
    print("images: ", request.files)

    titulo = request.form.get("titulo");
    sinopse = request.form.get("sinopse");
    
    image = request.files.get("image");
    image.filename = image.filename.replace(' ','_');
    filepath = os.path.join("localdata", image.filename)
    image.save(filepath)

    id_do_projeto = maracuja_funcs.insere_titulo_sinopse(sqlite3, titulo, sinopse, image.filename);

    maracuja_funcs.insere_projeto_mais_recente(sqlite3, time, id_do_projeto);

    resposta = {"msg":"ok","id":id_do_projeto}
    return jsonify(resposta)

@app.route('/project_info/<int:project_id>', methods=['GET'])
def project_info(project_id):
    titulo = maracuja_funcs.pega_titulo_por_id(sqlite3, project_id);
    sinopse = maracuja_funcs.pega_sinopse_por_id(sqlite3, project_id);
    capa = maracuja_funcs.pega_capa_por_id(sqlite3, project_id);
    print(titulo, sinopse, capa);

    capitulos = maracuja_funcs.pega_capitulos(sqlite3, project_id);

    data = {"name": titulo,"sinopse": sinopse, "capitulos":capitulos, "capa":capa}
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
    maracuja_funcs.atualiza_projeto_mais_recente(sqlite3, time, project_id);

    resposta = {"msg":"ok"}
    return jsonify(resposta);

@app.route('/deleta_capitulo', methods=['POST'])
def deleta_capitulo():
    data = request.get_json()

    project_id = data["project_id"]
    chapter_id = data["chapter_id"]
    version_id = data["version_id"]
    
    maracuja_funcs.excluir_capitulo(os, sqlite3, project_id, chapter_id, version_id);

    return jsonify({"message": "ok"})

@app.route('/deleta_projeto', methods=['POST'])
def deleta_projeto():
    data = request.get_json()

    project_id = data["project_id"];

    maracuja_funcs.excluir_projeto(os, Path, sqlite3, project_id);

    return jsonify({"message": "ok"});

@app.route('/move_capitulo', methods=['POST'])
def move_capitulo():
    data = request.get_json()

    project_id = data["project_id"]
    capituloASerMovido = data["capituloASerMovido"]
    novaPosicaoDoCapitulo = data["novaPosicaoDoCapitulo"]

    maracuja_funcs.mover_capitulo(sqlite3, project_id, capituloASerMovido, novaPosicaoDoCapitulo);

    return jsonify({"message": "ok"})

@app.route('/pega_versoes_capitulo', methods=['POST'])
def pega_versoes_capitulo():
    data = request.get_json()

    project_id = data["project_id"]
    chapter_id = data["chapter_id"]

    lista = maracuja_funcs.pega_versoes_capitulo(sqlite3, project_id, chapter_id);

    return jsonify({"message": "ok", "lista": lista});

if __name__ == '__main__':
    maracuja_funcs.DB_start(sqlite3);
    app.run(debug=True)