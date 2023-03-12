#!/usr/bin/env python3

import argparse
import bs4
import os
import requests
import tarfile
import tempfile
import unix_ar
import urllib.request

url = 'http://archive.ubuntu.com/ubuntu/pool/main/g/glibc/'


def _search_libc(arch='all'):
    r = requests.get(url)
    soup = bs4.BeautifulSoup(r.text, 'html.parser')

    is_libc = lambda x: x[:6] == 'libc6_' and x[-4:] == '.deb'
    libs = [x.text[:-4]
        for x in [row.find('a') for row in soup.find_all('tr')]
        if x and is_libc(x.text)]

    if arch == 'all': return libs

    is_arch = lambda x: x.split('_')[-1] == arch
    return list(filter(is_arch, libs))


def list_libc(args):
    arch = args.arch
    libs = _search_libc(arch)
    for lib in libs: print(lib)


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


def download_libc(args):
    name = args.target

    out = f'{name}.so'
    if args.out: out = args.out

    with tempfile.TemporaryDirectory() as tmp:
        file = os.path.join(tmp, name)
        urllib.request.urlretrieve(f'{url}{name}.deb', file)
        _extract_libc(file, out)


def arguments():
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(required=True)

    sp_list = subparsers.add_parser('list')
    sp_list.add_argument('-a', '--arch', help='filter by architecture', default='all')
    sp_list.set_defaults(func=list_libc)

    sp_download = subparsers.add_parser('download')
    sp_download.add_argument('-t', '--target', help='target libc name', required=True)
    sp_download.add_argument('-o', '--out', help='output file name')
    sp_download.set_defaults(func=download_libc)

    return parser.parse_args()


if __name__ == '__main__':
    args = arguments()
    args.func(args)

