# PyPortScan
This project is a port scanner made with Python, being the only core-extra dependency the library **termcolor**, used to make the experience a bit more spicy.

## Installation
The installation of the script is as simple as running
```bash
git clone https://github.com/ToniIvars/pyportscan
python3 -m venv env
source env/bin/activate # In Linux
pip install -r requirements.txt
```

## Usage
- Basic usage: `python pyportscan.py [TARGET IP] [PORT TO SCAN]`
- Advanced usage: You can also scan a range of ports. To do that, you must specify the `-lp` flag, which will be the last port of the range to be scanned, while the `PORT TO SCAN` will be the first port to scan. Example:
`python pyportscan.py [TARGET IP] [FIRST PORT] -lp [LAST PORT]`
- Threaded usage: To make use of multiprocessing, you must specify the `-t` flag and then write the number of processes you want to use. Example: `python pyportscan.py [TARGET IP] [FIRST PORT] -lp [LAST PORT] -t 20`