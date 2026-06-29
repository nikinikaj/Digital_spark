# Deployment Setup for the Agency Pipeline

This guide helps you move from local testing to a real online deployment.

## 1. Install Git

You need git installed on your machine. On Windows, download and install from:
https://git-scm.com/download/win

## 2. Create a GitHub Repository

You already have a repo: `https://github.com/nikinikaj/Digital_spark`

1. Install Git if it is not already installed.
   - The installer may ask for administrator approval to complete.
2. From your local workspace, run:

```bash
cd "c:\xampp\htdocs\glavna strana"
git init
git add .
git commit -m "Initial agency pipeline"
git branch -M main
git remote add origin https://github.com/nikinikaj/Digital_spark.git
git push -u origin main
```

## 3. Configure GitHub Pages

1. In your GitHub repo settings, open Pages.
2. Choose the `main` branch and `/docs` folder.
3. Save settings.

The generated preview site will be served from `docs/` after the pipeline run.

## 4. Set Real Environment Variables

Use the `.env.example` file as your template. In PowerShell, you can set env variables for the session like this:

```powershell
setx SMTP_HOST "smtp.example.com"
setx SMTP_PORT "587"
setx SMTP_USERNAME "your_smtp_username"
setx SMTP_PASSWORD "your_smtp_password"
setx EMAIL_FROM "agency@example.com"
setx PAYPAL_BASE_URL "https://www.paypal.com/paypalme/YourBusiness"
```

Restart your terminal after setting them.

## 5. Run the Pipeline

From the workspace root:

```bash
py run_agency.py --niche all --payment-provider paypal --deploy-target github-pages
```

If you want repeated daily runs, add `--loop`.

## 6. Next Real-World Improvements

- Add real client leads and their email contacts.
- Replace PayPal link simulation with a real PayPal invoice or payment API.
- Add a production email service such as SendGrid, Mailgun, or SMTP.
- Add a secure environment mechanism for deployment.
- Configure your chosen hosting provider if not using GitHub Pages.
