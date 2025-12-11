#!/usr/bin/env python3
"""
Scientific Calculator - Interactive CLI
Run: python calculator.py
Supports: arithmetic, trig, log, factorial, permutations/combinations,
power, parentheses, ans memory, degree/radian modes, and safe evaluation.
"""
import math
import ast
import operator as op
from utils import factorial, nCr, nPr

ALLOWED_OPERATORS = {
    ast.Add: op.add,
    ast.Sub: op.sub,
    ast.Mult: op.mul,
    ast.Div: op.truediv,
    ast.Pow: op.pow,
    ast.USub: op.neg,
    ast.UAdd: op.pos,
    ast.Mod: op.mod,
    ast.FloorDiv: op.floordiv,
}

class CalcEnvironment:
    def __init__(self):
        self.mode = 'rad'
        self.ans = 0
    def sin(self, x): return math.sin(math.radians(x)) if self.mode=='deg' else math.sin(x)
    def cos(self, x): return math.cos(math.radians(x)) if self.mode=='deg' else math.cos(x)
    def tan(self, x): return math.tan(math.radians(x)) if self.mode=='deg' else math.tan(x)
    def log(self, x, base=math.e): return math.log(x, base) if base!=math.e else math.log(x)
    def sqrt(self, x): return math.sqrt(x)
    def exp(self, x): return math.exp(x)
    def factorial(self, n): return factorial(int(n))
    def nCr(self, n, r): return nCr(int(n), int(r))
    def nPr(self, n, r): return nPr(int(n), int(r))
    def pow(self, a, b): return math.pow(a, b)
    def set_mode(self, m):
        if m in ('deg','rad'): self.mode = m

ENV = CalcEnvironment()

NAME_MAP = {
    'pi': math.pi,
    'e': math.e,
    'sin': ENV.sin,
    'cos': ENV.cos,
    'tan': ENV.tan,
    'log': ENV.log,
    'sqrt': ENV.sqrt,
    'exp': ENV.exp,
    'factorial': ENV.factorial,
    'nCr': ENV.nCr,
    'nPr': ENV.nPr,
    'pow': ENV.pow,
    'ans': lambda: ENV.ans,
}

def safe_eval(expr: str):
    try:
        node = ast.parse(expr, mode='eval').body
        return _eval(node)
    except Exception as e:
        raise ValueError(f"Invalid expression: {e}")

def _eval(node):
    if isinstance(node, ast.Constant): return node.value
    if isinstance(node, ast.Num): return node.n
    if isinstance(node, ast.BinOp): return ALLOWED_OPERATORS[type(node.op)](_eval(node.left), _eval(node.right))
    if isinstance(node, ast.UnaryOp): return ALLOWED_OPERATORS[type(node.op)](_eval(node.operand))
    if isinstance(node, ast.Call):
        if isinstance(node.func, ast.Name):
            fname = node.func.id
            if fname not in NAME_MAP: raise ValueError(f"Function '{fname}' not allowed")
            fn = NAME_MAP[fname]
            args = [_eval(a) for a in node.args]
            kwargs = {kw.arg: _eval(kw.value) for kw in node.keywords}
            return fn(*args, **kwargs)
    if isinstance(node, ast.Name):
        val = NAME_MAP[node.id]
        return val() if callable(val) else val
    raise ValueError("Unsupported expression")

HELP_TEXT = """Scientific Calculator Commands"""

def repl():
    print("Scientific Calculator — Interactive CLI")
    history = []
    while True:
        try:
            user = input("calc> ").strip()
        except:
            print("Goodbye")
            break
        if not user: continue
        if user in (":q", ":quit"):
            print("Goodbye"); break
        if user == ":help":
            print(HELP_TEXT); continue
        if user.startswith(":mode"):
            parts = user.split()
            if len(parts)==2 and parts[1] in ("deg","rad"):
                ENV.set_mode(parts[1])
                print("Mode set to", ENV.mode)
            continue
        try:
            expr = user.replace("^","**")
            result = safe_eval(expr)
            ENV.ans = result
            history.append((user,result))
            print(result)
        except Exception as e:
            print("Error:",e)

if __name__=="__main__":
    repl()
