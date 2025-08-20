# Netlify CLI Setup Instructions

## Install Netlify CLI (if not already installed)
```bash
npm install -g netlify-cli
# or
yarn global add netlify-cli
```

## Initialize Netlify Site
```bash
# Login to Netlify
netlify login

# Initialize site in the project directory
cd /path/to/NeuronAutomator
netlify init

# Follow the prompts:
# - Create & configure a new site
# - Choose your team
# - Site name: neuron-automator (or your preferred name)
# - Build command: pip install -r docs-requirements.txt && mkdocs build
# - Publish directory: site
```

## Get Site Information
```bash
# Get site ID and other details
netlify status

# Test local build
netlify build

# Manual deploy (optional)
netlify deploy --prod
```

## Configure GitHub Secrets
After initialization, add these secrets to your GitHub repository:

1. Go to GitHub repo → Settings → Secrets and variables → Actions
2. Add these repository secrets:
   - `NETLIFY_AUTH_TOKEN`: Get from https://app.netlify.com/user/applications/personal
   - `NETLIFY_SITE_ID`: Get from `netlify status` command or Netlify dashboard