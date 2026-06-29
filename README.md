# InsureLink — Django Insurance Web App

A full-featured insurance marketplace web app where **consultants** list their
life and non-life insurance plans, and **members** can browse, request
consultations, and message consultants directly on the site.

---

## Features

- **Homepage** — Lists all available consultants with their Life and Non-Life plan cards
- **Consultant Profiles** — Detailed page per consultant with full plan info
- **Member Sign-Up / Login** — Separate auth flow for members vs consultants
- **Consultant Sign-Up** — Registers both the user and their company profile
- **Consultation Request** — Members fill out name + contact → sent to consultant
- **Consultation Management** — Consultants accept/decline/complete requests
- **Messaging / Chat** — Real-time-style message thread between member and consultant
- **Dashboard** — Role-aware dashboard (stats for consultants, policies/requests for members)
- **Admin Panel** — Full Django admin for managing all data

---

## Quick Start

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Run migrations
python manage.py makemigrations
python manage.py migrate

# 3. Seed demo data (optional but recommended)
python manage.py seed_demo

# 4. Start the server
python manage.py runserver
```

Open: http://127.0.0.1:8000

---

## Demo Accounts (after seed_demo)

| Role        | Username         | Password   |
|-------------|------------------|------------|
| Admin       | admin            | admin1234  |
| Consultant  | sentinel_ins     | pass1234   |
| Consultant  | pinnacle_assure  | pass1234   |
| Member      | demo_member      | pass1234   |

Admin panel: http://127.0.0.1:8000/admin/

---

## Project Structure

```
InsuranceApp/
├── InsuranceApp/           # Django project config
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── core/                   # Main app
│   ├── models.py           # User, ConsultantProfile, LifePlan, NonLifePlan,
│   │                       # LifePolicy, NonLifePolicy, ConsultationRequest,
│   │                       # Conversation, Message
│   ├── views.py
│   ├── forms.py
│   ├── urls.py
│   ├── admin.py
│   ├── management/
│   │   └── commands/
│   │       └── seed_demo.py
│   └── templates/core/
│       ├── base.html
│       ├── home.html
│       ├── login.html
│       ├── signup_choose.html
│       ├── signup.html
│       ├── consultant_detail.html
│       ├── consult_request.html
│       ├── my_consultations.html
│       ├── conversation.html
│       └── dashboard.html
└── static/css/
    └── main.css
```

---

## Models Overview

| Model                | Purpose                                           |
|----------------------|---------------------------------------------------|
| `User`               | Custom user with `role` (member/consultant)       |
| `ConsultantProfile`  | Company name, license, bio, specialization        |
| `LifePlan`           | Term/Whole/Universal/Variable/Endowment plans     |
| `LifePolicy`         | Issued life policies tied to a member             |
| `NonLifePlan`        | Motor/Property/Health/Travel/Marine/Business plans|
| `NonLifePolicy`      | Issued non-life policies tied to a member         |
| `ConsultationRequest`| Member → Consultant contact with status workflow  |
| `Conversation`       | One-to-one tied to a ConsultationRequest          |
| `Message`            | Individual chat messages in a Conversation        |

---

## Extending the App

- **Add plans** via Django Admin (`/admin/`) or build a consultant-facing plan form
- **Policy issuance** — Link policies to members via admin after consultation
- **Notifications** — Hook into `ConsultationRequest.save()` to email consultants
- **Real-time chat** — Replace polling with Django Channels + WebSockets
- **Search/filter** — Add plan category filters on the homepage
