import unittest
from unittest import TestCase
from unittest.mock import MagicMock

from apt import Cache, Package
from apt.debfile import DebPackage
from context_logger import setup_logging
from package_downloader import IDebDownloader, PackageConfig

from package_installer import IDebProvider, DebInstaller


class DebInstallerTest(TestCase):

    @classmethod
    def setUpClass(cls):
        setup_logging('debian-package-installer', 'DEBUG', warn_on_overwrite=False)

    def setUp(self):
        print()

    def test_install_returns_true_when_package_is_installed_successfully(self):
        # Given
        apt_cache, deb_downloader, deb_provider = create_components()
        deb_installer = DebInstaller(apt_cache, deb_downloader, deb_provider)
        package_config = PackageConfig(package='package1')

        # When
        result = deb_installer.install(package_config)

        # Then
        self.assertTrue(result)

    def test_install_returns_false_when_package_file_download_failed(self):
        # Given
        apt_cache, deb_downloader, deb_provider = create_components()
        deb_downloader.download.return_value = None
        deb_installer = DebInstaller(apt_cache, deb_downloader, deb_provider)
        package_config = PackageConfig(package='package1')

        # When
        result = deb_installer.install(package_config)

        # Then
        self.assertFalse(result)

    def test_install_returns_false_when_deb_package_creation_failed(self):
        # Given
        apt_cache, deb_downloader, deb_provider = create_components()
        deb_provider.get_deb_package.return_value = None
        deb_installer = DebInstaller(apt_cache, deb_downloader, deb_provider)
        package_config = PackageConfig(package='package1')

        # When
        result = deb_installer.install(package_config)

        # Then
        self.assertFalse(result)

    def test_install_returns_true_when_conflicting_package_is_removed(self):
        # Given
        apt_cache, deb_downloader, deb_provider = create_components()
        deb_package = create_deb_package()
        deb_package.check_conflicts.return_value = False
        deb_package.conflicts = [[('package2', '', '')]]
        deb_provider.get_deb_package.return_value = deb_package
        apt_package = create_apt_package()
        conflict = create_apt_package()
        conflict.name = 'package2'
        conflict.is_installed = True
        apt_cache.get.side_effect = [conflict, apt_package]
        deb_installer = DebInstaller(apt_cache, deb_downloader, deb_provider)
        package_config = PackageConfig(package='package1')

        # When
        result = deb_installer.install(package_config)

        # Then
        self.assertTrue(result)

    def test_install_returns_true_when_package_dependency_is_installed(self):
        # Given
        apt_cache, deb_downloader, deb_provider = create_components()
        deb_package = create_deb_package()
        deb_package.depends = [[('package0', '', '')]]
        deb_provider.get_deb_package.return_value = deb_package
        apt_package = create_apt_package()
        dependency = create_apt_package()
        dependency.name = 'package0'
        dependency.is_installed = False
        apt_cache.get.side_effect = [dependency, apt_package]
        deb_installer = DebInstaller(apt_cache, deb_downloader, deb_provider)
        package_config = PackageConfig(package='package1')

        # When
        result = deb_installer.install(package_config)

        # Then
        self.assertTrue(result)

    def test_install_returns_false_when_deb_package_install_failed(self):
        # Given
        apt_cache, deb_downloader, deb_provider = create_components()
        deb_package = create_deb_package()
        deb_package.install.side_effect = Exception('Install failed')
        deb_provider.get_deb_package.return_value = deb_package
        apt_package = create_apt_package()
        apt_package.is_installed = False
        apt_cache.get.return_value = apt_package
        deb_installer = DebInstaller(apt_cache, deb_downloader, deb_provider)
        package_config = PackageConfig(package='package1')

        # When
        result = deb_installer.install(package_config)

        # Then
        self.assertFalse(result)


def create_apt_package():
    apt_package = MagicMock(spec=Package)
    apt_package.name = 'package1'
    apt_package.is_installed = True

    return apt_package


def create_deb_package():
    deb_package = MagicMock(spec=DebPackage)
    deb_package.filename = 'package1.deb'
    deb_package.pkgname = 'package1'
    deb_package._sections = {'Version': '1.0.0'}

    return deb_package


def create_components():
    apt_cache = MagicMock(spec=Cache)
    apt_cache.get.return_value = create_apt_package()
    deb_downloader = MagicMock(spec=IDebDownloader)
    deb_downloader.download.return_value = 'package1.deb'
    deb_provider = MagicMock(spec=IDebProvider)
    deb_provider.get_deb_package.return_value = create_deb_package()

    return apt_cache, deb_downloader, deb_provider


if __name__ == '__main__':
    unittest.main()
