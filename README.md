# 📚 Library Management System — FastAPI Backend

A RESTful API backend for the Library Management System, built with **FastAPI**, **MongoDB**, and **JWT authentication**.

---

## 🚀 Tech Stack

| Technology | Purpose |
|---|---|
| [FastAPI](https://fastapi.tiangolo.com/) | Web framework |
| [Uvicorn](https://www.uvicorn.org/) | ASGI server |
| [MongoDB Atlas](https://www.mongodb.com/atlas) | Database |
| [PyMongo](https://pymongo.readthedocs.io/) | MongoDB driver |
| [Python-JOSE](https://python-jose.readthedocs.io/) | JWT token handling |
| [Passlib + bcrypt](https://passlib.readthedocs.io/) | Password hashing |

---

## 📁 Project Structure

```
fastapi/
├── app/
│   ├── config/         # Database connection config
│   ├── controllers/    # Business logic
│   ├── middleware/     # Custom middleware (auth, etc.)
│   ├── models/         # MongoDB models
│   ├── routes/         # API route definitions
│   │   ├── auth_routes.py
│   │   ├── book_routes.py
│   │   ├── user_routes.py
│   │   ├── issue_routes.py
│   │   └── stats_routes.py
│   ├── schemas/        # Pydantic schemas
│   ├── utils/          # Utility functions
│   └── main.py         # FastAPI app entry point
├── run.py              # Local dev runner
├── requirements.txt    # Python dependencies
├── vercel.json         # Vercel deployment config
└── .env                # Environment variables (do NOT commit)
```

---

## ⚙️ Prerequisites

- **Python 3.9+** — [Download](https://www.python.org/downloads/)
- **pip** (comes with Python)
- A **MongoDB Atlas** account (or local MongoDB instance)

---

## 🛠️ Local Setup & Installation

### 1. Clone the repository

```bash
git clone <your-repo-url>
cd lib-manage/fastapi
```

### 2. Create a virtual environment

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS / Linux
python3 -m venv venv
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure environment variables

Create a `.env` file in the `fastapi/` directory:

```env
MONGO_URL=mongodb+srv://<username>:<password>@cluster0.xxxxx.mongodb.net
DATABASE_NAME=libraby
JWT_SECRET=your_super_secret_key_here
```

> ⚠️ **Never commit your `.env` file.** It is already listed in `.gitignore`.

### 5. Run the development server

```bash
python run.py
```

The API will be available at: **http://localhost:8000**

---

## 📖 API Documentation

Once the server is running, visit the interactive docs:

| Interface | URL |
|---|---|
| Swagger UI | [http://localhost:8000/docs](http://localhost:8000/docs) |
| ReDoc | [http://localhost:8000/redoc](http://localhost:8000/redoc) |

---

## 🔌 API Endpoints

### Auth — `/auth`
| Method | Endpoint | Description |
|---|---|---|
| POST | `/auth/register` | Register a new user |
| POST | `/auth/login` | Login and receive JWT token |

### Books — `/books`
| Method | Endpoint | Description |
|---|---|---|
| GET | `/books` | List all books |
| POST | `/books` | Add a new book |
| PUT | `/books/{id}` | Update a book |
| DELETE | `/books/{id}` | Delete a book |

### Users — `/users`
| Method | Endpoint | Description |
|---|---|---|
| GET | `/users` | List all users |
| GET | `/users/{id}` | Get a specific user |
| PUT | `/users/{id}` | Update user details |
| DELETE | `/users/{id}` | Delete a user |

### Issues — `/issues`
| Method | Endpoint | Description |
|---|---|---|
| GET | `/issues` | List all book issues |
| POST | `/issues` | Issue a book |
| PUT | `/issues/{id}` | Return / update an issue |
| DELETE | `/issues/{id}` | Delete an issue record |

### Stats — `/stats`
| Method | Endpoint | Description |
|---|---|---|
| GET | `/stats` | Get dashboard statistics |

---

## ☁️ Deploying to Vercel

This project includes a `vercel.json` for zero-config deployment.

### Steps

1. **Install Vercel CLI** (optional, can also use the dashboard):
   ```bash
   npm install -g vercel
   ```

2. **Login to Vercel:**
   ```bash
   vercel login
   ```

3. **Deploy:**
   ```bash
   vercel
   ```

4. **Add Environment Variables** in your Vercel project dashboard:
   - `MONGO_URL`
   - `DATABASE_NAME`
   - `JWT_SECRET`

   > Go to: **Vercel Dashboard → Your Project → Settings → Environment Variables**

5. **Update CORS origins** in `app/main.py` to include your deployed frontend URL:
   ```python
   origins = [
       "http://localhost:3000",
       "https://your-frontend.vercel.app",  # Add your frontend URL
   ]
   ```

---

## 🔐 Environment Variables Reference

| Variable | Description | Example |
|---|---|---|
| `MONGO_URL` | MongoDB connection string | `mongodb+srv://user:pass@cluster...` |
| `DATABASE_NAME` | Name of the MongoDB database | `libraby` |
| `JWT_SECRET` | Secret key for signing JWT tokens | `supersecretkey` |

---

## 🧪 Health Check

Visit the root endpoint to verify the API is running:

```
GET /
```

Response:
```json
{
  "message": "Library Management System API is running!"
}
```

---

## 📝 License

This project is for educational/personal use.
