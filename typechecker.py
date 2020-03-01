#1/usr/bin/python3

class BaseType():
    def __init__(self, name):
        self.tag = name

    def __str__(self):
        return f"{self.tag}"

    def __eq__(self, other):
        return other.tag == self.tag

Foo = BaseType("foo")
Bar = BaseType("bar")
Baz = BaseType("baz")

class Pair(BaseType):
    tag = "&"

    def __init__(self, left, right):
        if not judgement_type(left):
            raise TypeError("'left' is not a valid type")
        if not judgement_type(right):
            raise TypeError("'right' is not a valid type")

        self.left = left
        self.right = right

    def __eq__(self, other):
        try:
            return (other.tag == "&"
                    and self.left == other.left
                    and self.right == other.right)
        except AttributeError:
            return False

    def __str__(self):
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

    def __str__(self):
        return f"({self.domain} -> {self.rang})"


def judgement_type(thing):
    """returns true if its argument is a valid type"""
    try:
        if thing.tag == "->":
            return judgement_type(thing.domain) and judgement_type(thing.rang)

        if thing.tag == "&":
            return judgement_type(thing.left) and judgement_type(thing.right)

        return thing.tag == "foo" or thing.tag == "bar" or thing.tag == "baz"
    except AttributeError:
        print("something is wonky with your types")
        return False


class EmptyContext():
    tag = "empty"

    def __str__(self):
        return "empty context"

    def __contains__(self, anything):
        return False

class ContextWith():
    # dan get rid of this linked list; use a python list instead []
    tag = ":,"

    def __init__(self, rest, name, name_type):
        if not judgement_type(name_type):
            raise TypeError("'name_type' is not a valid type")
        if not judgement_ctx(rest):
            raise TypeError("'rest' is not a valid context")

        self.rest = rest
        self.name = name
        self.name_type = name_type

    def __str__(self):
        return f"{self.name}:{self.name_type}, {self.rest}"

    def __contains__(self, name):
        if self.tag ==  "empty":
            return False
        else:
            if name == self.name:
                return True
            else:
                return name in self.rest


def judgement_ctx(context):
    """returns true if its argument is a valid context"""
    try:
        if context.tag == ":,":
            return (judgement_ctx(context.rest)
                    and judgement_type(context.name_type)
                    and context.name not in context.rest)
        else:
            return context.tag == "empty"
    except AttributeError:
        print("something is wonky with your types")
        return False


class V():
    tag = "variable"

    def __init__(self, name):
        self.name = name

    def __str__(self):
        return f"variable {self.name}"

class MakeVar():
    tag = "variable"

    def __init__(self, name, name_type):
        if not judgement_type(name_type):
            raise TypeError(f"{name_type} is not any known type")

        self.name = name
        self.name_type = name_type

    def __str__(self):
        return f"variable {self.name} of {self.name_type}"


class MakePair():
    tag = "(,)"

    def __init__(self, first, second):
        self.first = first
        self.second = second

    def __str__(self):
        return f"pair containing {self.first} and {self.second}"

class SplitPair():
    # pattern matching on Pairs
    tag = "split"

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


    def __str__(self):
        return f"{self.body} where {self.x_name}:{self.x_type} and {self.y_name}:{self.y_type}"


class MakeLambda():
    # functions
    tag = "lambda"

    def __init__(self, x, m):
        self.name = x
        self.body = m

    def __str__(self):
        return f"\{self.body} -> {self.name}"


class Apply():
    tag = "apply"

    def __init__(self, f, n, a):
        if not judgement_type(a):
            raise TypeError("'a' is not a valid type")

        self.func = f
        self.arg = n
        self.arg_type = a

    def __str__(self):
        return f"{self.func}({self.arg}:{self.arg_type})"

def var_has_type(n, a, context):
    if context.tag == "empty":
        return False
    if context.tag == ":,":
        if n == context.name:
            return a == context.name_type
    return var_has_type(n, a, context.rest)


def judgement_check(context, m, a):
    """returns true if 'm' has type 'a' in 'context'"""
    if m.tag == "variable":
        return var_has_type(m.name, a, context)

    if m.tag == "(,)":
        if a.tag != "&":
            print("pair should have type &")
            return False
        return (judgement_check(context, m.first, a.left)
                and judgement_check(context, m.second, a.right))

    if m.tag == "split":
        new_context = ContextWith(context, m.x_name, m.x_type)
        new_context = ContextWith(new_context, m.y_name, m.y_type)
        return (judgement_check(context, m.pair, Pair(m.x_type, m.y_type))
                and judgement_check(new_context, m.body, a))

    if m.tag == "lambda":
        if a.tag != "->":
            print("function should have type ->")
            return False
        return judgement_check(ContextWith(context, m.name, a.domain), m.body, a.rang)

    if m.tag == "apply":
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

    p = Pair(x,y)
    print(f"p is {p}")
    assert( judgement_type(p) )
    assert( p == Pair(Foo, Bar) )

    f = Arrow(x,p)
    print(f"f is {f}")
    assert( judgement_type(f) )
    assert( f == Arrow(Foo, Pair(Foo, Bar)) )


def demo_contexts():
    e = EmptyContext()
    print(f"e is {e}")
    assert( judgement_ctx(e) )
    assert( "name" not in e )

    c = ContextWith(e, "var", Foo)
    print(f"c is {c}")
    assert( judgement_ctx(c) )
    assert( "var" in c )
    assert( "name" not in c )


    assert (var_has_type("var", Foo, c))

    v = V("var")
    print(f"v is {v}")
    assert( judgement_check(c, v, Foo) )

    v2 = V("val")
    print(f"v2 is {v2}")
    c2 = ContextWith(c, "val", Bar)
    print(f"c2 is {c2}")
    assert( judgement_check(c2, v2, Bar) )

    v3 = MakePair(v, v2)
    print(f"v3 is {v3}")
    assert( judgement_check(c2, v3, Pair(Foo,Bar)) )

    c3 = ContextWith(e, "pairofvars", Pair(Foo, Bar))
    print(f"c3 is {c3}")

    v4 = SplitPair(V("pairofvars"), "var", Foo, "val", Bar, V("var"))
    print(f"v4 is {v4}")
    assert( judgement_check(c3, v4, Foo) )

    v5 = MakeLambda("x", V("x"))
    print(f"v5 is {v5}")
    assert( judgement_check(e, v5, Arrow(Foo, Foo)) )

    c4 = ContextWith(c2, "f", Arrow(Foo, Bar))
    print(f"c4 is {c4}")
    v6 = Apply(V("f"), V("var"), Foo)
    print(f"v6 is {v6}")
    assert( judgement_check(c4, v6, Bar) )


def examples():
    e = EmptyContext()
    fst_defn = MakeLambda("p", SplitPair(V("p"), "x", Foo, "y", Bar, V("x")))
    fst_type = Arrow(Pair(Foo, Bar), Foo)
    assert( judgement_check(e, fst_defn, fst_type) )

    snd_defn = MakeLambda("p",SplitPair(V("p"), "x", Foo, "y", Bar, V("y")))
    snd_type = Arrow(Pair(Foo, Bar), Bar)
    assert( judgement_check(e, snd_defn, snd_type) )

    # \x -> (x,x)
    tuplify_defn = MakeLambda("x", MakePair(V("x"), V("x")))
    tuplify_type = Arrow(Foo, Pair(Foo, Foo))
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
                    Apply(V("f"), MakePair(V("x"), V("y")), Pair(Foo, Bar)))))
    curry_type = Arrow(Arrow(Pair(Foo, Bar), Baz), Arrow(Foo, Arrow(Bar, Baz)))
    assert( judgement_check(e, curry_defn, curry_type) )

    uncurry_defn = MakeLambda("f", MakeLambda("p", SplitPair(V("p"), "x", Foo, "y", Bar,
                    Apply(Apply(V("f"), V("x"), Foo), V("y"), Bar))))
    uncurry_type = Arrow(Arrow(Foo, Arrow(Bar, Baz)), Arrow(Pair(Foo, Bar), Baz))
    assert( judgement_check(e, uncurry_defn, uncurry_type) )

demo_types()
demo_contexts()
examples()
