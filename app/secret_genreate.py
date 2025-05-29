# this is to set secret key in .env file
import secrets
print(secrets.token_urlsafe(32))