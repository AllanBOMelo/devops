# Projeto Devops

## Build

Para a criação das imagens da API e do banco de dados, execute o comando:

```sh
docker-compose build
```

Ou

```sh
docker-compose up --build
```

## Rodar o Container

Para criação e execução do container, execute:

```sh
docker-compose up
```

## API

A API referente, se trata de um CRUD simples para criação de usuarios através das seguintes rotas:

- `GET /status/` - Retorna Status da API
- `GET /users/` - Listar usuarios.
- `POST /users/"` - Cadastrar usuario.
- `GET /users/{user_id}` - Retorna usuario pelo ID.
- `PUT /users/{user_id}` - Atualiza usuario pelo ID.
- `DELETE /users/{user_id}"` - Deleta um usuario pelo ID.
  a
