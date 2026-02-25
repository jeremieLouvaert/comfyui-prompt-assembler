"""
ComfyUI Custom Node: Prompt Assembler
Assembles multiple string inputs into a single prompt based on enable/disable switches.
"""


class PromptAssembler:
    """
    Assembles up to 8 prompt fragments into a single output string.
    Each slot has a boolean toggle to enable or disable it.
    """

    NUM_SLOTS = 8

    @classmethod
    def INPUT_TYPES(cls):
        inputs = {
            "required": {
                "separator": (["comma + space", "newline", "space", "period + space", "custom"], {
                    "default": "comma + space"
                }),
            },
            "optional": {
                "custom_separator": ("STRING", {
                    "default": ", ",
                    "multiline": False,
                }),
            },
        }

        for i in range(1, cls.NUM_SLOTS + 1):
            inputs["optional"][f"prompt_{i}"] = ("STRING", {
                "default": "",
                "multiline": True,
                "forceInput": True,
            })
            inputs["required"][f"enable_{i}"] = ("BOOLEAN", {
                "default": True,
                "label_on": "ON",
                "label_off": "OFF",
            })

        return inputs

    RETURN_TYPES = ("STRING", "STRING",)
    RETURN_NAMES = ("assembled_prompt", "debug_info",)
    FUNCTION = "assemble"
    CATEGORY = "utils/text"
    DESCRIPTION = "Assembles multiple prompt strings into one, with toggles to enable/disable each slot."

    SEPARATOR_MAP = {
        "comma + space": ", ",
        "newline": "\n",
        "space": " ",
        "period + space": ". ",
    }

    def assemble(self, separator, custom_separator=", ", **kwargs):
        # Resolve separator
        if separator == "custom":
            sep = custom_separator
        else:
            sep = self.SEPARATOR_MAP.get(separator, ", ")

        # Collect enabled, non-empty prompts
        active_parts = []
        debug_lines = []

        for i in range(1, self.NUM_SLOTS + 1):
            prompt_val = kwargs.get(f"prompt_{i}", "")
            enabled = kwargs.get(f"enable_{i}", True)

            status = "ON" if enabled else "OFF"
            connected = "connected" if prompt_val else "empty"
            debug_lines.append(f"Slot {i}: [{status}] ({connected}) {repr(prompt_val[:60])}")

            if enabled and prompt_val and prompt_val.strip():
                active_parts.append(prompt_val.strip())

        assembled = sep.join(active_parts)

        debug_info = (
            f"--- Prompt Assembler Debug ---\n"
            f"Separator: {repr(sep)}\n"
            f"Active slots: {len(active_parts)} / {self.NUM_SLOTS}\n"
            + "\n".join(debug_lines)
            + f"\n--- Output length: {len(assembled)} chars ---"
        )

        return (assembled, debug_info,)


class PromptAssemblerCompact:
    """
    A compact 4-slot version of the Prompt Assembler for simpler workflows.
    """

    NUM_SLOTS = 4

    @classmethod
    def INPUT_TYPES(cls):
        inputs = {
            "required": {
                "separator": (["comma + space", "newline", "space", "period + space", "custom"], {
                    "default": "comma + space"
                }),
            },
            "optional": {
                "custom_separator": ("STRING", {
                    "default": ", ",
                    "multiline": False,
                }),
            },
        }

        for i in range(1, cls.NUM_SLOTS + 1):
            inputs["optional"][f"prompt_{i}"] = ("STRING", {
                "default": "",
                "multiline": True,
                "forceInput": True,
            })
            inputs["required"][f"enable_{i}"] = ("BOOLEAN", {
                "default": True,
                "label_on": "ON",
                "label_off": "OFF",
            })

        return inputs

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("assembled_prompt",)
    FUNCTION = "assemble"
    CATEGORY = "utils/text"
    DESCRIPTION = "Compact 4-slot prompt assembler with toggles."

    SEPARATOR_MAP = {
        "comma + space": ", ",
        "newline": "\n",
        "space": " ",
        "period + space": ". ",
    }

    def assemble(self, separator, custom_separator=", ", **kwargs):
        if separator == "custom":
            sep = custom_separator
        else:
            sep = self.SEPARATOR_MAP.get(separator, ", ")

        active_parts = []
        for i in range(1, self.NUM_SLOTS + 1):
            prompt_val = kwargs.get(f"prompt_{i}", "")
            enabled = kwargs.get(f"enable_{i}", True)
            if enabled and prompt_val and prompt_val.strip():
                active_parts.append(prompt_val.strip())

        return (sep.join(active_parts),)


class PromptAssemblerWeighted:
    """
    Advanced version: each slot has a weight that wraps the prompt
    in ComfyUI attention syntax (prompt:weight).
    """

    NUM_SLOTS = 6

    @classmethod
    def INPUT_TYPES(cls):
        inputs = {
            "required": {
                "separator": (["comma + space", "newline", "space"], {
                    "default": "comma + space"
                }),
            },
            "optional": {},
        }

        for i in range(1, cls.NUM_SLOTS + 1):
            inputs["optional"][f"prompt_{i}"] = ("STRING", {
                "default": "",
                "multiline": True,
                "forceInput": True,
            })
            inputs["required"][f"enable_{i}"] = ("BOOLEAN", {
                "default": True,
                "label_on": "ON",
                "label_off": "OFF",
            })
            inputs["required"][f"weight_{i}"] = ("FLOAT", {
                "default": 1.0,
                "min": 0.0,
                "max": 2.0,
                "step": 0.05,
                "display": "slider",
            })

        return inputs

    RETURN_TYPES = ("STRING", "STRING",)
    RETURN_NAMES = ("assembled_prompt", "raw_prompt",)
    FUNCTION = "assemble"
    CATEGORY = "utils/text"
    DESCRIPTION = "Prompt assembler with per-slot attention weights. Wraps each fragment in (prompt:weight) syntax."

    SEPARATOR_MAP = {
        "comma + space": ", ",
        "newline": "\n",
        "space": " ",
    }

    def assemble(self, separator, **kwargs):
        sep = self.SEPARATOR_MAP.get(separator, ", ")

        weighted_parts = []
        raw_parts = []

        for i in range(1, self.NUM_SLOTS + 1):
            prompt_val = kwargs.get(f"prompt_{i}", "")
            enabled = kwargs.get(f"enable_{i}", True)
            weight = kwargs.get(f"weight_{i}", 1.0)

            if enabled and prompt_val and prompt_val.strip():
                clean = prompt_val.strip()
                raw_parts.append(clean)

                if abs(weight - 1.0) > 0.01:
                    weighted_parts.append(f"({clean}:{weight:.2f})")
                else:
                    weighted_parts.append(clean)

        assembled = sep.join(weighted_parts)
        raw = sep.join(raw_parts)

        return (assembled, raw,)


# ── Node Registration ──────────────────────────────────────────────

NODE_CLASS_MAPPINGS = {
    "PromptAssembler": PromptAssembler,
    "PromptAssemblerCompact": PromptAssemblerCompact,
    "PromptAssemblerWeighted": PromptAssemblerWeighted,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "PromptAssembler": "🧩 Prompt Assembler (8 slots)",
    "PromptAssemblerCompact": "🧩 Prompt Assembler Compact (4 slots)",
    "PromptAssemblerWeighted": "🧩 Prompt Assembler Weighted (6 slots)",
}
