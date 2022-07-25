# Slak

Slak is a command line tool for collecting data from Slack. And make you act
like a pro when using it. ⚡️

```bash
$ slak query-reacts LINK --count | sort -nr
100	likeapro
50	slak
25	zap
```

```bash
$ slak query-reacts LINK --users --clicked likeapro | slak query-users
mosky@idontlikespam.anyway
randcat@idontlikespam.neither
...
```

```bash
$ slak how-to-get-a-token
How to get a token?
...
```

🤘🏻

## Installation

```bash
$ pip install git+https://github.com/moskytw/slak.git
```

PyPI is too old school to cool kit. 😎

## PR Is Welcome

The command is a single Python script shipped with full tests, so it should be
super easy to extend. PR is welcome!

## More Examples

```bash
$ slak how-to-get-a-token
How to get a token?
...
```

```bash
$ slak query-reacts https://likeapro.slack.com/archives/C09GC1234/p1658718657123456
slak
likeapro
zap
```

```bash
$ slak query-reacts https://likeapro.slack.com/archives/C09GC1234/p1658718657123456 --count
50	slak
100	likeapro
25	zap
```

```bash
$ slak query-reacts https://likeapro.slack.com/archives/C09GC1234/p1658718657123456 --count | sort -nr
100	likeapro
50	slak
25	zap
```

```bash
$ slak query-reacts https://likeapro.slack.com/archives/C09GC1234/p1658718657123456 --users
...
likeapro	UMOSKY
likeapro	URANDCAT
...
zap	URANDCAT
```

```bash
$ slak query-reacts https://likeapro.slack.com/archives/C09GC1234/p1658718657123456 --users --clicked likeapro
UMOSKY
URANDCAT
...
```

```bash
$ slak query-reacts https://likeapro.slack.com/archives/C09GC1234/p1658718657123456 --users --clicked likeapro | slak query-users
mosky@idontlikespam.anyway
randcat@idontlikespam.neither
...
```

```bash
$ slak query-reacts https://likeapro.slack.com/archives/C09GC1234/p1658718657123456 --users --clicked likeapro | slak query-users --names --titles
mosky@idontlikespam.anyway	Mosky Liu	Slak Author
randcat@idontlikespam.neither	Rand Cat	A Flyer?
...
```

```bash
$ slak query-reacts https://likeapro.slack.com/archives/C09GC1234/p1658718657123456 --users | cut -f2 | slak query-users
mosky.liu@idontlikespam.com
slak@maylikespam.com
...
```

Enjoy! 🍻
