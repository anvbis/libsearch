#!/usr/bin/env python3

import argparse
from bs4 import BeautifulSoup
import os
import requests
import shutil
import tarfile
import tempfile
import unix_ar
from tqdm.auto import tqdm

url = 'http://archive.ubuntu.com/ubuntu/pool/main/g/glibc/'


def _search_libc(arch='all'):
    r = requests.get(url)
    soup = BeautifulSoup(r.text, 'html.parser')

    is_libc = lambda x: x[:len('libc6_')] == 'libc6_' and x[-len('.deb'):] == '.deb'
    libs = [x.text[:-len('.deb')]
        for x in [row.find('a') for row in soup.find_all('tr')]
        if x and is_libc(x.text)]

    if arch == 'all': return libs

    is_arch = lambda x: x.split('_')[-1] == arch
    return list(filter(is_arch, libs))


def _search_debug(arch='all'):
    r = requests.get(url)
    soup = BeautifulSoup(r.text, 'html.parser')

    is_debug = lambda x: x[:len('libc6-dbg_')] == 'libc6-dbg_' and x[-len('.deb'):] == '.deb'
    debugs = [x.text[:-len('.deb')]
        for x in [row.find('a') for row in soup.find_all('tr')]
        if x and is_debug(x.text)]

    if arch == 'all': return debugs

    is_arch = lambda x: x.split('_')[-1] == arch
    return list(filter(is_arch, debugs))


def list_libc(args):
    arch = args.arch
    if args.debug:
        libs = _search_debug(arch)
    else:
        libs = _search_libc(arch)
    for lib in libs: print(lib)


def list_debug(args):
    arch = args.arch
    debugs = _search_debug(arch)
    for debug in debugs: print(debug)


def _extract_libc(file, out):
    ar_file = unix_ar.open(file)

    # can result in key error if data.tar.zst is used
    tarball = ar_file.open('data.tar.xz')
    tf = tarfile.open(fileobj=tarball)

    is_libc = lambda x: x.split('/')[-1] == 'libc.so.6'
    target = list(filter(is_libc, tf.getnames()))[-1]

    lib = tf.extractfile(target)
    with open(out, 'wb') as f:
        f.write(lib.read(-1))

    tf.close()
    tarball.close()
    ar_file.close()


def _extract_debug(file, out):
    ar_file = unix_ar.open(file)

    # can result in key error if data.tar.zst is used
    tarball = ar_file.open('data.tar.xz')
    tf = tarfile.open(fileobj=tarball)

    def debug_dir(tar):
        for t in tar.getmembers():
            if '/debug/' in t.name:
                yield t

    tf.extractall(out, debug_dir(tf))

    tf.close()
    tarball.close()
    ar_file.close()


def _download_file(target, out):
    with requests.get(target, stream=True) as r:
        total_size = int(r.headers.get('Content-Length'))
        with tqdm.wrapattr(r.raw, 'read', total=total_size, desc='') as raw:
            with open(out, 'wb') as f:
                shutil.copyfileobj(raw, f)


def download_libc(args):
    name = args.target

    out = f'{name}.so'
    if args.out: out = args.out

    with tempfile.TemporaryDirectory() as tmp:
        file = os.path.join(tmp, name)
        _download_file(f'{url}{name}.deb', file)
        _extract_libc(file, out)


def download_debug(args):
    name = args.target

    out = f'{name}'
    if args.out: out = args.out

    with tempfile.TemporaryDirectory() as tmp:
        file = os.path.join(tmp, name)
        _download_file(f'{url}{name}.deb', file)
        _extract_debug(file, out)


def arguments():
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(required=True)

    sp_list = subparsers.add_parser('list')
    sp_list.add_argument('-a', '--arch', help='filter by architecture', default='all')
    sp_list.add_argument('-d', '--debug', help='list debug symbols', action='store_true')
    sp_list.set_defaults(func=list_libc)

    sp_download = subparsers.add_parser('get-lib')
    sp_download.add_argument('-t', '--target', help='target libc name', required=True)
    sp_download.add_argument('-o', '--out', help='output file name')
    sp_download.set_defaults(func=download_libc)

    sp_download = subparsers.add_parser('get-dbg')
    sp_download.add_argument('-t', '--target', help='target libc debug symbols', required=True)
    sp_download.add_argument('-o', '--out', help='output directory name')
    sp_download.set_defaults(func=download_debug)

    return parser.parse_args()


if __name__ == '__main__':
    args = arguments()
    args.func(args)

