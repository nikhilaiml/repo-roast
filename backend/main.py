from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
import os

from .github_fetcher import fetch_repo_data
from .analyzer import analyze_code
from .ai_roaster import get_roast

load_dotenv()

app = FastAPI(title="RepoRoast API", version="1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def home():
    return {"message": "RepoRoast API is running! Use /analyze?repo_url=..."}

@app.get("/analyze")
def analyze(repo_url: str):
    try:
        github_token = os.getenv("GITHUB_TOKEN")
        if github_token and "your_github" in github_token:
            github_token = None
            
        repo_data = fetch_repo_data(repo_url, github_token)
        analysis = analyze_code(repo_data['code'], repo_data['has_readme'], repo_data['file_count'])
        roast_data = get_roast(analysis, repo_data['full_name'])
        
        return {
            "repo": repo_data['full_name'],
            "stars": repo_data['stars'],
            "file_count": repo_data['file_count'],
            "has_readme": repo_data['has_readme'],
            "total_lines": len(repo_data['code'].splitlines()),
            "score": analysis['score'],
            "issues": analysis['issues'],
            "bug_risks": analysis['bug_risks'],
            "security_report": analysis.get('security_report', []),
            "roast": roast_data
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))