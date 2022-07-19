#!/usr/bin/env python


import os
from urllib.parse import urljoin
from pprint import pformat

import click
import requests
import funcy as fy


def get_slack(path, token, params):
    return requests.get(
        urljoin('https://slack.com/api', path),
        headers={'Authorization': f'Bearer {token}'},
        params=params,
    )


@click.group()
def cli():
    pass


@click.command()
def debug():
    click.secho('DEBUG', bg='red', fg='white')
    click.echo(f"{os.environ['USER']=}")
    click.echo(f"{os.environ.get('TMP')=}")

    # fmt: off
    resp_json_dict = {'channel': 'CCCCCCCCC', 'message': {'blocks': [], 'client_msg_id': 'ffffffff-ffff-ffff-ffff-ffffffffffff', 'edited': {'ts': '9999999999.999999', 'user': 'U0475S3UU'}, 'is_locked': False, 'latest_reply': '9999999999.999999', 'permalink': 'https://COMPANY.slack.com/archives/CCCCCCCCC/p9999999999999999?thread_ts=9999999999.999999&cid=CCCCCCCCC', 'reactions': [{'count': 29, 'name': 'myreact', 'users': ['U018V1SL001', 'U037H4ET002', 'U03468ND003', 'U01UGH95004', 'U0171HXD005', 'U03HZDM9006', 'U037J5YF007', 'U017JVB9008', 'U016CPBJ009', 'U02AHQJC010', 'U01JM2GH011', 'U01THP8B012', 'U03M6CDT013', 'U01856GE014', 'U018HQVR015', 'UH841R016', 'U02G1091017', 'U02MQ9018', 'U037MLF6019', 'U03FWMR5020', 'U23D30021', 'U7JPG7022', 'U19255023', 'UHEHSS024', 'U01ENGL7025', 'U01RZGXQ026', 'UGN9FR027', 'U03M991G028', 'U015DFTJ029']}], 'reply_count': 16, 'reply_users': ['U0475S3AA', 'U029K07BB', 'U08KHCYCC', 'UGUABENDD', 'U4QJVN1EE', 'U02JJ67HCFF', 'U0G1KCKGG'], 'reply_users_count': 7, 'subscribed': False, 'team': 'TTTTTTTTT', 'text': '', 'thread_ts': '9999999999.999999', 'ts': '9999999999.999999', 'type': 'message', 'user': 'U0475S3UU'}, 'ok': True, 'type': 'message'}  # noqa
    # fmt: on
    click.echo(pformat(fy.get_in(resp_json_dict, ['message', 'reactions'])))


@click.command()
@click.option('--token', prompt=True)
@click.option('--channel', prompt=True)
@click.option('--timestamp', prompt=True)
def get_reacted_users(token, channel, timestamp):
    resp = get_slack(
        '/api/reactions.get',
        token=token,
        params=dict(
            channel=channel,
            timestamp=timestamp,
            full=1,
        ),
    )
    click.echo(pformat(resp.json()))


@click.command()
def get_emails(users):
    pass


cli.add_command(debug)
cli.add_command(get_reacted_users)
cli.add_command(get_emails)


if __name__ == '__main__':
    cli()
