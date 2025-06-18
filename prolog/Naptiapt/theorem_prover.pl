% theorem_prover.pl
% Automatic Theorem Prover in Prolog
% Supports basic logical reasoning and mathematical structures

:- dynamic axiom/1.
:- dynamic rule/2.
:- dynamic fact/1.

% Clear previous knowledge base
clear_kb :-
    retractall(axiom(_)),
    retractall(rule(_, _)),
    retractall(fact(_)).

% Add axiom to knowledge base
assert_axiom(Axiom) :-
    assertz(axiom(Axiom)).

% Add inference rule to knowledge base
assert_rule(Premise, Conclusion) :-
    assertz(rule(Premise, Conclusion)).

% Add fact to knowledge base
assert_fact(Fact) :-
    assertz(fact(Fact)).

% Basic logical operators and structures
% Implication: implies(P, Q) means P -> Q
% Conjunction: and(P, Q) means P ∧ Q
% Disjunction: or(P, Q) means P ∨ Q
% Negation: not(P) means ¬P
% Universal quantification: forall(X, P) means ∀X P
% Existential quantification: exists(X, P) means ∃X P

% Prove a theorem using forward chaining
prove(Goal) :-
    prove(Goal, []).

prove(Goal, Visited) :-
    \+ member(Goal, Visited),
    (   axiom(Goal)
    ;   fact(Goal)
    ;   prove_by_rule(Goal, [Goal|Visited])
    ).

% Prove using inference rules
prove_by_rule(Goal, Visited) :-
    rule(Premise, Goal),
    prove_premise(Premise, Visited).

% Prove premises
prove_premise(and(P, Q), Visited) :-
    prove(P, Visited),
    prove(Q, Visited).

prove_premise(or(P, Q), Visited) :-
    (prove(P, Visited) ; prove(Q, Visited)).

prove_premise(implies(P, Q), Visited) :-
    (prove(not(P), Visited) ; prove(Q, Visited)).

prove_premise(not(not(P)), Visited) :-
    prove(P, Visited).

prove_premise(P, Visited) :-
    P \= and(_, _),
    P \= or(_, _),
    P \= implies(_, _),
    P \= not(not(_)),
    prove(P, Visited).

% Modus Ponens: If P and P->Q, then Q
modus_ponens(P, Q) :-
    axiom(P),
    axiom(implies(P, Q)).

% Universal instantiation
universal_instantiation(forall(X, P), Instance) :-
    copy_term(P, Instance).

% Mathematical structures

% Peano arithmetic axioms
init_peano_axioms :-
    % Zero is a natural number
    assert_axiom(natural(zero)),
    
    % Successor function
    assert_rule(natural(X), natural(succ(X))),
    
    % Addition axioms
    assert_axiom(add(zero, X, X)),
    assert_rule(add(X, Y, Z), add(succ(X), Y, succ(Z))),
    
    % Multiplication axioms
    assert_axiom(mult(zero, X, zero)),
    assert_rule(and(mult(X, Y, Z), add(Z, Y, W)), mult(succ(X), Y, W)).

% Set theory basics
init_set_theory :-
    % Empty set axiom
    assert_axiom(set(empty)),
    
    % Set membership rules
    assert_rule(element(X, S), subset(singleton(X), S)),
    assert_rule(and(subset(A, C), subset(B, C)), subset(union(A, B), C)).

% Classical logic axioms
init_classical_logic :-
    % Law of excluded middle
    assert_axiom(or(P, not(P))),
    
    % Law of non-contradiction
    assert_axiom(not(and(P, not(P)))),
    
    % Double negation elimination
    assert_rule(not(not(P)), P),
    
    % Modus ponens rule
    assert_rule(and(P, implies(P, Q)), Q),
    
    % Hypothetical syllogism
    assert_rule(and(implies(P, Q), implies(Q, R)), implies(P, R)).

% Prove with detailed trace
prove_with_trace(Goal, Trace) :-
    prove_trace(Goal, [], Trace).

prove_trace(Goal, Visited, [step(Goal, axiom)]) :-
    axiom(Goal),
    \+ member(Goal, Visited).

prove_trace(Goal, Visited, [step(Goal, fact)]) :-
    fact(Goal),
    \+ member(Goal, Visited).

prove_trace(Goal, Visited, [step(Goal, rule(Premise)) | SubTrace]) :-
    \+ member(Goal, Visited),
    rule(Premise, Goal),
    prove_premise_trace(Premise, [Goal|Visited], SubTrace).

prove_premise_trace(and(P, Q), Visited, Trace) :-
    prove_trace(P, Visited, TraceP),
    prove_trace(Q, Visited, TraceQ),
    append(TraceP, TraceQ, Trace).

prove_premise_trace(P, Visited, Trace) :-
    P \= and(_, _),
    prove_trace(P, Visited, Trace).

% Main theorem proving interface
prove_theorem(Axioms, Rules, Facts, Goal, Result) :-
    clear_kb,
    load_axioms(Axioms),
    load_rules(Rules),
    load_facts(Facts),
    (   prove_with_trace(Goal, Trace) ->
        Result = success(Trace)
    ;   Result = failure
    ).

load_axioms([]).
load_axioms([H|T]) :-
    assert_axiom(H),
    load_axioms(T).

load_rules([]).
load_rules([rule(P, C)|T]) :-
    assert_rule(P, C),
    load_rules(T).

load_facts([]).
load_facts([H|T]) :-
    assert_fact(H),
    load_facts(T).

% Example predicates for testing
example_socrates :-
    clear_kb,
    assert_axiom(human(socrates)),
    assert_axiom(forall(X, implies(human(X), mortal(X)))),
    assert_rule(human(X), mortal(X)),
    prove(mortal(socrates)).

% Mathematical example: prove 1 + 1 = 2 in Peano arithmetic
example_arithmetic :-
    clear_kb,
    init_peano_axioms,
    prove(add(succ(zero), succ(zero), succ(succ(zero)))).

% Test if the system can prove a simple logical tautology
example_tautology :-
    clear_kb,
    init_classical_logic,
    assert_axiom(p),
    prove(or(p, not(p))).