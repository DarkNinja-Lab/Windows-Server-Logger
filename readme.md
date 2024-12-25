# Windows Event Logger mit Discord-Benachrichtigungen

## Überblick
Dieser Windows Event Logger liest Sicherheitsereignisse aus den Windows-Ereignisprotokollen und sendet diese in Echtzeit an einen Discord-Kanal über einen Webhook. Das Tool ermöglicht es, kritische Ereignisse wie Benutzererstellung, Benutzerlöschung, RDP-Verbindungen und andere sicherheitsrelevante Aktionen zu überwachen.

## Funktionen
- 🔑 Echtzeitüberwachung von Windows-Sicherheitsereignissen
- 🔗 Integration mit Discord über Webhook
- ❌ Duplikatüberprüfung innerhalb eines definierten Zeitfensters
- 🔧 Anpassbare Ereignistypen und Nachrichtenfarben

## Voraussetzungen und Installation 
1. **Python 3.9 oder höher** <br /> 
Ich selber habe 3.9 verwendet. <br /> <br />
2. **Pip-Pakete:**
   - `pywin32`
   - `requests`
   - `python-dotenv`
3. .env muss erstellt werden mit dem Inhalt : <br />
`DISCORD_WEBHOOK_URL=discordwebhookurl`

4. **Klonen Sie das Repository**<br />
git clone https://github.com/IhrBenutzername/windows-event-logger.git

5. **Navigieren Sie in das Projektverzeichnis**<br />
cd windows-event-logger

6. **Erstellen Sie eine virtuelle Umgebung (optional aber empfohlen)**<br />
python -m venv venv
source venv/bin/activate  # Bei Windows: venv\Scripts\activate

7. **Installieren Sie die Abhängigkeiten**<br />
pip install -r requirements.txt

8. **Konfigurieren Sie den Discord-Webhook**<br />
Bearbeiten Sie die config.json-Datei und fügen Sie Ihre Webhook-URL hinzu.

9. **Starten Sie das Tool** <br />
python main.py