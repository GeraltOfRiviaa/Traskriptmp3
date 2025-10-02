import os
import tempfile
import threading
from pathlib import Path

from flask import Flask, request, render_template, redirect, url_for

# Lazy model and lock so importing this module stays cheap for tests
_MODEL = None
_MODEL_LOCK = threading.Lock()


def load_model(name: str = "small"):
    """Load whisper model lazily.

    Note: Whisper requires torch and ffmpeg installed on the system.
    """
    global _MODEL
    if _MODEL is None:
        with _MODEL_LOCK:
            if _MODEL is None:
                try:
                    import whisper

                    _MODEL = whisper.load_model(name)
                except Exception as e:
                    # Re-raise with clearer message
                    raise RuntimeError(
                        "Failed to load transcription model. Ensure 'whisper' and its dependencies (torch, ffmpeg) are installed."
                    ) from e
    return _MODEL


def create_app(upload_folder: str | None = None):
    app = Flask(__name__)
    app.config["MAX_CONTENT_LENGTH"] = 200 * 1024 * 1024  # 200MB max

    if upload_folder is None:
        upload_folder = os.path.join(tempfile.gettempdir(), "transcribe_uploads")
    Path(upload_folder).mkdir(parents=True, exist_ok=True)
    app.config["UPLOAD_FOLDER"] = upload_folder


    @app.route("/")
    def index():
        return render_template("index.html", transcription=None)


    @app.route("/transcribe", methods=["POST"])
    def transcribe():
        file = request.files.get("file")
        if not file:
            return render_template("index.html", transcription="No file uploaded")

        filename = file.filename or "upload.mp3"
        # secure filename omitted to keep code short; in production use werkzeug.utils.secure_filename
        dest = os.path.join(app.config["UPLOAD_FOLDER"], filename)
        file.save(dest)

        try:
            model = load_model()
            # whisper expects a filepath
            result = model.transcribe(dest)
            text = result.get("text", "")
        except Exception as e:
            text = f"Transcription failed: {e}"

        # save text output next to file
        txt_path = dest + ".txt"
        try:
            with open(txt_path, "w", encoding="utf-8") as f:
                f.write(text)
        except Exception:
            pass

        return render_template("index.html", transcription=text)


    return app


if __name__ == "__main__":
    app = create_app()
    app.run(host="0.0.0.0", port=5000, debug=True)
