# -*- coding: utf-8 -*-

"""
Define the language and semantics of classical (standard and modal) (prepositional and first-order) logic.
"""


from main import *
from structure import *
# from tableau import *

from typing import List, Dict, Set, Tuple


class Expr:
    """
    Well-formed expression of predicate logic.
    α, β, ...

    @method freevars: the set of free variables in the expression
    @method boundvars: the set of bound variables in the expression
    @method subst: substitution of a term for a variable in the expression
    @method denot: denotation of the expression relative to a structure m and assignment g
    """

    def propvars(self) -> Set[str]:
        """
        The set of propositional variables in the expression.

        @return: the seet of propositional varibles in the expression
        @rtype: set[str]
        """
        return self.phi.propvars()

    def freevars(self) -> Set[str]:
        """
        The set of free variables in the expression.

        @return: the set of free variables in the expression
        @rtype: set[str]
        """
        pass

    def boundvars(self) -> Set[str]:
        """
        The set of bound variables in the expression.

        @return: the set of bound variables in the expression
        @rtype: set[str]
        """
        pass
    
    def nonlogs(self):
        """
        The set of non-logical symbols in the expression.
        
        @return the set of non-logical symbols in the expression: (constants, functions, predicates)
        @rtype: tuple[set[str]]
        """

    def subst(self, u, t):
        """
        Substitute all occurrences of the variable u for the term t in self.

        @param u: the variable to be substituted
        @type u: Var
        @param t: the term to substitute
        @type t: Term
        @return: the result of substituting all occurrences of the variable v for the term t in self
        @rtype Expr
        """
        pass

    def denot(self, m: Structure, v: Dict[str,str] = None, w: str = None):
        """
        Compute the denotation of the expression relative to a structure m and assignment g.

        @param m: the structure to evaluate the formula against
        @type m: Structure
        @param v: the assignment to evaluate the formula against
        @type v: dict[str,str]
        @param w: the possible world to evaluate the formula against
        @type w: str
        @return: the denotation of the expression relative to the structure m and assignment g
        """
        pass


class Term(Expr):
    """
    Term (constant, variable).
    t1, t2, ...
    """

    def subst(self, u, t):
        """
        @rtype: Term
        """
        pass

    def denot(self, m, v=None, w=None) -> str:
        """
        @rtype: str
        """
        pass


class Const(Term):
    """
    Individual constant.
    a, b, c, c1, c2, ...

    @attr c: the constant name
    @type c: str
    """

    def __init__(self, c: str):
        self.c = c

    def __str__(self):
        return self.c

    def __eq__(self, other):
        return isinstance(other, Const) and self.c == other.c

    def propvars(self):
        return set()

    def freevars(self):
        return set()

    def boundvars(self):
        return set()

    def nonlogs(self):
        return {self.c}, set(), set()

    def subst(self, u, t):
        return self

    def denot(self, m, v=None, w=None):
        """
        The denotation of a constant is that individual that the interpretation function f assigns it.
        """
        i = m.i
        if isinstance(m, ModalStructure):
            i = m.i[w]
        return i[self.c]


class Var(Term):
    """
    Individual variable.
    x, y, z, u, v, w, x1, x2, ...

    @attr u: the variable name
    @type u: str
    """
    # NB: When dealing with variable occurrences in the further processing,
    # it will be necessary to reference the variables by their name (self.v)
    # rather than the variable objects themselves (self)
    # in order for different variable occurrences with the same name to be identified, as desired in the theory.

    def __init__(self, u: str):
        self.u = u

    def __str__(self):
        return self.u

    def __eq__(self, other):
        return isinstance(other, Var) and self.u == other.u

    def propvars(self):
        return set()

    def freevars(self):
        return {self.u}

    def boundvars(self):
        return set()

    def nonlogs(self):
        return set(), set(), set()

    def subst(self, u, t):
        if u.u == self.u:
            return t
        else:
            return self

    def denot(self, m, v=None, w=None):
        """
        The denotation of a constant is that individual that the assignment function g assigns it.
        """
        return v[self.u]


class Func(Expr):
    """
    Function symbol.
    f, h, ...

    @attr f: the function name
    @type f: str
    """

    def __init__(self, f: str):
        self.f = f

    def __str__(self):
        return self.f

    def __eq__(self, other):
        return isinstance(other, Func) and self.f == other.f

    def propvars(self):
        return set()

    def freevars(self):
        return set()

    def boundvars(self):
        return set()

    def nonlogs(self):
        return set(), {self.f}, set()

    def subst(self, u, t):
        return self

    def denot(self, m, v=None, w=None) -> str:
        """
        The denotation of a constant is that individual that the assignment function g assigns it.
        """
        i = m.i
        if isinstance(m, ModalStructure):
            i = m.i[w]
        return i[self.i]


class FuncTerm(Term):
    """
    Function symbol applied to an appropriate number of terms.
    f(m), h(x,t), ...

    Note that 1-place function applications have to be specified as
    Atm('f', (t1, ))
    rather than
    Atm('f', (t))
    or
    Atm('f', t1).

    @attr f: the function symbol
    @type f: Func
    @attr terms: the term tuple to apply the function symbol to
    @type terms: tuple[Term]
    """

    def __init__(self, f: Func, terms: Tuple[Term]):
        self.f = f
        self.terms = terms

    def __str__(self):
        return str(self.f) + "(" + ", ".join([str(t) for t in self.terms]) + ")"

    def __eq__(self, other):
        return isinstance(other, FuncTerm) and self.f == other.f and self.terms == other.terms

    def propvars(self):
        return set()

    def freevars(self):
        return set().union(*[t.freevars() for t in self.terms])

    def boundvars(self):
        return set().union(*[t.boundvars() for t in self.terms])

    def nonlogs(self):
        return set().union(*[t.nonlogs()[0] for t in self.terms]), \
               set().union(*[t.nonlogs()[1] for t in self.terms]) | {self.f}, \
               set()

    def subst(self, u, t):
        return FuncTerm(self.f, tuple(map(lambda t: t.subst(u, t), self.terms)))

    def denot(self, m, v=None, w=None) -> str:
        """
        The denotation of a function symbol applied to an appropriate number of terms is that individual that the
        interpretation function f assigns to the application.
        """
        i = m.i
        if isinstance(m, ModalStructure):
            i = m.i[w]
        return i[self.f.f][tuple([t.denot(m, v, w) for t in self.terms])]


class Pred(Expr):
    """
    Predicate.
    P, Q, ...

    @attr p: the predicate name
    @type p: str
    """
    def __init__(self, p: str):
        self.p = p

    def __str__(self):
        return self.p

    def __eq__(self, other):
        return isinstance(other, Pred) and self.p == other.p

    def propvars(self):
        return set()

    def freevars(self):
        return set()

    def boundvars(self):
        return set()

    def nonlogs(self):
        return set(), set(), {self.p}

    def subst(self, u, t):
        return self

    def denot(self, m, v=None, w=None) -> Set[Tuple[str]]:
        """
        The denotation of a predicate is the set of ordered tuples of individuals that the interpretation function f
        assigns it.
        """
        i = m.i
        if isinstance(m, ModalStructure):
            i = m.i[w]
        return i[self.p]


depth = 0  # keep track of the level of nesting


class Formula(Expr):
    """
    Formula.
    φ, ψ, ...

    @method denotV: the truth value of a formula relative to a structure m (without reference to a particular assignment)
    """
    def subst(self, u, t):
        """
        @rtype: Formula
        """
        pass

    def denot(self, m: Structure, v=None, w=None) -> bool:
        """
        @rtype: bool
        """
        pass

    def denotV(self, m: Structure, w: str = None) -> bool:
        """
        The truth value of a formula relative to a structure M (without reference to a particular assignment).
        A formula is true in a structure M iff it is true in M under all assignment functions g.

        @param m: a structure
        @type m: Structure
        @attr w: a possible world
        @type w: str
        @return: the truth value of self in m
        @rtype: bool
        """
        global depth
        # for efficiency, restrict the domain of the assignment functions o the vars that actually occur in the formula
        var_occs = self.freevars() | self.boundvars()
        vs__ = m.vs
        if isinstance(m, VarModalStructure):
            vs__ = m.vs[w]
        vs_ = [{u: v[u] for u in v if u in var_occs} for v in vs__]
        vs = [dict(tpl) for tpl in {tuple(v.items()) for v in vs_}]  # filter out now duplicate assignment functions

        if not self.freevars():  # if the formula is closed,
            # spare yourself the quantification over all assignment functions and pick an arbitrary assignment
            # (here: the first)
            return self.denot(m, vs[0], w)

        for v in vs:  # otherwise, check the denotation for all assignment functions
            depth += 1
            if verbose:
                print((depth * " ") + "checking v := " + str(v) + " ...")
            witness = self.denot(m, v, w)
            if witness:
                if verbose:
                    print((depth * 2 * " ") + "✓")
                depth -= 1
            else:
                if verbose:
                    print((depth * 2 * " ") + "✗")
                    print((depth * " ") + "counter assignment: v := " + str(v))
                depth -= 1
                return False
        return True

    def denotW(self, m: Structure, v: Dict[str,str]) -> bool:
        """
        The truth value of a formula relative to a structure M and assmnt. g (without reference to a particular world).
        A formula is true in a structure M iff it is true in M and g in all possible worlds w.

        @param m: a structure
        @type m: ModalStructure
        @attr g: an assignment function
        @type v: dict[str,str]
        @return: the truth value of self in m under g
        @rtype: bool
        """
        global depth
        # for efficiency, restrict the domain of the assignment functions to the vars that actually occur in the formula
        var_occs = self.freevars() | self.boundvars()
        vs_ = [{u: v[u] for u in v if u in var_occs} for v in m.vs]
        m.vs_ = [dict(tpl) for tpl in {tuple(v.items()) for v in vs_}]  # filter out duplicate assignment functions

        for w in m.w:
            depth += 1
            if verbose:
                print((depth * "  ") + "checking w := " + str(w) + " ...")
            witness = self.denot(m, v, w)
            if witness:
                if verbose:
                    print((depth * 2 * " ") + "✓")
                depth -= 1
            else:
                if verbose:
                    print((depth * 2 * " ") + "✗")
                    print((depth * " ") + "counter world: w := " + str(w))
                depth -= 1
                return False
        return True

    def denotVW(self, m: Structure) -> bool:
        """
        The truth value of a formula relative to a structure M (without reference to a particular assignment and world).
        A formula is true in a structure M iff it is true in M and g under all assignments g and all possible worlds w.

        @param m: a structure
        @type m: ModalStructure
        @attr g: an assignment function
        @type v: dict[str,str]
        @return: the truth value of self in m under g
        @rtype: bool
        """
        # todo doesn't work for modal structures with varying domain yet (due different structure of assignment functions)
        global depth

        for w in m.w:
            depth += 1
            if verbose:
                print((depth * " ") + "checking w := " + str(w) + " ...")
            witness = self.denotV(m, w)
            if witness:
                if verbose:
                    print((depth * 2 * " ") + "✓")
                depth -= 1
            else:
                if verbose:
                    print((depth * 2 * " ") + "✗")
                    print((depth * " ") + "counter world: w := " + str(w))
                depth -= 1
                return False
        return True

    def tableau_pos(self, node):
        pass

    def tableau_neg(self, node):
        pass


class Verum(Formula):
    """
    Verum.
    ⊤
    """
    def __init__(self):
        pass

    def __str__(self):
        return "⊤"

    def __eq__(self, other):
        return isinstance(other, Verum)

    def propvars(self):
        return set()

    def freevars(self):
        return set()

    def boundvars(self):
        return set()

    def nonlogs(self):
        return set(), set(), set()

    def subst(self, u, t):
        return self

    def denot(self, m, v=None, w=None):
        """
        The denotation of the verum is always true.
        """
        return True

    def tableau_pos(self, node):
        pass

    def tableau_neg(self, node):
        pass


class Falsum(Formula):
    """
    Falsum.
    ⊥
    """

    def __init__(self):
        pass

    def __str__(self):
        return "⊥"

    def __eq__(self, other):
        return isinstance(other, Falsum)

    def propvars(self):
        return set()

    def freevars(self):
        return set()

    def boundvars(self):
        return set()

    def nonlogs(self):
        return set(), set(), set()

    def subst(self, u, t):
        return self

    def denot(self, m, v=None, w=None):
        """
        The denotation of the falsum is always false.
        """
        return False

    def tableau_pos(self, node):
        pass

    def tableau_neg(self, node):
        pass

class Prop(Formula):
    """
    Propositional variable.
    p, q, ...

    @attr p: the propositional variable
    @type p: str
    """

    def __init__(self, p: str):
        self.p = p

    def __str__(self):
        return self.p

    def __eq__(self, other):
        return isinstance(other, Prop) and self.p == other.p

    def propvars(self):
        return {self.p}

    def freevars(self):
        return set()

    def boundvars(self):
        return set()

    def nonlogs(self):
        return set(), set(), set()

    def subst(self, u, t):
        return self

    def denot(self, m, v=None, w=None):
        """
        The denotation of a propositional variable is the truth value the valuation function V assigns it.
        """
        v = m.v
        return v[self.p]

    def tableau_pos(self, node):
        pass

    def tableau_neg(self, node):
        pass


class Eq(Formula):
    """
    Equality between terms.
    t1 = t2

    @attr t1: the left equality term
    @type t1: Term
    @attr t2: the right equality term
    @type t2: Term
    """

    def __init__(self, t1: Term, t2: Term):
        self.t1 = t1
        self.t2 = t2

    def __str__(self):
        return str(self.t1) + " = " + str(self.t2)

    def __eq__(self, other):
        return isinstance(other, Eq) and self.t1 == other.t1 and self.t2 == other.t2

    def propvars(self):
        return set()

    def freevars(self):
        return self.t1.freevars() | self.t2.freevars()

    def boundvars(self):
        return self.t1.boundvars() | self.t2.boundvars()

    def nonlogs(self):
        return self.t1.nonlogs()[0] | self.t2.nonlogs()[0], \
               self.t1.nonlogs()[1] | self.t2.nonlogs()[1], \
               set()

    def subst(self, u, t):
        return Eq(self.t1.subst(u, t), self.t2.subst(u, t))

    def denot(self, m, v=None, w=None):
        """
        The denotation of a term equality t1 = t2 is true iff t1 and t2 denote the same individual.
        """
        return self.t1.denot(m, v, w) == self.t2.denot(m, v, w)

    def tableau_pos(self, node):
        pass

    def tableau_neg(self, node):
        pass


class Atm(Formula):
    """
    Atomic formula (predicate symbol applied to a number of terms).
    P(t1, ..., tn)

    Note that 1-place predications have to be specified as
    Atm('P', (t1, ))
    rather than
    Atm('P', (t))
    or
    Atm('P', t1).

    @attr pred: the predicate symbol
    @type pred: Pred
    @attr terms: the terms to apply the predicate symbol to
    @type terms: tuple[Term]
    """
    def __init__(self, pred: Pred, terms: Tuple[Term]):
        self.pred = pred
        self.terms = terms

    def __str__(self):
        return str(self.pred) + "(" + ",".join([str(t) for t in self.terms]) + ")"

    def __eq__(self, other):
        return isinstance(other, Atm) and self.pred == other.pred and self.terms == other.terms

    def propvars(self):
        return set()

    def freevars(self):
        return set().union(*[t.freevars() for t in self.terms])

    def boundvars(self):
        return set().union(*[t.boundvars() for t in self.terms])

    def nonlogs(self):
        return set().union(*[t.nonlogs()[0] for t in self.terms]), \
               set().union(*[t.nonlogs()[1] for t in self.terms]), \
               {self.pred.p}

    def subst(self, u, t):
        return Atm(self.pred, tuple(map(lambda t: t.subst(u, t), self.terms)))

    def denot(self, m, v=None, w=None):
        """
        The denotation of an atomic predication P(t1, ..., tn) is true iff the tuple of the denotation of the terms is
        an element of the interpretation of the predicate.
        """
        return tuple([t.denot(m, v, w) for t in self.terms]) in self.pred.denot(m, v, w)


class Neg(Formula):
    """
    Negation.
    ¬φ

    @attr phi: the negated formula
    @type phi: Formula
    """
    def __init__(self, phi: Formula):
        self.phi = phi

    def __str__(self):
        if isinstance(self.phi, Eq):
            return str(self.phi.t1) + "≠" + str(self.phi.t2)
        return "¬" + str(self.phi)

    def __eq__(self, other):
        return isinstance(other, Neg) and self.phi == other.phi

    def propvars(self):
        return self.phi.propvars()

    def freevars(self):
        return self.phi.freevars()

    def boundvars(self):
        return self.phi.boundvars()

    def nonlogs(self):
        return self.phi.nonlogs()[0], \
               self.phi.nonlogs()[1], \
               self.phi.nonlogs()[2]

    def subst(self, u, t):
        return Neg(self.phi.subst(u, t))

    def denot(self, m, v=None, w=None):
        """
        The denotation of a negated formula Neg(phi) is true iff phi is false.
        """
        return not self.phi.denot(m, v, w)

    def tableau_pos(self, node):
        """
        ¬φ
        ...
        """
        # If the negation does not occur under another neg., apply the negative tableau rule on the negative formula.
        self.phi.tableau_neg(node)

    def tableau_neg(self, node):
        """
        ¬¬φ
         φ
        """
        # If the negation is itself negated, apply the double negation elimination rule on the double negated formula.
        node.branch_unary([self.phi], "¬¬")


class Conj(Formula):
    """
    Conjunction.
    (φ∧ψ)

    @attr phi: the left conjunct
    @type phi: Formula
    @attr psi: the right conjunct
    @type psi: Formula
    """
    def __init__(self, phi: Formula, psi: Formula):
        self.phi = phi
        self.psi = psi

    def __str__(self):
        return "(" + str(self.phi) + " ∧ " + str(self.psi) + ")"

    def __eq__(self, other):
        return isinstance(other, Conj) and self.phi == other.phi and self.psi == other.psi

    def propvars(self):
        return self.phi.propvars() | self.psi.propvars()

    def freevars(self):
        return self.phi.freevars() | self.psi.freevars()

    def boundvars(self):
        return self.phi.boundvars() | self.psi.boundvars()

    def nonlogs(self):
        return self.phi.nonlogs()[0] | self.psi.nonlogs()[0], \
               self.phi.nonlogs()[1] | self.psi.nonlogs()[1], \
               self.phi.nonlogs()[2] | self.psi.nonlogs()[2]

    def subst(self, u, t):
        return Conj(self.phi.subst(u, t), self.psi.subst(u, t))

    def denot(self, m, v=None, w=None):
        """
        The denotation of a conjoined formula Con(phi,psi) is true iff phi is true and psi is true.
        """
        return self.phi.denot(m, v, w) and self.psi.denot(m, v, w)

    def tableau_pos(self, node):
        """
        (φ∧ψ)
          φ
          ψ
        """
        node.branch_unary([self.phi, self.psi], "∧")

    def tableau_neg(self, node):
        """
         ¬(φ∧ψ)
          /  \
        ¬φ   ¬ψ
        """
        node.branch_binary([Neg(self.phi)], [Neg(self.psi)], "¬∧")


class Disj(Formula):
    """
    Disjunction.
    (φ∨ψ)

    @attr phi: the left disjunct
    @type phi: Formula
    @attr psi: the right disjunct
    @type psi: Formula
    """
    def __init__(self, phi: Formula, psi: Formula):
        self.phi = phi
        self.psi = psi

    def __str__(self):
        return "(" + str(self.phi) + " ∨ " + str(self.psi) + ")"

    def __eq__(self, other):
        return isinstance(other, Disj) and self.phi == other.phi and self.psi == other.psi

    def propvars(self):
        return self.phi.propvars() | self.psi.propvars()

    def freevars(self):
        return self.phi.freevars() | self.psi.freevars()

    def boundvars(self):
        return self.phi.boundvars() | self.psi.boundvars()

    def nonlogs(self):
        return self.phi.nonlogs()[0] | self.psi.nonlogs()[0], \
               self.phi.nonlogs()[1] | self.psi.nonlogs()[1], \
               self.phi.nonlogs()[2] | self.psi.nonlogs()[2]

    def subst(self, u, t):
        return Disj(self.phi.subst(u, t), self.psi.subst(u, t))

    def denot(self, m, v=None, w=None):
        """
        The denotation of a conjoined formula Disj(phi,psi) is true iff phi is true or psi is true.
        """
        return self.phi.denot(m, v, w) or self.psi.denot(m, v, w)

    def tableau_pos(self, node):
        """
        (φ∨ψ)
         /  \
        φ   ψ
        """
        node.branch_binary([self.phi], [self.psi], "∨")

    def tableau_neg(self, node):
        """
        ¬(φ∨ψ)
          ¬φ
          ¬ψ
        """
        node.branch_unary([Neg(self.phi), Neg(self.psi)], "¬∨")


class Imp(Formula):
    """
    Implication.
    (φ→ψ)

    @attr phi: the antecedent
    @type phi: Formula
    @attr psi: the consequent
    @type psi: Formula
    """
    def __init__(self, phi: Formula, psi: Formula):
        self.phi = phi
        self.psi = psi

    def __str__(self):
        return "(" + str(self.phi) + " → " + str(self.psi) + ")"

    def __eq__(self, other):
        return isinstance(other, Imp) and self.phi == other.phi and self.psi == other.psi

    def propvars(self):
        return self.phi.propvars() | self.psi.propvars()

    def freevars(self):
        return self.phi.freevars() | self.psi.freevars()

    def boundvars(self):
        return self.phi.boundvars() | self.psi.boundvars()

    def nonlogs(self):
        return self.phi.nonlogs()[0] | self.psi.nonlogs()[0], \
               self.phi.nonlogs()[1] | self.psi.nonlogs()[1], \
               self.phi.nonlogs()[2] | self.psi.nonlogs()[2]

    def subst(self, u, t):
        return Imp(self.phi.subst(u, t), self.psi.subst(u, t))

    def denot(self, m, v=None, w=None):
        """
        The denotation of an implicational formula Imp(phi,psi) is true iff phi is false or psi is true.
        """
        return not self.phi.denot(m, v, w) or self.psi.denot(m, v, w)

    def tableau_pos(self, node):
        """
        (φ→ψ)
         /  \
        ¬φ  ψ
        """
        node.branch_binary([Neg(self.phi)], [self.psi], "→")

    def tableau_neg(self, node):
        """
        ¬(φ→ψ)
           φ
          ¬ψ
        """
        node.branch_unary([self.phi, Neg(self.psi)], "¬→")


class Biimp(Formula):
    """
    Biimplication.
    (φ↔ψ)

    @attr phi: the left formula
    @type phi: Formula
    @attr psi: the right formula
    @type psi: Formula
    """
    def __init__(self, phi: Formula, psi: Formula):
        self.phi = phi
        self.psi = psi

    def __str__(self):
        return "(" + str(self.phi) + " ↔ " + str(self.psi) + ")"

    def __eq__(self, other):
        return isinstance(other, Biimp) and self.phi == other.phi and self.psi == other.psi

    def propvars(self):
        return self.phi.propvars() | self.psi.propvars()

    def freevars(self):
        return self.phi.freevars() | self.psi.freevars()

    def boundvars(self):
        return self.phi.boundvars() | self.psi.boundvars()

    def nonlogs(self):
        return self.phi.nonlogs()[0] | self.psi.nonlogs()[0], \
               self.phi.nonlogs()[1] | self.psi.nonlogs()[1], \
               self.phi.nonlogs()[2] | self.psi.nonlogs()[2]

    def subst(self, u, t):
        return Biimp(self.phi.subst(u, t), self.psi.subst(u, t))

    def denot(self, m, v=None, w=None):
        """
        The denotation of an biimplicational formula Biimp(phi,psi) is true iff phi and psi have the same truth value.
        """
        return self.phi.denot(m, v, w) == self.psi.denot(m, v, w)

    def tableau_pos(self, node):
        """
         (φ↔ψ)
         /  \
        φ   ¬φ
        ψ   ¬ψ
        """
        node.branch_binary([self.phi, self.psi], [Neg(self.phi), Neg(self.psi)], "↔")

    def tableau_neg(self, node):
        """
         (φ↔ψ)
          /  \
         φ   ¬φ
        ¬ψ    ψ
        """
        node.branch_binary([self.phi, Neg(self.psi)], [Neg(self.phi), self.psi], "¬↔")


class Exists(Formula):
    """
    Existential quantification.
    ∃xφ

    @attr u: the binding variable
    @type u: Var
    @attr phi: the formula to be quantified
    @type phi: Formula
    """
    def __init__(self, u: Var, phi: Formula):
        self.u = u
        self.phi = phi

    def __str__(self):
        return "∃" + str(self.u) + str(self.phi)

    def __eq__(self, other):
        return isinstance(other, Exists) and self.u == other.u and self.phi == other.phi

    def propvars(self):
        return set()

    def freevars(self):
        return self.phi.freevars() - {self.u.u}

    def boundvars(self):
        return self.phi.boundvars() | {self.u.u}

    def nonlogs(self):
        return self.phi.nonlogs()

    def subst(self, u, t):
        if u.u == self.u:
            return self
        else:
            return self.phi.subst(u, t)

    def denot(self, m, v=None, w=None):
        """
        The denotation of an existentially quantified formula Exists(x, phi) is true
        iff phi is true under at least one x-variant of v.
        """
        global verbose
        d = m.d
        if isinstance(m, VarModalStructure):
            d = m.d[w]

        # short version
        if not verbose:
            return any([self.phi.denot(m, {**v, self.u.u: d_}) for d_ in d])

        # long version
        global depth
        depth += 1

        # iterate through the individuals in the domain
        for d_ in sorted(d):

            # compute the x-variant v' of v
            v_ = v  # v' is just like v, except...
            v_[self.u.u] = d_  # ... the value for the variable u is now the new individual d

            # check whether the current x-variant under consideration makes phi true
            print((depth * 2 * " ") + "checking v" + (depth * "'") + "(" + str(self.u) + ") := " + str(d_) + " ...")
            witness = self.phi.denot(m, v_, w)

            # if yes, we found a witness, the existential statement is true, and we can stop checking (return)
            if witness:
                print((depth * 2 * " ") + "✓")
                depth -= 1
                return True

            # if not, we do nothing and try with the next one (continue)
            else:
                print((depth * 2 * " ") + "✗")
                continue

        # if we reach the end, then no witness has been found, and the existential statement is false
        depth -= 1
        return False

    def tableau_pos(self, node):
        """
        ∃xφ(x)
         φ(c)
        where c is new
        """
        node.branch_delta(self.phi, self.u, "∃")

    def tableau_neg(self, node):
        """
        ¬∃xφ(x)
         ¬φ(c)
        where c is arbitrary
        """
        node.branch_gamma(Neg(self.phi), self.u, "¬∃")


class Forall(Formula):
    """
    Universal quantification.
    ∀xφ

    @attr u: the binding variable
    @type u: Var
    @attr phi: the formula to be quantified
    @type phi: Formula
    """
    def __init__(self, u: Var, phi: Formula):
        self.u = u
        self.phi = phi

    def __str__(self):
        return "∀" + str(self.u) + str(self.phi)

    def __eq__(self, other):
        return isinstance(other, Forall) and self.u == other.u and self.phi == other.phi

    def propvars(self):
        return set()

    def freevars(self):
        return self.phi.freevars() - {self.u.u}

    def boundvars(self):
        return self.phi.boundvars() | {self.u.u}

    def nonlogs(self):
        return self.phi.nonlogs()

    def subst(self, u, t):
        if u.u == self.u:
            return self
        else:
            return self.phi.subst(u, t)

    def denot(self, m, v=None, w=None):
        """
        The denotation of universally quantified formula Forall(x, phi) is true iff
        phi is true under all x-variants of v.
        """
        global verbose
        d = m.d
        if isinstance(w, VarModalStructure):
            d = m.d[w]

        # short version
        if not verbose:
            return all([self.phi.denot(m, {**v, self.u.u: d_}) for d_ in d])

        # long version
        global depth
        depth += 1

        # iterate through the individuals in the domain
        for d_ in sorted(d):

            # compute the x-variant v' of v
            v_ = v  # v' is just like v, except...
            v_[self.u.u] = d_  # ... the value for the variable u is now the new individual d

            # check whether the current x-variant under consideration makes phi true
            print((depth * 2 * " ") + "checking v" + (depth * "'") + "(" + str(self.u) + ") := " + str(d_) + " ...")
            witness = self.phi.denot(m, v_, w)

            # if yes, everything is fine until now, we do nothing and go check the next one (continue)
            if witness:
                print((depth * 2 * " ") + "✓")
                continue

            # if not, we found a counter witness, the universal statement is false, and we can stop checking (return)
            else:
                print((depth * 2 * " ") + "✗")
                depth -= 1
                return False

        # if we reach the end, then no counter witness has been found, and the universal statement is true
        depth -= 1
        return True

    def tableau_pos(self, node):
        """
        ∀xφ(x)
         φ(c)
        where c is arbitrary
        """
        node.branch_gamma(self.phi, self.u, "∀")

    def tableau_neg(self, node):
        """
        ¬∀xφ(x)
         ¬φ(c)
        where c is new
        """
        node.branch_delta(self.phi, self.u, "¬∀")


class Poss(Formula):
    """
    Possibility.
    ◇φ

    @attr phi: the formula to apply the modal operator to
    @type phi: Expr
    """
    def __init__(self, phi: Formula):
        self.phi = phi

    def __str__(self):
        return "◇" + str(self.phi)

    def __eq__(self, other):
        return isinstance(other, Poss) and self.phi == other.phi

    def propvars(self):
        return self.phi.propvars()

    def freevars(self):
        return self.phi.freevars()

    def boundvars(self):
        return self.phi.boundvars()

    def nonlogs(self):
        return self.phi.nonlogs()

    def subst(self, u, t):
        return Poss(self.phi.subst(u, t))

    def denot(self, m, v, w):
        """
        The denotation of a possiblity formula is true iff
        phi is true at at least one world accessible from w.

        @param m: the structure to evaluate the formula in
        @type m: ModalStructure
        @param v: the assignment function to evaluate the formula in
        @type v: dict[str,str]
        @param w: the world to evaluate the formula in
        @type w: str
        @return: the denotation of Poss(phi)
        """
        # all possible worlds w' which are accessible from w
        neighbors = [w_ for w_ in m.w if (w, w_) in m.r]

        # short version
        if not verbose:
            return any([self.phi.denot(m, v, w_) for w_ in neighbors])

        # long version
        global depth
        depth += 1

        # iterate through ws neighbors w'
        for w_ in neighbors:

            # check whether phi is true in w
            print((depth * "  ") + "checking w" + (depth * "'") + " := " + str(w_) + " ...")
            witness = self.phi.denot(m, v, w_)

            # if yes, we found a witnessing neighbor, the poss. statement is true, and we can stop checking (return)
            if witness:
                print((depth * 2 * " ") + "✓")
                print((depth * 2 * " ") + "neighbor: w" + (depth * "'") + " := " + str(w_))
                depth -= 1
                return True

            # if not, we do nothing and try with the next one (continue)
            else:
                print((depth * 2 * " ") + "✗")
                continue

        # if no witness has been found, the possibility statement is false
        depth -= 1
        return False

    def tableau_pos(self, node):
        """
        σ  ◇φ
        σ.n φ
        where σ.n is new
        """
        node.branch_mu(self.phi, node.sig)

    def tableau_neg(self, node):
        """
        σ  ¬◇φ
        σ.n ¬φ
        where σ.n is old
        """
        node.branch_nu(Neg(self.phi), node.sig)


class Nec(Formula):
    """
    Necessity.
    ◻φ

    @attr phi: the formula to apply the modal operator to
    @type phi: Expr
    """

    def __init__(self, phi: Formula):
        self.phi = phi

    def __str__(self):
        return "◻" + str(self.phi)

    def __eq__(self, other):
        return isinstance(other, Nec) and self.phi == other.phi

    def propvars(self):
        return self.phi.propvars()

    def freevars(self):
        return self.phi.freevars()

    def boundvars(self):
        return self.phi.boundvars()

    def nonlogs(self):
        return self.phi.nonlogs()

    def subst(self, u, t):
        return Poss(self.phi.subst(u, t))

    def denot(self, m, v, w):
        """
        The denotation of a necessity formula is true iff
        phi is true at all worlds accessible from w.

        @param m: the structure to evaluate the formula in
        @type m: ModalStructure
        @param w: the world to evaluate the formula in
        @type w: str
        @param v: the assignment function to evaluate the formula in
        @type v: dict[str,str]
        """
        # all possible worlds w' which are accessible from w
        neighbors = [w_ for w_ in m.w if (w, w_) in m.r]

        # short version
        if not verbose:
            return all([self.phi.denot(m, v, w_) for w_ in neighbors])

        # long version
        global depth
        depth += 1

        # iterate through ws neighbors w'
        for w_ in neighbors:

            # check whether phi is true in w
            print((depth * "  ") + "checking w" + (depth * "'") + " := " + str(w_) + " ...")
            witness = self.phi.denot(m, v, w_)

            # if yes, everything is fine until now, we do nothing and go check the next one (continue)
            if witness:
                print((depth * 2 * " ") + "✓")
                continue

            # if not, we found a counter neighbor, the necessity statement is false, and we can stop checking
            else:
                print((depth * 2 * " ") + "✗")
                print((depth * 2 * " ") + "counter neighbor: w" + (depth * "'") + " := " + str(w_))
                depth -= 1
                return False

        # if no counter neighbor has been found, the necessity statement is true
        depth -= 1
        return True

    def tableau_pos(self, node):
        """
        σ  ◻φ
        σ.n φ
        where σ.n is old
        """
        node.branch_nu(self.phi, node.sig)

    def tableau_neg(self, node):
        """
        σ  ¬◻φ
        σ.n ¬φ
        where σ.n is new
        """
        node.branch_mu(Neg(self.phi), node.sig)


class Open(Formula):
    """
    Special pseudo-formula indicating a branch is open.
    ○
    """

    def __init__(self):
        pass

    def __str__(self):
        return "○"


class Closed(Formula):
    """
    Special pseudo-formula indicating a branch is closed.
    ×
    """

    def __init__(self):
        pass

    def __str__(self):
        return "×"