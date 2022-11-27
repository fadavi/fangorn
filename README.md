![CI Workflow Status](https://github.com/fadavi/fangorn/actions/workflows/ci.yml/badge.svg?branch=main)

# Fangorn

## Requiremenst
Python 3.10.x

## How to run
Directly using python:
```bash
$ python3 -mfangorn
```

Or via make:
```bash
$ make pvp # Orderus vs. Beast
$ make tdm # Team Deathmatch
```

## How to run tests
Directly using python:
```bash
$ python3 -mpip install -r requirements-dev.txt
$ python3 -mpytest
```

Or via make:
```bash
$ make requirements-dev
$ make test
```

## TODO
- [ ] Add setup.py
- [ ] Improve test coverage
- [ ] Smarter attack strategy(ies)
- [ ] More heros/hostiles
- [ ] More skills
- [ ] Display stats of heros/hostiles in command-line
- [ ] Re-write CLI using curses
- [ ] Ability to customize heros/hostiles by a config file
- [ ] Add user-controlled heros
