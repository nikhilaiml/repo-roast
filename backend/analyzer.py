from radon.complexity import cc_visit
# --- NAYA IMPORT ---
try:
    from .scanners.security_scanner import scan_security
except:
    from scanners.security_scanner import scan_security

def analyze_code(code_text:str, has_readme:bool, py_files_count:int=1):
    score = 100
    issues=[]
    bug_risks=[]
    security_report = []

    #  1 readme check
    if not has_readme:
        score -=20
        issues.append("README.md nahi hai - Recruiter pehle README hi dekhta hai")

    # complexity check - function ki complexity
    try:
        results = cc_visit(code_text)
        for func in results:
            if func.complexity>10:
                score -= 6
                bug_risks.append(f"Function'{func.name}'bahut complex hai(Score:{func.complexity}) - isko 2-3 part me todo")
    except :
        pass

   # 3. Gandi aadatein check
    if "TODO" in code_text:
        issues.append(f"{code_text.count('TODO')} TODO chhode hue hain")
        score -= 5
    if code_text.count("print(") > 5:
        issues.append(f"{code_text.count('print(')} print() mile - production me logging use karo")
        score -= 5

    # Bare except
    if "except:" in code_text:
        bug_risks.append("Bare 'except:' mila - ye saare errors chhupa dega, hamesha 'except Exception:' likho")
        score -= 10
        
    # Ek hi file me 800+ lines
    if len(code_text.splitlines()) > 800:
        issues.append(f"Ek hi file me {len(code_text.splitlines())} lines - ye Monolith hai, alag files banao")
        score -= 10

    # --- PHASE 2: SECURITY SCAN YAHAN JODEGA ---
    # Tera code_text ko dict me convert karke scanner ko de rahe hain
    try:
        findings = scan_security({"main.py": code_text})
        security_report = findings
        # Agar real issue hai toh score kaat
        if not (len(findings) == 1 and "No major" in findings[0]):
            score -= 15
            issues.extend(findings)
    except Exception as e:
        security_report = [f"Security scan error: {e}"]

    score = max(10, score)
    return {
        "score": score,
        "issues": issues,
        "bug_risks": bug_risks,
        "security_report": security_report
    }