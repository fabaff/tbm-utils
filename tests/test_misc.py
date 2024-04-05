from pathlib import Path

import pendulum

from tbm_utils import (
	filter_filepaths_by_dates,
	get_filepaths,
)

TEST_DIR = Path(__file__).parent / 'files'
TEST_DIR.mkdir(exist_ok=True)
for path in TEST_DIR.iterdir():
	path.unlink()

for name in [
	'test_file.1',
	'test_file.2',
	'test_file.3',
	'test_file.4',
	'test_file.5',
]:
	(TEST_DIR / name).touch()

TEST_FILEPATHS = list(TEST_DIR.iterdir())

THIS = pendulum.now()
LAST = THIS.start_of('year').previous(pendulum.MONDAY)

THIS_YEAR = pendulum.interval(
	THIS.start_of('year'),
	THIS.end_of('year'),
)

TODAY = pendulum.interval(
	THIS.start_of('day'),
	THIS.end_of('day'),
)

YESTERDAY = pendulum.interval(
	THIS.subtract(days=1).start_of('day'),
	THIS.subtract(days=1).end_of('day'),
)

LAST_YEAR = pendulum.interval(
	LAST.start_of('year'),
	LAST.end_of('year'),
)


# TODO: More test situations.
def test_filter_filepaths_by_dates():
	assert list(filter_filepaths_by_dates(TEST_FILEPATHS)) == TEST_FILEPATHS

	assert list(
		filter_filepaths_by_dates(
			TEST_FILEPATHS,
			creation_dates=[LAST_YEAR]
		)
	) == []

	assert list(
		filter_filepaths_by_dates(
			TEST_FILEPATHS,
			creation_dates=[THIS_YEAR]
		)
	) == TEST_FILEPATHS

	assert list(
		filter_filepaths_by_dates(
			TEST_FILEPATHS,
			creation_dates=[YESTERDAY]
		)
	) == []

	assert list(
		filter_filepaths_by_dates(
			TEST_FILEPATHS,
			creation_dates=[TODAY]
		)
	) == TEST_FILEPATHS

	assert list(
		filter_filepaths_by_dates(
			TEST_FILEPATHS,
			creation_dates=[
				pendulum.interval(
					pendulum.DateTime.min,
					THIS.start_of('day'),
				)
			]
		)
	) == []

	assert list(
		filter_filepaths_by_dates(
			TEST_FILEPATHS,
			creation_dates=[
				pendulum.interval(
					pendulum.DateTime.min,
					THIS.add(days=1),
				)
			]
		)
	) == TEST_FILEPATHS

	assert list(
		filter_filepaths_by_dates(
			TEST_FILEPATHS,
			creation_dates=[
				pendulum.interval(
					THIS.add(days=1),
					pendulum.DateTime.max,
				)
			]
		)
	) == []

	assert list(
		filter_filepaths_by_dates(
			TEST_FILEPATHS,
			creation_dates=[
				pendulum.interval(
					THIS.start_of('day'),
					pendulum.DateTime.max,
				)
			]
		)
	) == TEST_FILEPATHS

	assert list(
		filter_filepaths_by_dates(
			TEST_FILEPATHS,
			modification_dates=[LAST_YEAR]
		)
	) == []

	assert list(
		filter_filepaths_by_dates(
			TEST_FILEPATHS,
			modification_dates=[THIS_YEAR]
		)
	) == TEST_FILEPATHS

	assert list(
		filter_filepaths_by_dates(
			TEST_FILEPATHS,
			modification_dates=[YESTERDAY]
		)
	) == []

	assert list(
		filter_filepaths_by_dates(
			TEST_FILEPATHS,
			modification_dates=[TODAY]
		)
	) == TEST_FILEPATHS

	assert list(
		filter_filepaths_by_dates(
			TEST_FILEPATHS,
			modification_dates=[
				pendulum.interval(
					pendulum.DateTime.min,
					THIS.start_of('day'),
				)
			]
		)
	) == []

	assert list(
		filter_filepaths_by_dates(
			TEST_FILEPATHS,
			modification_dates=[
				pendulum.interval(
					pendulum.DateTime.min,
					THIS.add(days=1),
				)
			]
		)
	) == TEST_FILEPATHS

	assert list(
		filter_filepaths_by_dates(
			TEST_FILEPATHS,
			modification_dates=[
				pendulum.interval(
					THIS.add(days=1),
					pendulum.DateTime.max,
				)
			]
		)
	) == []

	assert list(
		filter_filepaths_by_dates(
			TEST_FILEPATHS,
			modification_dates=[
				pendulum.interval(
					THIS.start_of('day'),
					pendulum.DateTime.max,
				)
			]
		)
	) == TEST_FILEPATHS


def test_get_filepaths():
	assert list(get_filepaths(TEST_FILEPATHS)) == TEST_FILEPATHS
	assert list(get_filepaths([TEST_DIR])) == TEST_FILEPATHS
	assert list(get_filepaths([str(TEST_DIR)])) == TEST_FILEPATHS
	assert list(get_filepaths(TEST_DIR / 'test_file.1')) == [TEST_DIR / 'test_file.1']

	assert list(get_filepaths(TEST_FILEPATHS, exclude_paths=['test_file'])) == []
	assert list(get_filepaths(TEST_FILEPATHS, exclude_regexes=['test_.*'])) == []
	assert list(get_filepaths(TEST_DIR, exclude_paths=['test_file'])) == []
	assert list(get_filepaths(TEST_DIR, exclude_regexes=['test_.*'])) == []
	assert list(get_filepaths(TEST_DIR, exclude_globs=['test_*.*'])) == []
