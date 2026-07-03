from typing import List

from .database import (
    add_lead,
    fetch_clients_by_status,
    find_client_by_email,
    update_client_field,
    update_status,
)
from .tools import (
    deploy_basic_website,
    generate_html_for_requirements,
    generate_invoice_link,
    generate_requirements_questions,
    generate_requirements_summary,
    preview_sales_email,
    require_manual_approval,
    send_admin_notification,
    send_sales_email,
    simulate_payment_status,
    is_noninteractive,
)


NICHES = {
    "local cafe": [
        ("Кафе Бар Мели", "info@kafebarmeli.mk", "Small café in town center without a modern website."),
        ("Сладкарница Свет", "kontakt@sladkarhnicasvet.mk", "Dessert shop that needs online menu presentation."),
    ],
    "fitness": [
        ("Fit Zone", "hello@fitzone.mk", "Local gym that wants a landing page for memberships."),
        ("Енерџи Фит", "info@energfit.mk", "Personal trainer service with no website."),
    ],
    "beauty": [
        ("Салон Бјути", "salonbeauty@mk", "Hair and makeup studio without a booking page."),
        ("Козметика Ева", "eva@kozmetika.mk", "Skin care salon needing a polished online presence."),
    ],
    "restaurant": [
        ("Ресторан Свежина", "info@restoransvezina.mk", "Family restaurant without a modern website."),
        ("Таверна Арка", "contact@tavernaarka.mk", "Local tavern needing online menus and reservations."),
    ],
}


def lead_finder_agent(niche: str) -> List[int]:
    print(f"🤖 Lead Finder Agent targeting niche: {niche}")
    if niche.lower() == "all":
        samples = [item for niche_list in NICHES.values() for item in niche_list]
    else:
        samples = NICHES.get(niche.lower(), [])

    if not samples:
        print("No built-in sample leads for this niche. You can still add leads manually to the database.")
        return []

    added_ids = []
    for business_name, email, note in samples:
        existing = find_client_by_email(email)
        if existing:
            print(f"Lead already exists, skipping: {business_name} ({email})")
            continue
        client_id = add_lead(business_name, email, note)
        added_ids.append(client_id)
        print(f"Added lead: {business_name} ({email})")
    return added_ids


def sales_agent() -> None:
    leads = fetch_clients_by_status("lead")
    if not leads:
        print("No leads found to email.")
        return

    for client in leads:
        print("\n---")
        requirements_questions = generate_requirements_questions(client["business_name"], client["last_note"])
        email_text = preview_sales_email(
            client["email"],
            client["business_name"],
            client["last_note"],
            requirements_questions=requirements_questions,
        )
        print(email_text)

        if not client["requirements"]:
            suggested_requirements = generate_requirements_summary(client["business_name"], client["last_note"])
            print("\nSuggested initial requirements draft for this client:")
            print(suggested_requirements)
            if require_manual_approval("Save this as the client's initial requirements?"):
                update_client_field(client["id"], "requirements", suggested_requirements)
                print("Saved suggested requirements for later development.")
            elif not is_noninteractive():
                custom = input(
                    "Enter custom requirements for this client, or press Enter to skip:\n"
                ).strip()
                if custom:
                    update_client_field(client["id"], "requirements", custom)
                    print("Saved custom requirements for later development.")

        approved = require_manual_approval("Approve sending this email?")
        if approved:
            email_subject = f"Grow {client['business_name']} with a better website"
            send_result = send_sales_email(client["email"], email_subject, email_text)
            print(send_result)
            update_status(client["id"], "emailed")
            print(f"Marked {client['business_name']} as emailed.")
        else:
            print(f"Skipped {client['business_name']}.")


def order_capture_agent() -> None:
    emailed_clients = fetch_clients_by_status("emailed")
    if not emailed_clients:
        print("No emailed clients to follow up with.")
        return

    print("\n=== Sales follow-up: mark responses as ordered ===")
    for client in emailed_clients:
        print(f"\n[{client['id']}] {client['business_name']} - {client['email']}")
        print(f"Saved requirements: {client['requirements'] or 'None'}")
        if require_manual_approval("Did this client reply positively and request a website? "):
            update_status(client["id"], "ordered")
            print(f"Client {client['business_name']} marked as ordered.")
        elif is_noninteractive():
            update_status(client["id"], "ordered")
            print(f"Non-interactive mode: Client {client['business_name']} auto-marked as ordered.")
        else:
            print(f"Client {client['business_name']} remains emailed.")


def developer_agent(deploy_target: str = "local") -> None:
    orders = fetch_clients_by_status("ordered")
    if not orders:
        print("No ordered clients found for development.")
        return

    for client in orders:
        requirements = (client["requirements"] or "").strip()
        if not requirements:
            requirements = "Generic local business website with contact details, services, and a call-to-action."
            update_client_field(client["id"], "requirements", requirements)

        html_content = generate_html_for_requirements(client["business_name"], requirements)
        success, path_or_message = deploy_basic_website(client["id"], client["business_name"], html_content, target=deploy_target)
        if success:
            update_client_field(client["id"], "website_url", path_or_message)
            update_status(client["id"], "built")
            print(f"Website built for {client['business_name']}: {path_or_message}")
        else:
            print(path_or_message)


def quality_and_billing_agent(payment_provider: str = "paypal") -> None:
    built_clients = fetch_clients_by_status("built")
    if built_clients:
        print("\n🤖 QA & Billing Agent checking built websites...")
    for client in built_clients:
        if not client["website_url"]:
            print(f"Client {client['business_name']} has no website URL recorded.")
            continue

        invoice_link = generate_invoice_link(client["id"], client["business_name"], provider=payment_provider)
        update_client_field(client["id"], "invoice_id", invoice_link)
        print(f"Invoice link ready for {client['business_name']}: {invoice_link}")

        admin_message = (
            f"Invoice prepared for {client['business_name']}\n"
            f"Website: {client['website_url']}\n"
            f"Invoice link: {invoice_link}\n"
            f"Client email: {client['email']}\n"
        )
        admin_result = send_admin_notification(
            f"Invoice ready for {client['business_name']}", admin_message
        )
        print(admin_result)

        approved = require_manual_approval("Approve sending invoice link and moving client to invoiced status?")
        if approved:
            update_status(client["id"], "invoiced")
            print(f"Client {client['business_name']} marked as invoiced.")

    invoiced_clients = fetch_clients_by_status("invoiced")
    for client in invoiced_clients:
        payment_status = simulate_payment_status(client["invoice_id"])
        print(f"Invoice status for {client['business_name']}: {payment_status}")
        if payment_status == "PAID":
            if require_manual_approval(f"Mark {client['business_name']} as paid?"):
                update_status(client["id"], "paid")
                print(f"Client {client['business_name']} marked as paid.")


def review_clients() -> None:
    from .database import fetch_all_clients

    clients = fetch_all_clients()
    if not clients:
        print("Database is empty.")
        return

    print("\nCurrent client pipeline status:")
    for client in clients:
        print(
            f"[{client['id']}] {client['business_name']} - {client['status']} - {client['email']}"
        )
