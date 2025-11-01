# SkillPath Navigator

## AI-Powered Personalized Learning Path Generator for NCVET

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![Node 18+](https://img.shields.io/badge/node-18+-green.svg)](https://nodejs.org/)

### Overview

SkillPath Navigator is an AI-driven platform that provides personalized vocational training pathways aligned with India's National Skills Qualifications Framework (NSQF). It helps learners discover the right courses based on their background, skills, and career aspirations while considering real-time labor market demands.

### Key Features

- **🎯 Personalized Recommendations**: AI-powered course suggestions based on learner profiles
- **📊 NSQF Alignment**: All courses mapped to NSQF levels (1-10)
- **🔄 Adaptive Learning Paths**: Dynamic pathways that evolve with learner progress
- **💼 Labor Market Intelligence**: Real-time job market data integration
- **🌐 Multilingual Support**: Available in English, Hindi, Tamil, Telugu, Bengali, and Marathi
- **📈 Progress Tracking**: Monitor skill development and course completion
- **🔍 Skill Gap Analysis**: Identify missing skills for target roles
- **♿ Accessible Design**: WCAG 2.1 AA compliant

### Architecture

```
┌─────────────────┐      ┌─────────────────┐      ┌─────────────────┐
│                 │      │                 │      │                 │
│  Next.js        │─────▶│  FastAPI        │─────▶│  PostgreSQL     │
│  Frontend       │      │  Backend        │      │  Database       │
│                 │      │                 │      │                 │
└─────────────────┘      └─────────────────┘      └─────────────────┘
                                │
                                │
                                ▼
                         ┌─────────────────┐
                         │                 │
                         │  ML Service     │
                         │  (Python)       │
                         │                 │
                         └─────────────────┘
```

### Tech Stack

#### Backend
- **FastAPI**: High-performance async API framework
- **SQLAlchemy**: ORM for database operations
- **PostgreSQL**: Primary database
- **JWT**: Authentication and authorization
- **Alembic**: Database migrations

#### Machine Learning
- **scikit-learn**: Classical ML algorithms
- **LightGBM**: Gradient boosting for predictions
- **Sentence Transformers**: Text embeddings for recommendations
- **SHAP**: Model explainability
- **MLflow**: Experiment tracking

#### Frontend
- **Next.js 14**: React framework with SSR
- **TypeScript**: Type-safe development
- **Tailwind CSS**: Utility-first styling
- **Axios**: HTTP client
- **i18next**: Internationalization

### Quick Start

#### Prerequisites

- Docker and Docker Compose
- Python 3.11+
- Node.js 18+
- PostgreSQL 15+ (if running locally)

#### Using Docker Compose (Recommended)

```bash
# Clone the repository
git clone <repository-url>
cd SkillPath-Navigator

# Copy environment variables
cp .env.example .env

# Edit .env with your configuration
nano .env

# Start all services
cd infra
docker-compose up -d

# Check service status
docker-compose ps

# View logs
docker-compose logs -f

# Access the application
# Frontend: http://localhost:3000
# Backend API: http://localhost:8000
# API Docs: http://localhost:8000/api/docs
# ML Service: http://localhost:8001
```

#### Manual Setup

##### Backend Setup

```bash
cd backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Set up database
export DATABASE_URL="postgresql://user:password@localhost:5432/skillpath_db"

# Run migrations
alembic upgrade head

# Start server
uvicorn app.main:app --reload --port 8000
```

##### ML Service Setup

```bash
cd ml

# Create virtual environment
python -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Train models (optional)
python src/train.py

# Start ML service
python src/ml_service.py
```

##### Frontend Setup

```bash
cd frontend

# Install dependencies
npm install

# Set environment variables
export NEXT_PUBLIC_API_URL=http://localhost:8000

# Start development server
npm run dev

# Build for production
npm run build
npm start
```

### Data Setup

#### Load Sample Data

```bash
# Load NSQF courses
python samples/ingestion-scripts/load_courses.py samples/nsqf_courses.csv

# Load job market data
python samples/ingestion-scripts/load_courses.py samples/nsqf_courses.csv samples/job_market_sample.csv
```

### API Documentation

Once the backend is running, access interactive API documentation at:

- **Swagger UI**: http://localhost:8000/api/docs
- **ReDoc**: http://localhost:8000/api/redoc

### Key API Endpoints

#### Authentication
- `POST /api/users/register` - Register new user
- `POST /api/users/login` - Login and get JWT token
- `GET /api/users/me` - Get current user info

#### Learner Profile
- `POST /api/users/profile` - Create/update learner profile
- `GET /api/users/profile` - Get learner profile

#### Courses
- `GET /api/courses/` - List all courses
- `GET /api/courses/{id}` - Get course details
- `GET /api/courses/sectors` - List available sectors

#### ML & Recommendations
- `POST /api/ml/recommendations` - Get personalized recommendations
- `GET /api/ml/learning-path` - Generate learning path
- `GET /api/ml/skill-gap-analysis` - Analyze skill gaps
- `GET /api/ml/job-market-insights` - Get market insights

### Testing

#### Backend Tests
```bash
cd backend
pytest tests/ --cov=app
```

#### Frontend Tests
```bash
cd frontend
npm test
```

#### Integration Tests
```bash
cd tests/integration
pytest
```

### Deployment

#### Vercel (Frontend)
```bash
cd frontend
vercel deploy --prod
```

#### Render/Railway (Backend)
- Connect your GitHub repository
- Set environment variables
- Deploy from main branch

#### Docker Deployment
```bash
# Build images
docker-compose -f infra/docker-compose.yml build

# Push to registry
docker-compose push

# Deploy to your server
docker-compose up -d
```

### Configuration

Key environment variables:

```env
# Database
DATABASE_URL=postgresql://user:password@host:5432/dbname

# Security
SECRET_KEY=your-secret-key-here
ACCESS_TOKEN_EXPIRE_MINUTES=30

# Services
NEXT_PUBLIC_API_URL=https://api.yourdom ain.com
ML_SERVICE_URL=http://ml-service:8001
```

### Project Structure

```
SkillPath-Navigator/
├── backend/              # FastAPI backend
│   ├── app/
│   │   ├── main.py      # Application entry point
│   │   ├── models.py    # Pydantic models
│   │   ├── auth.py      # Authentication logic
│   │   ├── routes/      # API routes
│   │   └── utils/       # Utilities
│   └── requirements.txt
├── frontend/            # Next.js frontend
│   ├── pages/          # Next.js pages
│   ├── components/     # React components
│   ├── utils/          # Utilities
│   └── package.json
├── ml/                 # ML service
│   ├── src/
│   │   ├── recommend.py    # Recommendation engine
│   │   ├── train.py        # Model training
│   │   └── ml_service.py   # ML API service
│   └── requirements.txt
├── infra/              # Infrastructure
│   ├── docker-compose.yml
│   └── terraform/
├── docs/               # Documentation
├── samples/            # Sample data
└── tests/              # Tests
```

### Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

### Security

- All passwords are hashed using bcrypt
- JWT tokens for authentication
- SQL injection prevention via ORM
- CORS configuration
- Input validation with Pydantic
- Rate limiting (recommended for production)

### Privacy & Compliance

- Data anonymization for analytics
- User consent management
- GDPR-like data handling
- Secure data storage
- Right to data deletion

See [docs/privacy-checklist.md](docs/privacy-checklist.md) for details.

### License

This project is licensed under the MIT License - see the LICENSE file for details.

### Support

For issues and questions:
- GitHub Issues: [Create an issue](https://github.com/your-org/skillpath-navigator/issues)
- Email: support@skillpath.in
- Documentation: [docs/](docs/)

### Acknowledgments

- National Council for Vocational Education and Training (NCVET)
- National Skills Qualifications Framework (NSQF)
- Open source community

### Roadmap

- [ ] Mobile app (Flutter)
- [ ] Offline mode support
- [ ] Advanced analytics dashboard
- [ ] Integration with training providers
- [ ] Certification verification
- [ ] Peer learning features
- [ ] Gamification elements

---

**Built with ❤️ for India's skilling ecosystem**
