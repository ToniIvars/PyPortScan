import argparse
import math
from multiprocessing import Process
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

    try:
        s.connect((ip, 80))
        return True

    except socket.timeout: return False

    except socket.error: return True

    finally:
        s.close()

def check_errors(args):
    if not re.match('(\d{1,3}.){3}\d{1,3}', args.ip):
        error('The IP address is not valid.')

    if args.port < 1 or args.port > 65535:
        error('The port is not valid.')

    if args.last_port is not None and (args.port >= args.last_port or args.last_port < 1 or args.last_port > 65535):
        error('The last port is not valid.')

    if not reachable_ip(args.ip):
        error(f'The IP ADDRESS {args.ip} is not reachable.')

    if args.threads < 1:
        error('The threads cannot be less than 1.')

def check_port(ip, port):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        errors = s.connect_ex((ip, port))
        return errors == 0

def generate_port_range(first_port, last_port, threads):
    if threads == 1:
        yield range(first_port, last_port)

    else:
        quant = math.ceil((last_port - first_port) / threads)
        while last_port - first_port > quant:
            yield range(first_port, first_port + quant)
            first_port += quant

        yield range(first_port, last_port)

def scan_subrange(ip, port_range):
    for port in port_range:
        if check_port(ip, port):
            success(f'PORT {port}: OPEN')

def scan_ports_range(ip, first_port, last_port, threads):
    last_port += 1
    threads = min(last_port - first_port, threads)

    processes = []
    for port_range in generate_port_range(first_port, last_port, threads):
        p = Process(target=scan_subrange, args=(ip, port_range))
        p.start()
        processes.append(p)

    for p in processes:
        p.join()

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
    parser.add_argument(
        '-t', '--threads',
        help='Threads to use in the scan.',
        type=int, default=1
    )

    args = parser.parse_args()

    check_errors(args)

    info(f'Scanning IP ADDRESS: {args.ip}')

    if args.last_port is not None:
        info(f'PORTS to scan: {args.port} - {args.last_port}\n')

        scan_ports_range(args.ip, args.port, args.last_port, args.threads)

    else:
        info(f'PORT to scan: {args.port}\n')

        port_open = check_port(args.ip, args.port)

        if port_open:
            success(f'PORT {args.port}: OPEN')
        else:
            error(f'PORT {args.port}: CLOSE')