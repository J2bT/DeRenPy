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
