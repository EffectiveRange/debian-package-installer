import unittest
from unittest import TestCase
from unittest.mock import MagicMock

from aptsources.sourceslist import SourcesList
from context_logger import setup_logging
from package_downloader import IJsonLoader, IFileDownloader

from package_installer import IKeyAdder, SourceAdder, SourceConfig


class SourceAdderTest(TestCase):

    @classmethod
    def setUpClass(cls):
        setup_logging('debian-package-installer', 'DEBUG', warn_on_overwrite=False)

    def setUp(self):
        print()

    def test_add_sources_adds_sources_and_keys(self):
        # Given
        json_loader, sources_list, key_adder, file_downloader = create_components()
        source_adder = SourceAdder('path/to/config.json', json_loader, sources_list, key_adder, file_downloader)

        # When
        source_adder.add_sources()

        # Then
        sources_list.add.assert_any_call('deb', 'http://url1', 'stable', ['main'])
        key_adder.add_from_key_server.assert_any_call('keyserver.test1.com', '0123456789ABCDEF012345671111111111111111')
        sources_list.add.assert_any_call('deb', 'http://url2', 'stable', ['main'])
        key_adder.add_from_key_file.assert_any_call('/path/to/public2.key')
        sources_list.add.assert_any_call('deb', 'http://url3', 'stable', ['main'])
        key_adder.add_from_key_file.assert_any_call('/path/to/public3.key')

    def test_add_sources_fails_to_add_key(self):
        # Given
        json_loader, sources_list, key_adder, file_downloader = create_components()
        key_adder.get_available_key_ids.side_effect = [['1111111111111111'], [], []]
        source_adder = SourceAdder('path/to/config.json', json_loader, sources_list, key_adder, file_downloader)

        # When
        source_adder.add_sources()

        # Then
        sources_list.add.assert_any_call('deb', 'http://url1', 'stable', ['main'])
        sources_list.add.assert_any_call('deb', 'http://url2', 'stable', ['main'])
        key_adder.add_from_key_file.assert_any_call('/path/to/public2.key')
        sources_list.add.assert_any_call('deb', 'http://url3', 'stable', ['main'])
        key_adder.add_from_key_file.assert_any_call('/path/to/public3.key')


def create_components():
    json_loader = MagicMock(spec=IJsonLoader)
    json_loader.load_list.return_value = [
        SourceConfig(name='source1', source='deb http://url1 stable main',
                     key_id='0123456789ABCDEF012345671111111111111111',
                     key_file='http://url1/dists/stable/public1.key',
                     key_server='keyserver.test1.com'),
        SourceConfig(name='source2', source='deb http://url2 stable main',
                     key_id='0123456789ABCDEF012345672222222222222222',
                     key_file='http://url2/dists/stable/public2.key'),
        SourceConfig(name='source3', source='deb http://url3 stable main',
                     key_id='0123456789ABCDEF012345673333333333333333',
                     key_file='/path/to/public3.key')
    ]
    sources_list = MagicMock(spec=SourcesList)
    key_adder = MagicMock(spec=IKeyAdder)
    key_adder.get_available_key_ids.side_effect = [
        [],
        ['1111111111111111'],
        ['2222222222222222'],
        ['3333333333333333']
    ]
    file_downloader = MagicMock(spec=IFileDownloader)
    file_downloader.download.return_value = '/path/to/public2.key'

    return json_loader, sources_list, key_adder, file_downloader


if __name__ == '__main__':
    unittest.main()
