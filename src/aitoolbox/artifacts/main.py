import logging
import asyncio
import tornado
import json
import argparse
from aitoolbox.context import Context, ServerContext
from aitoolbox.sources import RESTSources,SourcesError
from aitoolboy.errors import ServiceError


class MainHandler(tornado.web.RequestHandler):
    def post(self):
        logging.info('Got request')
        logging.debug(f'Headers: {self.request.headers}')

        context = Context.get()
        context.set_sources(RESTSources(self.request))

        try:
            exec(service_code)
        except Exception as e:
            self.write(str(e))
            self.set_status(500)
            return

        context.get_destinations().generate_response(self)
        context.get_destinations().clear()


async def main():
    app = tornado.web.Application([
        (r"/", MainHandler),
    ])

    app.listen(args.port)
    logging.info(f"Server started on port {args.port}")

    context = ServerContext(app)
    Context.set(context)

    await asyncio.Event().wait()

if __name__ == "__main__":
    logging.basicConfig(level = logging.DEBUG)

    logging.debug('Open setup and service files')
    with open('setup.py') as f:
        setup_code = f.read()
        setup_code = compile(setup_code,'<string>','exec')

    with open('service.py') as f:
        service_code = f.read()
        service_code = compile(service_code,'<string>','exec')

    logging.info('Initialize tool')
    exec(setup_code)

    parser = argparse.ArgumentParser(description='LLM server')
    parser.add_argument('--port', metavar='p', type=int, default=80,
                    help='the server port number (default: 80)')
    args = parser.parse_args()

    asyncio.run(main())