import os
from dotenv import load_dotenv
load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), '..', '.env'))
from openai import OpenAI

def get_roast(analysis_data, repo_name=""):
    key = os.getenv("OPENROUTER_API_KEY")
    client = OpenAI(base_url="https://openrouter.ai/api/v1", api_key=key)

    prompt = f"""You are a funny senior dev who roasts code in Hinglish.
    Repo: {repo_name} Score: {analysis_data['score']}/100
    Issues: {analysis_data['issues']} Bug Risks: {analysis_data['bug_risks']}
    Give ONLY JSON: {{"one_liner": "funny hinglish roast", "improvements": ["tip1","tip2","tip3"], "fixed_example": "code"}}"""

    try:
        res = client.chat.completions.create(
            model="recursive/flint-v1.0:free",
            messages=[{"role": "user", "content": prompt}],
        )
        import json
        text = res.choices[0].message.content.replace("```json","").replace("```","").strip()
        return json.loads(text)
    except Exception as e:
        return {"one_liner": f"Error: {e}", "improvements": ["README add karo"], "fixed_example": "#"}