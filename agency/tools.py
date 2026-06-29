import smtplib
from email.message import EmailMessage
from pathlib import Path
from typing import Tuple

from .config import (
    DEPLOY_DIR,
    GITHUB_PAGES_DIR,
    PAYPAL_BASE_URL,
    USE_SMTP,
    SMTP_HOST,
    SMTP_PORT,
    SMTP_USERNAME,
    SMTP_PASSWORD,
    EMAIL_FROM,
    ADMIN_EMAIL,
)

DEPLOY_DIR.mkdir(exist_ok=True)
GITHUB_PAGES_DIR.mkdir(exist_ok=True)


def preview_sales_email(
    to_email: str,
    business_name: str,
    note: str = "",
    requirements_questions: str = "",
) -> str:
    body = (
        f"Subject: Grow {business_name} with a better website\n"
        f"To: {to_email}\n\n"
        f"Hi {business_name},\n\n"
        f"I noticed your business could benefit from a fast, modern website that turns visitors into customers.\n"
        f"We build responsive sites, simplify online bookings, and help local businesses appear professional online.\n\n"
    )
    if requirements_questions:
        body += (
            "To help us prepare a tailored proposal, please reply with the following details:\n"
            f"{requirements_questions}\n\n"
        )
    body += (
        f"Why not start with a short call?\n\n"
        f"Best regards,\n"
        f"Agency Team\n"
        f"Note: {note}\n"
    )
    return body


def send_sales_email(to_email: str, subject: str, body: str) -> str:
    if not USE_SMTP:
        return "Warning: SMTP not configured. Email not sent."

    message = EmailMessage()
    message["From"] = EMAIL_FROM
    message["To"] = to_email
    message["Subject"] = subject
    message.set_content(body)

    try:
        if SMTP_PORT == 465:
            server = smtplib.SMTP_SSL(SMTP_HOST, SMTP_PORT, timeout=30)
        else:
            server = smtplib.SMTP(SMTP_HOST, SMTP_PORT, timeout=30)
            server.starttls()
        server.login(SMTP_USERNAME, SMTP_PASSWORD)
        server.send_message(message)
        server.quit()
        return "Success: Email sent via SMTP."
    except Exception as e:
        return f"Failed to send email: {e}"


def send_admin_notification(subject: str, message_body: str) -> str:
    if not USE_SMTP:
        return "Warning: SMTP not configured. Admin notification not sent."

    message = EmailMessage()
    message["From"] = EMAIL_FROM
    message["To"] = ADMIN_EMAIL
    message["Subject"] = subject
    message.set_content(message_body)

    try:
        if SMTP_PORT == 465:
            server = smtplib.SMTP_SSL(SMTP_HOST, SMTP_PORT, timeout=30)
        else:
            server = smtplib.SMTP(SMTP_HOST, SMTP_PORT, timeout=30)
            server.starttls()
        server.login(SMTP_USERNAME, SMTP_PASSWORD)
        server.send_message(message)
        server.quit()
        return "Success: Admin notification sent via SMTP."
    except Exception as e:
        return f"Failed to send admin notification: {e}"


def generate_requirements_questions(business_name: str, note: str) -> str:
    text = f"{business_name} {note}".lower()
    questions = [
        "What are your main services or products?",
        "What should visitors understand first when they land on the page?",
        "Do you want an online booking, menu, or contact form?",
        "What are your opening hours and location details?",
    ]
    if any(keyword in text for keyword in ["café", "coffee", "cake", "menu", "restaur", "kafe"]):
        questions = [
            "What are your most popular menu items or specialties?",
            "Do you want a reservations or order button?",
            "Should the site show opening hours, address, and a map?",
            "Do you want a gallery of food and interior photos?",
        ]
    elif any(keyword in text for keyword in ["gym", "fitness", "trainer"]):
        questions = [
            "What training programs or memberships do you offer?",
            "Do you want to highlight coaches, classes, or schedules?",
            "Should visitors be able to book sessions or request a consultation?",
            "Are there special promotions or packages to show?",
        ]
    elif any(keyword in text for keyword in ["salon", "beauty", "kozmet", "hair"]):
        questions = [
            "What beauty or salon services do you offer?",
            "Would you like a booking request form or appointment call-to-action?",
            "Should we display a gallery of your work or service prices?",
            "Do you want to highlight special offers or packages?",
        ]
    return "\n".join(f"- {question}" for question in questions)


def generate_requirements_summary(business_name: str, note: str) -> str:
    text = f"{business_name} {note}".lower()
    if any(keyword in text for keyword in ["café", "coffee", "cake", "menu", "restaur", "kafe"]):
        return (
            "Модерен кафе/рестораниски веб-сајт со менито, работно време, контакт, галерија и опција за резервации или нарачки."
        )
    if any(keyword in text for keyword in ["gym", "fitness", "trainer"]):
        return (
            "Модерен фитнес веб-сајт со тренинг програми, опис на услуги, тренери, распоред и контакт за резервации."
        )
    if any(keyword in text for keyword in ["salon", "beauty", "kozmet", "hair"]):
        return (
            "Салонски веб-сајт со услуги, галерија, ценовник и форма за резервации или контакт."
        )
    return (
        "Локален бизнис веб-сајт со јасен опис на услугите, контакт информации и повик за акција."
    )


def deploy_basic_website(client_id: int, business_name: str, html_content: str, target: str = "local") -> Tuple[bool, str]:
    if target == "github-pages":
        client_dir = GITHUB_PAGES_DIR / f"client_{client_id}"
        client_dir.mkdir(parents=True, exist_ok=True)
        filename = client_dir / "index.html"
        deploy_url = f"gh_pages_site/client_{client_id}/index.html"
    else:
        filename = DEPLOY_DIR / f"site_client_{client_id}.html"
        deploy_url = str(filename)

    try:
        with open(filename, "w", encoding="utf-8") as f:
            f.write(html_content)
        return True, deploy_url
    except OSError as e:
        return False, f"Failed to build website: {e}"


def generate_html_for_requirements(business_name: str, requirements: str) -> str:
    safe_name = business_name.replace("<", "").replace(">", "")
    return f"""<!DOCTYPE html>
<html lang=\"mk\">
<head>
    <meta charset=\"UTF-8\">
    <meta name=\"viewport\" content=\"width=device-width, initial-scale=1.0\">
    <title>{safe_name} | Нов веб сајт</title>
    <style>
        body {{ font-family: Arial, sans-serif; margin: 0; padding: 0; background: #f9f6f2; color: #222; }}
        .hero {{ padding: 4rem 1.5rem; text-align: center; background: #ffe9d2; }}
        .hero h1 {{ margin: 0 0 1rem; font-size: clamp(2rem, 4vw, 3.5rem); }}
        .hero p {{ margin: 0 auto; max-width: 700px; line-height: 1.6; }}
        .section {{ padding: 3rem 1.5rem; max-width: 1080px; margin: 0 auto; }}
        .cards {{ display: grid; gap: 1rem; grid-template-columns: repeat(auto-fit, minmax(220px, 1fr)); }}
        .card {{ background: white; border-radius: 18px; padding: 1.5rem; box-shadow: 0 12px 30px rgba(0,0,0,0.08); }}
        .contact {{ background: #fff4ea; text-align: center; }}
        .button {{ display: inline-block; padding: 0.9rem 1.5rem; background: #d66b2d; color: white; border-radius: 999px; text-decoration: none; margin-top: 1rem; }}
    </style>
</head>
<body>
    <section class=\"hero\">
        <h1>{safe_name}</h1>
        <p>{requirements}</p>
        <a class=\"button\" href=\"#contact\">Контактирај нè</a>
    </section>
    <section class=\"section\">
        <h2>Што правиме</h2>
        <div class=\"cards\">
            <div class=\"card\"><h3>Дизајн</h3><p>Чист, брз и мобилен прв дизајн што изгледа професионално.</p></div>
            <div class=\"card\"><h3>Присутност на Интернет</h3><p>Оптимизирани страници за локални клиенти, со лесно наоѓање.</p></div>
            <div class=\"card\"><h3>Поддршка</h3><p>Ние поддржуваме објавување и едноставни промени додека се во производство.</p></div>
        </div>
    </section>
    <section class=\"section contact\" id=\"contact\">
        <h2>Закажи состанок</h2>
        <p>Испрати ни информации за твојот бизнис, и ние ќе ти подготвиме понуда.</p>
        <a class=\"button\" href=\"mailto:info@example.com\">Прати е-пошта</a>
    </section>
</body>
</html>"""


def generate_invoice_link(client_id: int, business_name: str, amount: float = 350.0, provider: str = "paypal") -> str:
    safe_name = business_name.replace(" ", "%20")
    if provider.lower() == "paypal":
        return f"{PAYPAL_BASE_URL}/{safe_name}/{amount:.2f}"
    return f"https://invoice.example.com/{client_id}?name={safe_name}&amount={amount:.2f}"


def simulate_payment_status(invoice_id: str) -> str:
    if not invoice_id:
        return "PENDING"
    if invoice_id.startswith("https://invoice.example.com/"):
        return "PAID"
    if invoice_id.startswith(PAYPAL_BASE_URL):
        return "PAID"
    return "PENDING"


def require_manual_approval(prompt: str) -> bool:
    answer = input(f"{prompt} [Y/n]: ").strip().lower()
    return answer in ("", "y", "yes")
