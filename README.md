# Transkripce MP3 do textu

Jednoduchá Flask aplikace, která přijme MP3 soubor, přepíše ho pomocí OpenAI Whisper a zobrazí text na webu.

Požadavky:
- Python 3.8+
- ffmpeg v PATH
- nainstalované závislosti: viz `requirements.txt`

Spuštění (lokálně):

1. Vytvořte virtuální prostředí a nainstalujte závislosti:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

2. Spusťte aplikaci:

```bash
python app.py
```

Otevřete http://localhost:5000 a nahrajte MP3.

Poznámky:
- Pokud nechcete instalovat `whisper` místně, můžete upravit `app.py` a připojit externí API pro přepis.
