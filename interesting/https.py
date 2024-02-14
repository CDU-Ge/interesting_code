# encoding: utf-8

from typing import Any


class Uri:
    scheme: str

    def __init__(self):
        self._uri = ''

    def __truediv__(self, path: str) -> 'Uri':
        if '/' in path:
            raise ValueError('Invalid path')
        self._uri += '/' + path
        return self

    def __floordiv__(self, path: str) -> 'Uri':
        path = path if isinstance(path, str) else f'{path}'
        if '//' in self._uri or '/' in path:
            raise ValueError('Invalid path')
        self._uri += '//' + str(path)
        return self

    def __str__(self) -> str:
        return f'{self.scheme}:' + self._uri


class Http(Uri):
    scheme = 'http'


class Https(Uri):
    scheme = 'https'


class Domain:
    def __init__(self, prefix='') -> None:
        self._domain = prefix

    def __getattr__(self, __name: str) -> Any:
        if __name.startswith('_'):
            return super().__getattribute__(__name)
        self._domain += '.' + __name
        return self

    def __getitem__(self, __name: str | int) -> Any:
        __name = __name if isinstance(__name, str) else f'{__name}'
        self._domain += f'.{__name}'
        return self

    def __str__(self) -> str:
        return self._domain


if __name__ == '__main__':
    print(Http() // 'example.com' / 'path')  # http://example.com/path

    print(Domain('www').example.com[12352])  # https://example.com/path

    # https://example.com/path
    print(Https() // Domain('example').com / 'path' / 'pathx.html')
