# SPDX-FileCopyrightText: 2024 Ferenc Nandor Janky <ferenj@effective-range.com>
# SPDX-FileCopyrightText: 2024 Attila Gombos <attila.gombos@effective-range.com>
# SPDX-License-Identifier: MIT

from typing import Optional

from apt import Cache, Package
from context_logger import get_logger
from package_downloader import PackageConfig

log = get_logger('AptInstaller')


class IAptInstaller(object):

    def install(self, package_config: PackageConfig) -> bool:
        raise NotImplementedError()


class AptInstaller(IAptInstaller):

    def __init__(self, apt_cache: Cache):
        self._apt_cache = apt_cache

    def install(self, package_config: PackageConfig) -> bool:
        package = self._get_apt_package(package_config)

        if not package:
            return False

        if package.is_installed:
            installed_version = self._get_installed_version(package)
            log.info('Package is already installed', package=package.name, version=installed_version)
            return True

        version = self._get_candidate_version(package)

        try:
            log.info('Installing package from repository', package=package.name, version=version)
            package.mark_install()
            self._apt_cache.commit()
            self._apt_cache.open()

            if package.is_installed:
                installed_version = self._get_installed_version(package)
                log.info('Package installed successfully', package=package.name, version=installed_version)
                return True
        except Exception as error:
            self._apt_cache.clear()
            log.error('Error during package installation', package=package.name, version=version, error=error)

        return False

    def _get_apt_package(self, package_config: PackageConfig) -> Optional[Package]:
        package: Package = self._apt_cache.get(package_config.package)

        if package and package_config.version:
            target_version = package.versions.get(package_config.version)
            if target_version:
                package.candidate = target_version
            else:
                log.error('Package version is not available', package=package_config.package,
                          version=package_config.version, available_versions=package.versions.keys())
                return None

        return package

    def _get_installed_version(self, package: Package) -> Optional[str]:
        return package.installed.version if package.installed else None

    def _get_candidate_version(self, package: Package) -> Optional[str]:
        return package.candidate.version if package.candidate else None
