import pytest
from pendulum import (
	DateTime,
	datetime,
	interval,
	today,
	yesterday
)
from pendulum.tz import fixed_timezone

from tbm_utils import datetime_string_to_time_period
from tbm_utils.datetime import _convert_to_int


def test_convert_to_int():
	assert _convert_to_int(None) is None
	assert _convert_to_int(3) == 3
	assert _convert_to_int('3') == 3

	with pytest.raises(ValueError):
		_convert_to_int('test')


def test_datetime_string_to_time_period_no_kwargs():
	with pytest.raises(ValueError):
		datetime_string_to_time_period('today')


@pytest.mark.parametrize(
	'dt_string',
	[
		'text',
		'2019/08',
		'2019-08-22-16:00:00',
		'2019-08-22T16-00-00',
		'2019-08-22T16:00:00|5:00',
		'2019-08-22T16:00:00-5-00',
		'16:00:00'
	]
)
def test_datetime_string_to_time_period_unsupported_datetime_string(dt_string):
	with pytest.raises(ValueError):
		datetime_string_to_time_period(dt_string, on=True)


@pytest.mark.parametrize(
	'dt_string, expected',
	[
		(
			'2019',
			interval(
				datetime(2019, 1, 1, tz='local').start_of('year'),
				datetime(2019, 12, 31, tz='local').end_of('year')
			)
		),
		(
			'2019-08',
			interval(
				datetime(2019, 8, 1, tz='local').start_of('month'),
				datetime(2019, 8, 31, tz='local').end_of('month')
			)
		),
		(
			'201908',
			interval(
				datetime(2019, 8, 1, tz='local').start_of('month'),
				datetime(2019, 8, 31, tz='local').end_of('month')
			)
		)
	]
)
def test_datetime_string_to_time_period_in(dt_string, expected):
	assert datetime_string_to_time_period(dt_string, in_=True) == expected


@pytest.mark.parametrize(
	'dt_string',
	[
		'today',
		'yesterday'
		'2019-08-22',
		'2019-08-22T16:00:00'
	]
)
def test_datetime_string_to_time_period_in_unsupported_datetime_string(dt_string):
	with pytest.raises(ValueError):
		datetime_string_to_time_period(dt_string, in_=True)


@pytest.mark.parametrize(
	'dt_string, expected',
	[
		(
			'today',
			interval(
				today(),
				today().end_of('day')
			)
		),
		(
			'yesterday',
			interval(
				yesterday(),
				yesterday().end_of('day')
			)
		),
		(
			'2019-08-22',
			interval(
				datetime(2019, 8, 22, tz='local').start_of('day'),
				datetime(2019, 8, 22, tz='local').end_of('day')
			)
		),
		(
			'20190822',
			interval(
				datetime(2019, 8, 22, tz='local').start_of('day'),
				datetime(2019, 8, 22, tz='local').end_of('day')
			)
		)
	]
)
def test_datetime_string_to_time_period_on(dt_string, expected):
	assert datetime_string_to_time_period(dt_string, on=True) == expected


@pytest.mark.parametrize(
	'dt_string',
	[
		'2019-08',
		'2019-08-22T16:00:00'
	]
)
def test_datetime_string_to_time_period_on_unsupported_datetime_string(dt_string):
	with pytest.raises(ValueError):
		datetime_string_to_time_period(dt_string, on=True)


@pytest.mark.parametrize(
	'dt_string, expected',
	[
		(
			'today',
			interval(
				DateTime.min,
				today()
			)
		),
		(
			'yesterday',
			interval(
				DateTime.min,
				yesterday()
			)
		),
		(
			'2019',
			interval(
				DateTime.min,
				datetime(2019, 1, 1, tz='local')
			)
		),
		(
			'2019-08',
			interval(
				DateTime.min,
				datetime(2019, 8, 1, tz='local')
			)
		),
		(
			'201908',
			interval(
				DateTime.min,
				datetime(2019, 8, 1, tz='local')
			)
		),
		(
			'2019-08-22',
			interval(
				DateTime.min,
				datetime(2019, 8, 22, tz='local')
			)
		),
		(
			'20190822',
			interval(
				DateTime.min,
				datetime(2019, 8, 22, tz='local')
			)
		),
		(
			'2019-08-22T16',
			interval(
				DateTime.min,
				datetime(2019, 8, 22, 16, tz='local')
			)
		),
		(
			'2019-08-22T16:00',
			interval(
				DateTime.min,
				datetime(2019, 8, 22, 16, tz='local')
			)
		),
		(
			'2019-08-22T16:00:00',
			interval(
				DateTime.min,
				datetime(2019, 8, 22, 16, tz='local')
			)
		),
		(
			'2019-08-22 16:00:00',
			interval(
				DateTime.min,
				datetime(2019, 8, 22, 16, tz='local')
			)
		),
		(
			'2019-08-22T16:00:00 04',
			interval(
				DateTime.min,
				datetime(2019, 8, 22, 16, tz=fixed_timezone(4 * 3600))
			)
		),
		(
			'2019-08-22T16:00:00+04',
			interval(
				DateTime.min,
				datetime(2019, 8, 22, 16, tz=fixed_timezone(4 * 3600))
			)
		),
		(
			'2019-08-22T16:00:00-04',
			interval(
				DateTime.min,
				datetime(2019, 8, 22, 16, tz=fixed_timezone(-4 * 3600))
			)
		),
		(
			'2019-08-22T16:00:00 04:00',
			interval(
				DateTime.min,
				datetime(2019, 8, 22, 16, tz=fixed_timezone(4 * 3600))
			)
		),
		(
			'2019-08-22T16:00:00+04:00',
			interval(
				DateTime.min,
				datetime(2019, 8, 22, 16, tz=fixed_timezone(4 * 3600))
			)
		),
		(
			'2019-08-22T16:00:00-04:00',
			interval(
				DateTime.min,
				datetime(2019, 8, 22, 16, tz=fixed_timezone(-4 * 3600))
			)
		),
		(
			'2019-08-22T16:00:00 04:30',
			interval(
				DateTime.min,
				datetime(2019, 8, 22, 16, tz=fixed_timezone((4 * 3600) + (30 * 60)))
			)
		),
		(
			'2019-08-22T16:00:00+04:30',
			interval(
				DateTime.min,
				datetime(2019, 8, 22, 16, tz=fixed_timezone((4 * 3600) + (30 * 60)))
			)
		),
		(
			'2019-08-22T16:00:00-04:30',
			interval(
				DateTime.min,
				datetime(2019, 8, 22, 16, tz=fixed_timezone((-4 * 3600) - (30 * 60)))
			)
		)
	]
)
def test_datetime_string_to_time_period_before(dt_string, expected):
	assert datetime_string_to_time_period(dt_string, before=True) == expected


@pytest.mark.parametrize(
	'dt_string, expected',
	[
		(
			'today',
			interval(
				today().end_of('day'),
				DateTime.max
			)
		),
		(
			'yesterday',
			interval(
				yesterday().end_of('day'),
				DateTime.max
			)
		),
		(
			'2019',
			interval(
				datetime(2019, 12, 31, tz='local').end_of('year'),
				DateTime.max
			)
		),
		(
			'2019-08',
			interval(
				datetime(2019, 8, 31, tz='local').end_of('month'),
				DateTime.max
			)
		),
		(
			'201908',
			interval(
				datetime(2019, 8, 31, tz='local').end_of('month'),
				DateTime.max
			)
		),
		(
			'2019-08-22',
			interval(
				datetime(2019, 8, 22, tz='local').end_of('day'),
				DateTime.max
			)
		),
		(
			'20190822',
			interval(
				datetime(2019, 8, 22, tz='local').end_of('day'),
				DateTime.max
			)
		),
		(
			'2019-08-22T16',
			interval(
				datetime(2019, 8, 22, 16, tz='local'),
				DateTime.max
			)
		),
		(
			'2019-08-22T16:00',
			interval(
				datetime(2019, 8, 22, 16, tz='local'),
				DateTime.max
			)
		),
		(
			'2019-08-22T16:00:00',
			interval(
				datetime(2019, 8, 22, 16, tz='local'),
				DateTime.max
			)
		),
		(
			'2019-08-22 16:00:00',
			interval(
				datetime(2019, 8, 22, 16, tz='local'),
				DateTime.max
			)
		),
		(
			'2019-08-22T16:00:00 04',
			interval(
				datetime(2019, 8, 22, 16, tz=fixed_timezone(4 * 3600)),
				DateTime.max
			)
		),
		(
			'2019-08-22T16:00:00+04',
			interval(
				datetime(2019, 8, 22, 16, tz=fixed_timezone(4 * 3600)),
				DateTime.max
			)
		),
		(
			'2019-08-22T16:00:00-04',
			interval(
				datetime(2019, 8, 22, 16, tz=fixed_timezone(-4 * 3600)),
				DateTime.max
			)
		),
		(
			'2019-08-22T16:00:00 04:00',
			interval(
				datetime(2019, 8, 22, 16, tz=fixed_timezone(4 * 3600)),
				DateTime.max
			)
		),
		(
			'2019-08-22T16:00:00+04:00',
			interval(
				datetime(2019, 8, 22, 16, tz=fixed_timezone(4 * 3600)),
				DateTime.max
			)
		),
		(
			'2019-08-22T16:00:00-04:00',
			interval(
				datetime(2019, 8, 22, 16, tz=fixed_timezone(-4 * 3600)),
				DateTime.max
			)
		),
		(
			'2019-08-22T16:00:00 04:30',
			interval(
				datetime(2019, 8, 22, 16, tz=fixed_timezone((4 * 3600) + (30 * 60))),
				DateTime.max
			)
		),
		(
			'2019-08-22T16:00:00+04:30',
			interval(
				datetime(2019, 8, 22, 16, tz=fixed_timezone((4 * 3600) + (30 * 60))),
				DateTime.max
			)
		),
		(
			'2019-08-22T16:00:00-04:30',
			interval(
				datetime(2019, 8, 22, 16, tz=fixed_timezone((-4 * 3600) - (30 * 60))),
				DateTime.max
			)
		)
	]
)
def test_datetime_string_to_time_period_after(dt_string, expected):
	assert datetime_string_to_time_period(dt_string, after=True) == expected
