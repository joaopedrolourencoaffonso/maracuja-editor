# Usando o maracuja-editor

# 1. Iniciando a aplicação

1. Acesse o path do repositório

```bash
$ cd maracuja-editor
```

2. Use o comando para iniciar a aplicação:

```bash
$ python ./app.py
```

3. Acesse a página http://127.0.0.1:5000/ e você verá uma página similar ao abaixo:

![](./img/pagina-principal-nova-instalacao.png)

# 2. Criar um novo projeto

1. Na página principal: http://127.0.0.1:5000/, clique em "Criar novo Projeto":

![](./img/1-criar-novo-projeto.png)

2. Preencha os dados do projeto. Clique na imagem para realizar o upload de uma imagem de capa e preencha os campos de título e sinopse.

![](./img/2-preencha-dados-do-projeto.png)

3. Salve o projeto e clique em "OK" no alerta:

![](./img/3-novo-projeto.png)

4. Você será levado para a página do projeto, onde você pode atualizar detalhes, criar capítulos e notas do projeto:

![](./img/4-pagina-de-projeto.png)

# 3. Criar Capítulo

1. Na página do projeto, clique em "_criar capítulo_":

![](./img/5-criar-capitulo.png)

2. Você será levado a uma página similar a abaixo. Edite o arquivo conforme desejado e quando terminar, clique em "salvar capítulo":

![](./img/6-capitulo-em-branco.png)

3. Para voltar para a página inicial, clique no botão no canto superior direito. Para voltar para a página inicial do editor, clique no botão no canto superior esquerdo

![](./img/7-saindo-do-editor.png)

# 4. Mudando capítulos de posição

1. Antes de mover o capítulo, veja seu índice e o índice da posição desejada, conforme indicado pelos numeradores destacados na imagem abaixo:

![](./img/7-5-indice-do-capitulo.png)

2. Para mover um capítulo de posição, clique no botão "_Mover Capítulo_":

![](./img/8-mover-capitulos.png)

3. Digite o índice atual do capítulo e a posição desejada no menu. No exemplo abaixo, estamos movendo o capítulo 2 para a posição 4:

![](./img/9-digitando-posicoes-capitulo.png)

4. Clique em "OK":

![](./img/10-clique-em-ok.png)

5. Pronto, capítulo movido! Perceba que os capítulos com índice menor ou igual ao índice destino (nesse caso, capítulos 2 e 3) foram movidos para os índices abaixo, enquanto que o capítulo 5 foi mantido no índice 5.

![](./img/11-capitulos-movidos.png)

# 5. Versionando um capítulo

1. Clique no botão "Nova Versão":

![](./img/12-nova-versao.png)

2. Digite o nome da nova versão:

![](./img/13-nome-versao.png)

3. Clique em salvar e depois em 'OK' e você será levado diretamente para a página da nova versão:

![](./img/14-pagina-nova-versao.png)

4. Caso queira mudar de versão, basta clicar na lista:

![](./img/15-lista-de-versoes.png)

5. Caso goste da nova versão mais que a antiga, clique no botão "canonizar" para torná-la a nova versão canônica (isto é, a que será exposta por padrão ao acessar o capítulo e exportada):

![](./img/16-botao-canonizar.png)

6. Clique em salvar, depois em "OK" e pronto, a nova versão é a versão canônica.

![](./img/17-clique-salvar-canonizar.png)

# 6. Comparando versões

1. Para comparar duas versões do mesmo capítulo, basta clicar em comparar:

![](./img/18-comparar-versoes-capitulo.png)

2. Selecione as versões desejadas para a comparação e cliquem em "comparar":

![](./img/19-selecionando-versoes.png)

3. Você será levado a uma tela similar a esta. Compare, edite e salve as versões conforme lhe for interessante:

![](./img/20-comparando-versoes.png)

# 7. Deletando versão de capítulo

1. Deslize até o fim da página do capítulo e clique no botão de deletar. Perceba que apenas versões não canônicas podem ser deletadas

![](./img/22-botao-deletar-versao.png)

2. Confirme sua decisão e depois clique em "OK", você será levado de volta para a página principal do projeto:

![](./img/22-botao-deletar-versao.png)

# 8. Ler e Deletar Capítulo

1. Na página do projeto, selecione a opção desejada:

![](./img/23-ler-deletar-capitulos.png)

# 9. Notas do Projeto

1. Para acessar as notas do projeto, clique no botão "_Notas do Projeto_":

![](./img/24-botao-notas-projeto.png)

2. Você será levado para a página de notas do projeto. Para criar uma nota do projeto, clique no botão amarelo:

![](./img/25-pagina-notas-projeto.png)

3. Defina um título e uma descrição para a nota:

![](./img/26-titulo-e-descricao.png)

4. Na página de nota, você pode editar o título, descrição e conteúdo das notas

![](./img/27-pagina-de-nota.png)

5. Para deletar a nota, use o botão vermelho na base da página:

![](./img/28-deletar-nota.png)

# 10. Ver todos os projetos

1. Na página inicial, clique em "Ver todos os projetos":

![](./img/29-ver-todos-os-projetos.png)

2. A página com todos os projetos será exposta. Para acessar um projeto, basta clicar:

![](./img/30-todos-os-projetos.png)

# 11. Backup

1. Para realizar um backup, acesse as configurações, na página principal:

![](./img/30-todos-os-projetos.png)

2. Clique em gerar backup e o arquivo `.tar.gz` será disponibilizado no seu diretório de downloads:

![](./img/31-configuracoes.png)

# 12. Importar Backup

1. Importar um backup irá apagar todos os dados já salvos na instância do editor, então pense bem antes de fazê-lo.

2. Devido a um bug no código, o banco de dados trava se você tentar importar um backup após ter realizado operações (criar um novo projeto, editar um capítulo, etc). Por isso, pare sua instância e a reinicie em seguida:

![](./img/33-reiniciando-app.png)

3. Retorne à página de configurações e realize o upload:

![](./img/34-importando-backup.png)


# 13. Exportando projeto

1. Para exportar o projeto, clique no botão "_Exportar Projeto_", para acessar as opções disponíveis:

![](./img/35-exportar-projeto-botao.png)

2. Selecione a opção de exportação desejada. Note que para as opções com "múltiplos" será gerado um arquivo `.tar.gz` com arquivos indivíduais para cada capítulo. No exemplo abaixo, um PDF foi gerado:

![](./img/37-PDF-gerado.png)

3. O PDF terá uma aparência similar ao abaixo:

> OBS: no momento ainda não é possível customizar o PDF gerado, mas a feature deve estar disponível para a versão 3.0.0

![](./img/38-PDF-gerado.png)

