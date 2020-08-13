#!/usr/bin/python3

from types import *
from contexts import *
from typechecker import *


Foo = BaseType("foo")
Bar = BaseType("bar")
Baz = BaseType("baz")


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

    snd_defn = MakeLambda("p", SplitPair(V("p"), "x", Foo, "y", Bar, V("y")))
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
