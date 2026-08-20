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
        # INSERIR TABELA PARA CAPÍTULOS: PROJECT_ID, CHAPTER_ID, CHAPTER_TITLE
        conn.commit();
    
    conn.close();
    return True;

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