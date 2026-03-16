#!/usr/bin/env python3
"""envsubst - Substitute environment variables in files."""
import os, re, argparse, sys

def substitute(text, env=None, strict=False, default=''):
    env = env or os.environ
    def repl(m):
        key = m.group(1) or m.group(2)
        if strict and key not in env:
            print(f"Warning: ${key} not set", file=sys.stderr)
        return env.get(key, default)
    return re.sub(r'\$\{(\w+)\}|\$(\w+)', repl, text)

def main():
    p = argparse.ArgumentParser(description='Substitute env vars in files')
    p.add_argument('file', nargs='?', help='Input file (stdin if omitted)')
    p.add_argument('-o', '--output', help='Output file')
    p.add_argument('-e', '--env', nargs='*', help='Extra KEY=VALUE pairs')
    p.add_argument('--env-file', help='Load env from .env file')
    p.add_argument('--strict', action='store_true', help='Warn on missing vars')
    p.add_argument('--default', default='', help='Default for missing vars')
    args = p.parse_args()

    env = dict(os.environ)
    if args.env_file:
        with open(args.env_file) as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#') and '=' in line:
                    k, v = line.split('=', 1)
                    env[k.strip()] = v.strip().strip('"').strip("'")
    if args.env:
        for kv in args.env:
            k, v = kv.split('=', 1)
            env[k] = v

    text = open(args.file).read() if args.file else sys.stdin.read()
    result = substitute(text, env, args.strict, args.default)

    if args.output:
        with open(args.output, 'w') as f: f.write(result)
    else:
        sys.stdout.write(result)

if __name__ == '__main__':
    main()
