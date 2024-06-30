import logging
import re
import subprocess

from setuptools import setup


def get_python_apt_version() -> str:
    proc = subprocess.Popen(['dpkg-query', '-W', '-f', '${Version}', 'python3-apt'],
                            stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    out, _ = proc.communicate()

    if proc.returncode == 0:
        version = out.decode('utf-8').strip()
        if version:
            version = clean_version(version)
            logging.info(f'Using python-apt version {version}')
            if version == '2.6.0':
                version = 'a1ecf380cb6688a239c30f2786424f864e9b32af'
            return version

    logging.error('Failed to get python-apt version. Please install python3-apt debian package.')

    exit(1)


def clean_version(version: str) -> str:
    match = re.match(r'(\d+\.\d+\.\d+)', version)
    return match.group(1) if match else version


setup(
    name='debian-package-installer',
    version='1.0.0',
    description='Debian package installer',
    author='Ferenc Nandor Janky & Attila Gombos',
    author_email='info@effective-range.com',
    packages=['package_installer'],
    scripts=['bin/debian-package-installer.py'],
    package_data={'package_installer': ['py.typed']},
    install_requires=['PyGithub', 'requests', 'pydantic',
                      f'python-apt@git+https://salsa.debian.org/apt-team/python-apt@{get_python_apt_version()}',
                      'python-context-logger@git+https://github.com/EffectiveRange/python-context-logger.git@latest',
                      'debian-package-downloader'
                      '@git+https://github.com/EffectiveRange/debian-package-downloader.git@latest']
)
