Discord bot to check stock of RTX3080 GPU

Bot checks every minute if any stock is available. Currently only setup to check Newegg.

Setup
1. Create env file or hard code the discord server name and token.
2. Text channel id and place text channel id in the applicable places in gpucheck.py.
3. Create a role called notify in the server.
4. Run bot. I used Heroku to deploy the bot, so the procfile and requirements.txt are included.
5. If a user responds to the bots text with a green checkmark emoji then the user will be added to the notify role.
6. If there is a card in stock then the bot will post a link the product page along with mentioning those in the notify role.
