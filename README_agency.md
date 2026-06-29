# Multi-Agent Agency Automation

This workspace includes a small Python-based agency pipeline with a shared SQLite database and four specialized agents:

- `Lead Finder Agent` — discovers sample leads for a chosen niche and stores them in `agency_business.db`
- `Sales Agent` — drafts pitch emails and asks for manual approval before marking leads as emailed
- `Developer Agent` — generates a simple responsive HTML website and saves it under `deployed_sites/`
- `Quality & Billing Agent` — prepares invoice links and asks for manual approval to mark invoices and payments

## Files

- `agency/database.py` — shared SQLite database schema and helpers
- `agency/tools.py` — site deployment, email preview, and invoice simulation tools
- `agency/agents.py` — four agent functions implementing the pipeline
- `run_agency.py` — pipeline orchestration and optional loop mode
- `deployed_sites/` — generated websites are saved here
- `agency_business.db` — created after first run

## How to use

From the workspace root, run:

```bash
py run_agency.py --niche "local cafe"
```

Use another built-in niche or all of them:

```bash
py run_agency.py --niche "fitness"
py run_agency.py --niche "beauty"
py run_agency.py --niche "restaurant"
py run_agency.py --niche "all"
```

To use PayPal invoice links and deploy the completed sites for GitHub Pages preview:

```bash
py run_agency.py --niche "all" --payment-provider paypal --deploy-target github-pages
```

After that command completes, the generated site preview is copied into `docs/`, which you can host with GitHub Pages.

If you configure SMTP in environment variables or via `.env`, the pipeline will send real emails during the outreach phase.

A local `.env` file has been created in the workspace with your deployed SMTP/PayPal settings. It is ignored by `.gitignore`.

Current target repository: `https://github.com/nikinikaj/Digital_spark.git`

If git is not installed, install it first and then run the repository setup commands in `DEPLOYMENT_SETUP.md`.

Use `.env.example` as a template for your real deployment settings. Create a `.env` file or set environment variables before running the script.

### Optional environment configuration
Set these variables in your shell or environment to enable real email sending and PayPal behavior:

```bash
set SMTP_HOST=smtp.example.com
set SMTP_PORT=587
set SMTP_USERNAME=your_username
set SMTP_PASSWORD=your_password
set EMAIL_FROM=agency@example.com
set PAYPAL_BASE_URL=https://www.paypal.com/paypalme/YourBusiness
```

## Safety guardrails

- Emails are never sent automatically; you must confirm each draft manually.
- Invoice and payment updates also require manual approval.
- Website generation is local only; no remote deployment is performed.

## How to adapt it

1. Change `NICHES` in `agency/agents.py` for your target industry.
2. Replace `preview_sales_email()` in `agency/tools.py` with a real SMTP or SendGrid integration when ready.
3. Replace `generate_invoice_link()` in `agency/tools.py` with a real PayPal or Stripe invoice generator.
4. Replace `generate_html_for_requirements()` with an OpenAI call or a more advanced template engine.
5. The sales agent now suggests client-specific requirements and request questions to make communication easier.
## GitHub Pages deployment

The repository includes a `gh_pages_site/` folder when you run with `--deploy-target github-pages`. You can publish that folder as a GitHub Pages site by pushing it to a branch like `gh-pages` or by copying its contents to the repository root on a Pages-enabled branch.

Example workflow:

1. Run the pipeline:
   ```bash
   python run_agency.py --niche "all" --payment-provider paypal --deploy-target github-pages
   ```
2. Copy or move `gh_pages_site/` content into your GitHub Pages branch.
3. Publish the branch in your GitHub repository settings.

## Recommended next step

If you want, I can also adapt this directly to your specific niche and connect it to real hosting or billing providers like PayPal.
