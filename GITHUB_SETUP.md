# 🚀 Quick GitHub & Streamlit Deployment

Your project is ready to deploy! Follow these steps:

## Step 1: Create GitHub Repository
1. Go to **[github.com/new](https://github.com/new)**
2. **Repository name**: `multi_source_agentic_ai`
3. **Description**: "Multi-agent Q&A system with SQL and RAG agents"
4. **Public** (so others can see it)
5. **Skip** "Initialize this repository with..." options
6. Click **"Create repository"**
7. Copy the repository URL (looks like: `https://github.com/YOUR_USERNAME/multi_source_agentic_ai.git`)

## Step 2: Push to GitHub
Replace `YOUR_USERNAME` with your actual GitHub username, then run in PowerShell:

```powershell
cd d:\multi_source_agentic_ai

git config user.email "your.email@example.com"
git config user.name "Your Name"

git commit -m "Initial commit: Multi-source agentic AI system with SQL and RAG agents"

git branch -M main

git remote add origin https://github.com/YOUR_USERNAME/multi_source_agentic_ai.git

git push -u origin main
```

*First time? GitHub will ask for your credentials. Use your GitHub personal access token (or authenticate via browser).*

## Step 3: Deploy on Streamlit Cloud
1. Go to **[share.streamlit.io](https://share.streamlit.io)**
2. Click "Sign in with GitHub"
3. Click "New app"
4. Select:
   - **Repository**: `YOUR_USERNAME/multi_source_agentic_ai`
   - **Branch**: `main`
   - **Main file path**: `streamlit_app.py`
5. Click "Deploy" and **wait 2-5 minutes**

## Step 4: Add Secrets to Streamlit
1. In Streamlit Cloud dashboard, click the **⋯** (three dots) menu
2. Click **"Edit secrets"**
3. Paste this (with YOUR actual keys):
```toml
GROQ_API_KEY = "gsk_YOUR_GROQ_KEY"
HF_TOKEN = "hf_YOUR_HF_TOKEN"
```
4. Save and app will **auto-restart**

## Step 5: Get Your Live Link ✨
Your app is now live at:
```
https://share.streamlit.io/YOUR_USERNAME/multi_source_agentic_ai/main/streamlit_app.py
```

Update your GitHub README with this link!

---

## Files Already Prepared

✅ **README.md** - Comprehensive documentation with quick start  
✅ **.gitignore** - Prevents committing secrets (.env, database, vectorstore)  
✅ **.env.example** - Template for users to see what keys they need  
✅ **.streamlit/secrets.toml** - Streamlit Cloud secrets (add via dashboard)  
✅ **DEPLOYMENT_GUIDE.md** - Detailed deployment instructions  
✅ **requirements.txt** - All Python dependencies listed  

---

## What Gets Published

✅ All Python source code  
✅ Documentation (README, guides, features)  
✅ Sample documents (data/company_docs/)  
✅ Requirements and configuration  

❌ NOT published:  
- .env file (has your API keys)  
- database/northwind.db  
- vectorstore/ (generated at runtime)  
- Virtual environment  

---

## Next Actions

1. **Create GitHub repo** → copy HTTPS URL  
2. **Run `git push` commands** (see Step 2 above) with YOUR username and email  
3. **Go to Streamlit Cloud** → deploy from GitHub  
4. **Add secrets** in Streamlit dashboard  
5. **Share your live link!** 🎉  

Need help with any step? Check DEPLOYMENT_GUIDE.md for troubleshooting.
