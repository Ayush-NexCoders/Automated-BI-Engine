# Meta Graph API Setup Guide

This guide will walk you through registering a Meta Graph API app and obtaining a long-lived page access token.

## Step 1: Register as a Meta Developer
1. Go to the [Meta for Developers](https://developers.facebook.com/) portal.
2. Log in with your Facebook account and register as a developer if you haven't already.

## Step 2: Create an App
1. Go to **My Apps** and click **Create App**.
2. Select **Other** > **Next**.
3. Select **Business** > **Next**.
4. Fill in the "App Name" (e.g., Automated-BI-Engine) and "App Contact Email".
5. Click **Create App**.

## Step 3: Add the Graph API Explorer
1. In your App Dashboard, find "Graph API Explorer" under Tools or navigate directly to the [Graph API Explorer](https://developers.facebook.com/tools/explorer/).

## Step 4: Obtain a User Access Token
1. In the Graph API Explorer, select your App in the "Meta App" dropdown.
2. In the "User or Page" dropdown, select **Get User Access Token**.
3. A popup will appear asking for permissions. You need the following permissions for page insights:
   - `pages_read_engagement`
   - `pages_read_user_content`
   - `read_insights`
4. Click **Generate Access Token** and approve the request.

## Step 5: Obtain a Page Access Token
1. In the "User or Page" dropdown, you should now see your Facebook Pages. Select the Page you want to analyze.
2. This generates a **short-lived Page Access Token**.

## Step 6: Convert to a Long-Lived Token
1. Click the "i" (info) icon next to the Access Token field.
2. Click **Open in Access Token Tool**.
3. At the bottom of the page, click **Extend Access Token**.
4. This new token will last for 60 days (or never expire, depending on the app type). Copy this token.

## Step 7: Get Your Page ID
1. You can find your Page ID in the Graph API Explorer by querying `me/accounts` with your user token, or directly from your Facebook Page's "About" section.

## Step 8: Test the Token
Use the `test_meta_insights.py` script provided in this directory to verify the token works.
