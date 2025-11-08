import webbrowser
from requests_oauthlib import OAuth2Session
from solid_client import config

def authenticate():
    print("Starting Solid OIDC authentication...")

    discovery_url = f"{config.SOLID_ISSUER}/.well-known/openid-configuration"
    solid = OAuth2Session(config.CLIENT_ID, redirect_uri=config.REDIRECT_URI, scope=["openid", "profile", "offline_access"])

    # Step 1: Authorization
    authorization_url, state = solid.authorization_url(
        f"{config.SOLID_ISSUER}/authorize",
        access_type="offline",
        prompt="consent"
    )
    print(f"Open this URL in your browser to authenticate:\n{authorization_url}")
    webbrowser.open(authorization_url)

    # Step 2: Get authorization response manually
    redirect_response = input("Paste the full callback URL after authorization:\n")

    # Step 3: Exchange for token
    token = solid.fetch_token(
        token_url=f"{config.SOLID_ISSUER}/token",
        authorization_response=redirect_response,
        client_secret=config.CLIENT_SECRET
    )

    print("\n✅ Authentication successful!")
    print(f"Access token: {token['access_token'][:40]}...")
    return token
