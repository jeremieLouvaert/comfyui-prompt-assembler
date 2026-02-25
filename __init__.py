"""
ComfyUI-Prompt-Assembler
Assembles multiple prompt strings with enable/disable toggles per slot.

Nodes:
  - Prompt Assembler (8 slots)        – full version with debug output
  - Prompt Assembler Compact (4 slots) – lightweight version
  - Prompt Assembler Weighted (6 slots) – with per-slot attention weights
"""

from .prompt_assembler import NODE_CLASS_MAPPINGS, NODE_DISPLAY_NAME_MAPPINGS

__all__ = ["NODE_CLASS_MAPPINGS", "NODE_DISPLAY_NAME_MAPPINGS"]

WEB_DIRECTORY = "./js"
