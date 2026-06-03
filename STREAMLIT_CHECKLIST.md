# Quick Streamlit Deployment Checklist

## Before Deploying
- [ ] GitHub repo is public: https://github.com/atharva7592/multi_source_agentic_ai
- [ ] All files pushed to `main` branch
- [ ] `.env` is NOT in git (only `.env.example` is)
- [ ] `requirements.txt` is complete and no local paths

## On Streamlit Cloud
- [ ] Signed in with GitHub account
- [ ] Clicked "New app"
- [ ] Selected correct repo and branch
- [ ] Main file: `streamlit_app.py`
- [ ] Deployed app

## After Initial Deploy
- [ ] Waited 3-5 minutes for build
- [ ] Saw deployment message
- [ ] Got app URL (https://...)

## Adding Secrets (CRITICAL)
- [ ] Clicked app menu (three dots)
- [ ] Selected "Settings"
- [ ] Clicked "Secrets"
- [ ] Pasted API key in secrets editor
- [ ] Clicked "Save"
- [ ] App automatically restarted

## Testing
- [ ] App loads without error
- [ ] Can type in question box
- [ ] Get response from assistant
- [ ] Response includes sources

## If Something Failed
1. Check app logs (menu → View logs)
2. See what went wrong
3. Make fix locally
4. Push to GitHub
5. Streamlit auto-redeploys in ~2 minutes

## Common Errors & Fixes

| Error | Fix |
|-------|-----|
| GROQ_API_KEY not configured | Add to Streamlit Secrets (not .env) |
| ModuleNotFoundError | Wait longer (5+ min) or check requirements.txt |
| Connection timeout | Increase timeout in config or try different query |
| App crashes repeatedly | Check logs, might be memory issue |
| Very slow first time | First vectorstore build takes time (3-5 min) |
