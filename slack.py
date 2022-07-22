#!/usr/bin/env python


import os
from urllib.parse import urljoin
from pprint import pformat

import click
import requests
import funcy as fy


# The `set_`/`get_` usually hints a quick operation, so here we avoid to use
# `get_` for HTTP GET.
def call_api(path, token, params):

    resp = requests.get(
        urljoin('https://slack.com/api', path),
        headers={'Authorization': f'Bearer {token}'},
        params=params,
    )

    resp_json_dict = resp.json()
    if resp_json_dict.get('ok') in (None, False):
        error = resp_json_dict.get('error', '')
        raise RuntimeError(f'Slack replied {error!r}')

    return resp_json_dict


@click.group()
def cli():
    pass


@cli.command(hidden=True)
def develop():
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


def call_reaction_gets(token, channel, timestamp):
    return call_api(
        '/api/reactions.get',
        token=token,
        params=dict(
            channel=channel,
            timestamp=timestamp,
            full=1,
        ),
    )


def get_reaction_dicts(resp_json_dict):
    return fy.get_in(resp_json_dict, ['message', 'reactions'])


@cli.command()
@click.option('--token', envvar='SLACK_LAB_TOKEN', prompt=True)
@click.option('--channel', prompt=True)
@click.option('--timestamp', prompt=True)
def list_react_names(token, channel, timestamp):
    for d in get_reaction_dicts(call_reaction_gets(token, channel, timestamp)):
        click.echo(d['name'])


@cli.command()
@click.option('--token', envvar='SLACK_LAB_TOKEN', prompt=True)
@click.option('--channel', prompt=True)
@click.option('--timestamp', prompt=True)
@click.option('--react-name', default='')
def list_react_users(token, channel, timestamp, react_name):
    for d in get_reaction_dicts(call_reaction_gets(token, channel, timestamp)):
        current_react_name = d['name']
        users = d['users']
        count = d['count']
        if not react_name or react_name == current_react_name:
            assert len(users) == count
            for u in users:
                click.echo(u)


@click.command()
def query_emails(users):
    pass


if __name__ == '__main__':
    cli()
