#!/usr/bin/env python
import ROOT
import array

def deepGetattr(obj, attr):
    """Recurses through an attribute chain to get the ultimate value.
        via http://pingfive.typepad.com/blog/2010/04/deep-getattr-python-function.html"""
    try:
        return float(attr)
    except ValueError:
        return evaluateNested(getattr, attr.split('.'), obj)
def evaluateNested(func, iterable, start=None):
    it = iter(iterable)
    if start is None:
        try:
            start = next(it)
        except StopIteration:
            raise TypeError('reduce() of empty sequence with no initial value')
    accum_value = start
    for x in iterable:
        split = str(x).strip(")").split("(")
        function_call = split[0]
        accum_value = func(accum_value, function_call)
        if len(split) != 1:
            if len(split[1]) == 0:
                accum_value = accum_value()
            else:
                func_args = split[1].split(",")
                accum_value = accum_value(*func_args)
    return accum_value
def setAttributes(tObject, attributes):
    functions = []
    for function_call, params in attributes.iteritems():
        if not isinstance(params, list): 
            params = [params]
        parsed_params = []
        for param in params:
            param_str = str(param)
            if "ROOT" in param_str:
                expr = param_str.replace("ROOT.", "")
                if "+" in param_str:
                    values = [x.strip() for x in expr.split("+")]
                    root_val = deepGetattr(ROOT, values[0])
                    root_val += int(values[1]) 
                elif "-" in param_str:
                    values = [x.strip() for x in expr.split("-")]
                    root_val =deepGetattr(ROOT, values[0])
                    root_val -= int(values[1]) 
                else:
                    root_val = deepGetattr(ROOT, expr)
                param = root_val
            parsed_params.append(param)
        deepGetattr(tObject, function_call)(*parsed_params)
