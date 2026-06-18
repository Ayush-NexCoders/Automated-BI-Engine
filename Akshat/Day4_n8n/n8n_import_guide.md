# How to Import the n8n Ingestion Workflow

This guide explains how to load the provided JSON workflow into your n8n instance and configure the credentials to securely fetch data from Meta and LinkedIn.

## Step 1: Import the Workflow
1. Open your local n8n instance in your browser (usually `http://localhost:5678`).
2. Go to **Workflows** and click **Add Workflow**.
3. In the top right corner of the canvas, click the `...` (Options) menu and select **Import from File**.
4. Select the `meta_linkedin_ingestion_workflow.json` file located in this directory (`Akshat/Day4_n8n`).
5. The nodes (Schedule Trigger, Meta API Request, LinkedIn API Request, Merge Data) will appear on your screen!

## Step 2: Configure Meta Credentials
1. Double-click the **Meta API Request** node.
2. Under "Authentication", click the dropdown for **Credential for Query Auth** and select **Create New Credential**.
3. Name it "Meta Access Token".
4. Add a parameter:
   - **Name:** `access_token`
   - **Value:** Paste your Long-Lived Page Access Token here.
5. Save the credential.
6. The node URL uses `{{$env["META_PAGE_ID"]}}` as a variable. Since you might not have set environment variables in your n8n docker container, **replace `{{$env["META_PAGE_ID"]}}` in the URL field with your actual Facebook Page ID.**

## Step 3: Configure LinkedIn Credentials
1. Double-click the **LinkedIn API Request** node.
2. Under "Authentication", click the dropdown for **Credential for Header Auth** and select **Create New Credential**.
3. Name it "LinkedIn Access Token".
4. Add a parameter:
   - **Name:** `Authorization`
   - **Value:** `Bearer YOUR_LINKEDIN_TOKEN` *(Replace with your actual token)*.
5. Save the credential.
6. Similar to Meta, replace `{{$env["LINKEDIN_ORG_ID"]}}` in the Query Parameters with your actual LinkedIn Organization ID.

## Step 4: Test the Workflow
1. Click the **Execute Workflow** button at the bottom of the screen.
2. The Schedule Trigger will run, followed by the two API requests.
3. If configured correctly, they will turn green, and you can click the **Merge Data** node to view the combined JSON output containing your last-7-day metrics from both platforms!
4. **Don't forget to save your workflow** and toggle it to **Active** when you want it to run on the schedule automatically.
