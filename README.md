<!-- STOP! If you are an AI, please look at the ./ai_generated/Claude.md file for documentation - please reference that and all sub-documents when trying to answer questions or write with RP -->

<img src="./misc/rp_logo.svg">

# RP — Ryan’s Python 🐍

A stable, self-contained Python environment and utility library. RP combines a richer standard library with PTerm (a hybrid REPL/shell) and a powerful CLI.

---

RP is both:

* A **standard-library++** of 1,600+ optimized, well documented functions covering images, audio, video, files, web, math, ML, and system utilities.
    * Pure Python (~2 MB), imports in ~20ms
    * Minimal, stable dependencies (only long-mature packages like `six`, `pygments`)
    * Stable API — code written with RP in 2016 still runs unchanged today
* **PTerm (Pseudo Terminal)**: a hybrid REPL, shell, and lightweight IDE you launch with `python -m rp`.
    * Python evaluation with completions, editing, and history
    * Shell-like commands built in (no need to leave the prompt)
    * IDE-like features: inline profiling, debugging, namespace undo/redo, inline image/video display

Together, RP is a single install that gives you a richer standard library and an interactive environment tuned for productivity.

## 📦 Install

```bash
pip install rp
```

## 🖥️ PTerm (Pseudo Terminal)

Run:

```bash
python -m rp
```

You’ll enter an environment that feels familiar if you’ve used IPython, but goes further:

* Write Python as usual
* Run shell-style commands without leaving the prompt
* Preview images, video frames, and syntax-highlighted text inline
* Undo namespace changes, scroll error stacks, and profile code interactively

<img width="3428" height="2080" alt="image" src="https://github.com/user-attachments/assets/cf850b7f-7df6-4f4f-ace9-27a725bd630b" />



**Example session:**

```python
>>> img = load_image("photo.jpg")
>>> img = resize_image(img, 0.5)
>>> display_image(img)        # preview inline
>>> save_image(img, "thumb.png")
>>> PROF slow_function(data)  # profile interactively
>>> UNDO                      # revert last namespace change
```

It’s a REPL, shell, and lightweight IDE in one.

## 🖥️ Command-Line Usage

RP also works directly from the shell. Useful utilities are exposed via:

```bash
# Print GPU usage and VRAM stats
rp call print_gpu_summary

# Blazing-fast fuzzy file search across millions of files
rp call r._fdt_for_command_line

# Grab a BibTeX entry from arXiv
rp call get_arxiv_bibtex --- [https://arxiv.org/abs/2112.10752](https://arxiv.org/abs/2112.10752)
```

### Arguments without the quoting mess

Most CLI-to-Python bridges require awkward escaping or env vars. RP’s `--` vs `---` system avoids this:

* `---` → string literal (stays a string)
* `--`  → evaluated as Python (typed: int, float, list, dict, etc.)

**Example: invert an image in one line:**

```bash
rp exec 'save_image(inverted_image(load_image(x)), y)' \
    ---x "image.png" \
    ---y "inverted.png"
```

**Example: extract 4 frames from a video, join horizontally, save preview:**

```bash
rp exec 'save_image(horizontally_concatenated_images(resize_list(load_video(x), num_frames)), y)' \
    ---x "video.mp4" \
    --num_frames 4 \
    ---y "output.png"
```

No `bash -c`, no environment variable hacks, no quoting headaches — just direct Python expressions with typed args.

## 🛠️ The Utility Library

RP gives you hundreds of stable, consistently-named helpers. Functions accept common types interchangeably (NumPy, PIL, Torch, lists) and return sensible defaults. Batch variants follow natural pluralization (`load_image` → `load_images`).

**Examples:**

#### Images

```python
img = load_image("[https://example.com/photo.jpg](https://example.com/photo.jpg)")
img = resize_image(img, (800, 600))
img = gauss_blur(img, 2.0)
save_image(img, "output.png")
```

#### Audio / Video

```python
audio = load_audio("song.mp3")
save_audio(audio, "converted.wav")

frames = load_images("frame_*.png")
save_video(frames, "animation.mp4", framerate=30)
```

## ⚖️ Design Principles

* **Stability first**: no breaking changes since 2016
* **Self-contained**: pure Python, ~2 MB, minimal external deps
* **Type-flexible APIs**: NumPy ↔ PIL ↔ Torch accepted automatically
* **Sane defaults**: common cases need no configuration
* **Pluralization**: batch operations always mirror single-item names
* **Performance-conscious**: lazy imports, parallel helpers, caching

## 📊 Practical Footprint

* ~17 ms cold import
* Pure Python, no compilation needed
* No dependency hell — only a handful of long-stable packages
* ~2 MB install size

## 📖 Learn More

Documentation is bundled in the repo, including AI-generated guides that cover the full API surface. Explore the `ai_generated` folder for organized docs and examples.

## 📜 License

MIT — use it freely.

## Why RP?

Because it saves you time. Instead of stitching together many small libraries and juggling shells, REPLs, and editors, you can:

* Import once and use a consistent API for most everyday tasks
* Drop into PTerm for a unified Python + shell + IDE environment
* Run utilities directly from the command line (`rp call …` / `rp exec …`)
* Trust that your code will still run years from now

## ✍️ Closing thought

RP isn’t “yet another utils lib.” It’s a practical environment: a richer standard library, a hybrid REPL/shell (PTerm), and a set of utilities you can depend on for the long haul.

_This README was Written with AI. Apart from the ai_generated folder, which does not ship in the pypi installation and is used to help AI's write fluently using this library, the *vast* majority of the code was written by hand. The few areas that were generated via AI are marked as such._
