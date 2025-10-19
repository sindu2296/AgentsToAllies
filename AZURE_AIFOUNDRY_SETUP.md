# Azure AI Foundry Setup Guide

This guide walks you through setting up Azure AI Foundry to get started with the multi-agent workflows.

---

## Step 1: Create a Microsoft Account

### For New Users (Free Trial - 200 Credits)
- **Credits**: $200 free credit for the first month
- **Requirement**: Credit card needed
- **Link**: [Azure Free Account](https://azure.microsoft.com/en-us/pricing/purchase-options/azure-account/?ef_id=_k_CjwKCAjwmNLHBhA4EiwA3ts3mez_Wer_ImE9M9PXaccfcKuWeRlhobk6thIXjcnIO9KMmpDm1DMZoBoC1sQQAvD_BwE_k_&OCID=AIDcmmfq865whp_SEM__k_CjwKCAjwmNLHBhA4EiwA3ts3mez_Wer_ImE9M9PXaccfcKuWeRlhobk6thIXjcnIO9KMmpDm1DMZoBoC1sQQAvD_BwE_k_&gad_source=1&gad_campaignid=21503043035&gbraid=0AAAAADcJh_uMqcfIjBVtFqflxZCaycVOa&gclid=CjwKCAjwmNLHBhA4EiwA3ts3mez_Wer_ImE9M9PXaccfcKuWeRlhobk6thIXjcnIO9KMmpDm1DMZoBoC1sQQAvD_BwE)

### For Students (Free Credits - 100 Credits Lifetime)
- **Credits**: $100 free credit (lifetime)
- **Requirement**: No credit card needed
- **Link**: [Azure for Students](https://azure.microsoft.com/en-us/free/students/)

### Sign Up Steps:
1. Visit the link above based on your account type
2. Click **"Start free"** button
3. Sign in with your Microsoft account (or create one)
4. Fill in your profile information
5. Complete the verification process
6. Accept terms and conditions

---

## Step 2: Create an Azure AI Foundry Resource

Once you've signed in to your Azure account:

1. Go to the **Azure Portal** (https://portal.azure.com)
2. Click **"+ Create a resource"** button
3. Search for **"AI Foundry"** or **"Azure AI Foundry"**
4. Click on the AI Foundry option and select **"Create"**
5. Fill in the required details:
   - **Resource name**: Give it a meaningful name (e.g., `my-ai-foundry`)
   - **Subscription**: Select your subscription
   - **Resource group**: Create a new one or select existing
   - **Region**: Choose a region close to you
6. Click **"Review + Create"** → **"Create"**
7. Wait for deployment to complete

---

## Step 3: Access Azure AI Foundry Portal

1. After the resource is created, click **"Go to resource"**
2. On the **Overview** page, you'll see a link to the **Azure AI Foundry portal**
3. Click the link to open the portal
4. You're now in the AI Foundry workspace!

---

## Step 4: Deploy a Model

### Access Models & Endpoints:
1. In the left sidebar, find and click **"Models + endpoints"**
2. Click on **"Deploy model"** button
3. Choose a model from the available options:
   - **GPT-4o**
   - **GPT-4 Turbo**
   - **GPT-3.5 Turbo**
   - Or any other available model

### Deploy Steps:
1. Select your preferred model
2. Click **"Confirm"** or **"Deploy"**
3. Choose a **deployment name** (e.g., `gpt-4-deployment`)
4. Set quota/limits if needed
5. Click **"Deploy"**
6. Wait for deployment to complete (usually 2-5 minutes)

---

## Step 5: Get Azure Credentials

Once your model is deployed:

1. Click on the **deployed model** in the Models + endpoints section
2. On the model details page, find the **"Keys and endpoint"** section
3. Copy the following values:
   - **Endpoint URL**: The API endpoint (e.g., `https://your-resource.openai.azure.com/`)
   - **API Key**: Your authentication key

---

## Step 6: Configure .env File

Now add your Azure credentials to the `.env` file in the project root:

```env
Replace <your-api-key> using your API key.
Replace <your_endpoint> using Endpoint URL.
Replace <your_model_name> using your model name.
```

### Example:
```env
<your-api-key>=abc123xyz789...
<your_endpoint>=https://my-ai-foundry.openai.azure.com/
<your_model_name>=gpt-4o
```

---

## Step 7: Verify Setup

To verify your setup is working:

1. Make sure all credentials are in the `.env` file
2. Run any of the sample scripts:
   ```bash
   python AIFoundry_sample.py
   ```
3. If successful, you'll see API responses and the workflow will execute

---

## Troubleshooting

### Issue: "Unauthorized" or "Invalid API Key"
- ✅ Double-check your API key in `.env`
- ✅ Make sure you copied the entire key without extra spaces
- ✅ Verify the deployment is in "Active" state

### Issue: "Model not found"
- ✅ Ensure deployment name matches exactly in `.env`
- ✅ Check that the model is still deployed in the portal
- ✅ Verify the endpoint URL is correct

### Issue: "Resource quota exceeded"
- ✅ Check your Azure credit balance
- ✅ Review deployment quotas in Models + endpoints
- ✅ Consider using a cheaper model (GPT-3.5 Turbo)

### Issue: Out of credits
- ✅ For students: You get $100 lifetime - request more free credits if available
- ✅ For trial users: Set up billing to continue after trial ends
- ✅ Monitor your usage in Azure Portal → Cost Management

---

## Quick Reference

| Item | Link |
|------|------|
| New Users (200 Credits) | https://azure.microsoft.com/en-us/pricing/purchase-options/azure-account/ |
| Students (100 Credits) | https://azure.microsoft.com/en-us/free/students/ |
| Azure Portal | https://portal.azure.com |
| AI Foundry Docs | https://learn.microsoft.com/en-us/azure/ai-foundry/ |

---

## Next Steps

✅ Once setup is complete, you can:
1. Run the [news_maf Streamlit UI](../news_maf/README.md)
2. Run the [job_recommendation_maf Streamlit UI](../job_recommendation_maf/README.md)
3. Explore the [AIFoundry_sample.py](../AIFoundry_sample.py) script
4. Build your own multi-agent workflows!

---

**Happy building! 🚀**
