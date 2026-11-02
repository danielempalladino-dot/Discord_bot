# Discord Bot 🤖

A multi-functional Discord bot built with Python.

> **Status:** ⚠️ Still in active development. 

---

## 🚀 Features

- Core/essential Discord bot functionality
- Simple configuration and deployment

---
## What is coming

- Easily extensible modular design
- more advanced functionality
- resiter based stats of the server member to create a monthly database of the interests in the server
- implementation of AI and Machine learning using discord as a test envyroment

## ⚙️ Setup & Configuration

To run this bot, follow these quick setup steps:

1. **Create a Discord Application:**
   - Go to the [Discord Developer Portal](https://discord.com/developers/applications).
   - Click on **New Application** and give your bot a name.

2. **Configure Bot Permissions & Intents:**
   - In the Developer Portal, go to the **Bot** tab.
   - Enable the required **Privileged Gateway Intents** (e.g., Presence, Server Members, Message Content).
   - Under **OAuth2 > URL Generator**, select the `bot` scope and grant necessary permissions (e.g., *Administrator* for full access during testing).

3. **Get Your Bot Token:**
   - Copy your Bot Token from the **Bot** tab and put it in `config/config.json`:

     ```json
     {
       "credenziali": {
         "token": "YOUR_BOT_TOKEN",
         "CANALE_GENERALE": 123456789012345678,
         "ID_CANALE_ATTIVITA": 123456789012345678
       }
     }
     ```

   - Replace the example channel IDs with your Discord channel IDs. Keep the IDs as JSON numbers, and do not publish or commit the token.

---

## 📺 Helpful Resources

Need help setting up your bot on the Discord Developer Portal?  
Check out this step-by-step video guide:
- 🎬 [Discord Bot Setup Guide on YouTube](https://youtu.be/eiK34_asMRk?si=J1GpWFyZGEwJGA8E)

---

## 🛠️ Prerequisites & Installation

- **Python 3.8+** installed on your system.
- Required library: `discord.py`

*Hope to update this document soon!*