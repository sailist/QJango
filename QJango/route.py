"""

"""

import socket

from flask import Flask


def get_host() -> str:
    # global _ip
    # if _ip is not None:
    #     return _ip

    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(('8.8.8.8', 80))
        _ip = s.getsockname()[0]
    finally:
        s.close()

    # if isinstance(_ip,str):
    #     if _ip.startswith('192'):
    #         _ip = '127.0.0.1'

    return _ip


app = Flask(__name__)

_ip = None
host = get_host()
# host = '0.0.0.0'
port = 5679


@app.route('/', methods=['GET'])
def index():
    print(app.url_map)
    return 'hello world'


def run():
    app.run(host=host, port=port)
