# GitHub Agent 🤖

A conversational AI-powered GitHub assistant that helps you discover and explore GitHub issues and repository activity. Built with Google Gemini 2.5 and FastAPI, this agent provides an intuitive way to find issues and analyze repository metrics.

## ✨ Features

- 🔍 **Smart Issue Search**: Find GitHub issues based on custom criteria
- 💬 **Conversational Interface**: Natural language interaction with the AI agent
- 🎯 **Customizable Filters**: Filter by programming language, labels, and username
- 📊 **Repository Analytics**: Get detailed activity metrics for any repository
- 🚀 **FastAPI Backend**: High-performance REST API endpoints
- 🤖 **Google Gemini Integration**: Powered by Gemini 2.5 Flash model

### Core Capabilities

1. **Good First Issue Finder**
   - Search for beginner-friendly issues across repositories
   - Filter by programming languages (Python, JavaScript, Go, etc.)
   - Customize labels and result limits
   - View issue details with formatted labels and metadata

2. **Repository Activity Tracker**
   - Stars and forks count
   - Open issues and pull requests
   - Total commits
   - Direct URLs to PRs, issues, and commits

## 🛠️ Installation

### Prerequisites

- Python 3.8 or higher
- GitHub Personal Access Token
- Google Cloud API credentials (for Gemini)

### Setup

1. **Clone the repository**
```bash
git clone https://github.com/osansinghrai/github-agent.git
cd github-agent
```

2. **Create a virtual environment**
```bash
python -m venv venv
source .venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies**
```bash
pip install fastapi uvicorn requests pydantic python-dotenv google-adk
```

4. **Set up environment variables**

Create a `.env` file in the project root:
```env
GITHUB_TOKEN=your_github_personal_access_token
GITHUB_USERNAME=your_github_username
```

> **Note**: To get a GitHub Personal Access Token:
> 1. Go to GitHub Settings → Developer settings → Personal access tokens
> 2. Generate a new token with `repo` and `read:org` scopes
> 3. Copy and paste it into your `.env` file

## 🚀 Usage

### Starting the Server

```bash
python -m uvicorn server:app --reload
```

The server will start at `http://localhost:8000`

### API Endpoints

#### 1. Health Check
```
GET /
```
Returns: `{"Connected successfully"}`

#### 2. Find Good First Issues
```
POST /api/good-first-issue/
```

**Request Body:**
```json
{
  "language": ["Python", "JavaScript"],  // Optional
  "label": "good first issue",            // Optional (default: "good first issue")
  "limit": 10,                            // Optional (default: 10)
  "username": "your_username"             // Optional (uses env var if not provided)
}
```

**Response:**
```json
{
  "status_code": 200,
  "count": 5,
  "message": "Good first issue found",
  "results": [
    {
      "repository": "repo-name",
      "repo_open_issues": 15,
      "issue_title": "Add dark mode support",
      "issue_url": "https://github.com/user/repo/issues/123",
      "issue_count": 2,
      "language": "Python",
      "issue_created_at": "2025-12-01T10:00:00Z",
      "issue_labels": [
        "good first issue - Good for newcomers",
        "enhancement - New feature or request"
      ]
    }
  ]
}
```

#### 3. Get Repository Activity
```
POST /api/get-repo-activity/
```

**Request Body:**
```json
{
  "repo": "https://github.com/username/repository"
}
```

**Response:**
```json
{
  "status_code": 200,
  "count": 1,
  "message": "Repo activity found",
  "results": [
    {
      "stars": 1234,
      "forks": 567,
      "open_issues": 89,
      "issues_url": ["https://github.com/..."],
      "issues_number": [1, 2, 3],
      "open_prs": 12,
      "prs_url": ["https://github.com/..."],
      "total_commits": 345,
      "commits_url": ["https://github.com/..."]
    }
  ]
}
```

### Using the AI Agent

The AI agent provides a conversational interface for finding issues:

1. **Greeting**: Start by saying "hello" or "hi"
2. **Request Search**: Say "search for issues" or "find issues"
3. **Answer Questions**: The agent will ask you one question at a time:
   - Username preference
   - Programming language filters
   - Label preferences
   - Result limit

4. **View Results**: Get beautifully formatted issue listings
5. **Repository Details**: Ask for detailed activity on any repository

**Example Conversation:**

```
User: Hello!
Agent: Hello there! I'm your GitHub Assistant, ready to help you find some great 
       issues to contribute to. Just let me know when you'd like to search for issues!

User: search for issues
Agent: Would you like to search for a specific GitHub username, or use the default 
       username which is your_username?

User: use default
Agent: Would you like to filter by specific programming languages? (e.g., Python, 
       JavaScript, Go)

User: Python and JavaScript
Agent: Would you like to use a different label?

User: no
Agent: How many issues would you like to see?

User: 5
Agent: [Displays formatted search results]
```

## 📁 Project Structure

```
github-agent/
├── githubAgent/
│   ├── __init__.py
│   ├── agent.py              # Main AI agent with Gemini integration
│   ├── api_routes.py         # API router configuration
│   ├── good_first_issue.py   # Issue search endpoint
│   └── get_repo_activity.py  # Repository activity endpoint
├── server.py                 # FastAPI application entry point
├── .env                      # Environment variables (create this)
└── README.md                 # This file
```

## 🔧 Configuration

### Environment Variables

| Variable | Description | Required |
|----------|-------------|----------|
| `GITHUB_TOKEN` | Your GitHub Personal Access Token | Yes |
| `GITHUB_USERNAME` | Default GitHub username for searches | Yes |

### Agent Configuration

The agent is configured with:
- **Model**: `gemini-2.5-flash`
- **Tools**: `good_first_issue`, `get_repo_activity`
- **Conversation Style**: One question at a time, friendly and helpful

## 🎨 Features in Detail

### Smart Filtering

- **Language Filtering**: Search across multiple programming languages
- **Label Customization**: Find issues by any label (not just "good first issue")
- **User Scoping**: Search issues from specific GitHub users or organizations
- **Result Limits**: Control the number of results returned

### Beautiful Formatting

The agent formats results with:
- Clear headings and separators
- Emoji indicators for better readability
- Bulleted label descriptions
- Proper spacing and line breaks
- Direct links to issues and repositories

### Repository Insights

Get comprehensive repository metrics including:
- Community engagement (stars, forks)
- Development activity (commits, PRs)
- Issue tracking (open issues with direct links)
- Contributor-friendly data

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 License

This project is open source and available under the [MIT License](LICENSE).

## 🐛 Troubleshooting

### Common Issues

1. **"No issues found"**
   - Verify your GitHub token has the correct permissions
   - Check that the username exists and has public repositories
   - Try broadening your search criteria

2. **"Repository activity not found"**
   - Ensure the repository URL is correctly formatted
   - Verify the repository is public
   - Check your internet connection

3. **API Rate Limiting**
   - GitHub API has rate limits (5000 requests/hour for authenticated users)
   - Use a valid GitHub token to increase limits
   - Wait before retrying if you hit the limit

## 📧 Support

If you encounter any issues or have questions, please open an issue on GitHub.

## 🙏 Acknowledgments

- Built with [FastAPI](https://fastapi.tiangolo.com/)
- Powered by [Google Gemini](https://deepmind.google/technologies/gemini/)
- Inspired by the open-source community

---

Made with ❤️ for developers looking to contribute to open source

