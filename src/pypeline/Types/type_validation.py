from ..Step.step import step as base_step
from ..Extract.extractor import extractor as base_extractor
from ..Load.loader import loader as base_loader
from ..Context.Context import context as base_context

def is_extractor(extractor, _raise=False):
    if not isinstance(extractor, base_extractor):
        if _raise:
            raise TypeError("Not of type Extractor")
        return False
    return True

def is_loader(loader, _raise=False):
    if not isinstance(loader, base_loader):
        if _raise:
            raise TypeError("Not of type Loader")
        return False
    return True

def is_step(step, _raise=False):
    if not isinstance(step, base_step):
        if _raise:
            raise TypeError("Not of type Step")
        return False
    return True

def is_context(context, _raise=False):
    if not isinstance(context, base_context):
        if _raise:
            raise TypeError("Not of type Context")
        return False
    return True

def is_context_object(context, _raise=False):
    if not isinstance(context, dict):
        if _raise:
            raise TypeError("Not of type Context")
        return False
    for _, item in context.items():
        if not is_context(item, _raise):
            return False
    return True
