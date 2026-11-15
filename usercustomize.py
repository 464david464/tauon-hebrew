import builtins
import gettext
import os
import sys
import types
from pathlib import Path

def _setup_tauon_hebrew_l10n():
    candidates = [
        Path("/var/data/TauonMusicBox/locale"),
        Path.home() / ".var/app/com.github.taiko2k.tauonmb/data/TauonMusicBox/locale",
        Path.home() / ".local/share/TauonMusicBox/locale",
    ]
    locale_dir = None
    for c in candidates:
        if (c / "he" / "LC_MESSAGES" / "tauon.mo").exists():
            locale_dir = str(c)
            break

    if not locale_dir:
        return

    try:
        tr = gettext.translation("tauon", localedir=locale_dir, languages=["he"], fallback=True)
    except Exception:
        return

    builtins._ = tr.gettext
    builtins.N_ = lambda x: x

    class _ProtectedBuiltins(types.ModuleType):
        def __setattr__(self, name, value):
            if name == "_" and callable(value):
                # Ignore Tauon's initial `builtins._ = lambda x: x` overwrite at import time
                if getattr(value, "__name__", "") == "<lambda>":
                    try:
                        if value("__tauon_probe__") == "__tauon_probe__":
                            return
                    except Exception:
                        pass
            super().__setattr__(name, value)

    try:
        builtins.__class__ = _ProtectedBuiltins
    except Exception:
        pass

    _orig_find = gettext.find
    _orig_translation = gettext.translation

    def _patched_find(domain, localedir=None, languages=None, all=False):
        if domain == "tauon":
            res = _orig_find(domain, localedir=locale_dir, languages=["he"], all=all)
            if res:
                return res
        return _orig_find(domain, localedir=localedir, languages=languages, all=all)

    def _patched_translation(domain, localedir=None, languages=None, class_=None, fallback=False, codeset=None):
        if domain == "tauon":
            try:
                return _orig_translation(
                    domain,
                    localedir=locale_dir,
                    languages=["he"],
                    class_=class_,
                    fallback=fallback,
                )
            except Exception:
                pass
        return _orig_translation(
            domain,
            localedir=localedir,
            languages=languages,
            class_=class_,
            fallback=fallback,
        )

    gettext.find = _patched_find
    gettext.translation = _patched_translation

    # Also preserve Hebrew comments in tauon.conf when Tauon regenerates it
    try:
        conf_he_candidates = [
            Path("/var/data/TauonMusicBox/tauon_he.conf"),
            Path.home() / ".var/app/com.github.taiko2k.tauonmb/data/TauonMusicBox/tauon_he.conf",
        ]
        he_comments_by_key = {}
        for p in conf_he_candidates:
            if p.is_file():
                for line in p.read_text(encoding="utf-8").splitlines():
                    if "=" in line and " #" in line and not line.lstrip().startswith("#"):
                        k = line.split("=", 1)[0].strip()
                        c = line.split("#", 1)[1].strip()
                        he_comments_by_key[k] = c
                break

        header_comment_map = {
            "# Tauon Music Box configuration file": "# קובץ התצורה של Tauon Music Box",
            "# This file will be regenerated while app is running. Formatting and additional comments will be lost.": "# קובץ זה נוצר מחדש בזמן ריצת האפליקציה. עיצוב והערות נוספות יימחקו.",
            "# Tip: Use TOML syntax highlighting": "# טיפ: מומלץ להשתמש בהדגשת תחביר TOML",
            "# Changes take effect on tag rescan": "# השינויים יחולו בעת סריקת תגיות מחדש",
            "# Changes take effect on restart": "# השינויים יחולו בהפעלה מחדש",
            "# Numbers are in seconds": "# המספרים בשניות",
        }

        from tauon.t_modules import t_config
        _orig_dump = t_config.Config.dump

        def _patched_dump(self, path: str) -> None:
            for item in self.live:
                if item[0] == "comment" and item[1] in header_comment_map:
                    item[1] = header_comment_map[item[1]]
                elif item[0] != "comment" and len(item) > 3 and item[1] in he_comments_by_key:
                    item[3] = he_comments_by_key[item[1]]
            return _orig_dump(self, path)

        t_config.Config.dump = _patched_dump
    except Exception:
        pass

_setup_tauon_hebrew_l10n()
