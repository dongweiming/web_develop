# Modify from
# https://github.com/gevent/gevent/blob/master/examples/portforwarder.py
import socket
import sys
import signal
import gevent
from gevent.server import StreamServer
from gevent.socket import create_connection, gethostbyname


class PortForwarder(StreamServer):

    def __init__(self, listener, dest, **kwargs):
        StreamServer.__init__(self, listener, **kwargs)
        self.dest = dest

    def handle(self, source, address):  # pylint:disable=method-hidden
        log('%s:%s accepted', *address[:2])
        try:
            dest = create_connection(self.dest)
        except IOError as ex:
            log('%s:%s failed to connect to %s:%s: %s', address[
                0], address[1], self.dest[0], self.dest[1], ex)
            return
        forwarders = (gevent.spawn(forward, source, dest, self),
                      gevent.spawn(forward, dest, source, self))
        gevent.joinall(forwarders)

    def close(self):
        if self.closed:
            sys.exit('Multiple exit signals received - aborting.')
        else:
            log('Closing listener socket')
            StreamServer.close(self)


def forward(source, dest, server):
    source_address = '%s:%s' % source.getpeername()[:2]
    dest_address = '%s:%s' % dest.getpeername()[:2]
    try:
        while True:
            try:
                data = source.recv(1024)
                log('%s->%s', source_address, dest_address)
                if not data:
                    break
                dest.sendall(data)
            except KeyboardInterrupt:
                if not server.closed:
                    server.close()
                break
            except socket.error:
                if not server.closed:
                    server.close()
                break
    finally:
        source.close()
        dest.close()
        server = None


def parse_address(address):
    try:
        hostname, port = address.rsplit(':', 1)
        port = int(port)
    except ValueError:
        sys.exit('Expected HOST:PORT: %r' % address)
    return gethostbyname(hostname), port


def main():
    args = sys.argv[1:]
    if len(args) != 2:
        sys.exit('Usage: %s source-address destination-address' % __file__)
    source = args[0]
    dest = parse_address(args[1])
    server = PortForwarder(source, dest)
    log('Starting port forwarder %s:%s -> %s:%s', *(server.address[:2] + dest))
    gevent.signal(signal.SIGTERM, server.close)
    gevent.signal(signal.SIGINT, server.close)
    server.start()
    gevent.wait()


def log(message, *args):
    message = message % args
    sys.stderr.write(message + '\n')


if __name__ == '__main__':
    main()
