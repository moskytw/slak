#!/usr/bin/env python

'''Collect data from Slack like a pro. ⚡️'''

__version__ = '1.0.0'


import os
import sys
import json as _json
from urllib.parse import urljoin

import requests
import click


def _json_dumps(x, indent=2):
    return _json.dumps(x, ensure_ascii=False, indent=indent)


# The `set_`/`get_` usually cues a quick operation, so here we avoid to use
# `get_` for HTTP GET.
#
# (I use this file as a presentation, so here are some wordy comments.)
def call_api(path, token, params):
    resp = requests.get(
        urljoin('https://slack.com/api/', path),
        headers={'Authorization': f'Bearer {token}'},
        params=params,
    )

    # Yeah, the assumption to the response body may be too strict, but, in the
    # face of ambiguity, refuse the temptation to guess.
    resp_json_dict = resp.json()
    if resp_json_dict['ok'] is False:
        raise RuntimeError(f"Slack replied {resp_json_dict['error']!r}")

    return resp_json_dict


def call_reaction_gets(token, channel, timestamp):
    return call_api(
        'reactions.get',
        token=token,
        params=dict(
            channel=channel,
            timestamp=timestamp,
            full=1,
        ),
    )


# A link may look like:
#
# 1. https://COMPANY.slack.com/archives/CCCCCCCCC/p9999999999999999
# 2. https://COMPANY.slack.com/archives/CCCCCCCCC/p8888888888888888?thread_ts=99999999999999999&cid=CCCCCCCCC  # noqa
#
# 2-tuple === pair
def break_into_channel_timestamp_pair(link):
    the_rest, _, _ = link.partition('?')
    the_rest, _, dirty_timestamp = the_rest.rpartition('/')
    timestamp = f'{dirty_timestamp[1:-6]}.{dirty_timestamp[-6:]}'
    _, _, channel = the_rest.rpartition('/')
    return (channel, timestamp)


def call_reaction_gets_by_link(token, link):
    return call_reaction_gets(token, *break_into_channel_timestamp_pair(link))


def call_users_info(token, user):
    return call_api(
        'users.info',
        token=token,
        params=dict(user=user),
    )


@click.group(help=__doc__)
@click.version_option(version=__version__)
def cli():
    pass


@cli.command(hidden=True, help='Some random code snippets for developing.')
def develop():
    click.secho('DEVELOP', bg='red', fg='white')
    click.echo()

    # # They required Python 3.8+.
    # click.echo(f"{os.environ['USER']=}")
    # click.echo(f"{os.environ.get('TMP')=}")
    # click.echo(f"{os.environ.get('SLACK_LAB_TOKEN')=}")
    # click.echo()

    # fmt: off
    resp_json_dict = {'channel': 'CCCCCCCCC', 'message': {'blocks': [], 'client_msg_id': 'ffffffff-ffff-ffff-ffff-ffffffffffff', 'edited': {'ts': '9999999999.999999', 'user': 'U0475S3UU'}, 'is_locked': False, 'latest_reply': '9999999999.999999', 'permalink': 'https://COMPANY.slack.com/archives/CCCCCCCCC/p9999999999999999?thread_ts=9999999999.999999&cid=CCCCCCCCC', 'reactions': [{'count': 29, 'name': 'myreact', 'users': ['U018V1SL001', 'U037H4ET002', 'U03468ND003', 'U01UGH95004', 'U0171HXD005', 'U03HZDM9006', 'U037J5YF007', 'U017JVB9008', 'U016CPBJ009', 'U02AHQJC010', 'U01JM2GH011', 'U01THP8B012', 'U03M6CDT013', 'U01856GE014', 'U018HQVR015', 'UH841R016', 'U02G1091017', 'U02MQ9018', 'U037MLF6019', 'U03FWMR5020', 'U23D30021', 'U7JPG7022', 'U19255023', 'UHEHSS024', 'U01ENGL7025', 'U01RZGXQ026', 'UGN9FR027', 'U03M991G028', 'U015DFTJ029']}], 'reply_count': 16, 'reply_users': ['U0475S3AA', 'U029K07BB', 'U08KHCYCC', 'UGUABENDD', 'U4QJVN1EE', 'U02JJ67HCFF', 'U0G1KCKGG'], 'reply_users_count': 7, 'subscribed': False, 'team': 'TTTTTTTTT', 'text': '', 'thread_ts': '9999999999.999999', 'ts': '9999999999.999999', 'type': 'message', 'user': 'U0475S3UU'}, 'ok': True, 'type': 'message'}  # noqa
    # fmt: on

    click.echo(resp_json_dict['message']['reactions'])
    click.echo()

    specified_react_name = None  # -> 29 users
    specified_react_name = 'myreact'  # -> 29 users
    specified_react_name = 'myreact123'  # -> 0 users

    for d in resp_json_dict['message']['reactions']:
        current_react_name = d['name']
        users = d['users']
        count = d['count']

        # It means specifying the first react:
        if specified_react_name is None:
            specified_react_name = current_react_name

        if current_react_name == specified_react_name:
            assert len(users) == count
            for u in users:
                click.echo(u)


@cli.command(help="Start with me if you have no idea about token.")
def how_to_get_a_token():
    s = click.style
    bw = lambda text: s(text, fg='bright_white')  # noqa

    click.secho('How to get a token?', bold=True, underline=True)
    click.echo(
        f'''
1. Open {bw('https://api.slack.com/apps')}.
2. Click {bw('Create New App')}, {bw('From scratch')}, fill, and create the app.
3. Switch to {bw('OAuth & Permissions')}, find {bw('Scope')}, and add {bw('reactions:read')}, {bw('users:read')}, {bw('users:read.email')}.
4. Click {bw('Install to Workspace')}.
5. Copy your token!

Or ask your colleague for a token.'''  # noqa
    )
    click.echo('')
    click.secho('How to set the token?', bold=True, underline=True)
    click.echo(
        f'''
{s('$ read SLAK_TOKEN && export SLAK_TOKEN', bold=True)}

In this way, you're free from using {bw('--token')} every time and your token is secure from being recorded into the history file.
'''  # noqa
    )


def add_token_option(f):
    return click.option(
        '--token',
        metavar='TOKEN',
        envvar='SLAK_TOKEN',
        prompt=True,
        help="Something may start with 'xoxp-'.",
        show_envvar=True,
    )(f)


def add_json_option(f, jsonl=False):
    decl = '--json'
    format_name = 'JSON'

    if jsonl:
        decl = '--jsonl'
        format_name = 'JSON Lines'

    return click.option(
        decl,
        is_flag=True,
        help=f'Print the response body in {format_name} directly.',  # noqa
    )(f)


def add_jsonl_option(f):
    return add_json_option(f, jsonl=True)


# We use `react` and `reaction` interchangeably.
@cli.command(
    help='''Query like the users who clicked a reaction.

\b
$ slak list-react-users --token TOKEN https://company.slack.com/archives/C123ABCD4/p1658312123456789
'''  # noqa
)
@add_token_option
@click.argument('link')
@click.option(
    '--count',
    'to_count_reacts',
    is_flag=True,
    help='Show counts of reactions.',
)
@click.option(
    '--users', 'to_list_users', is_flag=True, help='List the user IDs.'
)
@click.option(
    '--clicked',
    '-c',
    'specified_name',
    metavar='REACT_NAME',
    help='Filter by a reaction name.',
)
@add_json_option
def query_reacts(
    token,
    link=None,
    to_count_reacts=None,
    to_list_users=None,
    specified_name=None,
    json=None,
):
    resp_json_dict = call_reaction_gets_by_link(token, link)
    if json:
        click.echo(_json_dumps(resp_json_dict))
        return

    for d in resp_json_dict['message']['reactions']:
        name = d['name']
        users = d['users']
        count = d['count']

        if not to_count_reacts and not to_list_users:
            click.echo(d['name'])
        elif to_count_reacts:
            click.echo(f"{count}\t{name}")
        elif to_list_users:
            if specified_name is None:
                for u in users:
                    click.echo(f"{name}\t{u}")
            elif name == specified_name:
                for u in users:
                    click.echo(u)


@cli.command(
    help='''Query user information like emails, names, titles from stdin or args.

\b
$ echo U123AB45C | slack query-emails --token TOKEN
'''
)
@add_token_option
@click.argument('users', nargs=-1)
@click.option(
    '--emails/--no-emails',
    'with_email',
    is_flag=True,
    default=True,
    show_default=True,
    help='Print the email column.',
)
@click.option(
    '--names/--no-names', 'with_name', is_flag=True, help='The name column.'
)
@click.option(
    '--titles/--no-titles',
    'with_title',
    is_flag=True,
    help='The title column.',
)
@add_jsonl_option
def query_users(
    token, users, with_email=None, with_name=None, with_title=None, jsonl=None
):
    if not users:
        users = sys.stdin.read().split()

    for user in users:
        resp_json_dict = call_users_info(token, user)
        if jsonl:
            # So, we get the output in JSON Lines.
            click.echo(_json_dumps(resp_json_dict, indent=None))
            continue

        d = resp_json_dict['user']['profile']
        cells = []
        if with_email:
            cells.append(d['email'])
        if with_name:
            cells.append(d['real_name'])
        if with_title:
            cells.append(d['title'])
        click.echo('\t'.join(cells))


if __name__ == '__main__':
    cli()
