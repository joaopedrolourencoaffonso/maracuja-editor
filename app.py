from flask import Flask, render_template, jsonify, request, send_file
import json
import os
from time import time;
import sqlite3
from pathlib import Path
from sys import argv;
import tarfile;
from pathlib import Path
import shutil
import tempfile
import urllib.request as requests_lib;
import maracuja_funcs;

app = Flask(__name__)

# global variables
version = "";

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/settings')
def settings():
    return render_template('settings.html')

@app.route('/apagaTudo', methods=['GET'])
def apagaTudo():
    try:
        maracuja_funcs.clean(Path, shutil)
        return jsonify({'msg':'Arquivos deletados com sucesso!'});
    except Exception as e:
        return jsonify({'msg':str(e)});

@app.route('/importandoArquivos', methods=['POST'])
def importandoArquivos():
    filepath = None
    try:
        arquivo = request.files.get('file')
        if arquivo is None or arquivo.filename == '':
            raise ValueError('Nenhum arquivo .tar.gz foi enviado')

        with tempfile.NamedTemporaryFile(suffix='.tar.gz', delete=False) as arquivo_temporario:
            filepath = arquivo_temporario.name
            arquivo.save(filepath)

        maracuja_funcs.importa_arquivos(argv, tarfile, filepath, Path, shutil)
        return jsonify({'msg': 'Arquivos importados com sucesso!'})
    except Exception as e:
        return jsonify({'msg': str(e)})
    finally:
        if filepath is not None:
            os.remove(filepath)

@app.route('/retornaBackup', methods=['GET'])
def retornaBackup():
    maracuja_funcs.exporta_arquivos(["a","b","meusProjetosExport.tar.gz"],tarfile);
    return send_file(
        "meusProjetosExport.tar.gz",
        mimetype="application/gzip",
        as_attachment=True,
        download_name="meusProjetosExport.tar.gz"
    )

@app.route('/editarNota/', methods=['GET'])
def editarNota():
    project_id = request.args.getlist('project_id')[0];
    nota_id = request.args.getlist('nota_id')[0];

    nota = maracuja_funcs.retorna_nota_especifica(sqlite3, project_id, nota_id);

    file_path = Path("notas") / f"nota-{project_id}-{nota_id}.json"
    with file_path.open("r", encoding="utf-8") as file:
        rawChapterData = file.read()

    chapterData = json.loads(rawChapterData);

    print("nota: ", nota, nota_id, project_id)

    return render_template('editarNota.html',projectID=project_id,notasID=nota_id, tituloNota = nota[0][0], descricaoNota = nota[0][1],chapterData=chapterData)

@app.route('/editarCapitulo/', methods=['GET'])
def editarCapitulo():
    # CONTINUAR DAQUI!
    project_id = request.args.getlist('project_id')[0];
    chapter_id = request.args.getlist('chapter_id')[0];
    version_id = request.args.getlist('version_id')[0];
    iframeFlag = request.args.getlist('iframeFlag');
    if iframeFlag == []:
        iframeFlag = 0
    else:
        iframeFlag = 1
    
    print("-> ", iframeFlag);
    # PLACEHOLDER
    #version_id = str(1);
    print(project_id, chapter_id);
    if chapter_id == "Novo":
        chapter_id = maracuja_funcs.retorna_novo_chapter_id(sqlite3, project_id, chapter_id)
        file_path = Path("capitulos") / f"{project_id}-{chapter_id}-{version_id}.json"
        with file_path.open("w", encoding="utf-8") as file:
            json.dump({"text": '{"text": "Era uma vez..."}'}, file);
    
    #file = open("capitulos/" + project_id + "-" + chapter_id + "-" + version_id  + ".json", "r")
    #rawChapterData = file.read();
    #file.close();
    file_path = Path("capitulos") / f"{project_id}-{chapter_id}-{version_id}.json"
    with file_path.open("r", encoding="utf-8") as file:
        rawChapterData = file.read()

    chapterData = json.loads(rawChapterData);

    titulo_capitulo = maracuja_funcs.retorna_titulo_capitulo(sqlite3, project_id, chapter_id, version_id);

    return render_template('editor.html',projectID=project_id, chapterID=chapter_id,chapterData=chapterData,versionID=version_id,tituloCapitulo=titulo_capitulo,iframeFlag=iframeFlag);

@app.route('/compararVersoes/', methods=['GET'])
def compararVersoes():
    # CONTINUAR DAQUI!
    project_id = request.args.getlist('project_id')[0];
    chapter_id = request.args.getlist('chapter_id')[0];
    v1 = request.args.getlist('v1')[0];
    v2 = request.args.getlist('v2')[0];

    titulo_v1 = maracuja_funcs.retorna_titulo_versao(sqlite3, project_id, chapter_id, v1);
    titulo_v2 = maracuja_funcs.retorna_titulo_versao(sqlite3, project_id, chapter_id, v2);
    
    return render_template('comparar_versoes.html',projectID=project_id, chapterID=chapter_id,v1=v1,v2=v2,titulo_v1=titulo_v1,titulo_v2=titulo_v2);

@app.route('/lerCapitulo/', methods=['GET'])
def lerCapitulo():
    # CONTINUAR DAQUI!
    project_id = request.args.getlist('project_id')[0];
    chapter_id = request.args.getlist('chapter_id')[0];
    version_id = request.args.getlist('version_id')[0];

    titulo_capitulo = maracuja_funcs.retorna_titulo_capitulo(sqlite3, project_id, chapter_id, version_id);

    #file = open("capitulos/" + project_id + "-" + chapter_id + "-" + version_id + ".json", "r")
    #rawChapterData = file.read();
    #file.close();
    file_path = Path("capitulos") / f"{project_id}-{chapter_id}-{version_id}.json"
    with file_path.open("r", encoding="utf-8") as file:
        rawChapterData = file.read()

    chapterData = json.loads(rawChapterData);
    
    return render_template('ler_capitulo.html',projectID=project_id, chapterID=chapter_id,version_id=version_id,titulo_capitulo=titulo_capitulo,chapterData=chapterData);

@app.route('/data', methods=['POST'])
def data():
    data = request.get_json()

    project_id = data["project_id"]
    chapter_id = data["chapter_id"]
    version_id = data["version_id"]
    contents = data["contents"]
    chapter_title = data["chapter_title"]

    file_path = Path("capitulos") / f"{project_id}-{chapter_id}-{version_id}.json"
    with file_path.open("w", encoding="utf-8") as file:
        json.dump(contents, file);

    maracuja_funcs.atualiza_titulo_capitulo(sqlite3, project_id, chapter_id, version_id, chapter_title)

    maracuja_funcs.atualiza_projeto_mais_recente(sqlite3, time, project_id);

    return jsonify({"message": "ok"})

@app.route('/dataNota', methods=['POST'])
def dataNota():
    data = request.get_json()

    print("1 -> ",  data["titulo_da_nota"]);

    project_id = data["project_id"]
    nota_id = data["nota_id"]
    titulo_da_nota = data["titulo_da_nota"]
    descricao_da_nota = data["descricao_da_nota"]
    contents = data["contents"]

    file_path = Path("notas") / f"nota-{project_id}-{nota_id}.json"
    with file_path.open("w", encoding="utf-8") as file:
        json.dump(contents, file);

    maracuja_funcs.atualiza_nota_projeto(sqlite3, project_id, nota_id, titulo_da_nota, descricao_da_nota);

    return jsonify({"msg": "ok"})

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

    #file = open("capitulos/" + str(project_id) + "-" + str(chapter_id) + "-" + str(version_id) + ".json", "w")
    #json.dump(contents, file)
    #file.close()
    file_path = Path("capitulos") / f"{project_id}-{chapter_id}-{version_id}.json"
    with file_path.open("w", encoding="utf-8") as file:
        json.dump(contents, file);

    maracuja_funcs.atualiza_titulo_capitulo(sqlite3, project_id, chapter_id, version_id, chapter_title)

    maracuja_funcs.atualiza_projeto_mais_recente(sqlite3, time, project_id);

    return jsonify({"message": "ok","version_id":version_id})

@app.route('/chapterData', methods=['POST'])
def chapterData():
    chapter_id = request.args.getlist("chapter_id")[0];
    project_id = request.args.getlist("project_id")[0];

    #file = open("capitulos/" + project_id + "-" + chapter_id + "-" + version_id + ".json", "r")
    #data = file.read();
    #file.close()
    file_path = Path("capitulos") / f"{project_id}-{chapter_id}-{version_id}.json"
    with file_path.open("r", encoding="utf-8") as file:
        data = file.read()

    return jsonify({"chapterData": data})

@app.route('/adicionaNota', methods=['POST'])
def adicionaNota():
    data = request.get_json();

    project_id = data["project_id"]
    titulo = data["titulo"]
    descricao = data["descricao"]

    nota_id = maracuja_funcs.insere_notas_projeto(sqlite3, project_id, titulo, descricao);

    file_path = Path("notas") / f"nota-{project_id}-{nota_id}.json"
    with file_path.open("w", encoding="utf-8") as file:
        json.dump('{"ops": [{"insert": ""}]}', file);

    return jsonify({"msg": "ok","nota_id":nota_id})

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

@app.route('/notasDoprojeto/<int:project_id>', methods=['GET'])
def notasDoprojeto(project_id):
    print(project_id);
    return render_template('notas_projeto.html',projectID=project_id)

@app.route('/retornaNotasProjeto/<int:project_id>', methods=['GET'])
def retornaNotasProjeto(project_id):
    print(project_id);
    lista_de_notas = maracuja_funcs.retorna_notas_projeto(sqlite3, project_id);
    return jsonify({"msg": "ok", "lista":lista_de_notas})

@app.route('/criar_projeto', methods=['GET'])
def criar_projeto():
    return render_template('criar_projeto.html')

@app.route('/cadastraProjeto', methods=['POST'])
def cadastraProjeto():
    print("images: ", request.files)

    titulo = request.form.get("titulo");
    sinopse = request.form.get("sinopse");

    titulo_ja_existe = maracuja_funcs.titulo_ja_existe(sqlite3, titulo);

    if (titulo_ja_existe):
        resposta = {"msg":"Erro. Já existe um projeto com esse título. Por favor, use outro título."};
        return jsonify(resposta)
    
    image = request.files.get("image");
    print("---> ", image);
    if (image == None):
        image_name = "CAPA_DO_PROJETO";
    else:
        image.filename = image.filename.replace(' ','_');
        filepath = os.path.join("localdata", image.filename)
        image.save(filepath)
        image_name = image.filename;

    id_do_projeto = maracuja_funcs.insere_titulo_sinopse(sqlite3, titulo, sinopse, image_name);

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

@app.route('/quilljs', methods=['GET'])
def quilljs():
    return send_file("quill.js", mimetype='application/javascript')

@app.route('/quillcss', methods=['GET'])
def quillcss():
    return send_file("quill.css", mimetype='text/css')

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

@app.route('/deleta_versao', methods=['POST'])
def deleta_versao():
    data = request.get_json()

    project_id = data["project_id"]
    chapter_id = data["chapter_id"]
    version_id = data["version_id"]
    
    message = maracuja_funcs.excluir_versao(Path, sqlite3, project_id, chapter_id, version_id);

    return jsonify({"message": message})

@app.route('/deleta_capitulo', methods=['POST'])
def deleta_capitulo():
    data = request.get_json()

    project_id = data["project_id"]
    chapter_id = data["chapter_id"]
    
    message = maracuja_funcs.excluir_capitulo(Path, sqlite3, project_id, chapter_id);

    return jsonify({"message": message})

@app.route('/deleta_nota', methods=['POST'])
def deleta_nota():
    data = request.get_json()

    project_id = data["project_id"]
    nota_id = data["nota_id"]
    
    message = maracuja_funcs.excluir_nota(Path, sqlite3, project_id, nota_id);

    return jsonify({"msg": message})

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

@app.route('/canonizar_capitulo', methods=['POST'])
def canonizar_capitulo():
    data = request.get_json()

    project_id = data["project_id"]
    chapter_id = data["chapter_id"]
    version_id = data["version_id"]

    maracuja_funcs.canonizar_versao_capitulo(sqlite3, project_id, chapter_id, version_id);

    return jsonify({"message": "ok"});

if __name__ == '__main__':
    print(argv)

    try:
        print(1);
    
        #file = open(".\\version", "r")
        #version = file.read();
        #file.close()
        file_path = Path(".") / "version"
        with file_path.open("r", encoding="utf-8") as file:
            data = file.read()

        if (len(argv) > 1):
            if (argv[1] == "-v" or argv[1] == "--version" or argv[1] == "-version"):
                print(version);
            
            if (argv[1] == "--export"):
                print("Exportando arquivos");
                maracuja_funcs.exporta_arquivos(argv,tarfile)
                
                print("Arquivos exportados para o formato .tar.gz!");
            
            if (argv[1] == "--clean"):
                decisao = input(
                    "\nTem certeza de que deseja deletar todos os arquivos do projeto? "
                    "Digite 'y' para sim: "
                )

                if decisao.lower() == "y":
                    maracuja_funcs.clean(Path, shutil);
                else:
                    print("Deleção cancelada.")
            
            if (argv[1] == "--import"):
                if(len(argv) != 3):
                    print("Somente um arquivo por vez. Revise o número de entradas");
                    exit();
                print("Importando dados do arquivo especificado")

                maracuja_funcs.importa_arquivos(argv,tarfile, argv[2],Path, shutil);

                print("Arquivos importados com sucesso!")

            exit();

        # tirando para teste
        maracuja_funcs.DB_start(sqlite3,requests_lib);
        app.run(debug=True);
    
    except Exception as e:
        print(e);