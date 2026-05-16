from rag.granite_client import GraniteClient

client = GraniteClient()

response = client.generate("What is CSS")

print("\n--- RESPONSE ---\n")
print(response)