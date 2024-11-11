from abc import ABC, abstractmethod
import json
from .datatypes.rest_decoder import RestDecoder


class SourcesError(Exception):
    pass

class Sources(ABC):
    @abstractmethod
    def __init__(self):
        pass

    @abstractmethod
    def set(self, param_name, value):
        pass

    @abstractmethod
    def get(self, param_name, dtype = None, default_val = None):
        pass

    @abstractmethod
    def to_dict(self):
        pass
    
    
class TestSources(Sources):
    def __init__(self, values = {}):
        self.values = values

    def set(self, param_name, value):
        self.values[param_name] = value
    
    def get(self, param_name, dtype = None, default_val = None):
        if param_name not in self.values:
            return default_val
        
        return self.values[param_name]

    def to_dict(self):
        return self.values

class RESTSources(Sources):
    def __init__(self, req, test_input = False):
        if test_input is True:
            self.d = req
        else:
            self.d = RestDecoder.decode(req)

    def set(self, param_name, value):
        self.d[param_name] = value

    def get(self, param_name, dtype = None, default_val = None):
        if param_name not in self.d:
            if default_val is None:
                raise SourcesError(f"Parameter '{param_name}' is missing in the request")
            else:
                return default_val

        val = self.d[param_name]

        if (dtype is not None) and not isinstance(val, dtype):
            raise SourcesError(f"Wrong type for '{param_name}', required: {dtype}, got {type(val)}")

        return val
    
    def to_dict(self):
        return self.d

    def __str__(self):
        return "\n".join((f"{k}: {v} [{type(v)}]" for k,v in self.d.items()))

