from solid_client.auth import authenticate
from solid_client.client import SolidPodClient

# Step 1: Authenticate and get token
token = authenticate()
access_token = token["access_token"]

# Step 2: Initialize client
username = input("Enter your Solid username (the part before '.solidcommunity.net'): ")
base_url = f"https://{username}.solidcommunity.net"

client = SolidPodClient(base_url, access_token)

# Step 3: Example CRUD operations
print("\n--- Creating RDF resource ---")
data = """
@prefix schema: <http://schema.org/> .
<> a schema:Event ;
   schema:name "Cully Community Meeting" ;
   schema:startDate "2025-11-10" .
"""
client.create("public/test/event.ttl", data)
print("✅ Resource created.")

print("\n--- Reading RDF resource ---")
graph = client.read("public/test/event.ttl")
for s, p, o in graph:
    print(s, p, o)

print("\n--- Deleting resource ---")
client.delete("public/test/event.ttl")
print("✅ Resource deleted.")
