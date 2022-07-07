import argparse
import re
import socket
import sys

from termcolor import cprint

def error(message):
    cprint(f'[-] {message}', 'red')
    sys.exit(1)

def info(message):
    cprint(f'[*] {message}', 'blue')

def success(message):
    cprint(f'[+] {message}', 'green')

def reachable_ip(ip):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try: s.connect((ip, 80))

    except socket.timeout: return False

    finally:
        s.close()
        return True

def check_errors(args):
    if not re.match('(\d{1,3}.){3}\d{1,3}', args.ip):
        error('The IP address is not valid.')

    if args.port < 1 or args.port > 65535:
        error('The port is not valid.')

    if args.last_port is not None and (args.port >= args.last_port or args.last_port < 1 or args.last_port > 65535):
        error('The last port is not valid.')

    if not reachable_ip(args.ip):
        error(f'The IP ADDRESS {args.ip} is not reachable.')

def check_port(ip, port):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        errors = s.connect_ex((ip, port))
        return errors == 0

if __name__ == '__main__':
    print('''
   _____  __   __  _____   _____   ______ _______ _______ _______ _______ __   _
  |_____]   \_/   |_____] |     | |_____/    |    |______ |       |_____| | \  |
  |          |    |       |_____| |    \_    |    ______| |_____  |     | |  \_|

    ''')

    socket.setdefaulttimeout(1)

    parser = argparse.ArgumentParser()
    parser.add_argument('ip', help='IP of the target address. It must be in the IPv4 form.', type=str)
    parser.add_argument(
        'port',
        help='Port of the target you want to scan. It is the first port to scan if the -lp option is specified',
        type=int
    )
    parser.add_argument(
        '-lp', '--last-port',
        help='If you want to specify a range of ports to scan, this is the last port to scan.',
        type=int
    )

    args = parser.parse_args()

    check_errors(args)

    info(f'Scanning IP ADDRESS: {args.ip}')

    if args.last_port is not None:
        info(f'PORTS to scan: {args.port} - {args.last_port}\n')

        for port in range(args.port, args.last_port + 1):
            if check_port(args.ip, port):
                success(f'PORT {port}: OPEN')

    else:
        info(f'PORT to scan: {args.port}\n')

        port_open = check_port(args.ip, args.port)

        if port_open:
            success(f'PORT {args.port}: OPEN')
        else:
            error(f'PORT {args.port}: CLOSE')