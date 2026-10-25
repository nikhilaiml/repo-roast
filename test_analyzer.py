from backend.analyzer import analyze_code

code = '''
def hello():
    print("hi")
    print("hello")
'''

result = analyze_code(code, True, 1)
print(result)
