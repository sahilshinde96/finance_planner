# ARTH — Requirements & Setup Guide

## 📋 System Requirements

### Minimum Requirements
- **Python**: 3.10+
- **Node.js**: 18+
- **npm**: 9+
- **pip**: Latest version
- **Git**: Latest version

### Operating Systems
- Windows 10 or later
- macOS 10.14+
- Linux (Ubuntu 18.04+)

---

## 🖥️ Backend Requirements (Django)

### Core Dependencies
| Package | Version | Purpose |
|---------|---------|---------|
| Django | ≥4.2 | Web framework |
| djangorestframework | ≥3.14.0 | REST API framework |
| djangorestframework-simplejwt | ≥5.3.0 | JWT authentication |
| django-cors-headers | ≥4.3.0 | CORS support |
| Pillow | ≥10.0.0 | Image processing |
| python-dotenv | ≥1.0.0 | Environment variables |
| nltk | ≥3.8.1 | NLP for chatbot |
| numpy | ≥1.26.0 | Numerical computing |

### Production Dependencies (Optional)
```
gunicorn>=21.2.0           # WSGI HTTP Server
psycopg2-binary>=2.9.9     # PostgreSQL adapter
whitenoise>=6.6.0          # Static file serving
```

### Installation
```bash
cd backend
python -m venv venv
source venv/bin/activate      # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

---

## 🎨 Frontend Requirements (React + TypeScript)

### Core Dependencies
| Package | Version | Purpose |
|---------|---------|---------|
| react | ^18.2.0 | UI library |
| react-dom | ^18.2.0 | React DOM integration |
| react-router-dom | ^6.30.3 | Client-side routing |
| axios | ^1.6.0 | HTTP client |

### Development Dependencies
| Package | Version | Purpose |
|---------|---------|---------|
| typescript | ^5.2.2 | Type safety |
| vite | ^5.0.8 | Build tool |
| @vitejs/plugin-react | ^4.2.1 | React support in Vite |
| @types/react | ^18.2.43 | Type definitions |
| @types/react-dom | ^18.2.17 | Type definitions |
| eslint | Latest | Code linting |

### Installation
```bash
cd frontend
npm install
```

### Build & Run
```bash
npm run dev       # Development server (http://localhost:5173)
npm run build     # Production build
npm run preview   # Preview production build
npm run lint      # Lint code
```

---

## 🤖 ML & AI Requirements

### ML Training Dependencies
| Package | Version | Purpose |
|---------|---------|---------|
| scikit-learn | ≥1.4.0 | Machine learning library |
| numpy | ≥1.26.0 | Numerical computing |
| pandas | ≥2.2.0 | Data manipulation |
| matplotlib | ≥3.8.0 | Data visualization |
| joblib | ≥1.3.0 | Serialization |

### NLP Components
- **NLTK**: Text processing for chatbot
- Uses pre-trained models for intent recognition

### Installation
```bash
cd ml
pip install -r requirements.txt
```

---

## 📁 Project Structure & Requirements

```
arth/
├── backend/                    # Django REST API
│   ├── accounts/              # User authentication & profiles
│   ├── blockchain/            # Blockchain/transactions
│   ├── chatbot/               # AI chatbot engine
│   ├── planner/               # Financial planning
│   ├── quiz/                  # Adaptive quiz system
│   ├── schemes/               # Government schemes
│   ├── streaks/               # User streaks & gamification
│   ├── config/                # Django settings
│   ├── manage.py              # Django CLI
│   └── requirements.txt        # Python dependencies
│
├── frontend/                   # React + TypeScript
│   ├── src/
│   │   ├── components/        # Reusable React components
│   │   ├── pages/             # Page components
│   │   ├── contexts/          # Context API
│   │   ├── api/               # API client
│   │   └── App.tsx            # Main app
│   ├── package.json           # Node dependencies
│   ├── tsconfig.json          # TypeScript config
│   ├── vite.config.ts         # Vite build config
│   └── index.html             # Entry HTML
│
├── ml/                         # Machine learning
│   ├── ml_predictor.py        # Prediction engine
│   ├── step1_generate_data.py # Data generation
│   ├── step2_train.py         # Model training
│   ├── step3_evaluate.py      # Model evaluation
│   └── requirements.txt        # ML dependencies
│
└── SETUP.md                    # Setup guide
```

---

## 🚀 Quick Start

### 1. Backend Setup
```bash
cd backend
python -m venv venv
# Windows
venv\Scripts\activate
# macOS/Linux
source venv/bin/activate

pip install -r requirements.txt
python manage.py migrate
python manage.py seed_data
python manage.py runserver
```
**Backend URL**: http://localhost:8000

### 2. Frontend Setup
```bash
cd frontend
npm install
npm run dev
```
**Frontend URL**: http://localhost:5173

### 3. ML Setup (Optional)
```bash
cd ml
pip install -r requirements.txt
python step2_train.py      # Train model
python step3_evaluate.py   # Evaluate model
```

---

## 🔧 Environment Configuration

### Backend (.env file)
```env
DEBUG=True
SECRET_KEY=your-secret-key-here
ALLOWED_HOSTS=localhost,127.0.0.1
DATABASE_URL=sqlite:///db.sqlite3

# For production:
# DEBUG=False
# ALLOWED_HOSTS=yourdomain.com
# DATABASE_URL=postgresql://user:password@localhost/dbname
```

### Frontend (vite.env.d.ts)
```typescript
VITE_API_URL=http://localhost:8000
VITE_API_TIMEOUT=5000
```

---

## 📦 Database Requirements

### Development
- **SQLite**: Built-in (db.sqlite3)

### Production (Recommended)
- **PostgreSQL** 12+
- **MySQL** 8.0+

### Initialize Database
```bash
python manage.py makemigrations
python manage.py migrate
python manage.py seed_data  # Load 72 quiz questions, schemes, badges
```

---

## 🔐 Authentication Requirements

- **JWT (JSON Web Tokens)**: For API authentication
- **CORS**: Configured for frontend-backend communication
- **Admin Panel**: Django admin at http://localhost:8000/admin

---

## 📊 Browser Compatibility

| Browser | Version |
|---------|---------|
| Chrome | 90+ |
| Firefox | 88+ |
| Safari | 14+ |
| Edge | 90+ |

---

## 🛠️ Development Tools

### Backend Tools
```bash
# Code formatting
pip install black
black backend/

# Type checking
pip install mypy
mypy backend/

# Testing
python manage.py test
```

### Frontend Tools
```bash
# ESLint for linting
npm run lint

# TypeScript checking
tsc --noEmit
```

---

## 📝 Feature Requirements Summary

### Core Features
1. **User Authentication**: JWT-based login/signup
2. **Financial Planner**: AI-powered financial recommendations
3. **KnowQuest Quiz**: Adaptive quiz with gamification (72 questions)
4. **Schemes Finder**: Government scheme recommendations
5. **Blockchain**: Transaction tracking (if enabled)
6. **Chatbot**: AI financial advisor
7. **Streaks**: User engagement tracking with badges

### Gamification Components
- **XP System**: Points earned through quiz participation
- **Streak System**: Daily engagement tracking
- **Badges**: Achievement milestones
- **Hearts/Lives**: Quiz attempt limits

---

## 🐛 Troubleshooting

### Backend Issues
```bash
# Clear database and start fresh
python manage.py flush
python manage.py migrate
python manage.py seed_data

# Check Python version
python --version

# Activate virtual environment
source venv/bin/activate  # Linux/macOS
# or
venv\Scripts\activate  # Windows
```

### Frontend Issues
```bash
# Clear cache and reinstall
rm -rf node_modules package-lock.json
npm install

# Check Node version
node --version
npm --version
```

### Database Issues
```bash
# Reset migrations
python manage.py migrate zero
python manage.py migrate

# Check SQLite database
sqlite3 db.sqlite3 ".tables"
```

---

## 📞 Support

For issues or questions, refer to:
- **Backend**: Django documentation (https://docs.djangoproject.com/)
- **Frontend**: React documentation (https://react.dev/)
- **ML**: Scikit-learn (https://scikit-learn.org/)

---

## 📄 License

ARTH v2.0 - Smart Financial Planning Platform

---

**Last Updated**: March 2026
**Status**: Production Ready
