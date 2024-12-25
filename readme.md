# Windows Event Logger mit Discord-Benachrichtigungen

## Überblick
Dieser Windows Event Logger liest Sicherheitsereignisse aus den Windows-Ereignisprotokollen und sendet diese in Echtzeit an einen Discord-Kanal über einen Webhook. Das Tool ermöglicht es, kritische Ereignisse wie Benutzererstellung, Benutzerlöschung, RDP-Verbindungen und andere sicherheitsrelevante Aktionen zu überwachen.

## Funktionen
- 🔑 Echtzeitüberwachung von Windows-Sicherheitsereignissen
- 🔗 Integration mit Discord über Webhook
- ❌ Duplikatüberprüfung innerhalb eines definierten Zeitfensters
- 🔧 Anpassbare Ereignistypen und Nachrichtenfarben

## Voraussetzungen
1. **Python 3.9 oder höher**
2. **Pip-Pakete:**
   - `pywin32`
   - `requests`
   - `python-dotenv`
3. Eine gültige Discord-Webhook-URL

.env muss erstellt werden mit dem Inhalt : DISCORD_WEBHOOK_URL=https://discord.com/api/webhooks/xxxx