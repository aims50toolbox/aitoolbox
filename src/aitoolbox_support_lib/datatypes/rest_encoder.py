import json

from base64 import b64encode
import imageio.v3 as iio
import numpy
from .image import Image

class RestEncoder():
    def encode(handler, kvps, single_mime = False):
        if single_mime and len(kvps) == 1:
            name,val = list(kvps.items())[0]
            if isinstance(val, (int, float, complex, str)):
                handler.set_header('Content-Type','text/plain')
                handler.write(str(val))
            elif isinstance(val, Image):
                handler.set_header('Content-Type','image/png')
                handler.write(RestEncoder.encode_image(val.to_numpy(), to_base64 = False))  
        else:
            j = { k: RestEncoder.encode_argument(v) for k,v in kvps.items() }
            handler.write(json.dumps(j))

    def encode_to_jsonstring(kvps):
        j = { k: RestEncoder.encode_argument(v) for k,v in kvps.items() }
        return json.dumps(j)

    def encode_argument(arg):
        if isinstance(arg, (int, float, complex, str)):
            return arg
        
        if isinstance(arg, numpy.ndarray):
            return arg.tolist()

        if isinstance(arg, Image):
            return { "_type": "image/png", "_data": RestEncoder.encode_image(arg.to_numpy()) }

        return arg
    
    def encode_image(data,to_base64 = True):
        data = iio.imwrite("<bytes>", data, extension='.png')
        if to_base64:
            return b64encode(data).decode('utf-8')
        else:
            return data