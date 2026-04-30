#!/usr/bin/env python3
"""Send a handoff to Telegram so the user can copy-paste it on any other machine.

Sends, in this order:
  1. A short header chat message with code + URL.
  2. The handoff content split in <=3500 char chunks, one Telegram message each.
     Each chunk is plain text with "[CODE · 1/N]" prefix so the user can long-press
     to copy on any device.
  3. The same handoff as a downloadable .md document (Telegram sendDocument
     pulls the file from the public GitHub Pages URL).

Usage:
  scripts/send-handoff-telegram.py handoff/2026-04-30-HX-GPMZ.md

Requires no extra deps (stdlib only). Bridge URL hardcoded to the production
admira-telegram-bridge worker.
"""
from __future__ import annotations

import json
import os
import sys
import re
import time
import urllib.request
import urllib.error
from pathlib import Path

BRIDGE = "https://admira-telegram-bridge.csilvasantin.workers.dev"
PAGES_BASE = "https://csilvasantin.github.io/diario"
CHUNK_LIMIT = 3500  # leave 596 chars of headroom under Telegram's 4096 limit
HEADER_FMT = "[{code} · {i}/{n}]\n"


def _post(path: str, payload: dict) -> dict:
    body = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(
        BRIDGE + path,
        data=body,
        headers={
            "Content-Type": "application/json",
            # Cloudflare's edge protection blocks the default Python-urllib UA
            # with error 1010. Use a real browser-style UA.
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 14_5) AppleWebKit/537.36 (KHTML, like Gecko) handoff-telegram/1.0",
        },
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=20) as resp:
            return json.loads(resp.read().decode("utf-8") or "{}")
    except urllib.error.HTTPError as e:
        try:
            return json.loads(e.read().decode("utf-8") or "{}")
        except Exception:
            return {"ok": False, "status": e.code, "error": str(e)}
    except Exception as e:
        return {"ok": False, "error": str(e)}


def split_into_chunks(text: str, code: str, max_len: int = CHUNK_LIMIT) -> list[str]:
    """Split markdown into chunks at section boundaries when possible."""
    # Section breaks: a line that starts with "## " (Markdown H2) or "# " (H1).
    sections = re.split(r"(?=^#{1,2} )", text, flags=re.MULTILINE)
    chunks: list[str] = []
    buf = ""
    for sec in sections:
        if not sec:
            continue
        # Reserve space for the [CODE · i/N] header
        reserve = len(HEADER_FMT.format(code=code, i=99, n=99))
        room = max_len - reserve
        # If a single section is bigger than `room`, hard-split it on paragraphs.
        if len(sec) > room:
            paragraphs = sec.split("\n\n")
            for p in paragraphs:
                if len(p) > room:
                    # Last resort: chop on raw chars
                    for i in range(0, len(p), room):
                        piece = p[i : i + room]
                        if len(buf) + len(piece) + 2 > room and buf:
                            chunks.append(buf)
                            buf = ""
                        buf += piece + "\n"
                else:
                    if len(buf) + len(p) + 2 > room and buf:
                        chunks.append(buf)
                        buf = ""
                    buf += p + "\n\n"
        else:
            if len(buf) + len(sec) > room and buf:
                chunks.append(buf)
                buf = ""
            buf += sec
    if buf.strip():
        chunks.append(buf)
    return [c.rstrip() + "\n" for c in chunks if c.strip()]


def parse_handoff(path: Path) -> tuple[str, str, str]:
    """Return (code, title, content) extracted from a handoff file."""
    text = path.read_text(encoding="utf-8")
    # Title: "# Handoff HX-GPMZ — Studio + Suno gating"
    m = re.search(r"^#\s+Handoff\s+(HX-[A-Z0-9]+)\s*—\s*(.+)$", text, re.MULTILINE)
    if not m:
        raise SystemExit("No se pudo encontrar el código HX-XXXX en el handoff.")
    code = m.group(1)
    title = m.group(2).strip()
    return code, title, text


def relative_pages_url(path: Path) -> str:
    """Convert /Users/.../diario/handoff/foo.md into the public Pages URL."""
    repo_root = Path("/Users/csilvasantin/Claude/diario").resolve()
    rel = path.resolve().relative_to(repo_root).as_posix()
    return f"{PAGES_BASE}/{rel}"


def main() -> None:
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)
    path = Path(sys.argv[1])
    if not path.is_file():
        path = Path("/Users/csilvasantin/Claude/diario") / sys.argv[1]
    if not path.is_file():
        raise SystemExit(f"No existe el handoff: {sys.argv[1]}")

    code, title, content = parse_handoff(path)
    pages_url = relative_pages_url(path)
    chunks = split_into_chunks(content, code)
    n = len(chunks)

    # 1. Header message
    header = (
        f"📦 Handoff {code} · {title}\n"
        f"🔗 {pages_url}\n\n"
        f"⏬ Contenido completo abajo en {n} {'mensajes' if n != 1 else 'mensaje'} · "
        f"long-press en cada uno para copiar."
    )
    res = _post("/telegram/send", {"text": header})
    if not res.get("ok"):
        raise SystemExit(f"Telegram header failed: {res}")
    print(f"[1/{n + 2}] header → message_id={res.get('messageId')}")

    # 2. N chunks
    for i, chunk in enumerate(chunks, start=1):
        body = HEADER_FMT.format(code=code, i=i, n=n) + chunk
        res = _post("/telegram/send", {"text": body})
        if not res.get("ok"):
            raise SystemExit(f"Telegram chunk {i}/{n} failed: {res}")
        print(f"[{i + 1}/{n + 2}] chunk {i}/{n} → message_id={res.get('messageId')}")
        time.sleep(0.3)  # gentle rate-limit

    # 3. Document attachment
    res = _post(
        "/telegram/send-document",
        {"document": pages_url, "caption": f"📦 {code} · {title}"},
    )
    if not res.get("ok"):
        # Document is icing — don't fail the whole job if Pages hasn't served yet
        print(f"[{n + 2}/{n + 2}] document SKIPPED · {res.get('error')}: {res.get('message') or ''}")
    else:
        print(f"[{n + 2}/{n + 2}] document → message_id={res.get('messageId')}")
    print(f"\n✅ Handoff {code} entregado en Telegram.")


if __name__ == "__main__":
    main()
