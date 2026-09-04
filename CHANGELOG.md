# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## 0.1 - 19-08-2026

### Added

- Ainda não funciona mas é uma fundação.
- UIs básicas definidas
- Base para começar a construir DB
- Construção da DB necessária para seguir para trabalho com os capítulos

## 0.2 - 20-08-2026

### Added

- Começando a trabalhar com DB: verifica e cria tabelas básicas e insere informação de projeto.
- Salva e serve imagens de capa do usuário
- Introduz [`maracuja_funcs`](./maracuja_funcs.py).

## 0.0.1 - 24-08-2026

### Added

- Começando a usar info da DB na página de projeto

## 0.0.2 - 25-08-2026

### Added

- Página de projetos carrega informação do banco de dados e atualiza informações no banco de dados.

## 0.0.3 - 26-08-2026

### Added

- Usando API do quill para salvar o texto em arquivo
- Usando API do quill para expôr texto dos arquivos para o usuário.

## 0.0.4 - 26-08-2026

### Added

- Adicionando título aos capítulos
- Adicionando variável `version_id` para rastrear versão do capítulo. Será usada em maior profundidade no futuro.

## 0.0.5 - 27-08-2026

### Added

- Adicionando API para listar todos os projetos

## 0.0.6 - 31-08-2026

### Added

- Adicionando API para listar projetos recentemente editados.

## 0.0.7 - 31-08-2026

### Added

- Adicionando API e botão para remover capítulos. Botão no próprio capítulo.
- Adicionando API e botão para remoção de projetos. Botão na própria página do projeto. 

## 0.1.0 - 02-09-2026

### Added

- Adicionei ids dos capítulos ao lado dos seus títulos na listagem.
- Adicionei funcionalidade para mover capítulos de posição (não é elegante, mas funciona). 

## 0.1.1 - 03-09-2026

### Added

- Esquema de banco de dados refatorado para suportar o versionamento (percebi retroativamente uma forma melhor de fazer).
- Provavelmente ainda serão necessárias outras mudanças, mas é um começo.
