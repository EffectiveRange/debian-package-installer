import unittest
from unittest import TestCase, mock
from unittest.mock import MagicMock

from apt import Cache
from context_logger import setup_logging
from package_downloader import PackageConfig, IJsonLoader

from package_installer import PackageInstaller, IAptInstaller, IDebInstaller, ISourceAdder


class PackageInstallerTest(TestCase):

    @classmethod
    def setUpClass(cls):
        setup_logging('debian-package-installer', 'DEBUG', warn_on_overwrite=False)

    def setUp(self):
        print()

    def test_install_packages_initialize_apt_cache(self):
        # Given
        json_loader, apt_cache, apt_installer, deb_installer, source_adder = create_components([])
        package_installer = PackageInstaller('path', json_loader, apt_cache, apt_installer, deb_installer, source_adder)

        # When
        package_installer.install_packages()

        # Then
        apt_cache.assert_has_calls([
            mock.call.open(),
            mock.call.update()
        ])

    def test_install_packages_from_apt_repository(self):
        # Given
        config_list = create_config_list()
        json_loader, apt_cache, apt_installer, deb_installer, source_adder = create_components(config_list)
        package_installer = PackageInstaller('path', json_loader, apt_cache, apt_installer, deb_installer, source_adder)

        # When
        package_installer.install_packages()

        # Then
        apt_installer.install.assert_has_calls([
            mock.call(config_list[0]), mock.call().__bool__(),
            mock.call(config_list[1]), mock.call().__bool__(),
            mock.call(config_list[2]), mock.call().__bool__()])

    def test_install_packages_from_dep_package(self):
        # Given
        config_list = create_config_list()
        json_loader, apt_cache, apt_installer, deb_installer, source_adder = create_components(config_list)
        apt_installer.install.side_effect = [False, False, False]
        package_installer = PackageInstaller('path', json_loader, apt_cache, apt_installer, deb_installer, source_adder)

        # When
        package_installer.install_packages()

        # Then
        apt_installer.install.assert_has_calls([
            mock.call(config_list[0]),
            mock.call(config_list[1]),
            mock.call(config_list[2])])
        deb_installer.install.assert_has_calls([
            mock.call(config_list[0]), mock.call().__bool__(),
            mock.call(config_list[1]), mock.call().__bool__(),
            mock.call(config_list[2]), mock.call().__bool__()])

    def test_install_packages_fail_to_install(self):
        # Given
        config_list = create_config_list()
        json_loader, apt_cache, apt_installer, deb_installer, source_adder = create_components(config_list)
        apt_installer.install.side_effect = [False, False, False]
        deb_installer.install.side_effect = [False, False, False]
        package_installer = PackageInstaller('path', json_loader, apt_cache, apt_installer, deb_installer, source_adder)

        # When
        package_installer.install_packages()

        # Then
        apt_installer.install.assert_has_calls([
            mock.call(config_list[0]),
            mock.call(config_list[1]),
            mock.call(config_list[2])])
        deb_installer.install.assert_has_calls([
            mock.call(config_list[0]),
            mock.call(config_list[1]),
            mock.call(config_list[2])])

    def test_install_packages_with_mixed_outcome(self):
        # Given
        config_list = create_config_list()
        json_loader, apt_cache, apt_installer, deb_installer, source_adder = create_components(config_list)
        apt_installer.install.side_effect = [True, False, False]
        deb_installer.install.side_effect = [True, False]
        package_installer = PackageInstaller('path', json_loader, apt_cache, apt_installer, deb_installer, source_adder)

        # When
        package_installer.install_packages()

        # Then
        apt_installer.install.assert_has_calls([
            mock.call(config_list[0]),
            mock.call(config_list[1]),
            mock.call(config_list[2])])
        deb_installer.install.assert_has_calls([
            mock.call(config_list[1]),
            mock.call(config_list[2])])


def create_config_list():
    return [
        PackageConfig(package='package1'),
        PackageConfig(package='package2'),
        PackageConfig(package='package3')
    ]


def create_components(config_list):
    json_loader = MagicMock(spec=IJsonLoader)
    json_loader.load_list.return_value = config_list
    apt_cache = MagicMock(spec=Cache)
    apt_installer = MagicMock(spec=IAptInstaller)
    deb_installer = MagicMock(spec=IDebInstaller)
    source_adder = MagicMock(spec=ISourceAdder)
    return json_loader, apt_cache, apt_installer, deb_installer, source_adder


if __name__ == '__main__':
    unittest.main()
