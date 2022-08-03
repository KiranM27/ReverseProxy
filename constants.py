import os

DESTINATION_DOMAIN = "backend.treehopper.finance"
REVERSE_PROXY_HOST = "127.0.0.1"
REVERSE_PROXY_PORT = os.environ.get("PORT") or 8080