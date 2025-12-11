"""
Email utilities for sending OTP
"""
import smtplib
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def send_otp_email(to_email, otp):
    """
    Send OTP via email using Gmail SMTP
    
    Args:
        to_email (str): Recipient email address
        otp (str): 6-digit OTP code
    
    Returns:
        bool: True if email sent successfully, False otherwise
    """
    try:
        # SMTP configuration from environment variables
        smtp_server = os.getenv('SMTP_HOST', 'smtp.gmail.com')
        smtp_port = int(os.getenv('SMTP_PORT', '587'))
        smtp_email = os.getenv('SMTP_EMAIL')
        smtp_password = os.getenv('SMTP_PASSWORD')
        
        print(f"📧 Email Config - Server: {smtp_server}, Port: {smtp_port}, From: {smtp_email}")
        print(f"📧 Password length: {len(smtp_password) if smtp_password else 0} chars")
        
        if not smtp_email or not smtp_password:
            print("❌ SMTP credentials not configured in .env file")
            return False
        
        # Create message
        message = MIMEMultipart("alternative")
        message["Subject"] = "Quantum Banking - Login OTP"
        message["From"] = smtp_email
        message["To"] = to_email
        
        # Create HTML content
        html_content = f"""
        <html>
        <body style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto;">
            <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 20px; text-align: center;">
                <h1 style="color: white; margin: 0;">🏦 Quantum Banking</h1>
            </div>
            
            <div style="padding: 30px; background-color: #f8f9fa;">
                <h2 style="color: #333; text-align: center;">Your Login OTP</h2>
                
                <div style="background: white; padding: 20px; border-radius: 8px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); text-align: center; margin: 20px 0;">
                    <p style="color: #666; margin-bottom: 15px;">Your one-time password for secure login:</p>
                    <h1 style="color: #667eea; font-size: 36px; letter-spacing: 8px; margin: 20px 0; font-family: 'Courier New', monospace;">{otp}</h1>
                    <p style="color: #d63384; font-weight: bold;">⏰ This OTP will expire in 2 minutes</p>
                </div>
                
                <div style="background: #fff3cd; border: 1px solid #ffeaa7; border-radius: 4px; padding: 15px; margin: 20px 0;">
                    <p style="color: #856404; margin: 0; font-size: 14px;">
                        🔒 <strong>Security Notice:</strong> Never share this OTP with anyone. Our team will never ask for your OTP via phone or email.
                    </p>
                </div>
                
                <p style="color: #666; text-align: center; font-size: 14px;">
                    If you didn't request this OTP, please ignore this email and ensure your account is secure.
                </p>
            </div>
            
            <div style="background: #343a40; padding: 15px; text-align: center;">
                <p style="color: #adb5bd; margin: 0; font-size: 12px;">
                    © 2025 Quantum Banking. Secure • Reliable • Advanced
                </p>
            </div>
        </body>
        </html>
        """
        
        # Create plain text version
        text_content = f"""
        Quantum Banking - Login OTP
        
        Your one-time password for secure login: {otp}
        
        This OTP will expire in 2 minutes.
        
        Security Notice: Never share this OTP with anyone. Our team will never ask for your OTP via phone or email.
        
        If you didn't request this OTP, please ignore this email and ensure your account is secure.
        
        © 2025 Quantum Banking
        """
        
        # Attach parts
        text_part = MIMEText(text_content, "plain")
        html_part = MIMEText(html_content, "html")
        
        message.attach(text_part)
        message.attach(html_part)
        
        # Send email
        print(f"📧 Connecting to SMTP server {smtp_server}:{smtp_port}...")
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            print(f"📧 Starting TLS encryption...")
            server.starttls()
            print(f"📧 Logging in as {smtp_email}...")
            server.login(smtp_email, smtp_password)
            print(f"📧 Sending email to {to_email}...")
            server.send_message(message)
        
        print(f"✅ OTP email sent successfully to {to_email}")
        return True
        
    except Exception as e:
        import traceback
        print(f"❌ Failed to send OTP email: {str(e)}")
        print(f"❌ Full traceback: {traceback.format_exc()}")
        return False

def send_welcome_email(to_email, name, account_number):
    """
    Send welcome email after successful registration
    
    Args:
        to_email (str): Recipient email address
        name (str): User's name
        account_number (str): User's account number
    
    Returns:
        bool: True if email sent successfully, False otherwise
    """
    try:
        # Use same SMTP configuration as OTP email
        smtp_server = os.getenv('SMTP_HOST', 'smtp.gmail.com')
        smtp_port = int(os.getenv('SMTP_PORT', '587'))
        smtp_email = os.getenv('SMTP_EMAIL')
        smtp_password = os.getenv('SMTP_PASSWORD')
        
        if not smtp_email or not smtp_password:
            return False
        
        message = MIMEMultipart("alternative")
        message["Subject"] = "Welcome to Quantum Banking!"
        message["From"] = smtp_email
        message["To"] = to_email
        
        html_content = f"""
        <html>
        <body style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto;">
            <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 20px; text-align: center;">
                <h1 style="color: white; margin: 0;">🏦 Quantum Banking</h1>
            </div>
            
            <div style="padding: 30px; background-color: #f8f9fa;">
                <h2 style="color: #333;">Welcome, {name}! 🎉</h2>
                
                <p style="color: #666; font-size: 16px;">
                    Congratulations! Your Quantum Banking account has been successfully created.
                </p>
                
                <div style="background: white; padding: 20px; border-radius: 8px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); margin: 20px 0;">
                    <h3 style="color: #667eea; margin-top: 0;">Account Details</h3>
                    <p><strong>Account Number:</strong> {account_number}</p>
                    <p><strong>Email:</strong> {to_email}</p>
                </div>
                
                <p style="color: #666;">
                    You can now log in to your account using your account number and password. 
                    For security, you'll receive an OTP via email during each login.
                </p>
            </div>
            
            <div style="background: #343a40; padding: 15px; text-align: center;">
                <p style="color: #adb5bd; margin: 0; font-size: 12px;">
                    © 2025 Quantum Banking. Secure • Reliable • Advanced
                </p>
            </div>
        </body>
        </html>
        """
        
        html_part = MIMEText(html_content, "html")
        message.attach(html_part)
        
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()
            server.login(smtp_email, smtp_password)
            server.send_message(message)
        
        return True
        
    except Exception as e:
        print(f"Failed to send welcome email: {str(e)}")
        return False
