# ChinaBridge Academy - Deploy to Fly.io

## Prerequisites

1. **Fly.io CLI installed**: [Download here](https://fly.io/docs/getting-started/installing-flyctl/)
2. **Free Fly.io account**: [Sign up here](https://fly.io) (includes free tier with 3 shared-cpu-1x VMs)
3. **GitHub repository set up** with your code pushed

## Step 1: Install Fly.io CLI

### On Windows (PowerShell):
```powershell
# Using Chocolatey
choco install flyctl

# Or download directly from https://fly.io/docs/getting-started/installing-flyctl/
```

### On macOS/Linux:
```bash
curl -L https://fly.io/install.sh | sh
```

## Step 2: Log in to Fly.io

```powershell
flyctl auth login
```

This will open your browser to authenticate. Login with your Fly.io account.

## Step 3: Create a Fly.io App

```powershell
cd c:\Users\mathu\Documents\ChinaBridge

# Create the app (use a unique app name)
flyctl apps create chinabridge-academy
# Or if that's taken, try: chinabridge-<yourname>
```

The Fly.io app name will be used as your URL: `https://chinabridge-academy.fly.dev`

## Step 4: Set Environment Variables

```powershell
# Set your email configuration for password resets
flyctl secrets set GMAIL_SENDER=your-email@gmail.com
flyctl secrets set GMAIL_PASSWORD=your_app_password_here
flyctl secrets set FLASK_ENV=production

# Verify secrets were set
flyctl secrets list
```

**Note**: For `GMAIL_PASSWORD`, use your [Gmail App Password](https://support.google.com/accounts/answer/185833) (not your regular password)

## Step 5: Deploy

```powershell
# Deploy your app
flyctl deploy

# This will:
# 1. Build your Docker image
# 2. Create a VM in Fly.io infrastructure
# 3. Deploy your application
# Wait for it to complete (2-5 minutes)
```

## Step 6: View Your App

```powershell
# Open the app in your browser
flyctl open

# Or manually visit: https://chinabridge-academy.fly.dev
```

To view logs:
```powershell
flyctl logs
```

## Advantages of Fly.io vs Render

| Feature | Fly.io | Render |
|---------|--------|--------|
| **Free tier** | 3 shared VMs (better value) | 1 web service (limited) |
| **Cold starts** | ~100ms | ~10-15 seconds |
| **Always-on** | Included on free tier | Need to upgrade to paid |
| **Region selection** | 30+ regions | Limited |
| **Pricing** | Pay-as-you-go (very cheap) | Fixed tier pricing |
| **Database** | Included storage | Ephemeral (resets) |

## Custom Domain (Optional)

To use your own domain (e.g., `chinabridge.com`):

1. Purchase a domain from Namecheap, GoDaddy, etc.
2. In Fly.io dashboard:
   ```powershell
   flyctl certs create chinabridge.com
   flyctl certs create *.chinabridge.com
   ```
3. Update your domain's DNS records to point to Fly.io

## Updating Your App

After making code changes:

```powershell
git add .
git commit -m "Your changes"
git push

flyctl deploy
```

## Monitoring

```powershell
# View real-time logs
flyctl logs

# Check app status
flyctl status

# View metrics
flyctl metrics
```

## Scale Your App (Optional)

By default, Fly.io runs 1 VM. If you want more capacity:

```powershell
# Scale to 3 instances (only pay for what you use)
flyctl scale count 3
```

## Troubleshooting

### App won't start?
```powershell
flyctl logs
```
Check the logs for errors. Common issues:
- Missing environment variables
- Wrong Python version
- Missing dependencies in requirements.txt

### Database not initializing?
The database will be created automatically on first run. Check logs with `flyctl logs`

### Port issues?
Fly.io uses port 8080. The code is pre-configured to use this.

---

## Cost Estimate

Fly.io free tier includes:
- 3 shared-cpu-1x 256MB RAM VMs
- 10GB egress bandwidth
- SQLite database storage

**Perfect for a small tutoring platform!** You'll likely stay on the free tier unless you get thousands of concurrent users.

## Next Steps

1. ✅ Deploy to Fly.io
2. 📧 Verify email sending works (send a password reset)
3. 🔒 Set up custom domain (optional)
4. 📊 Monitor for performance issues
5. 🚀 Add more features!

---

For more info: [Fly.io Docs](https://fly.io/docs/)
