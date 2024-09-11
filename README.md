# VOCODE Python app.

A voice powered programming assistant that uses AI to write software using voice commands.

### ADDITIONAL SETUP REQS:
Get docker working for server so we can ez deploy
DO NOT HARDCODE URL'S!
We will create global variables or a .env for urls so we never accidentally push a localhost end point to prod.
There is a bug in app/vocode.py `listen_command`, I need to figure that out.