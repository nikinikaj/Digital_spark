import shutil
from pathlib import Path

from .config import BASE_DIR, DOCS_DIR, GITHUB_PAGES_DIR
from .status import publish_status_report


def publish_docs_site() -> tuple[bool, str]:
    if not GITHUB_PAGES_DIR.exists():
        return False, "No GitHub Pages build directory found. Run the pipeline with --deploy-target github-pages first."

    if DOCS_DIR.exists():
        shutil.rmtree(DOCS_DIR)

    shutil.copytree(GITHUB_PAGES_DIR, DOCS_DIR)
    index_path = DOCS_DIR / "index.html"
    if not index_path.exists():
        with open(index_path, "w", encoding="utf-8") as f:
            f.write(
                "<html><head><meta charset='utf-8'><title>Agency Deployment</title></head>"
                "<body><h1>GitHub Pages Preview</h1><p>Build output copied to docs/.</p></body></html>"
            )

    status_path = publish_status_report()
    return True, f"Published GitHub Pages preview to {DOCS_DIR}. Status report created at {status_path}."

    if not index_path.exists():
        with open(index_path, "w", encoding="utf-8") as f:
            f.write(
                "<html><head><meta charset='utf-8'><title>Agency Deployment</title></head>"
                "<body><h1>GitHub Pages Preview</h1><p>Build output copied to docs/.</p></body></html>"
            )

    return True, f"Published GitHub Pages preview to {DOCS_DIR}."
