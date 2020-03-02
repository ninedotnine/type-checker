#1/usr/bin/python3

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

Foo = BaseType("foo")
Bar = BaseType("bar")
Baz = BaseType("baz")

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


def judgement_type(thing):
    """returns true if its argument is a valid type"""
    try:
        if thing.tag == "->":
            return judgement_type(thing.domain) and judgement_type(thing.rang)

        if thing.tag == "*" or thing.tag == "+":
            return judgement_type(thing.left) and judgement_type(thing.right)

        return thing.tag.isalpha()
    except AttributeError:
        print("something is wonky with your types")
        return False


class Context():
    # uses a dict to map names to types
    tag = "{}"

    def __init__(self, entries, subset=None):
        self.entries = dict()

        if subset:
            if not judgement_ctx(subset):
                raise TypeError("'subset' is not a valid context")
            for (name, name_type) in subset:
                self.entries[name] = name_type

        for (name, name_type) in entries.items():
            if not judgement_type(name_type):
                raise TypeError(f"name_type '{name_type}' is not a valid type")
            if name in self.entries:
                raise ValueError(f"name {name} is already in use")
            self.entries[name] = name_type

    def __contains__(self, name):
        return name in self.entries.keys()

    def __iter__(self):
        for name, name_type in self.entries.items():
            yield name, name_type

    def __repr__(self):
        return f"context of {self.entries}"


def judgement_ctx(context):
    """returns true if its argument is a valid context"""
    try:
        for t in context.entries.values():
            if not judgement_type(t):
                return False
        return True
    except AttributeError:
        print("something is wonky with your context-dict")
        return False


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


def judgement_check(context, m, a):
    """returns true if 'm' has type 'a' in 'context'"""
    if m.tag == "^_^":
        return context.entries.get(m.name) == a

    if m.tag == "&":
        if a.tag != "*":
            print("pair should have type *")
            return False
        return (judgement_check(context, m.first, a.left)
                and judgement_check(context, m.second, a.right))

    if m.tag == ".&.":
        new_context = Context({m.x_name: m.x_type, m.y_name: m.y_type}, context)
        return (judgement_check(context, m.pair, Product(m.x_type, m.y_type))
                and judgement_check(new_context, m.body, a))

    if m.tag == "|":
        if a.tag != "+":
            print("sum should have type +")
            return False
        return (judgement_check(context, m.first, a.left)
                and judgement_check(context, m.second, a.right))

    if m.tag == ".|.":
        new_context = Context({m.x_name: m.x_type, m.y_name: m.y_type}, context)
        return (judgement_check(context, m.either, Sum(m.x_type, m.y_type))
                and judgement_check(new_context, m.body, a))

    if m.tag == "\\":
        if a.tag != "->":
            print("function should have type ->")
            return False
        return judgement_check(Context({m.name: a.domain}, context), m.body, a.rang)

    if m.tag == "$":
        return (judgement_check(context, m.func, Arrow(m.arg_type, a))
                and judgement_check(context, m.arg, m.arg_type))

    return False


def demo_types():
    x = Foo
    print(f"x is {x}")
    assert( judgement_type(x) )
    assert( x == Foo )

    y = Bar
    print(f"y is {y}")
    assert( judgement_type(y) )
    assert( x != y )

    p = Product(x,y)
    print(f"p is {p}")
    assert( judgement_type(p) )
    assert( p == Product(Foo, Bar) )

    s = Sum(x,y)
    print(f"s is {s}")
    assert( judgement_type(s) )
    assert( s == Sum(Foo, Bar) )

    f = Arrow(x,p)
    print(f"f is {f}")
    assert( judgement_type(f) )
    assert( f == Arrow(Foo, Product(Foo, Bar)) )


def demo_contexts():
    e = Context({})
    print(f"e is {e}")
    assert( judgement_ctx(e) )
    assert( "name" not in e )

    c = Context({"var": Foo}, e)
    print(f"c is {c}")
    assert( judgement_ctx(c) )
    assert( "var" in c )
    assert( "name" not in c )

    v = V("var")
    print(f"v is {v}")
    assert( judgement_check(c, v, Foo) )

    v2 = V("val")
    print(f"v2 is {v2}")
    c2 = Context({"val": Bar}, c)
    print(f"c2 is {c2}")
    assert( judgement_ctx(c2) )
    assert( judgement_check(c2, v2, Bar) )

    v3 = Pair(v, v2)
    print(f"v3 is {v3}")
    assert( judgement_check(c2, v3, Product(Foo, Bar)) )

    c3 = Context({"pairofvars": Product(Foo, Bar)}, e)
    print(f"c3 is {c3}")
    assert( judgement_ctx(c3) )

    v4 = SplitPair(V("pairofvars"), "var", Foo, "val", Bar, V("var"))
    print(f"v4 is {v4}")
    assert( judgement_check(c3, v4, Foo) )

    v5 = MakeLambda("x", V("x"))
    print(f"v5 is {v5}")
    assert( judgement_check(e, v5, Arrow(Foo, Foo)) )

    c4 = Context({"f": Arrow(Foo, Bar)}, c2)
    print(f"c4 is {c4}")
    assert( judgement_ctx(c4) )
    v6 = Apply(V("f"), V("var"), Foo)
    print(f"v6 is {v6}")
    assert( judgement_check(c4, v6, Bar) )

    v7 = Either(v, v2)
    print(f"v7 is {v7}")
    assert( judgement_check(c2, v7, Sum(Foo, Bar)) )

    c5 = Context({"eitherfooorbar": Sum(Foo, Bar)}, e)
    print(f"c5 is {c5}")
    assert( judgement_ctx(c5) )
    v8 = SplitEither(V("eitherfooorbar"), "var", Foo, "val", Bar, V("var"))
    print(f"v8 is {v8}")
    assert( judgement_check(c5, v8, Foo) )



def examples():
    e = Context({})
    fst_defn = MakeLambda("p", SplitPair(V("p"), "x", Foo, "y", Bar, V("x")))
    fst_type = Arrow(Product(Foo, Bar), Foo)
    assert( judgement_check(e, fst_defn, fst_type) )

    snd_defn = MakeLambda("p",SplitPair(V("p"), "x", Foo, "y", Bar, V("y")))
    snd_type = Arrow(Product(Foo, Bar), Bar)
    assert( judgement_check(e, snd_defn, snd_type) )

    # \x -> (x,x)
    tuplify_defn = MakeLambda("x", Pair(V("x"), V("x")))
    tuplify_type = Arrow(Foo, Product(Foo, Foo))
    assert( judgement_check(e, tuplify_defn, tuplify_type) )

    # const
    const_defn = MakeLambda("x", MakeLambda("y", V("x")))
    const_type = Arrow(Foo, Arrow(Bar, Foo))
    assert( judgement_check(e, const_defn, const_type) )

    # ($)
    apply_defn = MakeLambda("f", MakeLambda("x", Apply(V("f"), V("x"), Foo)))
    apply_type = Arrow(Arrow(Foo, Bar), Arrow(Foo, Bar))
    assert( judgement_check(e, apply_defn, apply_type) )

    # flip ($)
    after_defn = MakeLambda("x", MakeLambda("f", Apply(V("f"), V("x"), Foo)))
    after_type = Arrow(Foo, Arrow(Arrow(Foo, Bar), Bar))
    assert( judgement_check(e, after_defn, after_type) )

    curry_defn = MakeLambda("f", MakeLambda("x", MakeLambda("y",
                    Apply(V("f"), Pair(V("x"), V("y")), Product(Foo, Bar)))))
    curry_type = Arrow(Arrow(Product(Foo, Bar), Baz), Arrow(Foo, Arrow(Bar, Baz)))
    assert( judgement_check(e, curry_defn, curry_type) )

    uncurry_defn = MakeLambda("f", MakeLambda("p", SplitPair(V("p"), "x", Foo, "y", Bar,
                    Apply(Apply(V("f"), V("x"), Foo), V("y"), Bar))))
    uncurry_type = Arrow(Arrow(Foo, Arrow(Bar, Baz)), Arrow(Product(Foo, Bar), Baz))
    assert( judgement_check(e, uncurry_defn, uncurry_type) )

demo_types()
demo_contexts()
examples()
