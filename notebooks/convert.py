import argparse
import datetime
import json
from pathlib import Path
import re
import shutil
import subprocess
import textwrap


import nbformat


def _add_language_metadata(path: Path):
    payload = json.loads(path.read_text())
    payload["metadata"]["language_info"] = {"name": "python"}

    path.write_text(json.dumps(payload, indent=4))


def _to_markdown(path: Path):

    # notebook = nbformat.reads(path.read_text(), as_version=4)
    
    # MarkdownExporter().from_notebook_node(notebook)
    
    subprocess.check_call(["jupyter", "nbconvert", "--to", "markdown", path])


def _move_assets(path: Path):
    current_assets_dir = path.parent.joinpath(path.name.replace(".ipynb", "_files"))
    target_assets_dir = (path.parent.joinpath(path.name.replace(".ipynb", "").lower())
                         .joinpath(path.name.replace(".ipynb", "_files")))

    if target_assets_dir.exists():
        print(f"Clearing target assets dir at {target_assets_dir}.")
        shutil.rmtree(str(target_assets_dir))

    print(f"Moving assets from {current_assets_dir} to {target_assets_dir}")
    try:
        shutil.move(str(current_assets_dir), str(target_assets_dir))
    except shutil.Error as e:
        if "already exists" not in str(e):
            raise


def _collapse_forms(path: Path):

    pattern = re.compile("```python\n#@title(?P<title>.*)\n(?P<code>[^`]+)```", re.MULTILINE)
    pattern = re.compile("```python\n#@title(?P<title>.*)\n(?P<code>^((?!```)[\s\S])+)```", re.MULTILINE)

    text = path.read_text()

    matches = ((match, text[match.span()[0]:match.span()[1]]) for match in re.finditer(pattern, text))

    while re.search(pattern, text) is not None:
        match = re.search(pattern, text)
        start, end = match.span()
        substring = text[start:end]
        title = match.group("title").strip() or "Code"
        text = text.replace(
            substring,
            textwrap.dedent(
                f"""
<details>
<summary>{title}</summary>

```python
{match.group('code')}
```

</details>
"""
            )
        )

    path.write_text(text)


def _get_front_matter(path: Path):

    default = f"""---\ntitle: "New post"\ndate: {datetime.datetime.now().isoformat()}\ndraft: true\nsummary: Post summary.\n---"""

    if not path.exists():
        return default
    
    text = path.read_text()
    pattern = re.compile("---\n(?P<frontmatter>^((?!---).)+)\n---", re.MULTILINE | re.DOTALL)

    match = re.search(pattern, text)
    if match is not None:
        return f"---\n{match.group('frontmatter')}\n---\n"

    return default


def _add_front_matter(path, front_matter):

    path.write_text(f"{front_matter}\n{path.read_text()}")


def _convert_notebook(path: Path):
    md_path = path.parent.joinpath(path.name.replace(".ipynb", ".md"))
    front_matter = _get_front_matter(md_path)
    
    _add_language_metadata(path)
    _to_markdown(path)
    _move_assets(path)
    _collapse_forms(md_path)

    _add_front_matter(md_path, front_matter)
    

def convert():

    print("Converting notebooks.")

    for path in Path(".").glob("*.ipynb"):
        print(f"Converting {path}.")
        _convert_notebook(path)
