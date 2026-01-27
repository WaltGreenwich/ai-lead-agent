import requests

lead = {
    "name": "Sarah Conor",
    "email": "sarah@example.com",
    "phone": "+1234567890",
    "company": "Acme Corp",
    "website": "https://acme.com",
    "message": "We urgently need communicate a personal 24/7",
    "source": "web_form",
}

response = requests.post("http://localhost:5678/webhook-test/lead", json=lead)

print(response.json())
