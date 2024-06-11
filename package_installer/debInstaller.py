# SPDX-FileCopyrightText: 2024 Ferenc Nandor Janky <ferenj@effective-range.com>
# SPDX-FileCopyrightText: 2024 Attila Gombos <attila.gombos@effective-range.com>
# SPDX-License-Identifier: MIT

from typing import Optional

from apt import Cache, Package as AptPackage
from apt.debfile import DebPackage
from context_logger import get_logger
from package_downloader import IDebDownloader, PackageConfig

from package_installer import IDebProvider

log = get_logger('DebInstaller')


class IDebInstaller(object):

    def install(self, package_config: PackageConfig) -> bool:
        raise NotImplementedError()


class DebInstaller(IDebInstaller):

    def __init__(self, apt_cache: Cache, deb_downloader: IDebDownloader, deb_provider: IDebProvider):
        self._apt_cache = apt_cache
        self._deb_downloader = deb_downloader
        self._deb_provider = deb_provider

    def install(self, package_config: PackageConfig) -> bool:
        package = self._download_package(package_config)

        if not package:
            return False

        version = self._get_package_file_version(package)

        try:
            self._prepare_install(package)

            log.info('Installing package file', package=package.pkgname, version=version, file=package.filename)
            package.install()
        except Exception as error:
            log.error('Error during installing package file',
                      package=package.pkgname, version=version, file=package.filename, error=error)

        if self._is_package_installed(package):
            log.info('Package file installed successfully',
                     package=package.pkgname, version=version, file=package.filename)
            return True

        return False

    def _download_package(self, package_config: PackageConfig) -> Optional[DebPackage]:
        package_file = self._deb_downloader.download(package_config)

        if package_file:
            return self._deb_provider.get_deb_package(package_file)

        return None

    def _get_package_file_version(self, package: DebPackage) -> str:
        return package._sections['Version']

    def _prepare_install(self, deb_package: DebPackage) -> None:
        if not deb_package.check_conflicts():
            self._remove_conflicting_packages(deb_package)

        if deb_package.depends:
            self._install_missing_dependencies(deb_package)

    def _remove_conflicting_packages(self, package: DebPackage) -> None:
        for conflict in package.conflicts:
            conflicting = conflict[0][0]
            apt_package = self._apt_cache.get(conflicting)
            if apt_package and apt_package.is_installed:
                log.info('Removing conflicting package', package=package.pkgname, conflict=conflicting)
                apt_package.mark_delete()
                self._apt_cache.commit()
        self._apt_cache.open()

    def _install_missing_dependencies(self, package: DebPackage) -> None:
        for depends in package.depends:
            dependency = depends[0][0]
            apt_package = self._apt_cache.get(dependency)
            if apt_package and not apt_package.is_installed:
                log.info('Installing missing dependency', package=package.pkgname, dependency=dependency)
                apt_package.mark_install()
                self._apt_cache.commit()
        self._apt_cache.open()

    def _is_package_installed(self, package: DebPackage) -> bool:
        self._apt_cache.open()
        apt_package: AptPackage = self._apt_cache.get(package.pkgname)
        return apt_package.is_installed if apt_package else False
