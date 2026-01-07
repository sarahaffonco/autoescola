# Email Configuration Setup Guide

## How to Enable Real Email Delivery

Your application is configured to send emails using Gmail's SMTP server. Follow these steps to enable email delivery:

### Step 1: Enable 2-Factor Authentication on Gmail
1. Go to [myaccount.google.com](https://myaccount.google.com)
2. Sign in with your Gmail account
3. Navigate to **Security** (left sidebar)
4. Enable **2-Step Verification** if not already enabled
5. Go back to Security tab

### Step 2: Generate Gmail App Password
1. Still in the **Security** tab, scroll down to **App passwords** (appears only if 2FA is enabled)
2. Select **Mail** and **Windows Computer** (or your device)
3. Click **Generate**
4. Google will display a 16-character app password
5. Copy this password

### Step 3: Update .env File
1. Open the `.env` file in the project root
2. Find the Email Configuration section
3. Replace the values:
   - `EMAIL_HOST_USER`: Replace `seu-email@gmail.com` with your Gmail address
   - `EMAIL_HOST_PASSWORD`: Replace `sua-senha-de-app-16-caracteres` with the 16-character password from Step 2

**Example:**
```
EMAIL_HOST_USER=seu-nome@gmail.com
EMAIL_HOST_PASSWORD=abcd efgh ijkl mnop
```

### Step 4: Restart Django Server
1. Stop your Django development server (Ctrl+C)
2. Run: `python manage.py runserver`
3. The server will automatically load the new environment variables

### Step 5: Test Email Delivery
1. Go to the login page
2. Click "Esqueceu a senha?"
3. Enter your Gmail address
4. Check your inbox for the password reset email
5. The email should arrive within a few seconds

## Troubleshooting

### Email not arriving?
- Make sure the `.env` file is in the project root directory
- Verify the EMAIL_HOST_USER and EMAIL_HOST_PASSWORD are correct
- Check Gmail's "Less secure app access" setting (may need to be enabled)
- Look at Django console output for error messages

### Permission Denied / Authentication Failed?
- Make sure you used an **App Password** (16 characters), not your regular Gmail password
- Verify 2FA is enabled on your Gmail account
- The App Password must be generated from Gmail account settings

### Still showing console output?
- Make sure Django server was restarted after updating `.env`
- Check that `.env` file is in the correct location (project root)
- Verify email configuration values are correct

## Default Configuration

If EMAIL_HOST_USER or EMAIL_HOST_PASSWORD are empty, the system will fall back to console email backend (prints to terminal).

## Environment Variables Reference

| Variable | Purpose | Example |
|----------|---------|---------|
| EMAIL_BACKEND | Email service backend | `django.core.mail.backends.smtp.EmailBackend` |
| EMAIL_HOST | SMTP server address | `smtp.gmail.com` |
| EMAIL_PORT | SMTP port | `587` |
| EMAIL_USE_TLS | Enable TLS encryption | `True` |
| EMAIL_HOST_USER | Gmail address | `seu-email@gmail.com` |
| EMAIL_HOST_PASSWORD | Gmail app password | `xxxx xxxx xxxx xxxx` |
