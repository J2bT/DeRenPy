# DeRenPy
#
# Copyright (C) 2026 J2bT
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.
#
# SPDX-License-Identifier: GPL-3.0-or-later

import gettext
from pathlib import Path

from . import ROOT


class TranslationManager():
    def __init__(self, domain: str = "derenpy", localedir: Path = ROOT / "locales"):
        self.domain = domain
        self.localedir = localedir
        self._cache = {}
        self._current_getter = lambda x: x

    def load(self, lang: str):
        if lang not in self._cache:
            self._cache[lang] = gettext.translation(
                self.domain,
                self.localedir,
                languages=[lang],
                fallback=True,
            )
        self._current_getter = self._cache[lang].gettext

    def gettext(self, message: str) -> str:
        return self._current_getter(message)


_translator = TranslationManager()


def _(message: str) -> str:
    return _translator.gettext(message)
