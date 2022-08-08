# Slak

Slak is a command line tool for collecting data from Slack and makes you look
like a pro when using it. ⚡️

Here are the examples:

```bash
$ slak query-reacts $LINK --count | sort -nr
100	likeapro
50	slak
25	zap
```

```bash
$ slak query-reacts $LINK --users --clicked likeapro | slak query-users
mosky@idontlikespam.anyway
randcat@idontcarespam.anyway
...
```

```bash
$ slak how-to-get-a-token
How to get a token?
...
```

Yes, it also teaches you how to be a pro. ✨

## Installation

PyPI is too old school to a cool kit: 😎

```bash
$ pip install git+https://github.com/moskytw/slak.git
```

Or a stable version:

```bash
$ pip install git+https://github.com/moskytw/slak.git@v1.0.0
```

## PR Is Welcome

The command is a single Python script shipped with full tests and Pipfile.lock.
You can always:

```bash
$ pipenv sync --dev
...
All dependencies are now up-to-date!
```

```bash
$ pipenv run pytest -q
...........
11 passed in 0.15s
```

So, it should be super easy to extend. PR is welcome!

## More Examples

```bash
$ slak how-to-get-a-token
How to get a token?
...
```

```bash
$ slak query-reacts https://likeapro.slack.com/archives/C12AB1234/p1234567711085949
slak
likeapro
zap
```

```bash
$ slak query-reacts $LINK --count
50	slak
100	likeapro
25	zap
```

```bash
$ slak query-reacts $LINK --count | sort -nr
100	likeapro
50	slak
25	zap
```

```bash
$ slak query-reacts $LINK --users
...
likeapro	UMOSKY
likeapro	URANDCAT
...
zap	URANDCAT
```

```bash
$ slak query-reacts $LINK --users --clicked likeapro
UMOSKY
URANDCAT
...
```

```bash
$ slak query-reacts $LINK --users --clicked likeapro | slak query-users
mosky@idontlikespam.anyway
randcat@idontcare.anyway
...
```

```bash
$ slak query-reacts $LINK --users --clicked likeapro | slak query-users --names --titles
mosky@idontlikespam.anyway	Mosky Liu	Slak Author
randcat@idontcarespam.anyway	Rand Cat	Lying There
...
```

```bash
$ slak query-reacts $LINK --users | cut -f2 | sort -u | slak query-users
mosky.liu@idontlikespam.anyway
randcat@idontcarespam.anyway
...
```

```bash
$ slak query-users UMOSKY URANDCAT --jsonl | jq '[.user.profile.email, .user.profile.display_name] | @tsv' -r
mosky@idontlikespam.anyway	Mosky
randcat@idontcarespam.anyway	ICat
```

Enjoy! 🍻
