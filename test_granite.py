from rag.granite_client import GraniteClient

client = GraniteClient()

response = client.generate("Explain what a Python function is.")

print("\n--- RESPONSE ---\n")
print(response)