import imaplib
import email
import re

def get_seek_verification_code(email_user, app_password):
    imap_host = 'imap.gmail.com'
    mail = imaplib.IMAP4_SSL(imap_host)

    try:
        mail.login(email_user, app_password)
        mail.select('inbox')

        # Search SEEK emails
        result, data = mail.search(None, '(FROM "noreply@seek.com.au" SUBJECT "is your code for SEEK")')
        mail_ids = data[0].split()

        if not mail_ids:
            return None

        latest_id = mail_ids[-1]

        result, message_data = mail.fetch(latest_id, '(RFC822)')
        raw_email = message_data[0][1]
        msg = email.message_from_bytes(raw_email)

        # Get email body
        if msg.is_multipart():
            for part in msg.walk():
                if part.get_content_type() == "text/plain":
                    body = part.get_payload(decode=True).decode()
                    break
        else:
            body = msg.get_payload(decode=True).decode()

        # Extract 6-digit code
        match = re.search(r'\b(\d{6})\b', body)
        if match:
            return match.group(1)

    except Exception as e:
        print(f"Error reading email: {e}")
        return None
    finally:
        mail.logout()
