"""Backend registry and factory functions."""

import os
import sys
import json

from .base import ImageBackend, VideoBackend

# CLI constants — defined here to avoid importing SDK-dependent modules at top level
GEMINI_SIZES = ["512", "1K", "2K", "4K"]
GEMINI_ASPECT_RATIOS = [
    "1:1", "1:4", "1:8", "2:3", "3:2", "3:4", "4:1", "4:3",
    "4:5", "5:4", "8:1", "9:16", "16:9", "21:9",
]
GROK_SIZES = ["1K", "2K"]
GROK_ASPECT_RATIOS = [
    "1:1", "16:9", "9:16", "4:3", "3:4", "3:2", "2:3",
    "2:1", "1:2", "19.5:9", "9:19.5", "20:9", "9:20", "auto",
]


def _fail(msg: str):
    print(json.dumps({"ok": False, "cost_cents": 0, "error": msg}))
    sys.exit(1)


def get_image_backend(name: str | None = None) -> ImageBackend:
    """Get image backend by name. Falls back to ASSET_BACKEND env var, then 'grok'."""
    backend_name = name or os.environ.get("ASSET_BACKEND", "grok")

    if backend_name == "gemini":
        from .gemini import GeminiBackend
        return GeminiBackend()
    elif backend_name == "grok":
        from .grok import GrokImageBackend
        return GrokImageBackend()
    elif backend_name == "dashscope":
        from .dashscope import DashScopeImageBackend
        return DashScopeImageBackend()
    else:
        _fail(f"Unknown image backend: {backend_name}. Available: gemini, grok, dashscope")


def get_video_backend(name: str | None = None) -> VideoBackend:
    """Get video backend by name. Falls back to ASSET_BACKEND env var, then 'grok'."""
    backend_name = name or os.environ.get("ASSET_BACKEND", "grok")

    if backend_name == "grok":
        from .grok import GrokVideoBackend
        return GrokVideoBackend()
    elif backend_name == "dashscope":
        from .dashscope import DashScopeVideoBackend
        return DashScopeVideoBackend()
    else:
        _fail(f"Unknown video backend: {backend_name}. Available: grok, dashscope")
