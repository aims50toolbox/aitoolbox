import json
import logging

from base64 import b64decode
import imageio.v3 as iio

from .image import Image

class RestDecoder():
    def decode(req):
        if 'mime-type' in req.headers:
            mimeType = req.headers["mime-type"]
            logging.debug(f'Mime type: {mimeType}')

            if mimeType == 'application/json':
                arguments = json.loads(req.body)
            elif mimeType.startswith('image/'):
                arguments = RestDecoder.decode_query_arguments(req)
                arguments["image"] = Image(RestDecoder.decode_image(mimeType,req.body,False))
        else:
            arguments = RestDecoder.decode_query_arguments(req)

        return { k: RestDecoder.decode_argument(v) for k,v in arguments.items() }

    def decode_argument(arg):
        if isinstance(arg, (int, float, complex, str)):
            return arg
        
        if isinstance(arg, dict) and "_type" in arg:
            mime = arg["_type"]
            if mime.startswith("image/"):
                return Image(RestDecoder.decode_image(mime,arg["_data"]))

        return arg
    
    def decode_query_arguments(req):
        def convert_strings(s):
            if isinstance(s, str):
                try:
                    return int(s)
                except:
                    pass

                try:
                    return float(s)
                except:
                    pass

                if s.lower() == "true":
                    return True
                elif s.lower() == "false":
                    return False
                else:
                    return s
            else:
                return s
                
        return { k: convert_strings(v[0].decode('utf-8')) for k,v in req.arguments.items()}

    def decode_image(mime,data,is_base64 = True):
        if is_base64 is True:
            data = b64decode(data)
        return iio.imread(data)