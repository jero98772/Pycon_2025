#!/usr/bin/env python3
"""
FastAPI backend for Automatic Theorem Prover
Interfaces with Prolog engine using pyswip
"""

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from pyswip import Prolog
import re
import os

app = FastAPI(title="Automatic Theorem Prover", version="1.0.0")

# Mount static files directory (CSS/JS)
app.mount("/static", StaticFiles(directory="static"), name="static")

# Setup templates directory (HTML)
current_dir = os.path.dirname(os.path.abspath(__file__))
templates = Jinja2Templates(directory=os.path.join(current_dir, "templates"))

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize Prolog
prolog = Prolog()

class PrologInterface:
    def __init__(self):
        self.prolog = Prolog()
        self.load_prolog_file()
    
    def load_prolog_file(self):
        """Load the Prolog theorem prover file"""
        self.prolog.consult("theorem_prover.pl")

    def _load_basic_predicates(self):
        basic_rules = [
            ":- dynamic axiom/1.",
            ":- dynamic rule/2.", 
            ":- dynamic fact/1.",
            "clear_kb :- retractall(axiom(_)), retractall(rule(_, _)), retractall(fact(_)).",
            "assert_axiom(A) :- assertz(axiom(A)).",
            "assert_rule(P, C) :- assertz(rule(P, C)).",
            "assert_fact(F) :- assertz(fact(F)).",
            "prove(G) :- axiom(G).",
            "prove(G) :- fact(G).",
            "prove(G) :- rule(P, G), prove(P).",
        ]
        
        for rule in basic_rules:
            list(self.prolog.query(rule))

    def sanitize_prolog_term(self, term):
        term = re.sub(r'[^\w\s\(\),\.\-\+\*\/]', '', term)
        if term.count('(') != term.count(')'):
            raise ValueError(f"Unbalanced parentheses in term: {term}")
        return term.strip()

    def prove_theorem(self, axioms, rules, facts, theorem):
        list(self.prolog.query("clear_kb"))
        
        for axiom in axioms:
            sanitized = self.sanitize_prolog_term(axiom)
            if sanitized:
                query = f"assert_axiom({sanitized})"
                list(self.prolog.query(query))
        
        for rule in rules:
            premise = self.sanitize_prolog_term(rule.get('premise', ''))
            conclusion = self.sanitize_prolog_term(rule.get('conclusion', ''))
            if premise and conclusion:
                query = f"assert_rule({premise}, {conclusion})"
                list(self.prolog.query(query))
        
        for fact in facts:
            sanitized = self.sanitize_prolog_term(fact)
            if sanitized:
                query = f"assert_fact({sanitized})"
                list(self.prolog.query(query))
        
        theorem_sanitized = self.sanitize_prolog_term(theorem)
        proof_query = f"prove({theorem_sanitized})"
        
        try:
            trace_query = f"prove_with_trace({theorem_sanitized}, Trace)"
            trace_result = list(self.prolog.query(trace_query))
            
            if trace_result:
                return {
                    'success': True,
                    'proof_trace': self._format_trace(trace_result[0].get('Trace', [])),
                    'message': f"Theorem '{theorem}' successfully proved!"
                }
        except:
            pass
        
        result = list(self.prolog.query(proof_query))
        if result:
            return {
                'success': True,
                'proof_trace': [{'goal': theorem, 'method': 'direct_proof', 'details': 'Theorem proved successfully'}],
                'message': f"Theorem '{theorem}' successfully proved!"
            }
        return {
            'success': False,
            'message': f"Could not prove theorem: '{theorem}'"
        }
    
    def _format_trace(self, trace):
        formatted_steps = []
        if isinstance(trace, list):
            for step in trace:
                if hasattr(step, 'functor') and step.functor == 'step':
                    args = step.args
                    formatted_steps.append({
                        'goal': str(args[0]) if len(args) > 0 else 'unknown',
                        'method': str(args[1]) if len(args) > 1 else 'unknown',
                        'details': str(args[2]) if len(args) > 2 else None
                    })
        return formatted_steps

# Initialize Prolog interface
prolog_interface = PrologInterface()

@app.get("/")
async def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/prove")
async def prove_theorem(request: Request):
    data = await request.json()
    result = prolog_interface.prove_theorem(
        data.get("axioms", []),
        data.get("rules", []),
        data.get("facts", []),
        data.get("theorem", "")
    )
    return JSONResponse(result)

@app.get("/examples")
async def get_examples():
    examples = {
        "socrates": {
            "name": "Socrates Mortality",
            "axioms": ["human(socrates)"],
            "rules": [{"premise": "human(X)", "conclusion": "mortal(X)"}],
            "facts": ["human(socrates)"],
            "theorem": "mortal(socrates)"
        },
        "arithmetic": {
            "name": "Basic Arithmetic",
            "axioms": ["natural(zero)", "add(zero, X, X)"],
            "rules": [
                {"premise": "natural(X)", "conclusion": "natural(succ(X))"},
                {"premise": "add(X, Y, Z)", "conclusion": "add(succ(X), Y, succ(Z))"}
            ],
            "facts": ["natural(zero)"],
            "theorem": "natural(succ(zero))"
        },
        "logic": {
            "name": "Logical Reasoning",
            "axioms": ["p", "implies(p, q)"],
            "rules": [{"premise": "and(P, implies(P, Q))", "conclusion": "Q"}],
            "facts": ["p", "implies(p, q)"],
            "theorem": "q"
        }
    }
    return JSONResponse(examples)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)