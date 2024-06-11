# SPDX-FileCopyrightText: 2024 Ferenc Nandor Janky <ferenj@effective-range.com>
# SPDX-FileCopyrightText: 2024 Attila Gombos <attila.gombos@effective-range.com>
# SPDX-License-Identifier: MIT

from typing import Optional

from apt import Cache
from apt.debfile import DebPackage
from context_logger import get_logger

log = get_logger('DebPackageProvider')


class IDebProvider(object):

    def get_deb_package(self, package_file: str) -> Optional[DebPackage]:
        raise NotImplementedError()


class DebProvider(IDebProvider):

    def __init__(self, apt_cache: Cache):
        self._apt_cache = apt_cache

    def get_deb_package(self, package_file: str) -> Optional[DebPackage]:
        try:
            return DebPackage(package_file, cache=self._apt_cache)
        except Exception as error:
            log.error('Error while reading package file', file=package_file, error=error)
            return None
