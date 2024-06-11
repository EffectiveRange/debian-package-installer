#!/usr/bin/env python3

# SPDX-FileCopyrightText: 2024 Ferenc Nandor Janky <ferenj@effective-range.com>
# SPDX-FileCopyrightText: 2024 Attila Gombos <attila.gombos@effective-range.com>
# SPDX-License-Identifier: MIT

import os
from argparse import ArgumentParser, ArgumentDefaultsHelpFormatter, Namespace
from pathlib import Path

import apt
from aptsources.sourceslist import SourcesList
from context_logger import get_logger, setup_logging
from package_downloader import FileDownloader, DebDownloader, AssetDownloader, RepositoryProvider, \
    SessionProvider, JsonLoader

from package_installer import PackageInstaller, DebInstaller, AptInstaller, DebProvider, SourceAdder, KeyAdder

log = get_logger('PackageInstallerApp')


def main() -> None:
    arguments = _get_arguments()

    setup_logging('package-installer', arguments.log_level, arguments.log_file)

    log.info('Starting package installer', arguments=vars(arguments))

    json_loader = JsonLoader()
    session_provider = SessionProvider()
    file_downloader = FileDownloader(session_provider, _get_absolute_path(arguments.download))

    if arguments.source_config:
        source_config = _get_absolute_path(arguments.source_config)
        sources_list = SourcesList()
        key_adder = KeyAdder()
        source_adder = SourceAdder(source_config, json_loader, sources_list, key_adder, file_downloader)
    else:
        source_adder = None

    repository_provider = RepositoryProvider()
    asset_downloader = AssetDownloader(file_downloader)
    deb_downloader = DebDownloader(repository_provider, asset_downloader, file_downloader)

    config = _get_absolute_path(arguments.package_config)
    apt_cache = apt.Cache()
    apt_installer = AptInstaller(apt_cache)
    deb_provider = DebProvider(apt_cache)
    deb_installer = DebInstaller(apt_cache, deb_downloader, deb_provider)

    package_installer = PackageInstaller(config, json_loader, apt_cache, apt_installer, deb_installer, source_adder)

    package_installer.install_packages()


def _get_arguments() -> Namespace:
    parser = ArgumentParser(formatter_class=ArgumentDefaultsHelpFormatter)
    parser.add_argument('-f', '--log-file', help='log file path')
    parser.add_argument('-l', '--log-level', help='logging level', default='info')
    parser.add_argument('-s', '--source-config', help='source config JSON file')
    parser.add_argument('-d', '--download', help='package download location', default='/tmp/packages')

    parser.add_argument('package_config', help='package config JSON file')

    return parser.parse_args()


def _get_absolute_path(path: str) -> str:
    return path if path.startswith('/') else f'{_get_resource_root()}/{path}'


def _get_resource_root() -> str:
    return str(Path(os.path.dirname(__file__)).parent.absolute())


if __name__ == '__main__':
    main()
