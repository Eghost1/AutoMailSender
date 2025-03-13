import pandas as pd
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
from datetime import datetime
from config import *

def load_template():
    """Carga la plantilla del email"""
    try:
        with open(EMAIL_TEMPLATE_FILE, 'r', encoding='utf-8') as f:
            return f.read()
    except FileNotFoundError:
        print(f"❌ Error: No se encuentra {EMAIL_TEMPLATE_FILE}")
        return None

def load_recipients():
    """Carga los destinatarios desde CSV o TXT"""
    print("\n📋 CARGAR DESTINATARIOS")
    print("1. Desde archivo CSV")
    print("2. Desde archivo TXT")
    
    while True:
        choice = input("Seleccione formato (1/2): ")
        if choice in ['1', '2']:
            break
    
    filename = input("Nombre del archivo: ")
    
    try:
        if choice == '1':
            df = pd.read_csv(filename)
            return [{'nombre': row['nombre'], 'email': row['email']} 
                   for _, row in df.iterrows()]
        else:
            recipients = []
            current_recipient = {}
            
            with open(filename, 'r', encoding='utf-8') as f:
                lines = f.readlines()
                
            for line in lines:
                line = line.strip()
                if line.startswith('Nombre: '):
                    if current_recipient:
                        recipients.append(current_recipient)
                    current_recipient = {'nombre': line.replace('Nombre: ', '')}
                elif line.startswith('Email: '):
                    current_recipient['email'] = line.replace('Email: ', '')
            
            if current_recipient:
                recipients.append(current_recipient)
            return recipients
            
    except Exception as e:
        print(f"❌ Error al cargar destinatarios: {str(e)}")
        return []

def record_sent_email(recipient):
    """Registra el email enviado"""
    with open(SENT_EMAILS_FILE, 'a', encoding='utf-8') as f:
        if os.path.getsize(SENT_EMAILS_FILE) == 0:
            f.write("HISTORIAL DE EMAILS ENVIADOS\n")
            f.write("=" * 50 + "\n\n")
        
        f.write("-" * 50 + "\n")
        f.write(f"Fecha: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write(f"Nombre: {recipient['nombre']}\n")
        f.write(f"Email: {recipient['email']}\n")
        f.write("-" * 50 + "\n")

def preview_email(template, recipient):
    """Muestra una previsualización del email"""
    print("\n📧 PREVISUALIZACIÓN DEL EMAIL\n")
    print("=" * 50)
    
    email_content = template.replace('[NOMBRE]', recipient['nombre'])
    print(f"Para: {recipient['email']}")
    print(f"De: {EMAIL_ORIGIN}")
    print(f"Asunto: {EMAIL_SUBJECT}")
    print("-" * 50)
    print("Contenido:")
    print(email_content)
    print("=" * 50)

def send_email(template, recipient):
    """Envía el email al destinatario"""
    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(EMAIL_ORIGIN, EMAIL_PASSWORD)
        
        msg = MIMEMultipart()
        msg['From'] = EMAIL_ORIGIN
        msg['To'] = recipient['email']
        msg['Subject'] = EMAIL_SUBJECT
        
        body = template.replace('[NOMBRE]', recipient['nombre'])
        msg.attach(MIMEText(body, 'plain'))
        
        server.send_message(msg)
        server.quit()
        
        record_sent_email(recipient)
        print(f"✅ Email enviado exitosamente a {recipient['email']}")
        return True
        
    except Exception as e:
        print(f"❌ Error al enviar email: {str(e)}")
        return False

def main():
    template = load_template()
    if not template:
        return
        
    recipients = load_recipients()
    if not recipients:
        print("❌ No hay destinatarios para enviar")
        return
        
    for recipient in recipients:
        preview_email(template, recipient)
        
        while True:
            choice = input("\n¿Desea enviar este email? (1: Sí, 2: No, 3: Salir): ")
            if choice in ['1', '2', '3']:
                break
            
        if choice == '1':
            send_email(template, recipient)
        elif choice == '3':
            break

if __name__ == "__main__":
    main()
