# maracuja-editor

Um editor de texto amigável ao usuário construído sobre o git para facilitar gerenciamento de textos longos.

Powered by [quilljs](https://github.com/slab/quill/).

# O que é canonização?

Do inglês, "canon", geralmente usado para simbolizar aspectos imutáveis de uma certa história (a morte do tio Ben do homem aranha, por exemplo).

A ideia é que quando um capítulo é "canonizado", ele é marcado como a versão 'oficial' ou no mínimo 'atual' do capítulo em questão, sendo o capítulo exposto por padrão quando se acessa o link pela página do projeto, assim como o capítulo que será adicionado ao texto em caso de exportação do projeto para html, pdf e/ou epub.

# Objetivos

- v0.1.0 Editor de Texto Mínimo

- [X] Escolher framework de edição de texto em browser
- [X] UI da página de edição básica
- [X] UI para a página principal
- [X] UI básica para visualizar detalhes de projeto (capítulos inclusos)
- [X] UI básica para Listar Projetos
- [X] UI para Criar Projeto 
- [X] Salvando arquivo enviado pelo usuário
- [X] UI para Criar Projeto (começando com o Sqlite)
- [X] Adaptar UI's anteriores para usar o SQLite
- [X] API para retornar imagens de capas
- [X] API para receber imagens de projetos
- [X] Adicionar título aos capítulos
- [X] Listar capítulos corretamente à listagem de capítulos do projeto
- [X] Adaptar página do projeto para exibir os verdadeiros capítulos
- [X] Adaptar página "todos os projetos" à exibir verdadeiros projetos cadastrados
- [X] Trabalhar em API para listar projetos recentes
- [X] Adicionar botões para excluir capítulos
- [X] Adicionar botões para excluir projetos
- [X] Adicionar botões para trocar capítulos de ordem

- v0.2.0 Editor com versionamento

- [X] Refatorar esquema de banco de dados para suportar o versionamento (percebi retroativamente)
- [X] Adicionar o `version_id=1` nos links do `/project_page` 
- [X] Editar endpoint `/editarCapitulo` para trabalhar com `version_id`
- [X] Permitir usuário cadastrar novas versões do capítulo
- [X] Expôr versões de arquivos na página do capítulo
- [X] Permitir usuário clicar e visualizar versões de capítulo
- [X] Permitir usuário redefinir versão principal (canonizar capítulo)
- [X] Função `excluir_capitulo` retorna erro se usuário tentar excluir um capítulo canon.
- [X] Expôr lista de capítulos na página de edição para permitir navegação mais fácil
- [X] Corrigir bug na página principal em que novos projetos não estão sendo expostos (bug era resultado do código permitir múltiplos projetos com o mesmo nome)
- [X] Aceitar projetos que não tem imagem de capa.
- [X] Implementar comparação de versões de capítulo lado a lado.
- [X] Na página de `editor` aglutinar as chamadas de dialog para deixar o código mais simples de ler
- [X] Corrigir bug da lista de versões que impede de acessar capítulo 1. (não tem mudança para detectar)
- [X] ~~Implementar árvore de mudanças~~(desnecessário, complicações demais para um aplicativo local)

- v0.3.0 Editor de Texto Avançado

- [X] Opção de apenas ler os capítulos
- [X] Adicionar "-v" na linha de comando
- [X] Adicionar opção de backup (CLI)
- [X] Corrigir bug de capítulo criar capítulo novo quando é salvo
- [X] Adicionar opção para limpar todos os dados do projeto (ajuda no teste e desenvolvimento) (CLI)
- [X] Transformar opções acima em funções para reciclar na UI
- [X] Adicionar opção de backup (UI)
- [X] Adicionar opção para limpar todos os dados do projeto (ajuda no teste e desenvolvimento) (UI)
- [X] Adicionar opção para importar dados a partir de tar.gz (CLI)
- [X] Adicionar opção para importar dados a partir de tar.gz (UI)
- [ ] Adequar para o linux (estou trabalhando no windows/sou preguiçoso)

- v0.4.0 Adaptando para Escritores

- [ ] Criando seção de notas da estória
- [ ] Criando seção de personagens
- [ ] Adicionando opção de adicionar notas aos documentos em si.

- v1.0.0 Editor de Texto Completo

- [ ] Refatorar UI para ficar mais amigável.
- [ ] Adicionar dark mode.
- [ ] Exportar projeto para `.md`
- [ ] Exportar projeto para html
- [ ] Exportar projeto para PDF (ver [pandoc](https://github.com/jgm/pandoc))
- [ ] Exportar projeto para epub (ver [pandoc](https://github.com/jgm/pandoc))
- [ ] Exportar para docx
- [ ] Criar logo
- [ ] Criar instalador (inclui baixar o quill.js localmente)
- [ ] Criar site para o projeto
- [ ] Criar tutoriais para usuários leigos

- v1.0.1 Melhorias

- [ ] Documentos únicos (editar sem associar a projetos)
- [ ] Contador de linhas
- [ ] Contador de palavras
- [ ] Exportar/Importar projetos seletivamente
- [ ] Tema darkmode (e outros)

