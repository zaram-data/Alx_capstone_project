# 📱 Social Media API Backend (Django REST Framework)

A fully functional backend for a social media platform built with **Django REST Framework**, supporting:

✔ User authentication (JWT)  
✔ Create, update, delete posts  
✔ Like/Unlike posts  
✔ Follow/Unfollow users  
✔ Personalized feed  
✔ Comments  
✔ API documentation (Swagger + Redoc)  

---

## 🚀 Features

- JWT Authentication
- CRUD for Posts
- Like/Unlike Mechanism
- Follows system
- Feed endpoint (posts from followed users)
- Comments on posts
- Swagger UI + Redoc API Docs
- Postman Collection Included

---

## 📦 Install & Setup

```bash
git clone https://github.com/<your-username>/social_media_api.git
cd social_media_api

python -m venv venv
venv\Scripts\activate  # Windows

pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
