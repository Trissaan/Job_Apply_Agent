# Job Apply Agent

An intelligent automation system that scrapes job listings and automatically applies to positions on your behalf using tailored resumes and cover letters.

## Features

- **🤖 Automated Job Applications**: Scrapes job boards and applies to matching positions automatically
- **📄 Resume Tailoring**: Uses GPT to customize resumes and cover letters for each application
- **🔐 Secure Authentication**: JWT-based authentication with AWS Cognito integration
- **💾 MongoDB Integration**: Persistent storage for job data, applications, and user preferences
- **⏰ Scheduled Scraping**: Background job scheduler for continuous job monitoring
- **📊 Dashboard**: Track application history and job statistics
- **🔧 Preference Management**: Configure job preferences, location, salary, and skills
- **📤 Resume Upload**: Upload and manage resume PDFs

## Tech Stack

### Backend
- **FastAPI** - Modern Python web framework
- **MongoDB** - NoSQL database
- **AWS Cognito** - Authentication and authorization
- **APScheduler** - Background job scheduling
- **OpenAI API** - GPT integration for resume tailoring

### Frontend
- **Next.js** - React framework
- **TypeScript** - Type-safe development
- **Tailwind CSS** - Styling
- **AWS Cognito** - Client-side auth integration

## Project Structure

```
Job_Apply_Agent/
├── backend/
│   ├── app/
│   │   ├── auth/              # Authentication & Cognito
│   │   ├── jobs/              # Job scraping & auto-apply logic
│   │   ├── resume/            # Resume management & tailoring
│   │   ├── user/              # User preferences & dashboard
│   │   ├── storage/           # File upload handling
│   │   ├── db/                # Database configuration
│   │   ├── main.py            # FastAPI app initialization
│   │   └── config.py          # Configuration management
│   ├── requirements.txt       # Python dependencies
│   └── ...
├── frontend/
│   ├── app/
│   │   ├── login/             # Authentication pages
│   │   ├── dashboard/         # Main dashboard
│   │   ├── apply/             # Job application UI
│   │   ├── upload/            # Resume upload
│   │   ├── preferences/       # User preferences
│   │   └── ...
│   ├── components/            # Reusable React components
│   ├── lib/                   # Utilities and API client
│   ├── package.json           # Node dependencies
│   └── ...
```

## Getting Started

### Prerequisites

- Python 3.9+
- Node.js 18+
- MongoDB instance (local or Atlas)
- AWS Cognito user pool configured
- OpenAI API key

### Backend Setup

1. **Clone and navigate to backend**
   ```bash
   cd backend
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

2. **Configure environment variables**
   ```bash
   cp .env.example .env
   ```
   Update `.env` with your credentials:
   - `MONGODB_URI`
   - `AWS_COGNITO_USER_POOL_ID`
   - `AWS_COGNITO_CLIENT_ID`
   - `OPENAI_API_KEY`

3. **Run the server**
   ```bash
   uvicorn app.main:app --reload
   ```
   Backend runs on `http://localhost:8000`
   API docs available at `http://localhost:8000/docs`

### Frontend Setup

1. **Navigate to frontend**
   ```bash
   cd frontend
   npm install
   ```

2. **Configure environment variables**
   ```bash
   cp .env.example .env.local
   ```
   Update with your Cognito configuration and backend URL.

3. **Run development server**
   ```bash
   npm run dev
   ```
   Frontend runs on `http://localhost:3000`

## API Endpoints

### Authentication
- `POST /auth/login` - User login
- `POST /auth/signup` - User registration
- `POST /auth/refresh` - Refresh JWT token

### Jobs
- `GET /jobs/scrape` - Scrape jobs from configured platforms
- `POST /jobs/apply-now` - Apply to specific job
- `GET /jobs/applications` - Get application history
- `POST /jobs/preferences` - Update job preferences

### Resume
- `POST /resume/upload` - Upload resume PDF
- `GET /resume/text` - Get extracted resume text
- `POST /resume/tailor` - Generate tailored version for job

### User
- `GET /user/dashboard` - Get dashboard data
- `GET /user/suggestions` - Get personalized job suggestions
- `POST /user/preferences` - Set user preferences

## Configuration

### Supported Job Boards

Currently integrated:
- Seek (Australian jobs)

Planned:
- LinkedIn
- Workday
- Lever boards
- Indeed

### Credential Storage

Sensitive credentials are encrypted and stored in MongoDB. Configure storage in `app/services/credentials.py`.

## Background Tasks

The system uses APScheduler to run automated tasks:
- Periodic job scraping
- Automatic applications based on preferences
- Resume updates

Configure scheduler intervals in `app/jobs/auto_apply_scheduler.py`.

## Development Roadmap

- [ ] Frontend dashboard with job tracking
- [ ] JWT validation in all endpoints
- [ ] PDF resume upload with text extraction
- [ ] Continuous background scraping daemon
- [ ] Multi-platform job board support
- [ ] End-to-end test endpoint
- [ ] Email notifications for successful applications

## Contributing

1. Create a feature branch (`git checkout -b feature/amazing-feature`)
2. Commit your changes (`git commit -m 'Add amazing feature'`)
3. Push to the branch (`git push origin feature/amazing-feature`)
4. Open a Pull Request

## License

This project is licensed under the MIT License - see LICENSE file for details.

## Support

For issues, questions, or suggestions, please open an issue on GitHub.

## Disclaimer

This tool is for personal use. Users are responsible for ensuring compliance with job board terms of service when using automated application features.
