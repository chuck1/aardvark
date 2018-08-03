import aardvark

def _clean(d0):
    assert isinstance(d0, dict)
    
    # yield key value pairs that have been cleaned

    for k, v in d0.items():
        if k.startswith("_"): continue
        yield k, clean(v)

def clean_list(l):
    return [clean(_) for _ in l]

def clean(d0):
    if isinstance(d0, list): return clean_list(d0)

    if not isinstance(d0, dict): return d0

    return dict((k, v) for k, v in _clean(d0))

 
def diffs_keys_set(diffs):
    for d in diffs:
        if len(d.address.lines) > 1:
            yield d.address.lines[0].key

        if isinstance(d, aardvark.OperationRemove):
            continue
        
        yield d.address.lines[0].key

def diffs_keys_unset(diffs):
    for d in diffs:
        if isinstance(d, aardvark.OperationRemove):
            if len(d.address.lines) == 1:
                yield d.address.lines[0].key

def diffs_to_update(diffs, item):

    update_unset = dict((k, "") for k in diffs_keys_unset(diffs))
    update_set = dict((k, item[k]) for k in diffs_keys_set(diffs))

    update = {} 

    if update_set:
        update['$set'] = update_set

    if update_unset:
        update['$unset'] = update_unset

    return update

def from_array(d, functions):

    #print('from_array', d, list(d.items())[0])

    s, args = list(d.items())[0]

    f = functions[s]

    if isinstance(args, list):
        return f(*args)
    else:
        return f(args)

def maybe_dict_func(a, functions):
    if isinstance(a, dict):
        return from_array(a, functions)
    else:
        return a


