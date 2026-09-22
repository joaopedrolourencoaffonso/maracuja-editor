def verifica_array_tuples(vetor,elemento):
    for x in vetor:
        if (x == elemento):
            return True;
    return False;

def DB_start(sqlite3, requests_lib):
    print("Updating DB")
    conn = sqlite3.connect('userdata');
    cursor = conn.cursor();

    tabelas = cursor.execute("""
    SELECT name FROM sqlite_schema 
    WHERE type='table' AND name NOT LIKE 'sqlite_%';
    """).fetchall();

    teste_tudoBem = verifica_array_tuples(tabelas,('tudoBem',));
    print(teste_tudoBem);

    if (not teste_tudoBem):
        # cria DB
        cursor.execute('CREATE TABLE tudoBem (tudoBem INTEGER)');
        cursor.execute('CREATE TABLE titulos (PROJECT_ID INTEGER, name TEXT)');
        cursor.execute('CREATE TABLE sinopses (PROJECT_ID INTEGER, sinopse TEXT)');
        cursor.execute('CREATE TABLE capas (PROJECT_ID INTEGER, imagem_capa TEXT)');
        cursor.execute('CREATE TABLE capitulos (PROJECT_ID INTEGER, CHAPTER_ID INTEGER, CHAPTER_TITLE TEXT, VERSION_ID INTEGER, VERSION_NAME TEXT, IS_CANON INTEGER, POSICAO INTEGER)');
        #cursor.execute('CREATE TABLE versoesDeCapitulos (PROJECT_ID INTEGER, CHAPTER_ID INTEGER, VERSION_ID INTEGER, VERSION_NAME TEXT)');
        cursor.execute('CREATE TABLE projetosRecentes (PROJECT_ID INTEGER, LAST_OPEN INTEGER)');
        cursor.execute('CREATE TABLE notasDeProjetos (PROJECT_ID INTEGER, NOTA_ID INTEGER, TITULO TEXT, DESCRICAO TEXT)');
        # INSERIR TABELA PARA CAPÍTULOS: PROJECT_ID, CHAPTER_ID, CHAPTER_TITLE
        conn.commit();
    
    conn.close();

    js_file_url = "https://cdn.jsdelivr.net/npm/quill@2/dist/quill.js";
    requests_lib.urlretrieve(js_file_url, "quill.js");

    css_file_url = "https://cdn.jsdelivr.net/npm/quill@2/dist/quill.snow.css";
    requests_lib.urlretrieve(css_file_url, "quill.css");

    return True;

def retorna_novo_chapter_id(sqlite3, project_id, chapter_id):
    conn = sqlite3.connect('userdata');
    cursor = conn.cursor();
    id = cursor.execute('SELECT MAX(chapter_id) FROM capitulos WHERE PROJECT_ID = ? AND IS_CANON = 1;', (project_id,)).fetchall();
    posicao = cursor.execute('SELECT MAX(posicao) FROM capitulos WHERE PROJECT_ID = ? AND IS_CANON = 1;', (project_id,)).fetchall();
    if (id == [(None,)]):
        id = 0;
    else:
        id = id[0][0];
    
    if (posicao == [(None,)]):
        posicao = 0;
    else:
        posicao = posicao[0][0];

    id = id + 1;
    id = str(id);

    posicao = posicao + 1;
    posicao = str(posicao);

    # (PROJECT_ID INTEGER, CHAPTER_ID INTEGER, CHAPTER_TITLE TEXT, VERSION_ID INTEGER, VERSION_NAME TEXT, IS_CANON INTEGER)
    cursor.execute('INSERT INTO capitulos VALUES (?, ?, ?, ?, ?, ?, ?)', (project_id, id, "Capítulo " + id, 1, "v1", 1,posicao));
    
    conn.commit();
    conn.close();

    return id;

def retorna_titulo_capitulo(sqlite3, project_id, chapter_id, version_id):
    conn = sqlite3.connect('userdata');
    cursor = conn.cursor();

    titulo = cursor.execute('select CHAPTER_TITLE from capitulos where PROJECT_ID = ? AND CHAPTER_ID = ? AND VERSION_ID = ?;', (project_id, chapter_id, version_id)).fetchall();
    titulo = titulo[0][0]

    conn.close();

    return titulo;

def retorna_titulo_versao(sqlite3, project_id, chapter_id, version_id):
    conn = sqlite3.connect('userdata');
    cursor = conn.cursor();

    titulo = cursor.execute('select VERSION_NAME from capitulos where PROJECT_ID = ? AND CHAPTER_ID = ? AND VERSION_ID = ?;', (project_id, chapter_id, version_id)).fetchall();
    titulo = titulo[0][0]

    conn.close();

    return titulo;

def retorna_notas_projeto(sqlite3, project_id):
    conn = sqlite3.connect('userdata');
    cursor = conn.cursor();

    lista_de_notas = cursor.execute('select NOTA_ID, TITULO, DESCRICAO from notasDeProjetos where PROJECT_ID = ?;', (project_id,)).fetchall();

    conn.close();

    print(lista_de_notas)

    return lista_de_notas;

def retorna_nota_especifica(sqlite3, project_id, nota_id):
    conn = sqlite3.connect('userdata');
    cursor = conn.cursor();

    nota = cursor.execute('select TITULO, DESCRICAO from notasDeProjetos where PROJECT_ID = ? AND NOTA_ID = ?;', (project_id,nota_id)).fetchall();

    conn.close();

    print(nota)

    return nota;

def insere_notas_projeto(sqlite3, project_id, titulo, descricao):
    conn = sqlite3.connect('userdata');
    cursor = conn.cursor();

    nota_id = cursor.execute('select max(NOTA_ID) from notasDeProjetos where PROJECT_ID = ?;', (project_id,)).fetchall();
    nota_id = nota_id[0][0];

    if (nota_id == None):
        nota_id = 0
    
    nota_id += 1;

    cursor.execute('insert into notasDeProjetos values (?,?,?,?);', (project_id, nota_id, titulo, descricao));

    conn.commit();
    conn.close();
    
    return nota_id;

def atualiza_nota_projeto(sqlite3, project_id, nota_id, titulo_da_nota, descricao_da_nota):
    conn = sqlite3.connect('userdata');
    cursor = conn.cursor();

    print("2 -> ", titulo_da_nota)

    # cursor.execute('CREATE TABLE notasDeProjetos (PROJECT_ID INTEGER, NOTA_ID INTEGER, TITULO TEXT, DESCRICAO TEXT)');
    cursor.execute('UPDATE notasDeProjetos set TITULO = ?, DESCRICAO = ? WHERE PROJECT_ID = ? AND NOTA_ID = ?;',(titulo_da_nota, descricao_da_nota, project_id, nota_id));
    
    conn.commit();
    conn.close();

def atualiza_titulo_capitulo(sqlite3, project_id, chapter_id, version_id, new_name):
    conn = sqlite3.connect('userdata');
    cursor = conn.cursor();

    cursor.execute('UPDATE capitulos set CHAPTER_TITLE = ? WHERE PROJECT_ID = ? AND CHAPTER_ID = ? AND VERSION_ID = ?',(new_name, project_id, chapter_id, version_id));
    
    conn.commit();
    conn.close();

def pega_capitulos(sqlite3, project_id):
    conn = sqlite3.connect('userdata');
    cursor = conn.cursor();

    capitulos = cursor.execute('select POSICAO, CHAPTER_ID, CHAPTER_TITLE, VERSION_ID from capitulos where IS_CANON = 1 AND PROJECT_ID = ? ORDER BY POSICAO ASC',(project_id,)).fetchall();
    
    conn.commit();
    conn.close();

    return capitulos;

def todos_projetos(sqlite3):
    conn = sqlite3.connect('userdata');
    cursor = conn.cursor();

    projetos = cursor.execute('select titulos.project_id, titulos.name, capas.imagem_capa from titulos INNER JOIN capas ON titulos.project_id=capas.project_id;').fetchall();
    rows = {};
    for projeto in projetos:
        n_capitulos = cursor.execute('select count(chapter_id) from capitulos where project_id = ?;',(projeto[0],)).fetchall();
        rows.update({f"{projeto[0]}": {"titulo": f"{projeto[1]}","src": f"{projeto[2]}","ncapitulos": f"{n_capitulos[0][0]}"}})
    
    conn.commit();
    conn.close();

    return rows;

def insere_titulo_sinopse(sqlite3, titulo, sinopse,filename):
    conn = sqlite3.connect('userdata');
    cursor = conn.cursor();
    id = cursor.execute('SELECT MAX(PROJECT_ID) FROM titulos;').fetchall();
    if (id == [(None,)]):
        id = 0;
    else:
        id = id[0][0];
    id = id + 1;
    id = str(id);
    
    cursor.execute('INSERT INTO titulos VALUES (' + id + ', "' + titulo + '")');
    cursor.execute('INSERT INTO sinopses VALUES (' + id + ', "' + sinopse + '")');
    cursor.execute('INSERT INTO capas VALUES (' + id + ', "' + filename + '")');
    conn.commit();
    conn.close();

    return id;

def atualiza_titulo_sinopse(sqlite3, project_id, titulo, sinopse,filename):
    conn = sqlite3.connect('userdata');
    cursor = conn.cursor();
    project_id = str(project_id);
    
    cursor.execute('UPDATE titulos set name = "' + titulo + '" where PROJECT_ID = ' + project_id + ';');
    cursor.execute('UPDATE sinopses set sinopse = "' + sinopse + '" where PROJECT_ID = ' + project_id + ';');
    
    if (filename != 'qiwuqiwuqoeuwhewh,djhbfejhv'):
        cursor.execute('UPDATE capas set imagem_capa = "' + filename + '" where PROJECT_ID = ' + project_id + ';');
    
    conn.commit();
    conn.close();

    return id;

def pega_titulo_por_id(sqlite3, id):
    conn = sqlite3.connect('userdata');
    cursor = conn.cursor();
    titulo = cursor.execute('SELECT name FROM titulos where PROJECT_ID = ?;', (str(id),)).fetchall()
    titulo = titulo[0][0];
    conn.close();
    return titulo

def pega_sinopse_por_id(sqlite3, id):
    conn = sqlite3.connect('userdata');
    cursor = conn.cursor();
    sinopse = cursor.execute('SELECT sinopse FROM sinopses where PROJECT_ID =' +  str(id) + ';').fetchall()
    sinopse = sinopse[0][0];
    conn.close();
    return sinopse

def titulo_ja_existe(sqlite3, titulo):
    conn = sqlite3.connect('userdata');
    cursor = conn.cursor();
    print("------> ", titulo);
    numero = cursor.execute('SELECT count() FROM titulos where name = ?;', (str(titulo),)).fetchall()
    conn.close();
    if (numero[0][0] > 0):
        return True;
    else:
        return False;

def pega_capa_por_id(sqlite3, id):
    conn = sqlite3.connect('userdata');
    cursor = conn.cursor();
    capas = cursor.execute('SELECT imagem_capa FROM capas where PROJECT_ID =' +  str(id) + ';').fetchall()
    capa = capas[0][0]
    return capa;

def atualiza_projeto_mais_recente(sqlite3, time, id):
    conn = sqlite3.connect('userdata');
    cursor = conn.cursor();

    nova_hora = int(time());

    cursor.execute('UPDATE projetosRecentes set LAST_OPEN = ? WHERE PROJECT_ID = ?;',(nova_hora, id));
    
    conn.commit();
    conn.close();

def insere_projeto_mais_recente(sqlite3, time, id):
    conn = sqlite3.connect('userdata');
    cursor = conn.cursor();

    nova_hora = int(time());

    cursor.execute('insert into projetosRecentes values (?, ?);',(id, nova_hora));
    
    conn.commit();
    conn.close();

def retorna_projetos_recentes(sqlite3):
    conn = sqlite3.connect('userdata');
    cursor = conn.cursor();

    order_desc = cursor.execute('select project_id from projetosRecentes order by last_open desc limit 10;').fetchall()

    conn.commit();
    conn.close();

    return order_desc;

def excluir_versao(Path, sqlite3, project_id, chapter_id, version_id):
    conn = sqlite3.connect('userdata');
    cursor = conn.cursor();

    is_canon = cursor.execute("select is_canon from capitulos where project_id = ? AND chapter_id = ? AND version_id = ?;",(project_id, chapter_id, version_id)).fetchall();
    if is_canon[0][0] == 1:
        retorno = "Não pode excluir versão canon. Canonize outra versão antes de deletar este";
    else:
        retorno = "ok";
        cursor.execute("delete from capitulos where project_id = ? AND chapter_id = ? AND version_id = ?;",(project_id, chapter_id, version_id));
        
        file_path = Path("capitulos") / f"{project_id}-{chapter_id}-{version_id}.json";
        file_path.unlink(missing_ok=True)

    conn.commit();
    conn.close();

    return retorno;

def excluir_capitulo(Path, sqlite3, project_id, chapter_id):
    conn = sqlite3.connect('userdata');
    cursor = conn.cursor();

    mover_capitulo(sqlite3, project_id, chapter_id, 888888);

    cursor.execute("delete from capitulos where project_id = ? AND posicao = 888888;",(project_id,));
    
    conn.commit();
    conn.close();
    
    folder = Path("capitulos")
    pattern = f"{project_id}-{chapter_id}-*.json"

    for file_path in folder.glob(pattern):
        file_path.unlink(missing_ok=True)

    return "ok";

def excluir_nota(Path, sqlite3, project_id, nota_id):
    conn = sqlite3.connect('userdata');
    cursor = conn.cursor();

    cursor.execute("delete from notasDeProjetos where project_id = ? AND nota_id = ?;",(project_id,nota_id));
    
    conn.commit();
    conn.close();
    
    file_path = Path("notas") / f"nota-{project_id}-{nota_id}.json";
    file_path.unlink(missing_ok=True)

    return "ok";

def excluir_projeto(os, Path, sqlite3, project_id):
    conn = sqlite3.connect('userdata');
    cursor = conn.cursor();

    cursor.execute("delete from titulos where project_id = ?;",(project_id,));
    cursor.execute("delete from sinopses where project_id = ?;",(project_id,));
    cursor.execute("delete from capitulos where project_id = ?;",(project_id,));
    # AINDA NÃO IMPLEMENTADO
    #cursor.execute("delete from versoesCapitulos where project_id = ?;",(project_id,));
    cursor.execute("delete from projetosRecentes where project_id = ?;",(project_id,));

    capa = cursor.execute("select imagem_capa from capas where project_id = ?", (project_id,)).fetchall();

    capa = capa[0][0];

    file_path = Path("localdata") / capa;
    file_path.unlink(missing_ok=True);

    cursor.execute("delete from capas where project_id = ?;",(project_id,));

    conn.commit();
    conn.close();

    for f in Path("capitulos").glob(str(project_id) + "*.json"):
        f.unlink()

def mover_capitulo(sqlite3, project_id, capituloASerMovido, novaPosicaoDoCapitulo):
    try:
        capituloASerMovido = int(capituloASerMovido)
        novaPosicaoDoCapitulo = int(novaPosicaoDoCapitulo)
    except (TypeError, ValueError):
        raise ValueError("A posição dos capítulos devem ser inteiros")

    if capituloASerMovido == novaPosicaoDoCapitulo:
        return

    conn = sqlite3.connect('userdata');
    cursor = conn.cursor();

    cursor.execute("UPDATE capitulos set posicao = 7777777777 where project_id = ? AND posicao = ?;",(project_id, capituloASerMovido));
    
    if (capituloASerMovido < novaPosicaoDoCapitulo):
        cursor.execute("UPDATE capitulos set posicao = posicao - 1 where project_id = ? AND posicao <= ? AND posicao > ?;",(project_id, novaPosicaoDoCapitulo, capituloASerMovido));
    else:
        cursor.execute("UPDATE capitulos set posicao = posicao + 1 where project_id = ? AND posicao >= ? AND posicao < ?;",(project_id, novaPosicaoDoCapitulo, capituloASerMovido));    
    
    cursor.execute("UPDATE capitulos set posicao = ? where project_id = ? AND posicao = 7777777777;",(novaPosicaoDoCapitulo, project_id));
    
    conn.commit();
    conn.close();

def registra_nova_versao(sqlite3, project_id, chapter_id, chapter_title, nome_nova_versao):
    conn = sqlite3.connect('userdata');
    cursor = conn.cursor();

    novo_id = cursor.execute('SELECT MAX(VERSION_ID) FROM capitulos WHERE PROJECT_ID = ? AND CHAPTER_ID = ?;',(project_id, chapter_id)).fetchall();
    novo_id = novo_id[0][0] + 1;

    posicao = cursor.execute('SELECT posicao FROM capitulos WHERE PROJECT_ID = ? AND CHAPTER_ID = ?;',(project_id, chapter_id)).fetchall();
    posicao = posicao[0][0];

    # PROJECT_ID INTEGER, CHAPTER_ID INTEGER, CHAPTER_TITLE TEXT, VERSION_ID INTEGER, VERSION_NAME TEXT, IS_CANON INTEGER
    cursor.execute('INSERT INTO capitulos VALUES (?, ?, ?, ?, ?, ?,?)', (project_id, chapter_id, chapter_title, novo_id, nome_nova_versao, 0,posicao));
    
    conn.commit();
    conn.close();

    return novo_id;

def pega_versoes_capitulo(sqlite3, project_id, chapter_id):
    conn = sqlite3.connect('userdata');
    cursor = conn.cursor();

    lista = cursor.execute("select version_id, version_name from capitulos where project_id = ? AND chapter_id = ?;",(project_id, chapter_id)).fetchall();

    conn.commit();
    conn.close();

    return lista;

def canonizar_versao_capitulo(sqlite3, project_id, chapter_id, version_id):
    conn = sqlite3.connect('userdata');
    cursor = conn.cursor();

    cursor.execute("UPDATE capitulos set is_canon = 0 where project_id = ? and chapter_id = ? and version_id != ?;",(project_id, chapter_id, version_id));
    cursor.execute("UPDATE capitulos set is_canon = 1 where project_id = ? and chapter_id = ?  and version_id = ?;",(project_id, chapter_id, version_id));

    conn.commit();
    conn.close();

def exporta_arquivos(argv, tarfile):
    if len(argv) > 2:
        print("aqui")
        print("-> ", argv)
        nome_do_projeto = argv[2]
    else:
        nome_do_projeto = "meusProjetosExport.tar.gz"

    with tarfile.open(nome_do_projeto, "w:gz") as archive:
        # Pass string paths without backslashes ('\\') or use Path objects.
        # tarfile accepts both, but standard forward slashes / Path objects ensure OS neutrality.
        archive.add("capitulos", arcname="capitulos")
        archive.add("localdata", arcname="localdata")
        archive.add("notas", arcname="notas")
        archive.add("userdata", arcname="userdata")


def clean(Path, shutil):
    for folder_name in ("localdata", "capitulos","notas"):
        folder = Path(folder_name)
        
        # Prevent FileNotFoundError on Linux/Windows if the directory doesn't exist yet
        if not folder.exists():
            continue

        for item in folder.iterdir():
            if item.is_dir():
                shutil.rmtree(item, ignore_errors=True)
            else:
                item.unlink(missing_ok=True)

    userdata = Path("userdata")
    if userdata.exists():
        if userdata.is_dir():
            shutil.rmtree(userdata, ignore_errors=True)
        else:
            userdata.unlink(missing_ok=True)

    print("Arquivos deletados.")

def importa_arquivos(argv,tarfile, filepath,Path, shutil):
    clean(Path, shutil);

    temp_dir = Path("temp_folder");

    with tarfile.open(filepath, "r:gz") as tar:
        tar.extractall(path=temp_dir)
    
    # 2. Use pathlib with ignore_errors=True for safe directory removal
    shutil.rmtree(Path("localdata"), ignore_errors=True)
    shutil.rmtree(Path("capitulos"), ignore_errors=True)
    shutil.rmtree(Path("notas"), ignore_errors=True)
    
    # 3. Move folders using Path objects
    shutil.move(temp_dir / "localdata", Path("."))
    shutil.move(temp_dir / "capitulos", Path("."))
    shutil.move(temp_dir / "notas", Path("."))
    
    # Note: shutil.move behavior varies if destination exists; 
    # ensure target is clear before moving directory trees.
    userdata_dst = Path("userdata")
    if userdata_dst.exists():
        shutil.rmtree(userdata_dst)
    shutil.move(temp_dir / "userdata", userdata_dst)
    
    # 4. Clean up temporary directory
    shutil.rmtree(temp_dir, ignore_errors=True)

def quill_to_md(json, path_do_arquivo):
    string_final = "";
    with path_do_arquivo.open("r", encoding="utf-8") as file:
        rawChapterData = file.read()

    jsonData = json.loads(rawChapterData);
    lista = jsonData["ops"]
    tamanho_lista = len(lista);

    i = 0;
    while i < tamanho_lista:
        if (i + 1 >= tamanho_lista):
            string_final = string_final + lista[i]["insert"];
            break
        
        if 'header' in lista[i+1]['attributes']:
            if (lista[i+1]['attributes']['header'] == 1):
                hashes = "# ";
            
            if (lista[i+1]['attributes']['header'] == 2):
                hashes = "## ";
            
            if (lista[i+1]['attributes']['header'] == 3):
                hashes = "### ";

            string_final = string_final + hashes + lista[i]["insert"] + lista[i+1]["insert"];
        
        if 'list' in lista[i+1]['attributes']:
            # lista de elementos entre \n
            temp = lista[i]["insert"].split("\n");

            if (len(temp) > 1):
                item_da_lista = temp[len(temp) - 1];
                temp.pop();
                intermediario = "\n".join(temp);
                intermediario += "\n";
            else:
                intermediario = ""

            if (lista[i+1]['attributes']["list"] == "ordered"):
                marcador = "1. "
            
            if (lista[i+1]['attributes']["list"] == "bullet"):
                marcador = "- "
            
            string_final = string_final + intermediario + marcador + item_da_lista + lista[i+1]["insert"];

        if 'bold' in lista[i+1]['attributes']:
            string_final = string_final + lista[i]["insert"] + "**"  + lista[i+1]["insert"] + "**";
        
        if 'italic' in lista[i+1]['attributes']:
            string_final = string_final + lista[i]["insert"] + "*"  + lista[i+1]["insert"] + "*";
        
        if 'underline' in lista[i+1]['attributes']:
            string_final = string_final + lista[i]["insert"] + "<ins>"  + lista[i+1]["insert"] + "</ins>";
        
        if 'link' in lista[i+1]['attributes']:
            string_final = string_final + lista[i]["insert"] + f"<a href='${lista[i+1]['attributes']['link']}'>"  + lista[i+1]["insert"] + "</a>";
        
        #print(i, i+1);
        i += 2;

    string_final = string_final.replace("\n", "\n\n");
    
    #with path_arquivo_saida.open("w", encoding="utf-8") as file:
    #    file.write(string_final)

    #print(jsonData);

    return string_final

def exporta_para_md_multiplos(sqlite3, tempfile, Path, json, tarfile, project_id, titulo):
    # 1. Fetch chapter metadata from SQLite
    conn = sqlite3.connect('userdata')
    cursor = conn.cursor()
    
    # Fix: SQL parameter must be a single-element tuple (project_id,)
    lista_capitulos = cursor.execute(
        "select project_id, chapter_id, version_id, chapter_title, posicao from capitulos where IS_CANON = 1 AND PROJECT_ID = ? ORDER BY POSICAO", 
        (project_id,)
    ).fetchall()
    
    conn.close()

    # 2. Prepare export_temp directory (create if missing, clean out existing files)
    export_dir = Path("export_temp")
    export_dir.mkdir(parents=True, exist_ok=True)

    for file_item in export_dir.iterdir():
        if file_item.is_file():
            file_item.unlink()

    # 3. Generate Markdown files and write them to export_temp
    for capitulo in lista_capitulos:
        capitulo_path = Path("capitulos") / f"{capitulo[0]}-{capitulo[1]}-{capitulo[2]}.json"
        markdown_text = quill_to_md(json, capitulo_path);
        markdown_text = "# " + capitulo[3] + "\n" + markdown_text;

        md_file_path = export_dir / f"{capitulo[4]}.md"
        with open(md_file_path, "w", encoding="utf-8") as file:
            file.write(markdown_text)

    # 4. Ensure filename ends with .tar.gz and create the archive after all files are generated
    archive_filename = titulo if titulo.endswith(".tar.gz") else f"{titulo}.tar.gz"

    with tarfile.open(archive_filename, "w:gz") as archive:
        archive.add(export_dir, arcname="capitulos")

    return archive_filename

def exporta_para_md_unico(sqlite3, Path, json, tarfile, project_id, titulo):
    conn = sqlite3.connect('userdata')
    cursor = conn.cursor()
    
    lista_capitulos = cursor.execute(
        "SELECT project_id, chapter_id, version_id, chapter_title FROM capitulos WHERE IS_CANON = 1 AND PROJECT_ID = ? ORDER BY POSICAO", 
        (project_id,)
    ).fetchall()
    conn.close()

    markdown_text = ""

    for capitulo in lista_capitulos:
        capitulo_path = Path("capitulos") / f"{capitulo[0]}-{capitulo[1]}-{capitulo[2]}.json"
        temp_text = quill_to_md(json, capitulo_path);
        markdown_text = markdown_text + "\n\n# " + capitulo[3] + "\n\n" + temp_text;

    md_file_path = f"{titulo}.md"
    with open(md_file_path, "w", encoding="utf-8") as file:
        file.write(markdown_text)

    return md_file_path

def quill_to_html(json, path_do_arquivo):
    string_final = ""

    with path_do_arquivo.open("r", encoding="utf-8") as file:
        rawChapterData = file.read()

    jsonData = json.loads(rawChapterData)
    lista = jsonData["ops"]
    tamanho_lista = len(lista)

    i = 0

    while i < tamanho_lista:

        # Caso seja o último elemento
        if i + 1 >= tamanho_lista:
            string_final += lista[i]["insert"]
            break

        texto = lista[i]["insert"]
        proximo = lista[i + 1]

        atributos = proximo.get("attributes", {})

        # HEADER
        if "header" in atributos:
            if atributos["header"] == 1:
                primeiro_elemento = "<h1>"
                segundo_elemento = "</h1>"

            elif atributos["header"] == 2:
                primeiro_elemento = "<h2>"
                segundo_elemento = "</h2>"

            elif atributos["header"] == 3:
                primeiro_elemento = "<h3>"
                segundo_elemento = "</h3>"

            else:
                primeiro_elemento = ""
                segundo_elemento = ""

            string_final += (
                primeiro_elemento
                + texto
                + segundo_elemento
                + proximo["insert"]
            )

        # LISTA
        elif "list" in atributos:
            tipo_lista = atributos["list"]

            # Texto antes da última quebra de linha
            temp = texto.split("\n")

            if len(temp) > 1:
                item_da_lista = temp[-1]
                temp.pop()

                intermediario = "\n".join(temp)

                if intermediario:
                    string_final += intermediario + "\n"
            else:
                item_da_lista = texto

            if tipo_lista == "ordered":
                string_final += "<ol><li>" + item_da_lista + "</li></ol>"
            elif tipo_lista == "bullet":
                string_final += "<ul><li>" + item_da_lista + "</li></ul>"

            string_final += proximo["insert"]

        # BOLD
        elif "bold" in atributos:
            string_final += (
                texto
                + "<strong>"
                + proximo["insert"]
                + "</strong>"
            )

        # ITALIC
        elif "italic" in atributos:
            string_final += (
                texto
                + "<em>"
                + proximo["insert"]
                + "</em>"
            )

        # UNDERLINE
        elif "underline" in atributos:
            string_final += (
                texto
                + "<ins>"
                + proximo["insert"]
                + "</ins>"
            )

        # LINK
        elif "link" in atributos:
            link = atributos["link"]

            string_final += (
                texto
                + f"<a href='{link}'>"
                + proximo["insert"]
                + "</a>"
            )

        # Nenhum atributo
        else:
            string_final += texto + proximo["insert"]

        i += 2

    # Quebras de linha do Quill para HTML
    string_final = string_final.replace("\n", "<br>\n")

    return string_final

def exporta_para_html_multiplos(sqlite3, tempfile, Path, json, tarfile, project_id, titulo):
    # 1. Fetch chapter metadata from SQLite
    conn = sqlite3.connect('userdata')
    cursor = conn.cursor()
    
    # Fix: SQL parameter must be a single-element tuple (project_id,)
    lista_capitulos = cursor.execute(
        "select project_id, chapter_id, version_id, chapter_title, posicao from capitulos where IS_CANON = 1 AND PROJECT_ID = ? ORDER BY POSICAO", 
        (project_id,)
    ).fetchall()
    
    conn.close()

    # 2. Prepare export_temp directory (create if missing, clean out existing files)
    export_dir = Path("export_temp")
    export_dir.mkdir(parents=True, exist_ok=True)

    for file_item in export_dir.iterdir():
        if file_item.is_file():
            file_item.unlink()

    # 3. Generate Markdown files and write them to export_temp
    for capitulo in lista_capitulos:
        capitulo_path = Path("capitulos") / f"{capitulo[0]}-{capitulo[1]}-{capitulo[2]}.json"
        html_text = quill_to_html(json, capitulo_path);
        html_text = "<h1>" + capitulo[3] + "</h1>" + html_text;

        md_file_path = export_dir / f"{capitulo[4]}.html"
        with open(md_file_path, "w", encoding="utf-8") as file:
            file.write(html_text)

    # 4. Ensure filename ends with .tar.gz and create the archive after all files are generated
    archive_filename = titulo if titulo.endswith(".tar.gz") else f"{titulo}.tar.gz"

    with tarfile.open(archive_filename, "w:gz") as archive:
        archive.add(export_dir, arcname="capitulos")

    return archive_filename

def exporta_para_html_unico(sqlite3, Path, json, tarfile, project_id, titulo):
    conn = sqlite3.connect('userdata')
    cursor = conn.cursor()
    
    lista_capitulos = cursor.execute(
        "SELECT project_id, chapter_id, version_id, chapter_title FROM capitulos WHERE IS_CANON = 1 AND PROJECT_ID = ? ORDER BY POSICAO", 
        (project_id,)
    ).fetchall()
    conn.close()

    html_text = ""

    for capitulo in lista_capitulos:
        capitulo_path = Path("capitulos") / f"{capitulo[0]}-{capitulo[1]}-{capitulo[2]}.json"
        temp_text = quill_to_html(json, capitulo_path);
        html_text = html_text + "<h2>" + capitulo[3] + "</h2>" + temp_text;

    md_file_path = f"{titulo}.html"
    with open(md_file_path, "w", encoding="utf-8") as file:
        file.write(html_text)

    return md_file_path