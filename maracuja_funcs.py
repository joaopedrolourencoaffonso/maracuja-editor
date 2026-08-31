def verifica_array_tuples(vetor,elemento):
    for x in vetor:
        if (x == elemento):
            return True;
    return False;

def DB_start(sqlite3):
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
        cursor.execute('CREATE TABLE capitulos (PROJECT_ID INTEGER, CHAPTER_ID INTEGER, VERSION_ID INTEGER, CHAPTER_TITLE TEXT)');
        cursor.execute('CREATE TABLE versoesDeCapitulos (PROJECT_ID INTEGER, CHAPTER_ID INTEGER, VERSION_ID INTEGER, VERSION_NAME TEXT)');
        cursor.execute('CREATE TABLE projetosRecentes (PROJECT_ID INTEGER, LAST_OPEN INTEGER)');
        # INSERIR TABELA PARA CAPÍTULOS: PROJECT_ID, CHAPTER_ID, CHAPTER_TITLE
        conn.commit();
    
    conn.close();
    return True;

def retorna_novo_chapter_id(sqlite3, project_id, chapter_id, version_id):
    conn = sqlite3.connect('userdata');
    cursor = conn.cursor();
    id = cursor.execute('SELECT MAX(chapter_id) FROM capitulos WHERE PROJECT_ID ="' + project_id + '";').fetchall();
    if (id == [(None,)]):
        id = 0;
    else:
        id = id[0][0];
    id = id + 1;
    id = str(id);

    cursor.execute('INSERT INTO capitulos VALUES (?, ?, ?,?)', (project_id, id, version_id, "Capítulo " + id));
    
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

def atualiza_titulo_capitulo(sqlite3, project_id, chapter_id, version_id, new_name):
    conn = sqlite3.connect('userdata');
    cursor = conn.cursor();

    cursor.execute('UPDATE capitulos set CHAPTER_TITLE = ? WHERE PROJECT_ID = ? AND CHAPTER_ID = ? AND VERSION_ID = ?',(new_name, project_id, chapter_id, version_id));
    
    conn.commit();
    conn.close();

def pega_capitulos(sqlite3, project_id):
    conn = sqlite3.connect('userdata');
    cursor = conn.cursor();

    capitulos = cursor.execute('select CHAPTER_ID, CHAPTER_TITLE from capitulos where VERSION_ID = 1 AND PROJECT_ID = ? ORDER BY CHAPTER_ID ASC',(project_id,)).fetchall();
    
    conn.commit();
    conn.close();

    return capitulos;

def todos_projetos(sqlite3):
    conn = sqlite3.connect('userdata');
    cursor = conn.cursor();

    projetos = cursor.execute('select titulos.project_id, titulos.name, capas.imagem_capa from titulos INNER JOIN capas ON titulos.project_id=capas.project_id;').fetchall();
    #rows = [];
    rows = {};
    for projeto in projetos:
        n_capitulos = cursor.execute('select count(chapter_id) from capitulos where project_id = ?;',(projeto[0],)).fetchall();
        #rows.append([projeto[0], projeto[1], projeto[2], n_capitulos[0][0]]);
        rows.update({f"{projeto[0]}": {"titulo": f"{projeto[1]}","src": f"{projeto[2]}","ncapitulos": f"{n_capitulos[0][0]}","ntimelines":6}})
    
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
    titulo = cursor.execute('SELECT name FROM titulos where PROJECT_ID =' +  str(id) + ';').fetchall()
    titulo = titulo[0][0]
    return titulo

def pega_sinopse_por_id(sqlite3, id):
    conn = sqlite3.connect('userdata');
    cursor = conn.cursor();
    sinopse = cursor.execute('SELECT sinopse FROM sinopses where PROJECT_ID =' +  str(id) + ';').fetchall()
    sinopse = sinopse[0][0]
    return sinopse

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
