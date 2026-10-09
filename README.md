# Backend / Cloud Solution

A Python/Flask backend assignment with three independently deployed REST services and separate PostgreSQL databases hosted on Neon.

## Architecture

| Service | Responsibility | Database |
|---|---|---|
| Server X | Platform 1 posts and platform activity | `db_x` |
| Server Y | Platform 2 posts and platform activity | `db_y` |
| Server C | Shared account registration and login | `db_c` |

X and Y forward registration and login requests to C, so the same account can be used on both platforms. Each platform service reads and writes its own platform data; it should not connect directly to the other platform's database.

## Implemented endpoints

### Server X

| Method | Route | Purpose |
|---|---|---|
| `GET` | `/status` | Check that Server X is running |
| `POST` | `/new_user` | Forward account registration to Server C |
| `POST` | `/login` | Forward login to Server C |
| `GET` | `/posts` | Read posts from `posts_x` in `db_x` |

### Server Y

| Method | Route | Purpose |
|---|---|---|
| `GET` | `/status` | Check that Server Y is running |
| `POST` | `/new_user` | Forward account registration to Server C |
| `POST` | `/login` | Forward login to Server C |
| `GET` | `/posts` | Read posts from `posts_y` in `db_y` |

### Server C

| Method | Route | Purpose |
|---|---|---|
| `GET` | `/status` | Check that Server C is running |
| `POST` | `/new_user` | Create a shared account in `db_c` |
| `POST` | `/login` | Check an account's email and password |

Registration stores an `account_id`, email, and password hash in the `accounts` table. Passwords are hashed with Werkzeug; plain-text passwords should not be stored or returned by an API.

## Local setup

Use a separate virtual environment and dependency file for each service. From each service's directory, create and activate the environment, then install its dependencies:

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

Create a local `.env` file for each service. Do not commit `.env` files or Neon connection strings to GitHub.

- **Server X:** `DATABASE_URL` must point to `db_x`; `C_URL` must point to Server C.
- **Server Y:** `DATABASE_URL` must point to `db_y`; `C_URL` must point to Server C.
- **Server C:** `DATABASE_URL` must point to `db_c`.

For local testing, run each service in a separate terminal on a different port. 

## Testing

1. Call `GET /status` on Server X and Server C.
2. Send a JSON registration request to Server X's `POST /new_user`, for example:

   ```json
   {
     "email": "test@example.com",
     "password": "use-a-test-password"
   }
   ```

3. Log in using `POST /login` and the same JSON fields. Server C should return the shared `account_id`.
4. Call `GET /posts` on X and Y. Confirm each service returns data from its own database.
5. Use the account ID returned by C when associating test activity with an account.

## Security and current scope

The current login response returns an `account_id`, not a login token. An account ID identifies an account but does not prove that a later request was made by that account's owner. Accepting an `account_id` directly from a request body is suitable only for a basic assignment demonstration, not for protecting real user activity.

