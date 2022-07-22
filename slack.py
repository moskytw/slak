#!/usr/bin/env python

# TODO: Rename this file.
# TODO: Make it as a package.
# TODO: Add examples in help.
# TODO: Comments as Slides.


import os
import sys
from urllib.parse import urljoin

import click
import requests
import funcy as fy


@click.group()
def cli():
    pass


@cli.command(hidden=True, help='Some random code snippets for developing.')
def develop():
    from pprint import pformat

    click.secho('DEVELOP', bg='red', fg='white')
    click.echo()

    click.echo(f"{os.environ['USER']=}")
    click.echo(f"{os.environ.get('TMP')=}")
    click.echo(f"{os.environ.get('SLACK_LAB_TOKEN')=}")
    click.echo()

    # fmt: off
    resp_json_dict = {'channel': 'CCCCCCCCC', 'message': {'blocks': [], 'client_msg_id': 'ffffffff-ffff-ffff-ffff-ffffffffffff', 'edited': {'ts': '9999999999.999999', 'user': 'U0475S3UU'}, 'is_locked': False, 'latest_reply': '9999999999.999999', 'permalink': 'https://COMPANY.slack.com/archives/CCCCCCCCC/p9999999999999999?thread_ts=9999999999.999999&cid=CCCCCCCCC', 'reactions': [{'count': 29, 'name': 'myreact', 'users': ['U018V1SL001', 'U037H4ET002', 'U03468ND003', 'U01UGH95004', 'U0171HXD005', 'U03HZDM9006', 'U037J5YF007', 'U017JVB9008', 'U016CPBJ009', 'U02AHQJC010', 'U01JM2GH011', 'U01THP8B012', 'U03M6CDT013', 'U01856GE014', 'U018HQVR015', 'UH841R016', 'U02G1091017', 'U02MQ9018', 'U037MLF6019', 'U03FWMR5020', 'U23D30021', 'U7JPG7022', 'U19255023', 'UHEHSS024', 'U01ENGL7025', 'U01RZGXQ026', 'UGN9FR027', 'U03M991G028', 'U015DFTJ029']}], 'reply_count': 16, 'reply_users': ['U0475S3AA', 'U029K07BB', 'U08KHCYCC', 'UGUABENDD', 'U4QJVN1EE', 'U02JJ67HCFF', 'U0G1KCKGG'], 'reply_users_count': 7, 'subscribed': False, 'team': 'TTTTTTTTT', 'text': '', 'thread_ts': '9999999999.999999', 'ts': '9999999999.999999', 'type': 'message', 'user': 'U0475S3UU'}, 'ok': True, 'type': 'message'}  # noqa
    # fmt: on

    click.echo(pformat(fy.get_in(resp_json_dict, ['message', 'reactions'])))
    click.echo()

    react_name = ''
    react_name = 'myreact'
    react_name = 'myreact123'

    for d in fy.get_in(resp_json_dict, ['message', 'reactions']):
        current_react_name = d['name']
        users = d['users']
        if not react_name or react_name == current_react_name:
            for u in users:
                click.echo(u)


# The `set_`/`get_` usually hints a quick operation, so here we avoid to use
# `get_` for HTTP GET.
def call_api(path, token, params):

    # TODO: Try requests-cache.
    resp = requests.get(
        urljoin('https://slack.com/api/', path),
        headers={'Authorization': f'Bearer {token}'},
        params=params,
    )

    # Yeah, the assumptions may be too strict, but, in the face of ambiguity,
    # refuse the temptation to guess.
    resp_json_dict = resp.json()
    if resp_json_dict['ok'] is False:
        error = resp_json_dict['error']
        raise RuntimeError(f'Slack replied {error!r}')

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


# 2-tuple === pair
def break_into_channel_timestamp_pair(link):
    the_rest, _, dirty_timestamp = link.rpartition('/')
    timestamp = f'{dirty_timestamp[1:-6]}.{dirty_timestamp[-6:]}'
    _, _, channel = the_rest.rpartition('/')
    return (channel, timestamp)


def call_reaction_gets_by_link(token, link):
    return call_reaction_gets(token, *break_into_channel_timestamp_pair(link))


def get_reaction_dicts(resp_json_dict):
    return fy.get_in(resp_json_dict, ['message', 'reactions'])


def _list_react(token, link, channel, timestamp):
    if link:
        return call_reaction_gets_by_link(token, link)
    elif channel and timestamp:
        return call_reaction_gets(token, channel, timestamp)
    else:
        click.echo(
            'Need at least a link, or both the channel and timestamp.',
            err=True,
        )
        sys.exit(1)


def add_token_option(f):
    return click.option(
        '--token',
        # TODO: Rename it.
        envvar='SLACK_LAB_TOKEN',
        prompt=True,
        help="Something may start with 'xoxp-'.",
        show_envvar=True,
    )(f)


# We use `react` and `reaction` interchangeably.
def add_common_parameters_for_react(f):
    return fy.compose(
        click.argument('link', required=False),
        click.option(
            '--channel',
            help='You can find it in the bottom of the channel details modal.',
        ),
        click.option('--timestamp', help='A Unix time in float.'),
    )(f)


@cli.command(help='List the names of reactions for a message.')
@add_token_option
@add_common_parameters_for_react
@click.option('--count', is_flag=True, help='Also count for each reaction.')
def list_react_names(token, link, channel=None, timestamp=None, count=False):
    for d in get_reaction_dicts(_list_react(token, link, channel, timestamp)):
        if count:
            click.echo(f"{d['count']}\t{d['name']}")
        else:
            click.echo(d['name'])


@cli.command(help='List the user IDs of a reaction in a message.')
@add_token_option
@add_common_parameters_for_react
@click.option(
    '--react-name', help='Specify a reaction rather than the first reaction.'
)
def list_react_users(
    token, link=None, channel=None, timestamp=None, react_name=None
):
    for d in get_reaction_dicts(_list_react(token, link, channel, timestamp)):

        current_react_name = d['name']
        users = d['users']
        count = d['count']
        if react_name is None:
            react_name = current_react_name

        if react_name == current_react_name:
            assert len(users) == count
            for u in users:
                click.echo(u)


def call_users_info(token, user):
    return call_api(
        'users.info',
        token=token,
        params=dict(user=user),
    )


@cli.command(help='Read user IDs from stdin and write the emails out.')
@add_token_option
@click.option(
    '--details', is_flag=True, help='Write emails with real names and titles.'
)
def query_emails(token, details):
    users = sys.stdin.read().split()
    for user in users:
        resp_json_dict = call_users_info(token, user)
        d = fy.get_in(resp_json_dict, ['user', 'profile'])
        if details:
            click.echo(f"{d['email']}\t{d['real_name']}\t{d['title']}")
        else:
            click.echo(d['email'])


if __name__ == '__main__':
    cli()
