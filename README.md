# LibSearch

## Installation

```
$ git clone https://github.com/anvbis/libsearch
$ cd libsearch && pip install -r requirements.txt
```


## Usage

```
usage: libsearch.py [-h] {list,get-lib,get-dbg} ...

positional arguments:
  {list,get-lib,get-dbg}

options:
  -h, --help            show this help message and exit
```

```
usage: libsearch.py list [-h] [-a ARCH] [-d]

options:
  -h, --help            show this help message and exit
  -a ARCH, --arch ARCH  filter by architecture
  -d, --debug           list debug symbols
```

```
usage: libsearch.py get-lib [-h] -t TARGET [-o OUT]

options:
  -h, --help            show this help message and exit
  -t TARGET, --target TARGET
                        target libc name
  -o OUT, --out OUT     output file name
```

```
usage: libsearch.py get-dbg [-h] -t TARGET [-o OUT]

options:
  -h, --help            show this help message and exit
  -t TARGET, --target TARGET
                        target libc debug symbols
  -o OUT, --out OUT     output directory name
```


## Retrieving a Shared Library

```
$ ./libsearch.py list -a amd64
libc6_2.23-0ubuntu3_amd64
libc6_2.23-0ubuntu11.3_amd64
libc6_2.27-3ubuntu1.5_amd64
libc6_2.27-3ubuntu1.6_amd64
libc6_2.27-3ubuntu1_amd64
libc6_2.31-0ubuntu9.7_amd64
libc6_2.31-0ubuntu9.9_amd64
libc6_2.31-0ubuntu9_amd64
libc6_2.35-0ubuntu3.1_amd64
libc6_2.35-0ubuntu3_amd64
libc6_2.36-0ubuntu4_amd64
libc6_2.37-0ubuntu1_amd64
libc6_2.37-0ubuntu2_amd64
```

```
$ ./libsearch.py get-lib -t libc6_2.31-0ubuntu9.9_amd64
100%|███████████████████████████████████████████████████████████| 2.60M/2.60M [00:03<00:00, 872kB/s]
$ ls *.so
libc6_2.31-0ubuntu9.9_amd64.so
```


## Retrieving Debug Symbols

```
$ ./libsearch.py list -a amd64 --debug
libc6-dbg_2.23-0ubuntu3_amd64
libc6-dbg_2.23-0ubuntu11.3_amd64
libc6-dbg_2.27-3ubuntu1.5_amd64
libc6-dbg_2.27-3ubuntu1.6_amd64
libc6-dbg_2.27-3ubuntu1_amd64
libc6-dbg_2.31-0ubuntu9.7_amd64
libc6-dbg_2.31-0ubuntu9.9_amd64
libc6-dbg_2.31-0ubuntu9_amd64
libc6-dbg_2.35-0ubuntu3.1_amd64
libc6-dbg_2.35-0ubuntu3_amd64
libc6-dbg_2.36-0ubuntu4_amd64
libc6-dbg_2.37-0ubuntu1_amd64
libc6-dbg_2.37-0ubuntu2_amd64
```

```
./libsearch.py get-dbg -t libc6-dbg_2.31-0ubuntu9.9_amd64
100%|██████████████████████████████████████████████████████████| 19.1M/19.1M [00:10<00:00, 1.98MB/s]
$ stat libc6-dbg_*stat libc6-dbg_*
  File: libc6-dbg_2.31-0ubuntu9.9_amd64
  Size: 4096      	Blocks: 8          IO Block: 4096   directory
  ...
```