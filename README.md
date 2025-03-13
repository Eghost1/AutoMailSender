# AutoMailSender

Programa para envío automático de emails utilizando Gmail.

## Instalación

1. Clone o descargue este repositorio
2. Instale las dependencias:
   ```
   pip install -r requirements.txt
   ```

## Requisitos

- Python 3.6 o superior
- Las siguientes librerías de Python:
  - pandas
  - smtplib
  - email

## Configuración

1. **Credenciales de Gmail:**
   - Copia `config.example.py` a `config.py`
   - En `config.py` modifica:
     - EMAIL_ORIGIN: Tu dirección de Gmail
     - EMAIL_PASSWORD: Tu contraseña de aplicación de Gmail
   (Para obtener una contraseña de aplicación, activa la autenticación de dos factores en tu cuenta de Gmail y genera una contraseña de aplicación)

2. **Plantilla de Email:**
   - Crea un archivo `email_template.txt`
   - Usa [NOMBRE] donde quieras que aparezca el nombre del destinatario
   - Ejemplo:
     ```
     Estimado/a [NOMBRE],

     Tu mensaje aquí...

     Saludos cordiales,
     Tu Nombre
     ```

3. **Lista de Destinatarios:**
   Puedes usar uno de estos dos formatos:

   a) Archivo CSV (recipients.csv):
   ```
   nombre,email
   Juan Pérez,juan@ejemplo.com
   María García,maria@ejemplo.com
   ```

   b) Archivo TXT (recipients.txt):
   ```
   Nombre: Juan Pérez
   Email: juan@ejemplo.com

   Nombre: María García
   Email: maria@ejemplo.com
   ```

## Uso

1. Ejecuta el script:
   ```
   python mail_sender.py
   ```

2. El programa te permitirá:
   - Seleccionar el archivo de destinatarios
   - Previsualizar los emails
   - Enviar los emails
   - Ver el historial de envíos

## Historial de Envíos

Los emails enviados se registran en `sent_emails.txt` con:
- Fecha y hora de envío
- Nombre del destinatario
- Email del destinatario

## Notas Importantes

- Se recomienda probar primero con pocos destinatarios
- Gmail tiene límites de envío diarios
- Verifica que los archivos tengan codificación UTF-8
