import unittest
from unittest import TestCase
from unittest.mock import MagicMock

from apt import Cache, Package, Version
from context_logger import setup_logging
from package_downloader import PackageConfig

from package_installer import AptInstaller


class AptInstallerTest(TestCase):

    @classmethod
    def setUpClass(cls):
        setup_logging('debian-package-installer', 'DEBUG', warn_on_overwrite=False)

    def setUp(self):
        print()

    def test_install_returns_false_when_package_not_found(self):
        # Given
        apt_cache = MagicMock(spec=Cache)
        apt_cache.get.return_value = None
        apt_installer = AptInstaller(apt_cache)
        package_config = PackageConfig(package='package1')

        # When
        result = apt_installer.install(package_config)

        # Then
        self.assertFalse(result)

    def test_install_returns_false_when_package_with_target_version_not_found(self):
        # Given
        apt_cache = MagicMock(spec=Cache)
        apt_package = MagicMock(spec=Package)
        apt_package.versions = {'version2': MagicMock(spec=Version)}
        apt_cache.get.return_value = apt_package
        apt_installer = AptInstaller(apt_cache)
        package_config = PackageConfig(package='package1', version='version1')

        # When
        result = apt_installer.install(package_config)

        # Then
        self.assertFalse(result)

    def test_install_returns_true_when_package_with_target_version_is_found_and_package_is_already_installed(self):
        # Given
        apt_cache = MagicMock(spec=Cache)
        apt_package = create_apt_package()
        apt_package.is_installed = True
        apt_package.versions = {'version1': MagicMock(spec=Version)}
        apt_cache.get.return_value = apt_package
        apt_installer = AptInstaller(apt_cache)
        package_config = PackageConfig(package='package1', version='version1')

        # When
        result = apt_installer.install(package_config)

        # Then
        self.assertTrue(result)

    def test_install_returns_true_when_package_is_installed_successfully(self):
        # Given
        apt_cache = MagicMock(spec=Cache)
        apt_package = create_apt_package()
        apt_package.mark_install.side_effect = lambda: setattr(apt_package, 'is_installed', True)
        apt_cache.get.return_value = apt_package
        apt_installer = AptInstaller(apt_cache)
        package_config = PackageConfig(package='package1')

        # When
        result = apt_installer.install(package_config)

        # Then
        self.assertTrue(result)
        apt_cache.commit.assert_called_once()
        apt_cache.open.assert_called_once()

    def test_install_returns_false_when_package_is_not_installed_successfully(self):
        # Given
        apt_cache = MagicMock(spec=Cache)
        apt_package = create_apt_package()
        apt_cache.get.return_value = apt_package
        apt_installer = AptInstaller(apt_cache)
        package_config = PackageConfig(package='package1')

        # When
        result = apt_installer.install(package_config)

        # Then
        self.assertFalse(result)
        apt_cache.commit.assert_called_once()
        apt_cache.open.assert_called_once()

    def test_install_returns_false_when_exception_raised_on_install(self):
        # Given
        apt_cache = MagicMock(spec=Cache)
        apt_package = create_apt_package()
        apt_cache.get.return_value = apt_package
        apt_cache.commit.side_effect = Exception('Error')
        apt_installer = AptInstaller(apt_cache)
        package_config = PackageConfig(package='package1')

        # When
        result = apt_installer.install(package_config)

        # Then
        self.assertFalse(result)
        apt_cache.commit.assert_called_once()


def create_apt_package():
    apt_package = MagicMock(spec=Package)
    apt_package.name = 'package1'
    apt_package.is_installed = False
    apt_package.candidate.version = 'version1'
    apt_package.installed.version = 'version1'
    return apt_package


if __name__ == '__main__':
    unittest.main()
