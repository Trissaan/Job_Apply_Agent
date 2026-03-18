# Setup Guide - Job Apply Agent

This guide will walk you through setting up the Job Apply Agent for development or deployment.

## Prerequisites

- Python 3.9 or higher
- Node.js 18 or higher
- Git
- MongoDB (local or MongoDB Atlas account)
- AWS Account (for Cognito authentication)
- OpenAI API key

## Step 1: AWS Cognito Setup

1. Go to [AWS Cognito](https://console.aws.amazon.com/cognito/)
2. Create a new User Pool
3. Configure the user pool with default settings
4. Create an App Client in your user pool
5. Note down:
   - User Pool ID
   - Client ID
   - Region

## Step 2: MongoDB Setup

### Option A: Local MongoDB
```bash
# Install MongoDB Community Edition from https://www.mongodb.com/try/download/community
# Start MongoDB
mongod
```

### Option B: MongoDB Atlas (Recommended)
1. Go to [MongoDB Atlas](https://www.mongodb.com/cloud/atlas)
2. Create a free cluster
3. Create a database user
4. Whitelist your IP
5. Get connection string: `mongodb+srv://user:password@cluster.mongodb.net/job_apply_agent`

## Step 3: Backend Setup

### 1. Navigate to backend directory
```bash
cd backend
```

### 2. Create virtual environment
```bash
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure environment
```bash
cp .env.example .env
```

Edit `.env` with your credentials:
- `MONGODB_URI` - from MongoDB Atlas or local setup
- `AWS_COGNITO_USER_POOL_ID` - from Cognito
- `AWS_COGNITO_CLIENT_ID` - from Cognito
- `AWS_COGNITO_REGION` - e.g., `ap-southeast-2`
- `OPENAI_API_KEY` - from https://platform.openai.com/api-keys

### 5. Run the backend
```bash
uvicorn app.main:app --reload
```

The backend will be available at:
- API: `http://localhost:8000`
- Docs: `http://localhost:8000/docs` (Swagger UI)
- ReDoc: `http://localhost:8000/redoc`

## Step 4: Frontend Setup

### 1. Navigate to frontend directory
```bash
cd frontend
```

### 2. Install dependencies
```bash
npm install
```

### 3. Configure environment
```bash
cp .env.example .env.local
```

Edit `.env.local` with your credentials:
- `NEXT_PUBLIC_API_URL` - backend URL (should match your backend)
- `NEXT_PUBLIC_COGNITO_DOMAIN` - your Cognito domain
- `NEXT_PUBLIC_COGNITO_CLIENT_ID` - from Cognito
- `NEXT_PUBLIC_COGNITO_USER_POOL_ID` - from Cognito
- `NEXT_PUBLIC_COGNITO_REGION` - e.g., `ap-southeast-2`
- `NEXT_PUBLIC_COGNITO_REDIRECT_URI` - callback URL after login

### 4. Run the frontend
```bash
npm run dev
```

The frontend will be available at `http://localhost:3000`

## Step 5: Verify Setup

1. **Backend Health Check**
   ```bash
   curl http://localhost:8000/docs
   ```

2. **Frontend Health Check**
   - Visit `http://localhost:3000` in your browser
   - You should see the login page

3. **Create Test User**
   - Click "Sign Up" on the login page
   - Create a test account
   - You should receive a verification email

## Troubleshooting

### MongoDB Connection Error
```
Error: Cannot connect to MongoDB
```
- Verify `MONGODB_URI` is correct
- If using MongoDB Atlas, check IP whitelist
- Ensure MongoDB is running (local)

### Cognito Authentication Error
```
Error: Cognito configuration invalid
```
- Double-check all Cognito IDs in `.env`
- Verify the region is correct
- Ensure Redirect URI matches in Cognito settings

### CORS Error in Browser
```
Access to XMLHttpRequest blocked by CORS policy
```
- Backend CORS is configured to allow `localhost:3000`
- If using different ports, update `CORS_ORIGINS` in backend `.env`

### OpenAI API Error
```
Error: Invalid API key
```
- Verify `OPENAI_API_KEY` is correct
- Check you have credits in your OpenAI account

## Development Workflow

1. **Start MongoDB** (if using local)
   ```bash
   mongod
   ```

2. **Start Backend** (in one terminal)
   ```bash
   cd backend
   source venv/bin/activate
   uvicorn app.main:app --reload
   ```

3. **Start Frontend** (in another terminal)
   ```bash
   cd frontend
   npm run dev
   ```

4. **Open Browser**
   - Visit `http://localhost:3000`
   - Login with your test account

## Production Deployment

### Backend (Docker)
```bash
cd backend
docker build -t job-apply-agent-backend .
docker run -e MONGODB_URI="..." -e OPENAI_API_KEY="..." -p 8000:8000 job-apply-agent-backend
```

### Frontend (Vercel/Docker)
```bash
cd frontend
npm run build
npm start
```

For more deployment options, see individual backend/frontend documentation.

## Next Steps

- Read the [README.md](README.md) for feature overview
- Check [ROADMAP.docx](ROADMAP.docx) for upcoming features
- Review API documentation at `/docs`
- Explore the codebase structure

## Getting Help

- Check existing [GitHub Issues](https://github.com/yourusername/Job_Apply_Agent/issues)
- Read [CONTRIBUTING.md](CONTRIBUTING.md)
- Open a new issue with detailed information
