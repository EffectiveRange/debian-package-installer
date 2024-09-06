
[![Test and Release](https://github.com/EffectiveRange/debian-package-installer/actions/workflows/test_and_release.yml/badge.svg)](https://github.com/EffectiveRange/debian-package-installer/actions/workflows/test_and_release.yml)
[![Coverage badge](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/EffectiveRange/debian-package-installer/python-coverage-comment-action-data/endpoint.json)](https://htmlpreview.github.io/?https://github.com/EffectiveRange/debian-package-installer/blob/python-coverage-comment-action-data/htmlcov/index.html)

# debian-package-installer

Debian package installer that supports installing from APT repository, .deb file URL and .deb GitHub release asset

## Table of contents

- [Features](#features)
- [Requirements](#requirements)
- [Installation](#installation)
  - [Install from source root directory](#install-from-source-root-directory)
  - [Install from source distribution](#install-from-source-distribution)
- [Usage](#usage)
  - [Command line reference](#command-line-reference)
  - [Example](#example)
  - [Example with APT repository source configuration](#example-with-apt-repository-source-configuration)

## Features

- [x] Install from APT repository
- [x] Install from .deb file URL
- [x] Install from .deb GitHub release asset
- [x] Adding custom APT repository
- [x] Adding custom APT key

## Requirements

- [Python3](https://www.python.org/downloads/)
- [PyGithub](https://pygithub.readthedocs.io/en/latest/index.html)
- [requests](https://requests.readthedocs.io/en/latest/)
- [pydantic](https://docs.pydantic.dev/latest/#pydantic-examples)
- [python-apt](https://apt-team.pages.debian.net/python-apt/library/index.html)

## Installation

### Install from source root directory

```bash
pip install .
```

### Install from source distribution

1. Create source distribution
    ```bash
    python setup.py sdist
    ```

2. Install from distribution file
    ```bash
    pip install dist/debian-package-installer-1.0.0.tar.gz
    ```

3. Install from GitHub repository
    ```bash
    pip install git+https://github.com/EffectiveRange/debian-package-installer.git@latest
    ```

## Usage

### Command line reference

```bash
$ bin/debian-package-installer.py --help
usage: debian-package-installer.py [-h] [-f LOG_FILE] [-l LOG_LEVEL] [-s SOURCE_CONFIG] [-d DOWNLOAD] package_config

positional arguments:
  package_config        package config JSON file or URL

options:
  -h, --help            show this help message and exit
  -f LOG_FILE, --log-file LOG_FILE
                        log file path (default: None)
  -l LOG_LEVEL, --log-level LOG_LEVEL
                        logging level (default: info)
  -s SOURCE_CONFIG, --source-config SOURCE_CONFIG
                        source config JSON file or URL (default: None)
  -d DOWNLOAD, --download DOWNLOAD
                        package download location (default: /tmp/packages)
```

### Example

```bash
$ bin/debian-package-installer.py ~/config/package-config.json
```

Example configuration (example `package-config.json` config file content):

```json
[
  {
    "name": "wifi-manager",
    "release": {
      "repo": "EffectiveRange/wifi-manager",
      "tag": "latest",
      "matcher": "*armhf.deb"
    }
  },
  {
    "name": "pic18-q20-programmer",
    "release": {
      "repo": "EffectiveRange/pic18-q20-programmer",
      "tag": "v0.3.0",
      "matcher": "*armhf.deb"
    }
  },
  {
    "name": "filebeat",
    "file_url": "https://github.com/EffectiveRange/elastic-beats-armhf-deb/releases/download/v8.12.2/filebeat-8.12.2-armv7l.deb"
  }
]
```

### Example with APT repository source configuration

Needs root privileges to add APT keys:

```bash
$ sudo bin/debian-package-installer.py ~/config/package-config.json -s ~/config/source-config.json
```

Example configuration (example `package-config.json` config file content):

```json
[
  {
    "package": "apt-server",
    "version": "1.1.4"
  }
]
```

Example source configuration (example `source-config.json` config file content):

```json
[
  {
    "name": "effective-range",
    "source": "deb http://aptrepo.effective-range.com stable main",
    "key_id": "C1AEE2EDBAEC37595801DDFAE15BC62117A4E0F3",
    "key_file": "http://aptrepo.effective-range.com/dists/stable/public.key",
    "keyserver": "keyserver.ubuntu.com"
  }
]
```

Output:

```bash
2024-07-04T07:16:37.793684Z [info     ] Starting package installer     [PackageInstallerApp] app_version=1.0.0 application=debian-package-installer arguments={'log_file': None, 'log_level': 'info', 'source_config': 'build/source-config.json', 'download': '/tmp/packages', 'package_config': 'build/package-config.json'} hostname=Legion7iPro
2024-07-04T07:16:37.794110Z [info     ] Local file path provided, skipping download [FileDownloader] app_version=1.0.0 application=debian-package-installer file=/home/attilagombos/EffectiveRange/debian-package-installer/build/source-config.json hostname=Legion7iPro
2024-07-04T07:16:37.906907Z [info     ] Local file path provided, skipping download [FileDownloader] app_version=1.0.0 application=debian-package-installer file=/home/attilagombos/EffectiveRange/debian-package-installer/build/package-config.json hostname=Legion7iPro
2024-07-04T07:16:37.907573Z [info     ] Adding apt sources             [PackageInstaller] app_version=1.0.0 application=debian-package-installer hostname=Legion7iPro
2024-07-04T07:16:38.148153Z [info     ] Adding apt source              [SourceAdder] app_version=1.0.0 application=debian-package-installer hostname=Legion7iPro source=deb http://aptrepo.effective-range.com stable main
2024-07-04T07:16:38.148625Z [info     ] Key not found, trying to add   [SourceAdder] app_version=1.0.0 application=debian-package-installer hostname=Legion7iPro key_id=C1AEE2EDBAEC37595801DDFAE15BC62117A4E0F3 source=deb http://aptrepo.effective-range.com stable main
2024-07-04T07:16:38.148831Z [info     ] Adding key from key server     [SourceAdder] app_version=1.0.0 application=debian-package-installer hostname=Legion7iPro key_id=C1AEE2EDBAEC37595801DDFAE15BC62117A4E0F3 key_server=keyserver.ubuntu.com source=deb http://aptrepo.effective-range.com stable main
gpg: WARNING: "--secret-keyring" is an obsolete option - it has no effect
gpg: keybox '/tmp/tmpj0fdcfku/pubring.gpg' created
gpg: /tmp/tmpj0fdcfku/trustdb.gpg: trustdb created
gpg: key E15BC62117A4E0F3: public key "Test User <test.user@example.com>" imported
gpg: Total number processed: 1
gpg:               imported: 1
2024-07-04T07:16:39.041188Z [info     ] Key added                      [SourceAdder] app_version=1.0.0 application=debian-package-installer hostname=Legion7iPro key_id=C1AEE2EDBAEC37595801DDFAE15BC62117A4E0F3 source=deb http://aptrepo.effective-range.com stable main
2024-07-04T07:16:39.041686Z [info     ] Updating apt cache             [PackageInstaller] app_version=1.0.0 application=debian-package-installer hostname=Legion7iPro
2024-07-04T07:16:39.795518Z [info     ] Installing package             [PackageInstaller] app_version=1.0.0 application=debian-package-installer hostname=Legion7iPro package=apt-server version=None
2024-07-04T07:16:39.796189Z [info     ] Installing package from repository [AptInstaller] app_version=1.0.0 application=debian-package-installer hostname=Legion7iPro package=apt-server version=1.1.4
Selecting previously unselected package apt-server.
(Reading database ... 84451 files and directories currently installed.)
Preparing to unpack .../apt-server_1.1.4_all.deb ...
Unpacking apt-server (1.1.4) ...
Setting up apt-server (1.1.4) ...
2024-07-04T07:16:41.277165Z [info     ] Package installed successfully [AptInstaller] app_version=1.0.0 application=debian-package-installer hostname=Legion7iPro package=apt-server version=1.1.4
```
