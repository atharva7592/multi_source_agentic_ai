# Deployment Guide: GitHub + Streamlit Cloud

This guide walks you through publishing your Multi-Source Agentic AI System on GitHub and deploying it on Streamlit Cloud.

## Part 1: Prepare for GitHub

### Step 1: Verify Files Are Ready
Ensure your project has:
- ✅ `.gitignore` (prevents committing secrets)
- ✅ `.env.example` (template for users)
- ✅ `requirements.txt` (all dependencies)
- ✅ `README.md` (comprehensive documentation)
- ✅ `.streamlit/secrets.toml` (already in .gitignore)

### Step 2: Create .env.example
This helps users know what keys they need:

```bash
GROQ_API_KEY=your_groq_api_key_here
HF_TOKEN=your_huggingface_token_here
```

## Part 2: Push to GitHub

### Step 1: Create GitHub Repository
1. Go to [github.com/new](https://github.com/new)
2. **Repository name**: `multi_source_agentic_ai`
3. **Description**: "Multi-agent Q&A system with SQL and RAG agents"
4. **Public** (so others can see it)
5. **Don't** initialize with README (we have one)
6. Click "Create repository"

### Step 2: Initialize Git Locally
Open PowerShell in your project directory and run:

```powershell
# Initialize git
git init

# Add all files (except those in .gitignore)
git add .

# Verify what will be committed (secrets should NOT appear)
git status

# Create first commit
git commit -m "Initial commit: Multi-source agentic AI system with SQL and RAG agents"

# Rename branch to main
git branch -M main

# Add GitHub as remote
git remote add origin https://github.com/YOUR_USERNAME/multi_source_agentic_ai.git

# Push to GitHub
git push -u origin main
```

### Step 3: Verify on GitHub
- Go to your GitHub repo URL: `https://github.com/YOUR_USERNAME/multi_source_agentic_ai`
- ✅ README.md displays
- ✅ No `.env` file visible
- ✅ All Python files present

---

## Part 3: Deploy on Streamlit Cloud

### Step 1: Create Streamlit Account
1. Go to [share.streamlit.io](https://share.streamlit.io)
2. Click "Sign in with GitHub"
3. Authorize Streamlit to access your GitHub account
4. ✅ You should see your GitHub repos

### Step 2: Deploy Your App
1. Click "New app" button (top right)
2. Fill in deployment details:
   - **Repository**: `YOUR_USERNAME/multi_source_agentic_ai`
   - **Branch**: `main`
   - **Main file path**: `streamlit_app.py`
3. Click "Deploy"

**⏳ Wait 2-5 minutes while it installs dependencies and starts**

### Step 3: Add Secrets to Streamlit
Once the app appears, it will timeout if secrets aren't configured:

1. Go to your Streamlit Cloud app dashboard
2. Click the **three dots** (menu) → **Edit secrets**
3. Paste your secrets in TOML format:

```toml
GROQ_API_KEY = "gsk_YOUR_ACTUAL_KEY_HERE"
HF_TOKEN = "hf_YOUR_ACTUAL_TOKEN_HERE"
```

4. Save and the app will **automatically restart**

### Step 4: Get Your Live Link
Your app is now live at:
```
https://share.streamlit.io/YOUR_USERNAME/multi_source_agentic_ai/main/streamlit_app.py
```

**Shorter shareable link**: Streamlit provides a short URL in the app header

---

## Part 4: Add Deployment Info to GitHub

### Update README with Live Link
Edit your GitHub `README.md` and replace:
```markdown
**🚀 [Live Demo on Streamlit Cloud](https://share.streamlit.io/YOUR_GITHUB_USERNAME/multi_source_agentic_ai/main/streamlit_app.py)**
```

With your actual link:
```markdown
**🚀 [Live Demo on Streamlit Cloud](https://share.streamlit.io/atharva/multi_source_agentic_ai/main/streamlit_app.py)**
```

### Push Update
```powershell
git add README.md
git commit -m "Add Streamlit Cloud deployment link"
git push
```

---

## Part 5: Usage Instructions for Users

### For Users Visiting Your GitHub
They'll see:
1. 📖 Comprehensive README
2. 🌐 **Live Demo Link** (directly runs Streamlit app)
3. 📁 Full source code
4. ⚙️ Configuration guide
5. 🧪 Test suite

### For Users Running Locally
```markdown
## Local Installation

```bash
git clone https://github.com/YOUR_USERNAME/multi_source_agentic_ai.git
cd multi_source_agentic_ai

# Create virtual environment
python -m venv venv
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Create .env file (copy from .env.example)
copy .env.example .env
# Edit .env with your API keys

# Run CLI
python app.py

# Or run web UI
streamlit run streamlit_app.py
```

---

## Troubleshooting Deployment

### Issue: App Timeout on Streamlit Cloud
**Cause**: Secrets not configured, or dependencies not installed  
**Fix**: 
1. Check secrets are added (Settings → Secrets)
2. Check `requirements.txt` has all dependencies
3. Restart the app (click menu → Reboot script)

### Issue: "ModuleNotFoundError: No module named..."
**Cause**: Missing dependency in `requirements.txt`  
**Fix**: Add to requirements.txt and push to GitHub (app auto-redeploy)

### Issue: GROQ_API_KEY Error
**Cause**: Secrets not in TOML format or not saved  
**Fix**: 
```toml
# Correct format (note: spaces around =)
GROQ_API_KEY = "gsk_YOUR_KEY"

# Wrong format
GROQ_API_KEY="gsk_YOUR_KEY"  # no spaces
```

### Issue: Rate Limit Exceeded (429 Error)
**Cause**: Exceeded Groq free tier (100k tokens/day)  
**Fix**: 
- Upgrade Groq plan at [console.groq.com](https://console.groq.com/settings/billing)
- Or deploy with a different LLM (GPT-4, Claude, etc.)

---

## Continuous Updates

### When You Update Code
```powershell
# Make changes, then:
git add .
git commit -m "Your message"
git push

# Streamlit Cloud auto-detects changes and redeploys
```

**Auto-redeploy happens within 30 seconds**

### When You Update Dependencies
1. Update `requirements.txt`
2. Push to GitHub
3. Streamlit Cloud automatically installs new packages
4. App redeploys

---

## Optional: Advanced Deployment

### Custom Domain
[Streamlit Cloud documentation](https://docs.streamlit.io/streamlit-cloud/get-started/share-your-app)

### Upgrade Streamlit Tier
For higher concurrency and resource limits, upgrade from Community to Professional tier in Streamlit Cloud dashboard

### Docker Deployment (Self-Hosted)
If you want full control, create a `Dockerfile`:
```dockerfile
FROM python:3.10
WORKDIR /app
COPY . .
RUN pip install -r requirements.txt
CMD ["streamlit", "run", "streamlit_app.py"]
```

---

## Security Best Practices

### DO:
✅ Keep `.env` in `.gitignore`  
✅ Use Streamlit Secrets for deployed app  
✅ Use GitHub private repo if sensitive data  
✅ Rotate API keys regularly  

### DON'T:
❌ Commit `.env` to GitHub  
❌ Hardcode secrets in code  
❌ Share your Groq/HF tokens  
❌ Leave secrets in plaintext comments  

---

## Final Checklist

Before sharing your deployment:

- [ ] App runs successfully on Streamlit Cloud
- [ ] No error messages or timeouts
- [ ] README has live link
- [ ] `.gitignore` properly excludes secrets
- [ ] All features work (SQL, RAG, validation, memory)
- [ ] GitHub repo is public and discoverable
- [ ] Source citations display correctly
- [ ] Conversation memory works in web UI

---

## You're Done! 🎉

Your Multi-Source Agentic AI System is now:
- 📦 Published on GitHub
- 🌐 Live on Streamlit Cloud
- 📚 Documented and shareable
- ✨ Ready for production use

Share your live link: `https://share.streamlit.io/YOUR_USERNAME/multi_source_agentic_ai/main/streamlit_app.py`
