# SPDX-FileCopyrightText: 2024 Ferenc Nandor Janky <ferenj@effective-range.com>
# SPDX-FileCopyrightText: 2024 Attila Gombos <attila.gombos@effective-range.com>
# SPDX-License-Identifier: MIT

from apt import auth


class IKeyAdder(object):

    def add_from_key_file(self, file_path: str) -> None:
        raise NotImplementedError()

    def add_from_key_server(self, key_server: str, key_id: str) -> None:
        raise NotImplementedError()

    def get_available_key_ids(self) -> list[str]:
        raise NotImplementedError()


class KeyAdder(IKeyAdder):

    def add_from_key_file(self, file_path: str) -> None:
        auth.add_key_from_file(file_path)

    def add_from_key_server(self, key_server: str, key_id: str) -> None:
        auth.add_key_from_keyserver(key_id, key_server)

    def get_available_key_ids(self) -> list[str]:
        return [key.keyid for key in auth.list_keys()]
