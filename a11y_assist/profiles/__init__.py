"""Accessibility profiles for a11y-assist.

Profiles transform AssistResult for different accessibility needs:
- lowvision: Default profile, clear labels and spacing
- cognitive-load: Reduced steps, simplified language, strict limits
"""

from .cognitive_load import apply_cognitive_load
from .cognitive_load_render import render_cognitive_load

__all__ = ["apply_cognitive_load", "render_cognitive_load"]
