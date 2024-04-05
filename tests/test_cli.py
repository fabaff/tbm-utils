import os
from pathlib import Path

import pendulum
import pytest

from tbm_utils import (
	Namespace,
	create_parser_dry_run,
	create_parser_filter_dates,
	create_parser_local,
	create_parser_logging,
	create_parser_meta,
	create_parser_yes,
	custom_path,
	merge_defaults,
	parse_args,
)


@pytest.mark.skipif(os.name != 'nt', reason="Windows-only test")
@pytest.mark.parametrize(
	'value',
	[
		'/cygdrive/d/Music/test.mp3',
		'/d/Music/test.mp3',
		'D:/Music/test.mp3',
		'D:\\Music\\test.mp3',
		r'D:\Music\test.mp3'
	]
)
def test_cli_custom_path_windows(value):
	assert custom_path(value) == Path('D:/Music/test.mp3')


@pytest.mark.skipif(os.name == 'nt', reason="*nix test")
def test_cli_custom_path_non_windows():
	assert custom_path('/d/Music/test.mp3') == Path('/d/Music/test.mp3')


def test_create_parser_dry_run():
	dry_run = create_parser_dry_run()
	args = dry_run.parse_args(['-n'])

	assert args.dry_run


def test_create_parser_filter_dates():
	filter_dates = create_parser_filter_dates()
	args = filter_dates.parse_args(
		[
			'--created-in', '2019-08',
			'--created-on', '2019-08-22',
			'--created-before', '2019-08-22T16:00:00',
			'--created-after', '2019-08-22T16:00:00',
			'--modified-in', '2019-08',
			'--modified-on', '2019-08-22',
			'--modified-before', '2019-08-22T16:00:00',
			'--modified-after', '2019-08-22T16:00:00'
		]
	)

	assert args.created_in == pendulum.interval(
		pendulum.datetime(2019, 8, 1, tz='local'),
		pendulum.datetime(2019, 8, 31, tz='local').end_of('day')
	)
	assert args.created_on == pendulum.interval(
		pendulum.datetime(2019, 8, 22, tz='local').start_of('day'),
		pendulum.datetime(2019, 8, 22, tz='local').end_of('day')
	)
	assert args.created_before == pendulum.interval(
		pendulum.DateTime.min,
		pendulum.datetime(2019, 8, 22, 16, tz='local')
	)
	assert args.created_after == pendulum.interval(
		pendulum.datetime(2019, 8, 22, 16, tz='local'),
		pendulum.DateTime.max
	)
	assert args.modified_in == pendulum.interval(
		pendulum.datetime(2019, 8, 1, tz='local'),
		pendulum.datetime(2019, 8, 31, tz='local').end_of('day')
	)
	assert args.modified_on == pendulum.interval(
		pendulum.datetime(2019, 8, 22, tz='local').start_of('day'),
		pendulum.datetime(2019, 8, 22, tz='local').end_of('day')
	)
	assert args.modified_before == pendulum.interval(
		pendulum.DateTime.min,
		pendulum.datetime(2019, 8, 22, 16, tz='local')
	)
	assert args.modified_after == pendulum.interval(
		pendulum.datetime(2019, 8, 22, 16, tz='local'),
		pendulum.DateTime.max
	)


def test_create_parser_local():
	local = create_parser_local()
	args = local.parse_args(
		[
			'--no-recursion',
			'--max-depth', '3',
			'-xp', 'test1',
			'--exclude-path', 'test2',
			'-xr', '.*.mp3',
			'--exclude-regex', '^.*.flac$',
			'-xg', '*.mp3',
			'--exclude-glob', '*.flac'
		]
	)

	assert args.no_recursion is True
	assert args.max_depth == 3
	assert args.exclude_paths == ['test1', 'test2']
	assert args.exclude_regexes == ['.*.mp3', '^.*.flac$']
	assert args.exclude_globs == ['*.mp3', '*.flac']


def test_create_parser_logging():
	logging_ = create_parser_logging()
	args = logging_.parse_args(
		[
			'-vvv',
			'-qq',
			'--debug',
			'--log-to-stdout',
			'--no-log-to-stdout',
			'--log-to-file',
			'--no-log-to-file'
		]
	)

	assert args.verbose == 3
	assert args.quiet == 2
	assert args.debug is True
	assert args.log_to_stdout is True
	assert args.no_log_to_stdout is True
	assert args.log_to_file is True
	assert args.no_log_to_file is True


def test_create_parser_meta():
	create_parser_meta('title', 1.0)


def test_create_parser_yes():
	yes = create_parser_yes()

	args = yes.parse_args(['-y'])
	assert args.yes is True

	args = yes.parse_args(['--yes'])
	assert args.yes is True


def test_merge_defaults():
	merged = merge_defaults(
		{'option1': 'default'},
		{'option2': 'parsed'}
	)

	assert merged.option1 == 'default'
	assert merged.option2 == 'parsed'


def test_parse_args():
	assert parse_args(create_parser_dry_run()) == Namespace()
	assert parse_args(create_parser_dry_run(), ['-n']) == Namespace(dry_run=True)
