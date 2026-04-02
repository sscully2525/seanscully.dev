# AI Code Reviewer

Intelligent code review system using AST analysis + LLM for comprehensive code quality assessment.

## Features

- **Static Analysis**: AST-based code structure analysis
- **Security Scanning**: Detects common vulnerabilities
- **Performance Analysis**: Identifies inefficient patterns
- **Style Enforcement**: Customizable style guidelines
- **Auto-Fix Suggestions**: Generates improved code

## Architecture

```
Code Input → AST Parsing → [Security | Performance | Style] Checks → LLM Review → Report
```

## Checks Performed

- Security: SQL injection, XSS, hardcoded secrets, unsafe eval
- Performance: Unnecessary loops, inefficient data structures
- Style: PEP8 compliance, naming conventions, docstrings
- Logic: Potential bugs, edge cases, error handling
