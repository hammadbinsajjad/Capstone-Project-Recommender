# API Documentation

## Chat Endpoints

### `POST /api/chat/`
Starts a new chat.

---

### `GET /api/chat/:id`
Fetch all messages from a specific chat.

### `PUT /api/chat/:id`
Continue an existing chat by asking more queries with the previous context.

---

## Authentication Endpoints

### `auth/`
Includes all [Djoser](https://djoser.readthedocs.io/) URLs for user management, such as:

- `auth/users/`
- `auth/users/me/`

---

### `auth/jwt/`
Includes all Djoser JWT authentication endpoints:

- `auth/jwt/create/`
- `auth/jwt/refresh/`
- `auth/jwt/verify/`
