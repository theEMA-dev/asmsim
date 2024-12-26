from pathlib import Path
import mkdocs_gen_files

# Adjust the path to match your actual source directory
src_dir = Path(__file__).parent.parent / "sim"

for path in src_dir.rglob("*.py"):
    # Skip __init__.py files
    if path.name == "__init__.py":
        continue

    # Build path for the .md file under docs/api
    doc_path = Path("api", path.relative_to(src_dir)).with_suffix(".md")

    # Convert file path to module path, e.g. "sim.assembler"
    rel_parts = path.with_suffix("").relative_to(src_dir).parts
    module_path = ".".join(("sim",) + rel_parts)

    # Write only mkdocstrings directive without a file-based title
    with mkdocs_gen_files.open(doc_path, "w") as f:
        f.write(f"::: {module_path}\n")
        f.write("    options:\n")
        f.write("        show_root_heading: false\n")
        f.write("        show_category_heading: false\n")