"""WoundSense AI Launcher Script."""
import sys
import uvicorn
from app.config import HOST, PORT

if __name__ == "__main__":
    # Ensure stdout handles UTF-8 gracefully on Windows consoles
    if sys.platform == "win32":
        try:
            sys.stdout.reconfigure(encoding="utf-8")
        except Exception:
            pass

    print("=" * 70)
    print("  [+] WoundSense AI - Wound Analysis & Treatment Support System")
    print(f"  Server URL: http://{HOST}:{PORT}")
    print("  Offline Edge CV Mode: ENABLED")
    print("  Medical Knowledge Base: ACTIVE")
    print("=" * 70)
    uvicorn.run("app.main:app", host=HOST, port=PORT, reload=False)
