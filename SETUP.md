# ARTH — Smart Financial Planning Platform
## Complete Setup & Feature Guide (v2.0)

---

## 🚀 Quick Start

### Prerequisites
- Python 3.10+, Node.js 18+, pip & npm

---

## 🖥️ Backend Setup (Django)

```bash
cd backend
python -m venv venv && source venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py seed_data      # Seeds all 72 KnowQuest questions + schemes + badges
python manage.py runserver
```
Backend → http://localhost:8000  |  Admin → http://localhost:8000/admin

---

## 🎨 Frontend Setup (React + Vite)

```bash
cd frontend && npm install && npm run dev
```
Frontend → http://localhost:5173

---

## 🎮 Quiz Gamification Rules (KnowQuest)

| Event | Value |
|-------|-------|
| Correct answer | +10 XP |
| Streak bonus (>2 in a row) | +5 XP |
| Wrong answer | −1 Heart (3 per quiz) |
| Stars: 90%+ / 60%+ / 30%+ | 3 / 2 / 1 stars |
| XP Formula | (correct × 10) + (max_streak × 5) |

### 3 User Tracks × 3 Levels × 8 Questions = 72 Total
- 🌾 **Farmer**: Crops → Soil Science → Farm Finance  
- 🏢 **Corporate**: Markets → Strategies → Advanced Finance  
- 👥 **General**: Money Basics → Save & Invest → Plan Ahead

---

## 🧠 ML Finance Planner

POST /api/planner/ml-plan/ with:
```json
{ "monthly_income": 75000, "housing": "rented", "monthly_rent": 15000,
  "monthly_food": 8000, "monthly_transport": 3000, "monthly_emi": 5000,
  "age": 28, "risk_appetite": "medium", "dependents": 1,
  "goals": ["Retirement"], "has_emergency_fund": false,
  "has_health_insurance": true, "has_life_insurance": false }
```
Returns: Health score (0–100), budget breakdown, asset allocation, prioritised product recommendations, SIP projection.

---

## 📡 Key API Endpoints

| Endpoint | Description |
|----------|-------------|
| POST /api/accounts/login/ | Get JWT tokens |
| GET /api/quiz/?user_type=farmer | List quizzes by type |
| POST /api/quiz/submit/ | Submit answers → XP/stars/hearts |
| GET /api/quiz/leaderboard/ | Top 15 users by XP |
| POST /api/planner/ml-plan/ | Personalized finance plan |
| GET /api/schemes/ | Government schemes |
| POST /api/chatbot/message/ | AI chatbot |
| GET /api/blockchain/records/ | Activity blockchain |

---

## 📂 Files Changed in This Update

**Backend:** quiz/models.py, quiz/views.py, quiz/serializers.py, quiz/urls.py,
quiz/migrations/0002, quiz/management/commands/seed_data.py (72 questions!),
planner/views.py (ML planner), planner/urls.py, streaks/models.py,
streaks/migrations/0002, config/urls.py

**Frontend:** src/index.css (+400 lines), src/pages/Chatbot.tsx (NEW),
src/pages/SchemeFinder.tsx (NEW), src/pages/Blockchain.tsx (NEW),
src/pages/ProfileSetup.tsx (NEW), src/components/Sidebar.tsx,
src/contexts/AuthContext.tsx, src/api/client.ts

