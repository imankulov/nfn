## nfn ("next file name")

`nfn` is a dependency-free console tool to generate the filename with sequential suffixes. Returns the next available filename in the directory. E.g., if your current directory has files `experiment001.json` and `experiment002.json`, the command `nfn experimentNNN.json` returns `experiment003.json`

## Installation

The script works with Python3.7 and newer.

```shell
curl -s https://raw.githubusercontent.com/imankulov/nfn/main/nfn.py -o /usr/local/bin/nfn
chmod +x /usr/local/bin/nfn
```

## Usage examples

Create new files.

```shell
$ nfn --touch experimentNNN.json
experiment001.json
$ nfn --touch experimentNNN.json
experiment002.json
```

Get the next of the next file without creating anything.

```
$ nfn experimentNNN.json
experiment003.json
```

Use in scripts. For example, profiling a Django management command with [cProfile](https://docs.python.org/3/library/profile.html).

```shell
$ python -m cProfile -o $(nfn djangoNNN.prof) ./manage.py migrate
```

## Uniqueness guarantees on concurrent calls

- The script doesn't guarantee file uniqueness on concurrent calls without the `--touch` flag. In other words, if you call `nfn` without `--touch` from multiple processes simultaneously, there's a chance that some of these calls return the same filenames.
- With a `--touch` flag, the script guarantees that all invocations from the same directory return different filenames. Notice that `--touch` will also create a file in the directory.
