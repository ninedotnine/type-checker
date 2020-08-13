#!/usr/bin/python3

from types import *
from contexts import *

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
