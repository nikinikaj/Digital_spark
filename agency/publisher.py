import shutil
from pathlib import Path

from .config import BASE_DIR, DOCS_DIR, GITHUB_PAGES_DIR
from .status import publish_status_report, publish_dashboard_page


def publish_docs_site() -> tuple[bool, str]:
    if not GITHUB_PAGES_DIR.exists():
        return False, "No GitHub Pages build directory found. Run the pipeline with --deploy-target github-pages first."

    if DOCS_DIR.exists():
        shutil.rmtree(DOCS_DIR)

    shutil.copytree(GITHUB_PAGES_DIR, DOCS_DIR)
    dashboard_path = publish_dashboard_page()
    status_path = publish_status_report()
    return True, f"Published GitHub Pages preview to {DOCS_DIR}. Dashboard created at {dashboard_path}, status report created at {status_path}."
