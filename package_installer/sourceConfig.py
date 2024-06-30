# SPDX-FileCopyrightText: 2024 Ferenc Nandor Janky <ferenj@effective-range.com>
# SPDX-FileCopyrightText: 2024 Attila Gombos <attila.gombos@effective-range.com>
# SPDX-License-Identifier: MIT

from typing import Optional

from pydantic import BaseModel


class SourceConfig(BaseModel):
    name: str
    source: str
    key_id: str
    key_file: Optional[str] = None
    key_server: Optional[str] = None

    def __repr__(self) -> str:
        return (f'SourceConfig(name={self.name}, source={self.source}, '
                f'key_id={self.key_id}, key_file={self.key_file}, key_server={self.key_server})')
