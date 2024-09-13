# SPDX-FileCopyrightText: 2024 Ferenc Nandor Janky <ferenj@effective-range.com>
# SPDX-FileCopyrightText: 2024 Attila Gombos <attila.gombos@effective-range.com>
# SPDX-License-Identifier: MIT

from typing import Optional

from apt import Cache
from common_utility.jsonLoader import IJsonLoader
from context_logger import get_logger
from package_downloader import PackageConfig

from package_installer import IAptInstaller, IDebInstaller, ISourceAdder

log = get_logger('PackageInstaller')


class PackageInstaller(object):

    def __init__(
        self,
        config_path: str,
        json_loader: IJsonLoader,
        apt_cache: Cache,
        apt_installer: IAptInstaller,
        deb_installer: IDebInstaller,
        source_adder: Optional[ISourceAdder] = None,
    ) -> None:
        self._config_path = config_path
        self._json_loader = json_loader
        self._apt_cache = apt_cache
        self._apt_installer = apt_installer
        self._deb_installer = deb_installer
        self._source_adder = source_adder

    def install_packages(self) -> None:
        if self._source_adder:
            log.info('Adding apt sources')
            self._source_adder.add_sources()

        log.info('Updating apt cache')
        self._apt_cache.open()
        self._apt_cache.update()
        self._apt_cache.open()

        config_list = self._json_loader.load_list(self._config_path, PackageConfig)

        for config in config_list:
            log.info('Installing package', package=config.package, version=config.version)

            if self._apt_installer.install(config):
                continue

            log.warn('Package is not available from apt repository', package=config.package)

            if self._deb_installer.install(config):
                continue

            log.error('Failed to install package', package=config.package)
