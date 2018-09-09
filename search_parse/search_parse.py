from pendulum import parse

__all__=['getValidType', 'allowsPrefix', 'getPrefix', 'validModifier', 'getModifier']

search_types = {
        'number': float,
        'string': str,
        'reference': str,
        'token': str,
        'date': parse,
        'composite': str,
        'quantity': str,
        'uri': str
        }

prefixes = ['eq', 'ne', 'gt', 'lt', 'ge', 'le', 'sa', 'eb', 'ap']
mods = ['exact', 'missing', 'exact', 'contains', 'text', 'in', 'above', 'below', 'not-in']

#### TYPE #####
def getValidType(type_, value):
    """
    Returns parsed value if correct type or False
    """
    try:
        return search_types[type_](value)
    except:
        return False
#### /TYPE #####

#### PREFIX #####
def allowsPrefix(type_):
    """
    Only number, date, and quantity allow prefixes
    """
    if type_ in ('number','date', 'quantity'):
        return True
    else:
        return False

def getPrefix(value):
    """
    Returns (prefix, base_value) or (None, base_value)
    """
    for pf in prefixes:
        if value.startswith(pf):
            return value[:2], value[2:]
    return None, value
#### /PREFIX #####

#### MODIFIER #####
def validModifier(modifier, type_):
    """
    All types allow certain modifiers, consequently need type of parameter, too, for further validation

    Returns true if type allows modifier, else false
    """
    # TODO Add reference 'type' modifier logic
    if modifier == 'missing': return True
    if modifier in ('exact', 'contains') and type_ == 'string': return True
    if modifier in ('text', 'in', 'below', 'above', 'not-in') and type_ == 'token': return True
    if modifier in ('below', 'above') and type_ == 'uri': return True
    if type_ == reference: return True
    return False


def getModifier(parameter):
    """
    Returns (base_paramater, mod) or (parameter, None)

    Base modifiers search, then do split on colons
    """
    if ':' in parameter:
        for mod in mods:
            if parameter.endswith(mod):
                return parameter[:len(mod)-1], mod

        base, mod = parameter.split(':')
        return base, mod

    return parameter, None
#### /MODIFIER #####
