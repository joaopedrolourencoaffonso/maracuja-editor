# maracuja-editor

Um editor de texto amigável ao usuário construído sobre o git para facilitar gerenciamento de textos longos.

Powered by [quilljs](https://github.com/slab/quill/).

- v0.1.0 Editor de Texto Mínimo

- [X] Excolher framework de edição de texto em browser
- [X] UI da página de edição básica
- [X] UI para a página principal
- [X] UI básica para visualizar detalhes de projeto (capítulos incluso)
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
- [ ] Adicionar o `version_id=1` nos links do `/project_page` 
- [ ] Editar endpoint `/editarCapitulo` para trabalhar com `version_id`
- [ ] Permitir usuário cadastrar novas versões do capítulo
- [ ] Expôr versões de arquivos na página do capítulo
- [ ] Permitir usuário clicar e visualizar versões de capítulo
- [ ] Permitir usuário redefinir versão principal (vai exigir rearranjar DB)
- [ ] Expôr lista de capítulos na página de edição para permitir navegação mais fácil
- [ ] Implementar comparação de versões de capítulo lado à lado.
- [ ] Implementar árvore de mundanças (?)

- v0.3.0 Editor de Texto Avançado

- [ ] Opção de apenas ler os capítulos
- [ ] Adicionar opção para limpar imagens que não estão sendo usadas como capas
- [ ] Adicionar opção para limpar todos os dados do projeto (ajuda no teste e desenvolvimento)
- [ ] Adicionar "-v" na linha de comando
- [ ] Adequar para o linux (estou trabalhando no windows/sou preguiçoso)

- v0.4.0 Adaptando para Escritores

- [ ] Criando seção de notas da estória
- [ ] Criando seção de personagens
- [ ] Adicionando opção de adicionar notas aos documentos em si.

- v1.0.0 Editor de Texto Completo

- [ ] Refatorar UI para ficar mais amigável.
- [ ] Exportar projeto para `.md`
- [ ] Exportar projeto para html
- [ ] Exportar projeto para PDF (ver [pandoc](https://github.com/jgm/pandoc))
- [ ] Exportar projeto para epub (ver [pandoc](https://github.com/jgm/pandoc))
- [ ] Criar logo

