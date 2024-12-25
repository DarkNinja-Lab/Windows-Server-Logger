# Windows Event Logger mit Discord-Benachrichtigungen

## Überblick
Dieser Windows Event Logger liest Sicherheitsereignisse aus den Windows-Ereignisprotokollen und sendet diese in Echtzeit an einen Discord-Kanal über einen Webhook. Das Tool ermöglicht es, kritische Ereignisse wie Benutzererstellung, Benutzerlöschung, RDP-Verbindungen und andere sicherheitsrelevante Aktionen zu überwachen.

## Funktionen
- 🔑 Echtzeitüberwachung von Windows-Sicherheitsereignissen
- 🔗 Integration mit Discord über Webhook
- ❌ Duplikatüberprüfung innerhalb eines definierten Zeitfensters
- 🔧 Anpassbare Ereignistypen und Nachrichtenfarben

## Installation und Nutuzng

1. **Klonen Sie das Repository**<br />
git clone https://github.com/IhrBenutzername/windows-event-logger.git

2. **Navigieren Sie in das Projektverzeichnis**<br />
cd windows-event-logger

3. **Erstellen Sie eine virtuelle Umgebung (optional aber empfohlen)**<br />
python -m venv venv
source venv/bin/activate  # Bei Windows: venv\Scripts\activate

4. **Installieren Sie die Abhängigkeiten**<br />
pip install -r requirements.txt

5. **Konfigurieren Sie den Discord-Webhook**<br />
env muss erstellt werden mit dem Inhalt : `DISCORD_WEBHOOK_URL=discordwebhookurl`
6. **Starten Sie das Tool** <br />
python main.py