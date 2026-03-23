# 🧩 ComfyUI Prompt Assembler

A set of utility nodes for ComfyUI that let you **assemble prompts from multiple string inputs**, each with an **ON/OFF toggle** to include or exclude it from the final output.

---

## Nodes

### 🧩 Prompt Assembler (8 slots)
The full-featured version.

| Feature | Details |
|---|---|
| **Inputs** | 8 optional string inputs (`prompt_1` … `prompt_8`) |
| **Toggles** | 8 boolean switches (`enable_1` … `enable_8`) — ON by default |
| **Separator** | `comma + space`, `newline`, `space`, `period + space`, or `custom` |
| **Outputs** | `assembled_prompt` (the final string) + `debug_info` (slot status summary) |

### 🧩 Prompt Assembler Compact (4 slots)
A lightweight version with 4 slots and a single string output. Great for simple workflows.

### 🧩 Prompt Assembler Weighted (6 slots)
Advanced version — each slot has a **weight slider** (0.0–2.0). Non-1.0 weights automatically wrap the fragment in `(prompt:weight)` attention syntax.

| Output | Description |
|---|---|
| `assembled_prompt` | Weighted prompt with `(text:1.30)` syntax applied |
| `raw_prompt` | Same assembly but without weight wrappers |

---

## Installation

### Option A — ComfyUI Manager
Search for **Prompt Assembler** in the ComfyUI Manager and install.

### Option B — Manual
```bash
cd ComfyUI/custom_nodes
git clone https://github.com/jeremieLouvaert/comfyui-prompt-assembler.git
```
Restart ComfyUI. No pip dependencies required.

---

## Usage Example

```
[ String node: "a beautiful landscape" ] ──► prompt_1   enable_1: ✅ ON
[ String node: "cyberpunk style" ]        ──► prompt_2   enable_2: ✅ ON
[ String node: "watercolor painting" ]    ──► prompt_3   enable_3: ❌ OFF
[ String node: "8k, detailed" ]           ──► prompt_4   enable_4: ✅ ON
```

**Output** (separator = `comma + space`):
```
a beautiful landscape, cyberpunk style, 8k, detailed
```

Slot 3 ("watercolor painting") is toggled OFF and excluded.

---

## Tips

- **Connect any STRING output** to the prompt slots — text nodes, other assemblers, LLM outputs, etc.
- **Unconnected slots are ignored**, so you only need to wire up the ones you use.
- The **debug output** on the full 8-slot version is handy for troubleshooting which slots are active.
- Use the **Weighted** version when you want to emphasize or de-emphasize specific parts of your prompt without editing the source strings.

---

## License

MIT
