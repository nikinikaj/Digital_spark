from pathlib import Path
from typing import Dict, List

from .database import fetch_all_clients
from .config import DOCS_DIR


def summarize_clients(clients: List[dict]) -> Dict[str, int]:
    summary = {
        "total": len(clients),
        "lead": 0,
        "emailed": 0,
        "ordered": 0,
        "built": 0,
        "invoiced": 0,
        "paid": 0,
    }
    for client in clients:
        status = client["status"].lower()
        if status in summary:
            summary[status] += 1
    return summary


def render_dashboard_page(clients: List[dict]) -> str:
    summary = summarize_clients(clients)
    status_rows = "\n".join(
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
  <title>Agency Dashboard</title>
  <style>
    body {{ font-family: Arial, sans-serif; margin: 0; padding: 2rem; background: #f9fafc; color: #1f2937; }}
    .hero {{ padding: 1.5rem; background: #111827; color: white; border-radius: 16px; }}
    .grid {{ display: grid; gap: 1rem; grid-template-columns: repeat(auto-fit, minmax(180px, 1fr)); margin-top: 1.5rem; }}
    .card {{ background: white; border: 1px solid #e5e7eb; border-radius: 16px; padding: 1rem; box-shadow: 0 10px 30px rgba(15, 23, 42, 0.08); }}
    .card h3 {{ margin: 0 0 0.5rem; font-size: 1rem; color: #111827; }}
    .card p {{ margin: 0; font-size: 2rem; font-weight: 700; color: #111827; }}
    table {{ width: 100%; border-collapse: collapse; margin-top: 2rem; background: white; }}
    th, td {{ padding: 0.75rem; border: 1px solid #e5e7eb; text-align: left; }}
    th {{ background: #f3f4f6; }}
    tr:nth-child(even) {{ background: #f9fafb; }}
    a {{ color: #2563eb; text-decoration: none; }}
  </style>
</head>
<body>
  <section class=\"hero\">
    <h1>Agency Dashboard</h1>
    <p>Ова е моменталната работа на агенцијата: lead-ови, продажба, веб-страници и испорака.</p>
  </section>
  <section class=\"grid\">
    <div class=\"card\"><h3>Total clients</h3><p>{summary['total']}</p></div>
    <div class=\"card\"><h3>New leads</h3><p>{summary['lead']}</p></div>
    <div class=\"card\"><h3>Emailed</h3><p>{summary['emailed']}</p></div>
    <div class=\"card\"><h3>Ordered</h3><p>{summary['ordered']}</p></div>
    <div class=\"card\"><h3>Built</h3><p>{summary['built']}</p></div>
    <div class=\"card\"><h3>Invoiced</h3><p>{summary['invoiced']}</p></div>
    <div class=\"card\"><h3>Paid</h3><p>{summary['paid']}</p></div>
  </section>
  <section>
    <h2>Client progress</h2>
    <p>Преглед на статус по клиент. Кликни на <a href=\"status.html\">Status report</a> за детален извештај.</p>
    <table>
      <thead>
        <tr>
          <th>ID</th>
          <th>Client</th>
          <th>Email</th>
          <th>Status</th>
          <th>Website</th>
          <th>Invoice</th>
          <th>Requirements</th>
          <th>Note</th>
        </tr>
      </thead>
      <tbody>
{status_rows}
      </tbody>
    </table>
  </section>
</body>
</html>"""


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
  <p><a href=\"index.html\">Back to dashboard</a></p>
</body>
</html>"""


def publish_status_report() -> Path:
    clients = fetch_all_clients()
    DOCS_DIR.mkdir(parents=True, exist_ok=True)
    file_path = DOCS_DIR / "status.html"
    with file_path.open("w", encoding="utf-8") as file:
        file.write(render_status_page(clients))
    return file_path


def publish_dashboard_page() -> Path:
    clients = fetch_all_clients()
    DOCS_DIR.mkdir(parents=True, exist_ok=True)
    file_path = DOCS_DIR / "index.html"
    with file_path.open("w", encoding="utf-8") as file:
        file.write(render_dashboard_page(clients))
    return file_path
