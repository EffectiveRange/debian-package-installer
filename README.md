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
    pip install dist/debian_package_installer-1.0.0.tar.gz
    ```

3. Install from GitHub repository
    ```bash
    pip install git+https://github.com/EffectiveRange/debian-package-installer.git@latest
    ```

## Usage

### Command line reference

```commandline
$ bin/debian-package-installer.py --help
usage: debian-package-installer.py [-h] [-f LOG_FILE] [-l LOG_LEVEL] [-s SOURCE_CONFIG] [-d DOWNLOAD] package_config

positional arguments:
  package_config        package config JSON file

options:
  -h, --help            show this help message and exit
  -f LOG_FILE, --log-file LOG_FILE
                        log file path (default: None)
  -l LOG_LEVEL, --log-level LOG_LEVEL
                        logging level (default: info)
  -s SOURCE_CONFIG, --source-config SOURCE_CONFIG
                        source config JSON file (default: None)
  -d DOWNLOAD, --download DOWNLOAD
                        package download location (default: /tmp/packages)
```

### Example

```commandline
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

```commandline
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

```commandline
2024-06-30T15:43:13.356457Z [info     ] Starting package installer     [PackageInstallerApp] app_version=none application=package-installer arguments={'log_file': None, 'log_level': 'info', 'source_config': 'build/sources.json', 'download': '/tmp/packages', 'package_config': 'build/packages.json'} hostname=Legion7iPro
2024-06-30T15:43:13.458664Z [info     ] Adding apt sources             [PackageInstaller] app_version=none application=package-installer hostname=Legion7iPro
2024-06-30T15:43:13.658914Z [info     ] Adding apt source              [SourceAdder] app_version=none application=package-installer hostname=Legion7iPro source=deb http://aptrepo.effective-range.com stable main
2024-06-30T15:43:13.659251Z [info     ] Key not found, trying to add   [SourceAdder] app_version=none application=package-installer hostname=Legion7iPro key_id=C1AEE2EDBAEC37595801DDFAE15BC62117A4E0F3 source=deb http://aptrepo.effective-range.com stable main
2024-06-30T15:43:13.659409Z [info     ] Downloading key file           [SourceAdder] app_version=none application=package-installer hostname=Legion7iPro key_id=C1AEE2EDBAEC37595801DDFAE15BC62117A4E0F3 source=deb http://aptrepo.effective-range.com stable main url=http://aptrepo.effective-range.com/dists/stable/public.key
2024-06-30T15:43:13.659539Z [info     ] Downloading file               [FileDownloader] app_version=none application=package-installer file_name=effective-range.pub headers=[] hostname=Legion7iPro url=http://aptrepo.effective-range.com/dists/stable/public.key
2024-06-30T15:43:13.733118Z [info     ] Downloaded file                [FileDownloader] app_version=none application=package-installer file=/tmp/packages/effective-range.pub hostname=Legion7iPro
2024-06-30T15:43:13.733936Z [info     ] Adding key from key file       [SourceAdder] app_version=none application=package-installer hostname=Legion7iPro key_file=/tmp/packages/effective-range.pub key_id=C1AEE2EDBAEC37595801DDFAE15BC62117A4E0F3 source=deb http://aptrepo.effective-range.com stable main
2024-06-30T15:43:14.183844Z [info     ] Key added                      [SourceAdder] app_version=none application=package-installer hostname=Legion7iPro key_id=C1AEE2EDBAEC37595801DDFAE15BC62117A4E0F3 source=deb http://aptrepo.effective-range.com stable main
2024-06-30T15:43:15.050601Z [info     ] Installing package             [PackageInstaller] app_version=none application=package-installer hostname=Legion7iPro package=apt-server version=1.1.4
2024-06-30T15:43:15.051703Z [info     ] Installing package from repository [AptInstaller] app_version=none application=package-installer hostname=Legion7iPro package=apt-server version=1.1.4
Selecting previously unselected package apt-server.
(Reading database ... 84451 files and directories currently installed.)
Preparing to unpack .../apt-server_1.1.4_all.deb ...
Unpacking apt-server (1.1.4) ...
Setting up apt-server (1.1.4) ...
2024-06-30T15:43:16.760278Z [info     ] Package installed successfully [AptInstaller] app_version=none application=package-installer hostname=Legion7iPro package=apt-server version=1.1.4
```
