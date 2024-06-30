# SPDX-FileCopyrightText: 2024 Ferenc Nandor Janky <ferenj@effective-range.com>
# SPDX-FileCopyrightText: 2024 Attila Gombos <attila.gombos@effective-range.com>
# SPDX-License-Identifier: MIT

from urllib.parse import urlparse

from aptsources.sourceslist import SourcesList, SourceEntry
from context_logger import get_logger
from package_downloader import IFileDownloader, IJsonLoader

from package_installer import SourceConfig, IKeyAdder

log = get_logger('SourceAdder')


class ISourceAdder(object):

    def add_sources(self) -> None:
        raise NotImplementedError()


class SourceAdder(ISourceAdder):

    def __init__(self, config_path: str, json_loader: IJsonLoader, sources_list: SourcesList, key_adder: IKeyAdder,
                 file_downloader: IFileDownloader) -> None:
        self._config_path = config_path
        self._json_loader = json_loader
        self._sources_list = sources_list
        self._key_adder = key_adder
        self._file_downloader = file_downloader
        self._available_key_ids: list[str] = []

    def add_sources(self) -> None:
        config_list = self._json_loader.load_list(self._config_path, SourceConfig)

        self._refresh_keys()

        for config in config_list:
            log.info('Adding apt source', source=config.source)
            entry = SourceEntry(config.source)
            self._sources_list.add(entry.type, entry.uri, entry.dist, entry.comps)
            self._add_key_for_source(config)

        self._sources_list.save()

    def _add_key_for_source(self, config: SourceConfig) -> None:
        source = config.source
        key_id = config.key_id

        if self._is_key_missing(key_id):
            log.info('Key not found, trying to add', key_id=key_id, source=source)
        else:
            log.info('Key found', key_id=key_id, source=source)
            return

        if self._is_key_missing(key_id) and config.key_server:
            self._add_from_key_server(config, config.key_server)

        if self._is_key_missing(key_id) and config.key_file:
            self._add_from_key_file(config, config.key_file)

        if self._is_key_missing(key_id):
            log.warn('Failed to add key', key_id=key_id, source=source)
        else:
            log.info('Key added', key_id=key_id, source=source)

    def _add_from_key_server(self, config: SourceConfig, key_server: str) -> None:
        log.info('Adding key from key server', key_server=key_server, key_id=config.key_id, source=config.source)
        self._key_adder.add_from_key_server(key_server, config.key_id)
        self._refresh_keys()

    def _add_from_key_file(self, config: SourceConfig, key_file: str) -> None:
        if urlparse(config.key_file).scheme:
            log.info('Downloading key file', url=config.key_file, key_id=config.key_id, source=config.source)
            key_file_path = self._file_downloader.download(key_file, f'{config.name}.pub')
        else:
            key_file_path = key_file

        log.info('Adding key from key file', key_file=key_file_path, key_id=config.key_id, source=config.source)

        self._key_adder.add_from_key_file(key_file_path)
        self._refresh_keys()

    def _refresh_keys(self) -> None:
        self._available_key_ids = self._key_adder.get_available_key_ids()

    def _is_key_missing(self, key_id_last_16: str) -> bool:
        key_id_last_16 = key_id_last_16[-16:]
        return key_id_last_16 not in self._available_key_ids
