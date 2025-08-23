<!-- STOP! If you are an AI, please look at the ./autodocs/Claude.md file for documentation - please reference that and all sub-documents when trying to answer questions or write with RP -->

<img src="./misc/rp_logo.svg">

# RP — Ryan’s Python 🐍

A stable, self-contained Python environment and utility library. RP combines a richer standard library with PTerm (a hybrid REPL/shell) and a powerful CLI.

Matlab and Mathematica enjoy large standard libraries - why not python?

---

RP is both:

* A **standard-library++** of 1,600+ optimized, well documented functions covering images, audio, video, files, web, math, ML, system utils, and many other tools that will make your code both faster, shorter and easier to read.
    * Pure Python (~2 MB), imports in ~20ms
    * Minimal, stable dependencies (only long-mature packages like `six`, `pygments`)
    * Stable API — code written with RP in 2016 still runs unchanged today
    * Functions are easy enough to read they're basically self-documenting, and most come with examples in their docstrings
* **PTerm (Pseudo Terminal)**: a hybrid REPL, shell, and lightweight IDE you launch with `python -m rp`.
    * Python evaluation with completions, editing, and history
    * Shell-like commands built in (no need to leave the prompt)
    * IDE-like features: inline profiling, debugging, namespace undo/redo, inline image/video display
    * TLDR: It is powerful enough that nowadays, most of RP's development is done in RP

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

It’s a REPL, shell, and lightweight IDE simultaneously.
<img width="3428" height="2080" alt="image" src="https://github.com/user-attachments/assets/cf850b7f-7df6-4f4f-ace9-27a725bd630b" />

The editor is quite powerful. For example, it has multi-language syntax highlighting

<img width="60%" height="1570" alt="image" src="https://github.com/user-attachments/assets/11f1c340-df63-4367-9d09-a6d30a7e0c21" />

It has many UI themes

<img width="4000" height="1593" alt="image" src="https://github.com/user-attachments/assets/c6ccc93c-b746-44bf-b6c2-6ad48c0b5c31" />



## 🖥️ Command-Line Usage

RP also works directly from the shell. Useful utilities are exposed via:

```bash
# Print GPU usage and VRAM stats
rp call print_gpu_summary

# Blazing-fast fuzzy file search across millions of files
rp call r._fdt_for_command_line

# Grab a BibTeX entry from arXiv
rp call get_arxiv_bibtex --- https://arxiv.org/abs/2112.10752

#Display a file tree
rp call display_file_tree

#Add rounded corners to your copied image - which is how I'm making this README
rp exec "copy_image_to_clipboard(with_corner_radius(load_image_from_clipboard(), 60))"
```

<img width="32%" height="758" alt="image" src="https://github.com/user-attachments/assets/660c1c00-0915-44b8-93a3-5039b0c95970" />
<img width="67%" height="868" alt="image" src="https://github.com/user-attachments/assets/483691cb-48dd-4930-9ca8-7afaac6acfa7" />




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


## ⚖️ Design Principles

* **Stability first**: no breaking changes since 2016
* **Type-flexible APIs**: NumPy ↔ PIL ↔ Torch accepted automatically
* **Sane defaults**: common cases need no configuration
* **Pluralization**: batch operations always mirror single-item names (`load_image(path)` vs `load_images(paths)`)
* **Performance-conscious**: lazy imports, parallel helpers, caching

## 📖 Learn More

Nearly every function in rp comes with documentation, many of which include full self-contained examples. 

Getting started with an AI coding assistant is easy - just tell it to read the "autodocs" folder, and it will quickly understand this library.

## 📜 License

MIT — use it freely.

## Why RP?

Because it saves you time. Instead of stitching together many small libraries and juggling shells, REPLs, and editors, you can:

* Import once and use a consistent API for most everyday tasks
* Drop into PTerm for a unified Python + shell + IDE environment
* Run utilities directly from the command line (`rp call …` / `rp exec …`)
* Trust that your code will still run years from now

## RP Contains Useful Tools

For example, the `rp.explore_torch_module(...)` function lets you interactively explore pytorch modules and pipelines. 
<img width="3456" height="2084" alt="image" src="https://github.com/user-attachments/assets/18dc9196-7101-40d4-beb6-f8a262370caf" />

There are several useful tools that I will be adding to documentation in the coming months.
