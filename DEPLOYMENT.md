# ChinaBridge Academy - Deployment Guide

## 🚀 Deploy to Render (Free)

Follow these steps to deploy your Flask app on Render.com:

### **Step 1: Create a GitHub Repository**

```bash
cd c:\Users\mathu\Documents\ChinaBridge

# Initialize git
git init
git add .
git commit -m "Initial commit - ChinaBridge Academy"

# Create a repository on GitHub and push
git remote add origin https://github.com/yourusername/chinabridge.git
git branch -M main
git push -u origin main
```

### **Step 2: Sign Up on Render**

1. Go to [render.com](https://render.com)
2. Click "Sign Up" and connect your GitHub account
3. Authorize Render to access your repositories

### **Step 3: Create a New Web Service**

1. On the Render dashboard, click **"New +"** → **"Web Service"**
2. Select your `chinabridge` repository
3. Configure the service:
   - **Name**: `chinabridge` (or your preferred name)
   - **Environment**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn server:app`
   - **Pricing Plan**: Free (recommended)

### **Step 4: Add Environment Variables**

In the Render settings, add these environment variables:

| Key | Value |
|-----|-------|
| `FLASK_ENV` | `production` |
| `GMAIL_SENDER` | `your-email@gmail.com` |
| `GMAIL_PASSWORD` | `your_app_password_here` |

**Note**: For `GMAIL_PASSWORD`, use your [Gmail App Password](https://support.google.com/accounts/answer/185833) (not your regular password)

### **Step 5: Deploy**

1. Click **"Create Web Service"**
2. Render will automatically build and deploy your app
3. Wait for deployment to complete (2-5 minutes)
4. Your app will be live at: `https://chinabridge.onrender.com`

### **Step 6: Update Your Domain (Optional)**

To use a custom domain:
1. Purchase a domain (e.g., `chinabridge.com` from Namecheap, GoDaddy, etc.)
2. In Render dashboard → **Settings** → **Custom Domains**
3. Add your domain and follow DNS setup instructions

### **Step 7: Verify Everything Works**

Test your deployed app:
- ✅ Homepage: `https://yourapp.onrender.com`
- ✅ Login/Register at the bottom of the page
- ✅ Dashboard after login
- ✅ Password reset email

---

## 📁 Project Structure

```
chinabridge/
├── index.html              (Homepage)
├── dashboard.html          (Student dashboard)
├── admin.html              (Admin panel)
├── reset-password.html     (Password reset page)
├── styles.css              (Shared stylesheet)
├── server.py               (Flask backend)
├── requirements.txt        (Python dependencies)
├── Procfile                (Render deployment config)
├── .gitignore              (Files to ignore in git)
└── chinabridge.db          (SQLite database)
```

---

## 🔑 Important Notes

### Email Configuration
- Your Flask app uses Gmail for password reset emails
- You MUST set up a Gmail App Password (not your regular password)
- [Create Gmail App Password](https://support.google.com/accounts/answer/185833)

### Database
- The app uses SQLite (`chinabridge.db`)
- Database is stored in the Render filesystem
- **Note**: Render's free tier has ephemeral storage, meaning the database resets when the app restarts
- For a production app, consider using a persistent database (PostgreSQL)

### Performance
- Free tier apps sleep after 15 minutes of inactivity
- First request after sleep will take 10-15 seconds to respond
- Upgrade to a paid plan for always-on performance

---

## 🛠️ Local Development

To test locally before deploying:

```bash
# Install dependencies
pip install -r requirements.txt

# Run the Flask app
python server.py
```

Then visit `http://localhost:5000` in your browser.

---

## 📝 Troubleshooting

### App won't start?
- Check Render logs: Dashboard → Your App → **Logs**
- Ensure `gunicorn` is in requirements.txt
- Check that Procfile has correct command

### Email not sending?
- Verify Gmail App Password is correct
- Check email is enabled in production environment variables
- Look at server logs for smtp errors

### Database not persisting?
- This is expected on Render's free tier
- Consider upgrading or switch to PostgreSQL

---

## 💡 Next Steps

1. ✅ Deploy to Render
2. ✅ Get custom domain
3. ⭕ Set up persistent database (PostgreSQL)
4. ⭕ Add payment processing for course enrollment
5. ⭕ Add more tutors and courses
6. ⭕ Upgrade to paid tier for 100% uptime

Good luck! 🚀
