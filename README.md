# 🛡️ Plagiarism & AI Detection System

A production-ready, open-source plagiarism and AI-generated content detection system with a premium UI and flexible deployment options. The system supports multiple users with role-based access control and automated database seeding.

## 🌟 Features

- **Semantic Plagiarism Detection**: Uses `pgvector` and `sentence-transformers` to detect similarities based on meaning, not just exact word matches.
- **AI-Generated Text Detection**: Detects content from GPT-3, GPT-4, and other models using local HuggingFace models, OpenAI's API, or **Together API**.
- **Smart Text Chunking**: Automatically splits long documents into overlapping chunks to ensure accurate analysis of large files.
- **Archive & Folder Support**: Upload `.zip`, `.tar`, or entire folders. The system extracts and filters relevant text files automatically.
- **Multi-Platform Support**: Runs anywhere Docker is available (Windows, macOS, Linux).
- **User Authentication**: JWT-based authentication with registration and login.
- **Role-Based Access Control**: Different access levels (user, moderator, admin).
- **Admin Dashboard**: System administration and user management interface.
- **Multi-User Support**: Full support for multiple concurrent users with data isolation.

## 🚀 Quick Start Guide 

This guide is designed to get you up and running in minutes, regardless of your technical background.

### 1. Install Docker (One-time setup)
Docker is the engine that runs the application. Think of it like a "virtual machine" that contains everything the app needs.

- **Windows**: Download and install [Docker Desktop](https://www.docker.com/products/docker-desktop/). Ensure "WSL 2" is enabled during installation.
- **macOS**: Download and install [Docker Desktop](https://www.docker.com/products/docker-desktop/).
- **Linux**: Follow the [official Docker installation guide](https://docs.docker.com/engine/install/).

### 2. Get the Code
- **Coders**: `git clone https://github.com/Kyle6012/plagiarism-detection.git`
- **Non-Coders**: Click the green **"Code"** button at the top of this page and select **"Download ZIP"**. Extract the ZIP file to a folder on your computer.

### 3. Configure Environment Variables
Create a copy of the example environment file:
```bash
cp backend/.env.docker.example backend/.env.docker
```

Edit `backend/.env.docker` to customize your installation:
- `ADMIN_EMAIL`: Email for the initial admin user (default: admin@example.com)
- `ADMIN_PASSWORD`: Password for the initial admin user (default: AdminPass123!)

### 4. Launch the App
1. Open your terminal (Command Prompt/PowerShell on Windows, Terminal on Mac/Linux).
2. Navigate to the project folder: `cd plagiarism-detection`
3. Run the command:
   ```bash
   docker-compose up --build -d
   ```
4. Wait a few minutes for the first-time setup. Once finished, open your browser to:
   👉 **[http://localhost](http://localhost)**

### 5. Initial Setup
- On first startup, the system automatically creates:
  - Database tables
  - An admin user account (credentials from environment variables)
  - Sample user accounts for testing
- Use the admin credentials to log in and manage the system

## 📊 System Features & Usage

### User Registration & Login
- **Register**: New users can create accounts via the registration page
- **Login**: Existing users can log in with their credentials
- **Session Management**: Secure JWT-based sessions with automatic logout

### Dashboard
- **Overview**: View your analysis statistics and recent activity
- **Quick Actions**: Access upload and AI detection tools
- **Reports**: Export PDF and CSV reports (functionality available per batch)

### Document Analysis
- **Upload**: Drag and drop or select files to upload (supports PDF, DOCX, TXT, PNG, JPG, ZIP, TAR)
- **Options**:
  - Select AI detection provider (Local, OpenAI, Together AI)
  - Choose analysis type (Plagiarism, AI Detection, or Full Scan)
  - Adjust AI detection sensitivity
- **Processing**: Documents are analyzed in the background with progress tracking

### AI Detection Tool
- **Direct Analysis**: Paste text directly for AI content detection
- **Provider Selection**: Choose between local, OpenAI, or Together AI models
- **Sensitivity Control**: Adjust detection thresholds
- **Detailed Results**: View probability scores, confidence levels, and provider information

### Admin Dashboard
- **User Management**: Create, update, and deactivate user accounts
- **Role Assignment**: Assign roles (user, moderator, admin) to users
- **System Statistics**: View overall system usage and user counts
- **Access Control**: Only accessible to users with admin role

## 🛠️ Technical Implementation

### Tech Stack
- **Frontend**: React 18, Vite, TypeScript, Tailwind CSS
- **Backend**: FastAPI (Python 3.11), SQLAlchemy 2.0
- **Database**: PostgreSQL 15 + `pgvector`
- **Task Queue**: Celery + Redis
- **Storage**: MinIO (S3 Compatible)

### Authentication & Authorization
- **JWT Tokens**: Secure token-based authentication
- **Role-Based Access**: Three-tier access control (user, moderator, admin)
- **Password Security**: Bcrypt hashing for password storage
- **Session Management**: Secure cookie transport

### Database Management
- **Automatic Seeding**: Tables and initial users created on first startup
- **Migration Support**: Alembic-based migration system
- **Async Operations**: Full async database operations for performance
- **Data Isolation**: User data separated by ownership

## 📄 Project Implementation Status

| Feature | Status | Notes |
| :--- | :--- | :--- |
| **Semantic Search** | ✅ Implemented | Uses `pgvector` with Cosine Similarity. |
| **AI Detection (Local)** | ✅ Implemented | Uses `roberta-base-openai-detector`. |
| **AI Detection (OpenAI/Together)** | ✅ Implemented | Optional; requires `OPENAI_API_KEY` or `TOGETHER_API_KEY`. |
| **Text Chunking** | ✅ Implemented | Handles long documents via overlapping chunks. |
| **Archive Extraction** | ✅ Implemented | Supports `.zip`, `.tar`, `.tar.gz`, `.tar.bz2`. |
| **File Parsing** | ✅ Implemented | Supports `.txt`, `.pdf`, `.docx`. |
| **User Auth** | ✅ Implemented | JWT-based authentication with registration. |
| **Dashboard** | ✅ Implemented | Basic stats for user batches and documents. |
| **Premium UI** | ✅ Implemented | Glassmorphism design with progress bars. |
| **OCR Support** | ✅ Implemented | Uses Tesseract for images and scanned PDFs. |
| **Export Results** | ✅ Implemented | PDF and CSV export of analysis. |
| **Admin Panel** | ✅ Implemented | System stats and management. |
| **Real-time Processing** | ✅ Implemented | Background task processing with Celery. |
| **Health Checks** | ✅ Implemented | Comprehensive service monitoring. |
| **Production Security** | ✅ Implemented | Hardened with non-root containers. |
| **Environment Config** | ✅ Implemented | Full environment variable support. |
| **Admin Dashboard** | ✅ Implemented | Complete user management system. |
| **Multi-User Support** | ✅ Implemented | Full role-based access control. |
| **Database Seeding** | ✅ Implemented | Auto creation of tables and users. |
| **User Management** | ✅ Implemented | Admin panel for user control. |

## 🔐 Initial Setup & Seeding

On first startup, the system automatically performs these setup tasks:

1. **Database Creation**: Creates all required database tables
2. **Admin Account**: Creates an admin user with credentials from environment variables:
   - Email: `ADMIN_EMAIL` (defaults to admin@example.com)
   - Password: `ADMIN_PASSWORD` (defaults to AdminPass123!)
3. **Sample Users**: Creates sample accounts for testing:
   - user1@example.com (password: UserPass123!)
   - user2@example.com (password: UserPass123!)
   - moderator@example.com (password: ModPass123!)

## 🔄 Usage Flow

### For Regular Users:
1. **Register/Login**: Create an account or log in with existing credentials
2. **Upload**: Go to the upload page to submit documents for analysis
3. **Configure**: Select analysis options (AI provider, analysis type, sensitivity)
4. **Process**: Documents are processed in the background
5. **View Results**: Check the dashboard or batch results page for analysis outcomes
6. **Export**: Download reports in PDF or CSV format

### For Administrators:
1. **Log In**: Use admin credentials to access the system
2. **Admin Dashboard**: Navigate to the admin panel via the navigation menu
3. **User Management**: Create, modify, or deactivate user accounts
4. **Role Assignment**: Change user roles (user/moderator/admin)
5. **System Stats**: View overall system usage and metrics

## 📁 File Structure

```
plagiarism-detection/
├── backend/              # Python/FastAPI backend
│   ├── app/              # Application code
│   │   ├── api/          # API routes
│   │   ├── core/         # Core utilities
│   │   ├── models/       # Database models
│   │   └── services/     # Business logic
│   └── requirements.txt  # Python dependencies
├── frontend/             # React frontend
│   ├── src/              # Source code
│   │   ├── components/   # React components
│   │   ├── contexts/     # React contexts
│   │   └── hooks/        # React hooks
│   └── package.json      # Node.js dependencies
├── docker-compose.yml    # Container orchestration
└── README.md             # This file
```

## 🏗️ System Architecture

The system follows a microservices architecture with the following components:

- **Frontend**: React 18 SPA served by Nginx
- **Backend API**: FastAPI with async database operations
- **Database**: PostgreSQL with pgvector for similarity search
- **Message Queue**: Redis with Celery for background tasks
- **Storage**: MinIO for document storage
- **Workers**: Celery workers for processing analysis tasks

## 📚 Documentation

### Core Documentation
- **[Deployment Guide](./DEPLOYMENT_GUIDE.md)** - Complete deployment instructions for Docker and manual setups
- **[Developer Guide](./DEVELOPER_GUIDE.md)** - Technical setup, development workflow, and contribution guidelines
- **[Technical Documentation](./TECHNICAL_DOCS.md)** - Detailed technical architecture and implementation details

### Feature-Specific Documentation
- **[AI Detection](./docs/ai-detection.md)** - AI detection providers, configuration, and usage
- **[Architecture](./docs/architecture.md)** - System architecture, components, and design patterns
- **[Plagiarism Detection](./docs/plagiarism.md)** - Plagiarism algorithms, similarity metrics, and implementation
- **[Providers](./docs/providers.md)** - External service providers and integration details

## 🧪 Testing

Run backend tests:
```bash
docker-compose exec api pytest backend/tests
```

## 📄 License

This project is open-source and available under the MIT License. Use it, modify it, and share it!

---

*Need help? Open an issue on GitHub or check the [API Documentation](http://localhost:8000/docs) when the app is running.*