# Zoho Books & Inventory OAuth 2.0 Setup Guide

This guide will walk you through registering a Server-based Application in the Zoho API Console and obtaining an Access Token and Refresh Token to authenticate your API calls.

## Step 1: Register your Application
1. Go to the [Zoho API Console](https://api-console.zoho.com/).
2. Click **Add Client** and select **Server-based Applications**.
3. Fill in the following details:
   - **Client Name:** `Automated-BI-Engine` (or anything you prefer).
   - **Homepage URL:** `https://localhost`
   - **Authorized Redirect URIs:** `https://localhost/callback`
4. Click **Create**.
5. You will now see your **Client ID** and **Client Secret**. Keep these secure.

## Step 2: Generate the initial Grant Token
To get access, we first need a Grant Token. You will do this directly in your web browser.

1. Copy the URL below and replace `YOUR_CLIENT_ID` with your actual Client ID.

```text
https://accounts.zoho.com/oauth/v2/auth?scope=ZohoBooks.invoices.READ,ZohoInventory.salesorders.READ&client_id=YOUR_CLIENT_ID&response_type=code&access_type=offline&redirect_uri=https://localhost/callback
```

2. Paste this URL into your browser and hit Enter.
3. You will be prompted to log in to Zoho (if not already) and click **Accept** to grant the application access to read invoices and sales orders.
4. After clicking Accept, your browser will redirect to a URL that looks like this:
   `https://localhost/callback?code=1000.xxxxxxx.yyyyyyy&location=us&accounts-server=https%3A%2F%2Faccounts.zoho.com`
5. The page will likely say "Site cannot be reached"—this is completely normal!
6. Look at the URL bar and copy the value of `code=`. This is your **Grant Token**. *(Note: This token expires in a few minutes, so proceed to Step 3 quickly!)*

## Step 3: Generate the Refresh & Access Tokens
Now, we exchange the Grant Token for a long-lasting Refresh Token and a short-lived Access Token.

You can do this using `curl` in your terminal (PowerShell) or by using a tool like Postman. Here is the `curl` command for your terminal. Replace the placeholders with your actual credentials:

```powershell
curl -X POST "https://accounts.zoho.com/oauth/v2/token" `
     -d "grant_type=authorization_code" `
     -d "client_id=YOUR_CLIENT_ID" `
     -d "client_secret=YOUR_CLIENT_SECRET" `
     -d "redirect_uri=https://localhost/callback" `
     -d "code=YOUR_GRANT_TOKEN"
```

*Note: If your Zoho account is not in the US, change `.com` to your region (e.g., `.in`, `.eu`, `.com.au`).*

The response will be a JSON object containing your `access_token` and `refresh_token`.
**IMPORTANT: Save your `refresh_token`!** You will use it to programmatically get new access tokens when the current one expires (they expire every hour).

## Step 4: Find your Organization ID
You need your Organization ID to query the Books and Inventory APIs.
1. Log in to your Zoho Books or Zoho Inventory account.
2. Click your profile picture/company name in the top right corner.
3. Your **Organization ID** will be displayed there (e.g., `Organization ID: 123456789`).

## Step 5: Test the API
You are now ready to run the `test_zoho_api.py` script provided in this folder!

```powershell
python test_zoho_api.py --org-id "YOUR_ORG_ID" --token "YOUR_ACCESS_TOKEN"
```
