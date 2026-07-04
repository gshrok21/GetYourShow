# Eventhooker
<div align="center">

# 🎟️ GetYourShow

### Scalable Event Management & Ticket Booking Platform

*Built with Django, DRF, Celery, RabbitMQ, and Redis*

[![Django](https://img.shields.io/badge/Django-092E20?style=for-the-badge&logo=django&logoColor=white)](https://www.djangoproject.com/)
[![DRF](https://img.shields.io/badge/DRF-A30000?style=for-the-badge&logo=django&logoColor=white)](https://www.django-rest-framework.org/)
[![Celery](https://img.shields.io/badge/Celery-37814A?style=for-the-badge&logo=celery&logoColor=white)](https://docs.celeryq.dev/)
[![RabbitMQ](https://img.shields.io/badge/RabbitMQ-FF6600?style=for-the-badge&logo=rabbitmq&logoColor=white)](https://www.rabbitmq.com/)
[![Redis](https://img.shields.io/badge/Redis-DC382D?style=for-the-badge&logo=redis&logoColor=white)](https://redis.io/)
[![Razorpay](https://img.shields.io/badge/Razorpay-0C2451?style=for-the-badge&logo=razorpay&logoColor=white)](https://razorpay.com/)

[![License](https://img.shields.io/badge/license-MIT-blue?style=flat-square)](#)
[![Stars](https://img.shields.io/github/stars/gshrok21/GetYourShow?style=flat-square)](https://github.com/gshrok21/GetYourShow/stargazers)
[![Issues](https://img.shields.io/github/issues/gshrok21/GetYourShow?style=flat-square)](https://github.com/gshrok21/GetYourShow/issues)

</div>

---

## 🚀 Overview

**GetYourShow** allows users to:

- 🎉 Browse events
- 🎫 Register & manage bookings
- 💳 Make secure payments
- 📄 Download invoices

Built with a **production-ready backend architecture** designed for scale.

---

## ✨ Features

<table>
<tr>
<th>👤 User</th>
<th>🛠️ Admin</th>
</tr>
<tr>
<td>

- 🔐 JWT Authentication
- 🎉 Browse Events
- 🎫 Register for Events
- 💳 Payment via Razorpay
- 📋 My Events
- 📄 Invoice Download

</td>
<td>

- ✍️ Create / Update Events
- 📢 Publish / Cancel Events
- 🗂️ Manage Registrations
- 👥 Track Users
- 📊 Dashboard Ready

</td>
</tr>
</table>

---

## ⚡ Architecture

### 🧩 Components

| Layer | Tool | Purpose |
|---|---|---|
| 🌐 API | Django REST Framework | Core backend |
| 🔐 Auth | JWT (SimpleJWT) | Secure login |
| 📬 Queue | RabbitMQ | Task broker |
| ⚙️ Worker | Celery | Background jobs |
| ⚡ Cache | Redis | Rate limiting + caching |
| 💳 Payment | Razorpay | Payment processing |

### 🔄 Flow

```
Client
  ↓
Django API
  ├─ JWT Auth
  ├─ Redis (Rate Limit)
  ├─ Business Logic
  ├─ Razorpay Payment
  └─ Celery → RabbitMQ → Worker → PDF
```

---

## 📂 Project Structure

```
GetYourShow/
├── backend/
│   ├── authentication/
│   ├── events/
│   ├── payments/
│   ├── tasks/
│
├── frontend/
│   ├── html/
│   ├── css/
│   └── js/
│
├── requirements.txt
└── README.md
```

---

## 🔗 API Endpoints

### 🔐 Auth

| Method | Endpoint |
|---|---|
| `POST` | `/auth/token/` |
| `POST` | `/auth/token/refresh/` |

### 👤 Users

| Method | Endpoint |
|---|---|
| `GET` | `/user/` |
| `GET` | `/user/<id>` |

### 📂 Categories

| Method | Endpoint |
|---|---|
| `GET` | `/categories/` |

### 🎉 Events

| Method | Endpoint |
|---|---|
| `GET` | `/list/event/` |
| `GET` | `/list/event/<slug>/` |
| `PUT` | `/list/event/<slug>/` |
| `POST` | `/list/event/<slug>/cancel` |
| `POST` | `/list/event/<slug>/publish` |
| `GET` | `/my-events/` |

### 🎫 Registration

| Method | Endpoint |
|---|---|
| `GET` | `/registration/` |
| `POST` | `/registration/` |
| `GET` | `/registration/<id>/` |

### 💳 Payment

| Method | Endpoint |
|---|---|
| `POST` | `/create-order/` |
| `POST` | `/verify-payment/` |

### 📄 Invoice

| Method | Endpoint |
|---|---|
| `GET` | `/generatePdf/<id>` |

---

## 💳 Payment Flow

1. 🧾 **Create Order** → `/create-order/`
2. 💰 **Pay** via Razorpay
3. ✅ **Verify** → `/verify-payment/`
4. 🎫 **Register Event**
5. 📄 **Generate Invoice** (Celery)

---

## ⚙️ Setup

### 🔧 Install

```bash
git clone https://github.com/gshrok21/GetYourShow.git
cd GetYourShow/backend

python -m venv env
source env/bin/activate
pip install -r requirements.txt
```

### 🔐 Environment Variables

Create a `.env` file in the `backend/` directory:

```env
SECRET_KEY=your_key
DEBUG=True

DATABASE_URL=your_db

RAZORPAY_KEY_ID=your_key
RAZORPAY_KEY_SECRET=your_secret

REDIS_URL=redis://localhost:6379/0
CELERY_BROKER_URL=your_rabbitmq_url
```

### ▶️ Run

```bash
python manage.py migrate
python manage.py runserver
```

### ⚙️ Celery Worker

```bash
celery -A backend worker --loglevel=info
```

---

## ⚠️ Known Fix

```diff
- path('/my-events/', ...)
+ path('my-events/', ...)
```

> Leading slashes in nested `path()` routes break Django's URL resolver — always omit them.

---

## 🧪 Roadmap

- [ ] 📧 Email notifications
- [ ] 🔔 Event reminders
- [ ] 📊 Analytics dashboard
- [ ] 📱 Mobile app

---

## 👨‍💻 Author

**Ganesh**

[![GitHub](https://img.shields.io/badge/GitHub-181717?style=flat-square&logo=github&logoColor=white)](https://github.com/gshrok21)

---

<div align="center">

### ⭐ Star the repo if you like it!

</div>
