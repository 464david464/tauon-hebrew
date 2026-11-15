# תרגום עברי מלא ל-Tauon Music Box 🎵🇮🇱

חבילת לוקליזציה מלאה לעברית עבור נגן המוזיקה **Tauon Music Box** (כולל תמיכה מלאה בגרסת ה-Flatpak הרשמית `com.github.taiko2k.tauonmb`).

## מה כלול במאגר?
- **`locale/he/LC_MESSAGES/tauon.po` ו-`tauon.mo`** – תרגום מלא, תמציתי ומדויק לפי הקשר של כל **2,286** מחרוזות הממשק (תפריטים, חלון ההגדרות, כפתורים, עמודות טבלה, עורך התגיות, עורך המילים והתראות).
- **`usercustomize.py`** – רכיב טעינה אוטומטי לסביבת Python בתוך ה-Flatpak, שמחבר את קובץ השפה העברי למנוע ה-`gettext` של הנגן ושומר על ההערות בעברית בקובץ ההגדרות גם כשהאפליקציה מייצרת אותו מחדש.
- **`config/tauon_he.conf`** – קובץ הגדרות מתורגם לעברית.
- **`config/input_he.txt`** – קובץ קיצורי המקלדת והעכבר מתורגם לעברית.
- **`install.sh`** – סקריפט התקנה אוטומטי בפקודה אחת.

---

## התקנה במחשב חדש

```bash
git clone https://github.com/464david464/tauon-hebrew.git
cd tauon-hebrew
chmod +x install.sh
./install.sh
```

לאחר הרצת `./install.sh`, הפעל את **Tauon Music Box** והממשק כולו יעלה בעברית.
