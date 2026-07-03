from pathlib import Path
from typing import List

from .database import fetch_all_clients
from .config import DOCS_DIR


def format_client_summary(clients: List[dict]) -> str:
    if not clients:
        return "No clients found."

    lines = ["Client progress report:\n"]
    for client in clients:
        lines.append(
            f"[{client['id']}] {client['business_name']} - {client['status']} - {client['email']}"
        )
        if client["website_url"]:
            lines.append(f"  Website: {client['website_url']}")
        if client["invoice_id"]:
            lines.append(f"  Invoice: {client['invoice_id']}")
        if client["requirements"]:
            lines.append(f"  Requirements: {client['requirements']}")
        if client["last_note"]:
            lines.append(f"  Note: {client['last_note']}")
        lines.append("")
    return "\n".join(lines)


def render_status_page(clients: List[dict]) -> str:
    rows = "\n".join(
        f"<tr>\n"
        f"  <td>{client['id']}</td>\n"
        f"  <td>{client['business_name']}</td>\n"
        f"  <td>{client['email']}</td>\n"
        f"  <td>{client['status']}</td>\n"
        f"  <td>{client['website_url']}</td>\n"
        f"  <td>{client['invoice_id']}</td>\n"
        f"  <td>{client['requirements']}</td>\n"
        f"  <td>{client['last_note']}</td>\n"
        f"</tr>"
        for client in clients
    )

    return f"""<!DOCTYPE html>
<html lang=\"mk\">
<head>
  <meta charset=\"UTF-8\">
  <meta name=\"viewport\" content=\"width=device-width, initial-scale=1.0\">
  <title>Client Progress Report</title>
  <style>
    body {{ font-family: Arial, sans-serif; margin: 0; padding: 2rem; background: #f4f4f7; color: #222; }}
    table {{ width: 100%; border-collapse: collapse; margin-top: 1rem; }}
    th, td {{ padding: 0.75rem; border: 1px solid #ddd; text-align: left; vertical-align: top; }}
    th {{ background: #f0f0f0; }}
    tr:nth-child(even) {{ background: #fbfbfb; }}
    h1 {{ margin-bottom: 0.5rem; }}
    p {{ margin-top: 0.25rem; color: #555; }}
  </style>
</head>
<body>
  <h1>Client Progress Report</h1>
  <p>Тука може да ја видите целата работа, статусот на клиентите, испораката на веб-страниците и сметките.</p>
  <table>
    <thead>
      <tr>
        <th>ID</th>
        <th>Client</th>
        <th>Email</th>
        <th>Status</th>
        <th>Website URL</th>
        <th>Invoice</th>
        <th>Requirements</th>
        <th>Note</th>
      </tr>
    </thead>
    <tbody>
{rows}
    </tbody>
  </table>
</body>
</html>"""


def publish_status_report() -> Path:
    clients = fetch_all_clients()
    DOCS_DIR.mkdir(parents=True, exist_ok=True)
    file_path = DOCS_DIR / "status.html"
    with file_path.open("w", encoding="utf-8") as file:
        file.write(render_status_page(clients))
    return file_path
