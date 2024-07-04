#!/usr/bin/env python3

# SPDX-FileCopyrightText: 2024 Ferenc Nandor Janky <ferenj@effective-range.com>
# SPDX-FileCopyrightText: 2024 Attila Gombos <attila.gombos@effective-range.com>
# SPDX-License-Identifier: MIT

import os
from argparse import ArgumentParser, ArgumentDefaultsHelpFormatter, Namespace

from apt.cache import Cache
from aptsources.sourceslist import SourcesList
from context_logger import get_logger, setup_logging
from package_downloader import FileDownloader, DebDownloader, AssetDownloader, RepositoryProvider, \
    SessionProvider, JsonLoader

from package_installer import PackageInstaller, DebInstaller, AptInstaller, DebProvider, SourceAdder, KeyAdder

log = get_logger('PackageInstallerApp')


def main() -> None:
    arguments = _get_arguments()

    setup_logging('debian-package-installer', arguments.log_level, arguments.log_file)

    log.info('Starting package installer', arguments=vars(arguments))

    json_loader = JsonLoader()
    session_provider = SessionProvider()
    file_downloader = FileDownloader(session_provider, os.path.abspath(arguments.download))

    if arguments.source_config:
        source_config_path = file_downloader.download(arguments.source_config, skip_if_exists=False)
        sources_list = SourcesList()
        key_adder = KeyAdder()
        source_adder = SourceAdder(source_config_path, json_loader, sources_list, key_adder, file_downloader)
    else:
        source_adder = None

    repository_provider = RepositoryProvider()
    asset_downloader = AssetDownloader(file_downloader)
    deb_downloader = DebDownloader(repository_provider, asset_downloader, file_downloader)

    apt_cache = Cache()
    apt_installer = AptInstaller(apt_cache)
    deb_provider = DebProvider(apt_cache)
    deb_installer = DebInstaller(apt_cache, deb_downloader, deb_provider)

    package_config_path = file_downloader.download(arguments.package_config, skip_if_exists=False)

    package_installer = PackageInstaller(package_config_path, json_loader,
                                         apt_cache, apt_installer, deb_installer, source_adder)

    package_installer.install_packages()


def _get_arguments() -> Namespace:
    parser = ArgumentParser(formatter_class=ArgumentDefaultsHelpFormatter)
    parser.add_argument('-f', '--log-file', help='log file path')
    parser.add_argument('-l', '--log-level', help='logging level', default='info')
    parser.add_argument('-s', '--source-config', help='source config JSON file or URL')
    parser.add_argument('-d', '--download', help='package download location', default='/tmp/packages')

    parser.add_argument('package_config', help='package config JSON file or URL')

    return parser.parse_args()


if __name__ == '__main__':
    main()
