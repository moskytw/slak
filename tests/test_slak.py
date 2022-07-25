#!/usr/bin/env python


from unittest.mock import patch
from click.testing import CliRunner
import slak


# You could always try to *make it work* first:
#
# (I use this file as a presentation, so here are some wordy comments.)
def test_hi():
    assert 'hi' != 'hello'


class TestReactCommands:
    def setup_method(self):
        p = patch('slak.call_reaction_gets')
        m = p.start()
        # fmt: off
        m.return_value = {'channel': 'CCCCCCCCC', 'message': {'blocks': [], 'client_msg_id': 'ffffffff-ffff-ffff-ffff-ffffffffffff', 'edited': {'ts': '9999999999.999999', 'user': 'U0475S3UU'}, 'is_locked': False, 'latest_reply': '9999999999.999999', 'permalink': 'https://COMPANY.slack.com/archives/CCCCCCCCC/p9999999999999999?thread_ts=9999999999.999999&cid=CCCCCCCCC', 'reactions': [{'count': 29, 'name': 'react-1', 'users': ['U018V1SL001', 'U037H4ET002', 'U03468ND003', 'U01UGH95004', 'U0171HXD005', 'U03HZDM9006', 'U037J5YF007', 'U017JVB9008', 'U016CPBJ009', 'U02AHQJC010', 'U01JM2GH011', 'U01THP8B012', 'U03M6CDT013', 'U01856GE014', 'U018HQVR015', 'UH841R016', 'U02G1091017', 'U02MQ9018', 'U037MLF6019', 'U03FWMR5020', 'U23D30021', 'U7JPG7022', 'U19255023', 'UHEHSS024', 'U01ENGL7025', 'U01RZGXQ026', 'UGN9FR027', 'U03M991G028', 'U015DFTJ029']}, {'count': 3, 'name': 'react-2', 'users': ['UUUUUUUUUAA', 'UUUUUUUUUBB', 'UUUUUUUUUCC']}], 'reply_count': 16, 'reply_users': ['U0475S3AA', 'U029K07BB', 'U08KHCYCC', 'UGUABENDD', 'U4QJVN1EE', 'U02JJ67HCFF', 'U0G1KCKGG'], 'reply_users_count': 7, 'subscribed': False, 'team': 'TTTTTTTTT', 'text': '', 'thread_ts': '9999999999.999999', 'ts': '9999999999.999999', 'type': 'message', 'user': 'U0475S3UU'}, 'ok': True, 'type': 'message'}  # noqa
        # fmt: on
        self.call_reaction_gets_patch = p

        p = patch('slak.call_users_info')
        m = p.start()
        # fmt: off
        m.return_value = {'ok': True, 'user': {'id': 'UUUUUUUUU', 'team_id': 'TTTTTTTTT', 'name': 'NAME', 'deleted': False, 'color': 'e7392d', 'real_name': 'REAL_NAME', 'tz': 'Asia/Taipei', 'tz_label': 'Taiwan Standard Time', 'tz_offset': 28800, 'profile': {'title': 'TITLE', 'phone': '', 'skype': '', 'real_name': 'REAL_NAME', 'real_name_normalized': 'REAL_NAME_NORMALIZED', 'display_name': 'DISPLAY_NAME', 'display_name_normalized': 'DISPLAY_NAME_NORMALIZED', 'fields': None, 'status_text': '', 'status_emoji': '', 'status_emoji_display_info': [], 'status_expiration': 0, 'avatar_hash': 'ffffffffffff', 'image_original': 'https://A.URL.TO/SOME.PNG', 'is_custom_image': True, 'email': 'ACCOUNT@COMPANY.COM', 'huddle_state': 'default_unset', 'huddle_state_expiration_ts': 0, 'first_name': 'FIRST_NAME', 'last_name': 'LAST_NAME', 'status_text_canonical': '', 'team': 'TTTTTTTTT'}, 'is_admin': False, 'is_owner': False, 'is_primary_owner': False, 'is_restricted': False, 'is_ultra_restricted': False, 'is_bot': False, 'is_app_user': False, 'updated': 9999999999, 'is_email_confirmed': True, 'who_can_share_contact_card': 'EVERYONE'}}  # noqa
        # fmt: on
        self.call_users_info_patch = p

    def teardown_method(self):
        self.call_reaction_gets_patch.stop()
        self.call_users_info_patch.stop()

    def test_hi_in_class(self):
        assert 'hi' != 'hello'

    # Test the test (setup):
    def test_patching_in_setup(self):
        # After mocking, you can call without the actual arguments:
        assert (
            slak.call_reaction_gets()['message']['reactions'][1]['name']
            == 'react-2'
        )
        assert (
            slak.call_reaction_gets()['message']['reactions'][1]['name']
            != 'react-3'
        )

    def test_query_react(self):
        runner = CliRunner()
        result = runner.invoke(
            slak.cli,
            [
                # fmt: off
                'query-reacts',
                '--token', 'token',
                'https://COMPANY.slack.com/archives/CCCCCCCCC/p9999999999999999',
                # fmt: on
            ],
        )
        assert result.exit_code == 0
        assert result.output == 'react-1\nreact-2\n'

    def test_query_react_with_thread_link(self):
        runner = CliRunner()
        result = runner.invoke(
            slak.cli,
            [
                # fmt: off
                'query-reacts',
                '--token', 'TOKEN',
                'https://COMPANY.slack.com/archives/CCCCCCCCC/p8888888888888888?thread_ts=99999999999999999&cid=CCCCCCCCC',
                # fmt: on
            ],
        )
        assert result.exit_code == 0
        assert result.output == 'react-1\nreact-2\n'
        runner = CliRunner()

    def test_query_react_with_count(self):
        runner = CliRunner()
        result = runner.invoke(
            slak.cli,
            [
                # fmt: off
                'query-reacts',
                '--token', 'TOKEN',
                'https://COMPANY.slack.com/archives/CCCCCCCCC/p9999999999999999',
                '--count',
                # fmt: on
            ],
        )
        assert result.exit_code == 0
        cells = result.output.split()
        assert cells == ['29', 'react-1', '3', 'react-2']

    def test_query_react_with_users(self):
        runner = CliRunner()
        result = runner.invoke(
            slak.cli,
            [
                # fmt: off
                'query-reacts',
                '--token', 'TOKEN',
                'https://COMPANY.slack.com/archives/CCCCCCCCC/p9999999999999999',
                '--users',
                # fmt: on
            ],
        )
        assert result.exit_code == 0
        assert result.output.count('\n') == 29 + 3

    def test_query_react_with_users_clicked(self):
        runner = CliRunner()
        result = runner.invoke(
            slak.cli,
            [
                # fmt: off
                'query-reacts',
                '--token', 'TOKEN',
                'https://COMPANY.slack.com/archives/CCCCCCCCC/p9999999999999999',
                '--users',
                '--clicked', 'react-2'
                # fmt: on
            ],
        )
        assert result.exit_code == 0
        assert result.output == 'UUUUUUUUUAA\nUUUUUUUUUBB\nUUUUUUUUUCC\n'

    def test_query_users(self):
        runner = CliRunner()
        result = runner.invoke(
            slak.cli,
            [
                # fmt: off
                'query-users',
                '--token', 'TOKEN',
                # fmt: on
            ],
            input='UUUUUUUUUU1\nUUUUUUUUUU2',
        )
        assert result.exit_code == 0
        assert result.output == 'ACCOUNT@COMPANY.COM\nACCOUNT@COMPANY.COM\n'

    def test_query_users_by_args(self):
        runner = CliRunner()
        result = runner.invoke(
            slak.cli,
            [
                # fmt: off
                'query-users',
                '--token', 'TOKEN',
                'UUUUUUUUUU1', 'UUUUUUUUUU2',
                # fmt: on
            ],
        )
        assert result.exit_code == 0
        assert result.output == 'ACCOUNT@COMPANY.COM\nACCOUNT@COMPANY.COM\n'

    def test_query_emails_with_names_titles(self):
        runner = CliRunner()
        result = runner.invoke(
            slak.cli,
            [
                # fmt: off
                'query-users',
                '--token', 'TOKEN',
                '--names', '--titles',
                # fmt: on
            ],
            input='UUUUUUUUUU1\nUUUUUUUUUU2',
        )
        assert result.exit_code == 0
        assert (
            result.output
            == 'ACCOUNT@COMPANY.COM\tREAL_NAME\tTITLE\nACCOUNT@COMPANY.COM\tREAL_NAME\tTITLE\n'  # noqa
        )
