import argparse
import time

from agency.database import setup_database
from agency.agents import (
    developer_agent,
    lead_finder_agent,
    order_capture_agent,
    quality_and_billing_agent,
    review_clients,
    sales_agent,
)
from agency.publisher import publish_docs_site


def run_agency_pipeline(niche: str, payment_provider: str, deploy_target: str) -> None:
    setup_database()

    print("\n=== Phase 1: Lead Finder ===")
    lead_finder_agent(niche)

    print("\n=== Phase 2: Sales Outreach ===")
    sales_agent()

    print("\n=== Phase 2.5: Sales Follow-Up ===")
    order_capture_agent()

    print("\n=== Phase 3: Development ===")
    developer_agent(deploy_target=deploy_target)

    print("\n=== Phase 4: Quality & Billing ===")
    quality_and_billing_agent(payment_provider=payment_provider)

    print("\n=== Review ===")
    review_clients()

    if deploy_target == "github-pages":
        print("\n=== Publish ===")
        success, message = publish_docs_site()
        print(message)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run the agency automation pipeline.")
    parser.add_argument("--niche", default="local cafe", help="Target niche for lead generation. Use 'all' to add every built-in sample lead.")
    parser.add_argument("--payment-provider", default="paypal", help="Payment method used for invoice links (paypal or invoice).")
    parser.add_argument("--deploy-target", default="local", help="Deployment target: 'local' or 'github-pages'.")
    parser.add_argument(
        "--loop",
        action="store_true",
        help="Run the pipeline repeatedly every 24 hours (for scheduled automation).",
    )
    args = parser.parse_args()

    if args.loop:
        while True:
            run_agency_pipeline(args.niche, args.payment_provider, args.deploy_target)
            print("Waiting 24 hours until next run... Press Ctrl+C to stop.")
            time.sleep(86400)
    else:
        run_agency_pipeline(args.niche, args.payment_provider, args.deploy_target)
