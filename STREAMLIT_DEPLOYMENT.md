# 🚀 Deploy to Streamlit Cloud - Complete Guide

Your project is now ready to deploy on Streamlit Cloud! Follow these steps carefully to avoid errors.

---

## **STEP 1: Verify GitHub Setup** ✅

Your repository is at:
```
https://github.com/atharva7592/multi_source_agentic_ai
```

**Verify on GitHub:**
1. Go to your repo
2. Check that you see these key files:
   - ✅ `streamlit_app.py` - Main app file
   - ✅ `requirements.txt` - All dependencies
   - ✅ `data/company_docs/` - Sample documents (50 files)
   - ✅ `.env.example` - Secrets template
   - ✅ `.gitignore` - Excludes `.env` and secrets

---

## **STEP 2: Create Streamlit Cloud Account** 📝

1. Go to: **https://share.streamlit.io**
2. Click **"Sign in"** (top right)
3. Click **"Sign in with GitHub"**
4. Authorize Streamlit to access your GitHub account
5. ✅ You should see your GitHub account

---

## **STEP 3: Deploy Your App** 🚀

1. On Streamlit dashboard, click **"New app"** (top left)
2. Fill in the details:

   | Field | Value |
   |-------|-------|
   | Repository | `atharva7592/multi_source_agentic_ai` |
   | Branch | `main` |
   | Main file path | `streamlit_app.py` |

3. Click **"Deploy"**

**⏳ WAIT 2-5 minutes** - Streamlit will build and deploy your app

---

## **STEP 4: Add Secrets (IMPORTANT!)** 🔑

Once deployment completes, you'll see your app with an **error about missing GROQ_API_KEY**.

**This is expected!** You need to add your API key:

1. Click the **three dots (⋮)** menu in the top right
2. Select **"Settings"** → **"Secrets"**
3. Paste this in the secrets editor:

```toml
# Streamlit Cloud Secrets
GROQ_API_KEY = "your_groq_api_key_here"
HF_TOKEN = "your_huggingface_token_here"
```

**Get your GROQ API key:** https://console.groq.com/keys

4. Click **"Save"** (bottom right)
5. **The app will automatically restart** ✨

---

## **STEP 5: Verify App is Working** ✅

After restart, you should see:
- ✅ Title: "Agentic Q&A Assistant"
- ✅ Sidebar with settings
- ✅ Input box to ask questions
- ✅ No error messages

**Test it:**
1. Try asking: "What databases are available?"
2. Should get a response from the SQL or RAG agent
3. Response should include source citations

---

## **Troubleshooting**

### ❌ **"GROQ_API_KEY not configured"**
- **Solution**: Check you added the key to Streamlit Secrets (not just `.env`)
- Secrets are for Streamlit Cloud, `.env` is only local

### ❌ **"ModuleNotFoundError"**
- **Solution**: Your `requirements.txt` is fine. Streamlit will install automatically
- Wait 5+ minutes on first deploy

### ❌ **"Connection timeout"**
- **Solution**: Vector database is initializing first time
- Wait 3-5 minutes, then refresh
- Second load will be much faster

### ❌ **"App crashes after 3 minutes"**
- **Solution**: Likely Streamlit session timeout
- This is normal - users start fresh conversation
- If constant crashes: check logs in Streamlit dashboard

### ❌ **"No documents found"**
- **Solution**: Data files are in repo - check `data/company_docs/` exists
- Run locally first: `streamlit run streamlit_app.py`

---

## **Getting Your Live Link** 🔗

Once deployed successfully, your app URL will be:
```
https://multi-source-agentic-ai-<random>.streamlit.app
```

You can:
- Share this link with anyone
- Bookmark it
- Add to your portfolio

---

## **Optional: Custom Domain** 💼

Pro users can add a custom domain:
1. Streamlit Dashboard → Your App → Settings
2. Scroll to "Custom Domain"
3. Enter your domain

---

## **Need Help?**

If you still get errors:

1. **Check build logs**: Click app dropdown menu → "View logs"
2. **Verify GitHub**: Make sure all files are pushed
3. **Restart**: Click "Reboot" in app menu
4. **Factory reset**: App menu → "Delete app" → redeploy

---

**✨ Your app is live! Share it with the world!**
