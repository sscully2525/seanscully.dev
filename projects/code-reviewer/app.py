import ast
import re
from typing import List, Dict, Optional
from dataclasses import dataclass
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
import json

@dataclass
class Issue:
    severity: str  # critical, warning, info
    category: str  # security, performance, style, logic
    line: int
    message: str
    suggestion: Optional[str] = None

class CodeReviewer:
    """AI-powered code review system"""
    
    def __init__(self):
        self.llm = ChatOpenAI(model="gpt-4", temperature=0.1)
        self.issues: List[Issue] = []
    
    def parse_code(self, code: str) -> ast.AST:
        """Parse code into AST"""
        try:
            return ast.parse(code)
        except SyntaxError as e:
            raise ValueError(f"Syntax error at line {e.lineno}: {e.msg}")
    
    def check_security(self, code: str, tree: ast.AST):
        """Security vulnerability checks"""
        # Hardcoded secrets pattern
        secret_patterns = [
            (r'password\s*=\s*["\'][^"\']+["\']', "Hardcoded password detected"),
            (r'api_key\s*=\s*["\'][^"\']+["\']', "Hardcoded API key detected"),
            (r'secret\s*=\s*["\'][^"\']+["\']', "Hardcoded secret detected"),
            (r'sk-[a-zA-Z0-9]{48}', "OpenAI API key exposed"),
        ]
        
        for pattern, message in secret_patterns:
            for match in re.finditer(pattern, code, re.IGNORECASE):
                line_num = code[:match.start()].count('\n') + 1
                self.issues.append(Issue(
                    severity="critical",
                    category="security",
                    line=line_num,
                    message=message,
                    suggestion="Use environment variables or a secrets manager"
                ))
        
        # Check for unsafe eval/exec
        for node in ast.walk(tree):
            if isinstance(node, ast.Call):
                if isinstance(node.func, ast.Name):
                    if node.func.id in ['eval', 'exec']:
                        self.issues.append(Issue(
                            severity="critical",
                            category="security",
                            line=node.lineno,
                            message=f"Unsafe use of {node.func.id}()",
                            suggestion="Use ast.literal_eval() for safe evaluation or json.loads()"
                        ))
            
            # SQL injection check (simplified)
            if isinstance(node, ast.BinOp) and isinstance(node.op, ast.Mod):
                self.issues.append(Issue(
                    severity="warning",
                    category="security",
                    line=node.lineno,
                    message="Potential SQL injection via string formatting",
                    suggestion="Use parameterized queries with placeholders"
                ))
    
    def check_performance(self, tree: ast.AST):
        """Performance issue detection"""
        for node in ast.walk(tree):
            # List concatenation in loop
            if isinstance(node, ast.For):
                for child in ast.walk(node):
                    if isinstance(child, ast.AugAssign):
                        if isinstance(child.op, ast.Add) and isinstance(child.target, ast.Name):
                            self.issues.append(Issue(
                                severity="warning",
                                category="performance",
                                line=node.lineno,
                                message="Inefficient list concatenation in loop",
                                suggestion="Use list.append() or list comprehension instead"
                            ))
            
            # Repeated function calls in loop condition
            if isinstance(node, ast.For) or isinstance(node, ast.While):
                # Simplified check
                pass
    
    def check_style(self, code: str, tree: ast.AST):
        """Style and best practice checks"""
        lines = code.split('\n')
        
        for i, line in enumerate(lines, 1):
            # Line length
            if len(line) > 100:
                self.issues.append(Issue(
                    severity="info",
                    category="style",
                    line=i,
                    message=f"Line too long ({len(line)} > 100 characters)",
                    suggestion="Break into multiple lines"
                ))
        
        # Function docstrings
        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef):
                if not ast.get_docstring(node):
                    self.issues.append(Issue(
                        severity="info",
                        category="style",
                        line=node.lineno,
                        message=f"Function '{node.name}' missing docstring",
                        suggestion="Add a docstring describing the function"
                    ))
                
                # Check function length
                func_lines = node.end_lineno - node.lineno if node.end_lineno else 0
                if func_lines > 50:
                    self.issues.append(Issue(
                        severity="warning",
                        category="style",
                        line=node.lineno,
                        message=f"Function '{node.name}' is too long ({func_lines} lines)",
                        suggestion="Consider breaking into smaller functions"
                    ))
    
    def llm_review(self, code: str) -> List[Issue]:
        """LLM-powered code review"""
        prompt = ChatPromptTemplate.from_messages([
            ("system", """You are an expert code reviewer. Analyze the provided code and identify issues.
            
Respond with a JSON array of issues:
[
    {
        "severity": "critical|warning|info",
        "category": "security|performance|style|logic",
        "line": line_number,
        "message": "issue description",
        "suggestion": "how to fix"
    }
]

Focus on: bugs, edge cases, maintainability, Python best practices."""),
            ("human", "```python\n{code}\n```")
        ])
        
        chain = prompt | self.llm
        response = chain.invoke({"code": code})
        
        try:
            llm_issues = json.loads(response.content)
            return [
                Issue(
                    severity=i.get("severity", "info"),
                    category=i.get("category", "logic"),
                    line=i.get("line", 1),
                    message=i["message"],
                    suggestion=i.get("suggestion")
                )
                for i in llm_issues
            ]
        except:
            return []
    
    def generate_fix(self, code: str, issues: List[Issue]) -> str:
        """Generate improved code"""
        critical_issues = [i for i in issues if i.severity == "critical"]
        
        if not critical_issues:
            return code
        
        prompt = ChatPromptTemplate.from_messages([
            ("system", """Fix the critical issues in the provided code. Return ONLY the fixed code, no explanation."""),
            ("human", "Issues to fix:\n{issues}\n\nCode:\n```python\n{code}\n```")
        ])
        
        issues_text = "\n".join([
            f"- Line {i.line}: {i.message}"
            for i in critical_issues
        ])
        
        chain = prompt | self.llm
        response = chain.invoke({"code": code, "issues": issues_text})
        
        # Extract code from markdown if present
        code_match = re.search(r'```python\n(.*?)```', response.content, re.DOTALL)
        if code_match:
            return code_match.group(1).strip()
        return response.content.strip()
    
    def review(self, code: str) -> Dict:
        """Complete code review pipeline"""
        self.issues = []
        
        # Parse
        tree = self.parse_code(code)
        
        # Static analysis
        self.check_security(code, tree)
        self.check_performance(tree)
        self.check_style(code, tree)
        
        # LLM review
        llm_issues = self.llm_review(code)
        self.issues.extend(llm_issues)
        
        # Sort by severity and line
        severity_order = {"critical": 0, "warning": 1, "info": 2}
        self.issues.sort(key=lambda x: (severity_order.get(x.severity, 3), x.line))
        
        # Generate fix
        fixed_code = self.generate_fix(code, self.issues)
        
        # Calculate score
        critical = sum(1 for i in self.issues if i.severity == "critical")
        warnings = sum(1 for i in self.issues if i.severity == "warning")
        info = sum(1 for i in self.issues if i.severity == "info")
        
        score = max(0, 100 - critical * 20 - warnings * 5 - info * 1)
        
        return {
            "score": score,
            "summary": {
                "critical": critical,
                "warnings": warnings,
                "info": info,
                "total": len(self.issues)
            },
            "issues": [
                {
                    "severity": i.severity,
                    "category": i.category,
                    "line": i.line,
                    "message": i.message,
                    "suggestion": i.suggestion
                }
                for i in self.issues
            ],
            "fixed_code": fixed_code if fixed_code != code else None
        }

# Demo
if __name__ == "__main__":
    reviewer = CodeReviewer()
    
    # Sample code with issues
    sample_code = '''
def process_data(data):
    result = []
    password = "secret123"  # Hardcoded secret
    
    for item in data:
        query = "SELECT * FROM users WHERE id = %s" % item  # SQL injection
        result = result + [process_item(item)]  # Inefficient
    
    return eval(result)  # Unsafe eval

def process_item(x):
    return x * 2
'''
    
    print("="*60)
    print("CODE REVIEW DEMO")
    print("="*60)
    
    result = reviewer.review(sample_code)
    
    print(f"\nScore: {result['score']}/100")
    print(f"Issues: {result['summary']['critical']} critical, "
          f"{result['summary']['warnings']} warnings, "
          f"{result['summary']['info']} info")
    
    print("\nIssues found:")
    for issue in result['issues'][:5]:
        print(f"  [{issue['severity'].upper()}] Line {issue['line']}: {issue['message']}")
        if issue['suggestion']:
            print(f"    → {issue['suggestion']}")
    
    if result['fixed_code']:
        print("\n" + "="*60)
        print("FIXED CODE:")
        print("="*60)
        print(result['fixed_code'])
