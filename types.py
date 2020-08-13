#!/usr/bin/python3

def judgement_type(thing):
    """returns true if its argument is a valid type"""
    try:
        if thing.tag == "*" or thing.tag == "+":
            return judgement_type(thing.left) and judgement_type(thing.right)

        if thing.tag == "->":
            return judgement_type(thing.domain) and judgement_type(thing.rang)

        return thing.tag.isalpha()
    except AttributeError:
        print("something is wonky with your types")
        return False


class BaseType():
    def __init__(self, name):
        if not name.isalpha():
            raise ValueError("type names should be alphabetical.")
        self.tag = name

    def __repr__(self):
        return f"{self.tag}"

    def __eq__(self, other):
        try:
            return other.tag == self.tag
        except AttributeError:
            return False

class Product(BaseType):
    tag = "*"

    def __init__(self, left, right):
        if not judgement_type(left):
            raise TypeError("'left' is not a valid type")
        if not judgement_type(right):
            raise TypeError("'right' is not a valid type")

        self.left = left
        self.right = right

    def __eq__(self, other):
        try:
            return (other.tag == "*"
                    and self.left == other.left
                    and self.right == other.right)
        except AttributeError:
            return False

    def __repr__(self):
        return f"({self.left} & {self.right})"


class Sum(BaseType):
    tag = "+"

    def __init__(self, left, right):
        if not judgement_type(left):
            raise TypeError("'left' is not a valid type")
        if not judgement_type(right):
            raise TypeError("'right' is not a valid type")

        self.left = left
        self.right = right

    def __eq__(self, other):
        try:
            return (other.tag == "+"
                    and self.left == other.left
                    and self.right == other.right)
        except AttributeError:
            return False

    def __repr__(self):
        return f"({self.left} + {self.right})"


class Arrow(BaseType):
    tag = "->"

    def __init__(self, domain, rang):
        if not judgement_type(domain):
            raise TypeError("'domain' is not a valid type")
        if not judgement_type(rang):
            raise TypeError("'rang' is not a valid type")

        self.domain = domain
        self.rang = rang

    def __eq__(self, other):
        try:
            return (other.tag == "->"
                    and self.domain == other.domain
                    and self.rang == other.rang)
        except AttributeError:
            return False

    def __repr__(self):
        return f"({self.domain} -> {self.rang})"


class V():
    tag = "^_^"

    def __init__(self, name):
        if not name.isalpha():
            raise ValueError("variable names should be alphabetical.")
        self.name = name

    def __repr__(self):
        return f"variable {self.name}"


class Pair():
    tag = "&"

    def __init__(self, first, second):
        self.first = first
        self.second = second

    def __repr__(self):
        return f"pair containing {self.first} and {self.second}"

class SplitPair():
    # pattern matching on Pairs
    tag = ".&."

    def __init__(self, p, x_name, x_type, y_name, y_type, body):
        if not judgement_type(x_type):
            raise TypeError("'x_type' is not a valid type")
        if not judgement_type(y_type):
            raise TypeError("'y_type' is not a valid type")

        self.pair = p
        self.x_name = x_name
        self.x_type = x_type
        self.y_name = y_name
        self.y_type = y_type
        self.body = body

    def __repr__(self):
        return f"{self.body} where {self.x_name}:{self.x_type} and {self.y_name}:{self.y_type}"


class Either():
    tag = "|"

    def __init__(self, first, second):
        self.first = first
        self.second = second

    def __repr__(self):
        return f"{self.first} | {self.second}"

class SplitEither():
    # pattern matching on Either
    tag = ".|."

    def __init__(self, e, x_name, x_type, y_name, y_type, body):
        if not judgement_type(x_type):
            raise TypeError("'x_type' is not a valid type")
        if not judgement_type(y_type):
            raise TypeError("'y_type' is not a valid type")

        self.either = e
        self.x_name = x_name
        self.x_type = x_type
        self.y_name = y_name
        self.y_type = y_type
        self.body = body

    def __repr__(self):
        return f"{self.body} where {self.x_name}:{self.x_type} and {self.y_name}:{self.y_type}"


class MakeLambda():
    # functions
    tag = "\\"

    def __init__(self, x, m):
        self.name = x
        self.body = m

    def __repr__(self):
        return f"\{self.body} -> {self.name}"

class Apply():
    tag = "$"

    def __init__(self, f, n, a):
        if not judgement_type(a):
            raise TypeError("'a' is not a valid type")

        self.func = f
        self.arg = n
        self.arg_type = a

    def __repr__(self):
        return f"{self.func}({self.arg}:{self.arg_type})"
