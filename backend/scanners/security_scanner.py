import re
import ast

def scan_security(files_code: dict):
    """
    files_code = {"app.py": "code content", "utils.py": "..."}
    """
    findings = []
    secrets_pattern = [
        (r'AKIA[0-9A-Z]{16}', 'Possible 【entity-AWS¦canonical_name=AWS】 Access Key'),
        (r'aws_secret_access_key.*[:=]\s*[\'"][A-Za-z0-9/+=]{40}[\'"]', '【entity-AWS¦canonical_name=AWS】 Secret Key hardcoded'),
        (r'["\']sk-[a-zA-Z0-9]{20,}["\']', 'OpenAI API Key leaked'),
        (r'password\s*=\s*["\'][^"\']{3,}["\']', 'Hardcoded Password'),
        (r'api_key\s*=\s*["\'][^"\']{5,}["\']', 'Hardcoded API Key'),
    ]
    dangerous_funcs = ["eval", "exec", "os.system", "subprocess.call", "pickle.loads"]

    for fname, code in files_code.items():
        # 1. Secrets check
        for pattern, msg in secrets_pattern:
            if re.search(pattern, code, re.IGNORECASE):
                findings.append(f"🔑 SECURITY [{fname}]: {msg}")

        # 2. Dangerous functions
        for d in dangerous_funcs:
            if d in code:
                findings.append(f"⚠️ RISKY [{fname}]: `{d}` ka use - injection ho sakta hai")

        # 3. SQL injection hint
        if "execute(f" in code or "execute(\"%s\" % " in code or ".format(" in code and "SELECT" in code:
            findings.append(f"💉 SQLi Risk [{fname}]: String formatting in SQL query")

        # 4. Random for security
        if "random.random()" in code or "random.choice(" in code:
            findings.append(f"🎲 WEAK RANDOM [{fname}]: `random` use kar raha hai, security ke liye `secrets` module use kar")

        # 5. Bare except
        if re.search(r'except\s*:', code):
            findings.append(f"🐛 BUG [{fname}]: Bare `except:` hai - error chhup jayega")

    if not findings:
        findings = ["✅ No major security issues found - solid hai!"]
    
    return findings