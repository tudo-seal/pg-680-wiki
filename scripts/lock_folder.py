import re
import shutil
from pathlib import Path
import mkdocs_gen_files

root = Path(__file__).parent.parent
src = root / "locked"

nav = mkdocs_gen_files.Nav()

# Example: Append content to all .md files in a subdirectory
for path in sorted(src.rglob("*.md")):
    censored_name = path.stem[:2] + '-' * 16 + path.stem[-2:]
    full_doc_path = Path("locked", f"{censored_name}{path.suffix}")
    with open(path, 'r') as f:
        content = f.read()
        content = f"""---
level: locked
---
#{censored_name}\n""" + content
        with mkdocs_gen_files.open(full_doc_path, "w") as fl:
            fl.write(content)

    nav[censored_name] = f"{censored_name}{path.suffix}"
    mkdocs_gen_files.set_edit_path(full_doc_path, path.relative_to(root))
    path.unlink()

with mkdocs_gen_files.open("locked/SUMMARY.md", "w") as nav_file:
    nav_file.writelines(nav.build_literate_nav())