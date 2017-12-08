import argparse
import json
import os
import sys

import requests
import syaml


def fetch_environ(token):
    url = f'https://circleci.com/api/v1.1/project/github/TakesxiSximada/aws-static-files/envvar?circle-token={token}'  # noqa
    headers = {
        'Content-Type': 'application/json',
    }
    res = requests.get(url, headers=headers)
    for entry in res.json():
        name = entry['name']
        value = entry['value']
        yield name, value


def remove_environ(token, name):
    url = f'https://circleci.com/api/v1.1/project/github/TakesxiSximada/aws-static-files/envvar/{name}?circle-token={token}'  # noqa
    headers = {
        'Content-Type': 'application/json',
    }
    res = requests.delete(url, headers=headers)
    return res


def main_show(args):
    for name, value in fetch_environ(token=args.token):
        print(f'{name}: {value}')


def main_apply(args):
    url = f'https://circleci.com/api/v1.1/project/github/TakesxiSximada/aws-static-files/envvar?circle-token={args.token}'  # noqa

    with open('secrets/circleci.environ.yml', 'rb') as fp:
        obj = syaml.load(fp)
        headers = {
            'Content-Type': 'application/json',
        }
        for name, value in obj.items():
            payload = json.dumps({
                'name': name,
                'value': value,
            })
            print(f'{name}')
            res = requests.post(url, data=payload, headers=headers)
            if res.reason:
                print(res.reason)


def main_reset(args):
    for name, value in fetch_environ(token=args.token):
        print(name)
        res = remove_environ(token=args.token, name=name)
        print(res.reason)


def main(argv=sys.argv[1:]):
    parser = argparse.ArgumentParser()
    parser.add_argument('--token', default=os.environ.get('CIRCLECI_TOKEN', ''))
    sub = parser.add_subparsers(dest='cmd')

    name_func = {}

    def install_cmd(func, name, *args, **kwargs):
        name_func[name] = func
        return sub.add_parser(name)

    install_cmd(main_apply, 'apply')
    install_cmd(main_reset, 'reset')
    install_cmd(main_show, 'show')

    args = parser.parse_args(argv)
    func = name_func[args.cmd]
    return func(args)

if __name__ == '__main__':
    res = main()
    sys.exit(int(0 if res is None else res))
