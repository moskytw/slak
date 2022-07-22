#!/usr/bin/env python


from unittest.mock import patch

from click.testing import CliRunner

import slack


def test_hi():
    assert 'hi' != 'hello'


class TestReactCommands:
    def setup_method(self):
        p = patch('slack.call_reaction_gets')

        m = p.start()
        # fmt: off
        m.return_value = {'channel': 'CCCCCCCCC', 'message': {'blocks': [], 'client_msg_id': 'ffffffff-ffff-ffff-ffff-ffffffffffff', 'edited': {'ts': '9999999999.999999', 'user': 'U0475S3UU'}, 'is_locked': False, 'latest_reply': '9999999999.999999', 'permalink': 'https://COMPANY.slack.com/archives/CCCCCCCCC/p9999999999999999?thread_ts=9999999999.999999&cid=CCCCCCCCC', 'reactions': [{'count': 29, 'name': 'react-1', 'users': ['U018V1SL001', 'U037H4ET002', 'U03468ND003', 'U01UGH95004', 'U0171HXD005', 'U03HZDM9006', 'U037J5YF007', 'U017JVB9008', 'U016CPBJ009', 'U02AHQJC010', 'U01JM2GH011', 'U01THP8B012', 'U03M6CDT013', 'U01856GE014', 'U018HQVR015', 'UH841R016', 'U02G1091017', 'U02MQ9018', 'U037MLF6019', 'U03FWMR5020', 'U23D30021', 'U7JPG7022', 'U19255023', 'UHEHSS024', 'U01ENGL7025', 'U01RZGXQ026', 'UGN9FR027', 'U03M991G028', 'U015DFTJ029']}, {'count': 3, 'name': 'react-2', 'users': ['UUUUUUUUUAA', 'UUUUUUUUUBB', 'UUUUUUUUUCC']}], 'reply_count': 16, 'reply_users': ['U0475S3AA', 'U029K07BB', 'U08KHCYCC', 'UGUABENDD', 'U4QJVN1EE', 'U02JJ67HCFF', 'U0G1KCKGG'], 'reply_users_count': 7, 'subscribed': False, 'team': 'TTTTTTTTT', 'text': '', 'thread_ts': '9999999999.999999', 'ts': '9999999999.999999', 'type': 'message', 'user': 'U0475S3UU'}, 'ok': True, 'type': 'message'}  # noqa
        # fmt: on

        self.call_reaction_gets_patch = p

    def teardown_method(self):
        self.call_reaction_gets_patch.stop()

    def test_hi_in_class(self):
        assert 'hi' != 'hello'

    def test_mock(self):
        # After mocking, you can call without the actual arguments:
        assert (
            slack.call_reaction_gets()['message']['reactions'][1]['name']
            == 'react-2'
        )
        assert (
            slack.call_reaction_gets()['message']['reactions'][1]['name']
            != 'react-3'
        )

    def test_list_react_names(self):
        runner = CliRunner()

        result = runner.invoke(
            slack.cli,
            [
                # fmt: off
                'list-react-names',
                '--token', 'TOKEN',
                '--channel', 'CHANNEL',
                '--timestamp', 'TIMESTAMP',
                # fmt: on
            ],
        )
        assert result.exit_code == 0
        assert result.output == 'react-1\nreact-2\n'

    def test_list_react_user(self):
        runner = CliRunner()

        result = runner.invoke(
            slack.cli,
            [
                # fmt: off
                'list-react-users',
                '--token', 'TOKEN',
                '--channel', 'CHANNEL',
                '--timestamp', 'TIMESTAMP',
                '--react-name', 'react-2',
                # fmt: on
            ],
        )
        assert result.exit_code == 0
        assert result.output == 'UUUUUUUUUAA\nUUUUUUUUUBB\nUUUUUUUUUCC\n'
