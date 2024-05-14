# E-commerce

E-commerce capacitação

## Referências da API

### Login usuário

```http
  POST /api/usuarios/login
```

- Loga o usuário

### Logout usuário

```http
  POST /api/usuarios/logout
```

- Desloga o usuário

### Busca todos os usuários

```http
  GET /api/usuarios
```

- É necessário que usuário esteja logado e seja um administrador

### Criar usuário

```http
  POST /api/usuarios
```

### Busca usuário

```http
  GET /api/usuarios/${id}
```

| Parâmetro | Tipo     | Descrição                         |
| :-------- | :------- | :-------------------------------- |
| `id`      | `string` | **Requerido**. Id do usuário a ser buscado |


### Atualizar usuário

```http
  PUT /api/usuarios/${id}/
```

| Parâmetro | Tipo     | Descrição                         |
| :-------- | :------- | :-------------------------------- |
| `id`      | `string` | **Requerido**. Id do usuário a ter suas informações atualizadas |

### Mudar senha do usuário

```http
  POST /api/usuarios/${id}/set_password
```

| Parâmetro | Tipo     | Descrição                         |
| :-------- | :------- | :-------------------------------- |
| `id`      | `string` | **Requerido**. Id do usuário a ter sua senha atualizada |

### Deletar usuário

```http
  DELETE /api/usuarios/${id}/
```

| Parâmetro | Tipo     | Descrição                         |
| :-------- | :------- | :-------------------------------- |
| `id`      | `string` | **Requerido**. Id do usuário a ser deletado |
