# LibSearch

## Installation

```
$ git clone https://github.com/anvbis/libsearch
$ pip install -r requirements.txt
```

## Usage

```
usage: libsearch.py [-h] {list,download} ...

positional arguments:
  {list,download}

options:
  -h, --help       show this help message and exit
```

```
usage: libsearch.py list [-h] [-a ARCH]

options:
  -h, --help            show this help message and exit
  -a ARCH, --arch ARCH  filter by architecture
```

```
usage: libsearch.py download [-h] -t TARGET [-o OUT]

options:
  -h, --help            show this help message and exit
  -t TARGET, --target TARGET
                        target libc name
  -o OUT, --out OUT     output file name
```

## Example

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
```

```
$ ./libsearch.py download -t libc6_2.27-3ubuntu1.6_amd64
$ ls *.so
libc6_2.27-3ubuntu1.6_amd64.so
```
