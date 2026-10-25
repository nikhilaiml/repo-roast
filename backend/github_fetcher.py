import requests
from urllib.parse import urlparse
import re

def parse_github_url(url: str):
    url = url.strip().rstrip('/')
    # Agar koi bhi tag ya bracket chipak gaya ho toh hata do
    url = re.sub(r'【[^】]+】', '', url)
    url = url.replace('entity-github', '').replace('canonical_name=', '')
    
    # Ab sirf github.com/owner/repo nikalenge
    match = re.search(r'github\.com/([^/]+)/([^/]+)', url)
    if not match:
        # normal urlparse se try karo
        path = urlparse(url).path.strip('/').split('/')
        if len(path) >= 2:
            return path[0], path[1].replace('.git','')
        raise ValueError(f"Invalid URL diya: {url}")
    
    owner = match.group(1)
    repo = match.group(2).replace('.git','')
    return owner, repo

def fetch_repo_data(repo_url: str, github_token: str = None):
    owner, repo = parse_github_url(repo_url)
    headers = {}
    if github_token:
        headers["Authorization"] = f"token {github_token}"
    
    api_url = f"https://api.github.com/repos/{owner}/{repo}"
    info_res = requests.get(api_url, headers=headers)
    if info_res.status_code != 200:
        raise Exception(f"GitHub API Error: {info_res.json().get('message')}")
    info = info_res.json()
    
    contents_res = requests.get(f"{api_url}/contents", headers=headers)
    contents = contents_res.json() if contents_res.status_code == 200 else []
    
    all_code = ""
    has_readme = False
    file_count = 0
    
    for item in contents:
        if isinstance(item, dict) and item.get('type') == 'file':
            if 'readme' in item.get('name','').lower():
                has_readme = True
            if item.get('name','').endswith('.py'):
                try:
                    code = requests.get(item.get('download_url')).text
                    all_code += code + "\n"
                    file_count += 1
                except:
                    pass
    
    return {
        "full_name": f"{owner}/{repo}",
        "stars": info.get('stargazers_count', 0),
        "has_readme": has_readme,
        "file_count": file_count,
        "code": all_code
    }