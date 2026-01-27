# n8n Workflow Setup Guide

## 🎯 Objetivo

Automatizar la calificación de leads y enviar notificaciones para leads de alta prioridad.

## 🚀 Inicio Rápido

### 1. Levantar n8n

```bash
docker-compose up -d n8n
```

### 2. Acceder a n8n

- URL: http://localhost:5678
- Usuario: `admin`
- Contraseña: `admin123`
- Email: `test@test.com`

### 3. Importar Workflow

1. Abre n8n en tu navegador
2. Click en "+" para crear nuevo workflow
3. Click en el menú (tres puntos) → "Import from File"
4. Selecciona `n8n/workflows/Lead_Qualification.json`
5. Click en "Save" y "Publish" (toggle en la esquina superior derecha)

## 📊 Cómo funciona el Workflow

```
┌─────────────────┐
│  Webhook        │  ← Recibe lead desde formulario web
│  /lead-webhook  │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  HTTP Request   │  ← Llama a tu API FastAPI
│  POST /leads    │     http://backend:8000/leads
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  IF Node        │  ← ¿Es lead HOT?
│  Priority=hot?  │
└────┬────────┬───┘
     │        │
     │ YES    │ NO
     │        │
     ▼        ▼
┌─────────┐  ┌──────────┐
│ Send    │  │ Normal   │
│ Alert   │  │ Response │
│ 🔥      │  │          │
└─────────┘  └──────────┘
```

## 🔗 Webhook URL

Una vez activado el workflow, obtendrás una URL como:

```
http://localhost:5678/webhook-test/lead
```

O en producción:

```
https://tu-dominio.com/webhook/lead-webhook
```

## 📝 Ejemplo de Uso

### Enviar lead al webhook:

```bash
curl -X POST http://localhost:5678/webhook-test/lead \
  -H "Content-Type: application/json" \
  -d '{
    "name": "John Doe",
    "email": "john@example.com",
    "phone": "+1234567890",
    "company": "Acme Corp",
    "website": "https://acme.com",
    "message": "We urgently need a CRM solution for our 100-person sales team. Budget is approved at $75k and we need to implement ASAP within the next month.",
    "source": "web_form"
  }'
```

y/o

```bash
curl -X POST http://localhost:5678/webhook-test/lead \
  -H "Content-Type: application/json" \
  -d '{
  "name": "Sarah Johnson",
  "email": "sarah@bigcorp.com",
  "phone": "+1234567890",
  "company": "BigCorp Inc",
  "website": "https://bigcorp.com",
  "message": "We urgently need a CRM solution for our 200-person sales team. Budget approved at $100k and need to implement ASAP.",
  "source": "referral"
}'
```

### Respuesta esperada:

```json
{
  "success": true,
  "message": "HOT lead - immediate action required!",
  "lead_id": "recXXXXXXXXXXXXXX",
  "score": 85.5
}
```

## 🎨 Personalización

### Agregar notificaciones por Email

1. Agrega un nodo "Send Email"
2. Conéctalo después del nodo "Is HOT Lead?" (ruta TRUE)
3. Configura:
   - To: `sales@tuempresa.com`
   - Subject: `🔥 HOT Lead: {{ $json.qualified_lead.name }}`
   - Body: Usa el texto del nodo "Format Notification"

### Agregar Slack

1. Agrega un nodo "Slack"
2. Configura tu webhook de Slack
3. Conecta después del nodo "Is HOT Lead?"
4. Mensaje: Usa el formato del nodo "Format Notification"

### Agregar SMS (Twilio)

1. Agrega un nodo "Twilio"
2. Configura tus credenciales
3. Solo para leads HOT con score > 90

## 🔧 Configuración Avanzada

### Variables de Entorno

En `docker-compose.yml`:

```yaml
environment:
  - N8N_BASIC_AUTH_USER=tu_usuario
  - N8N_BASIC_AUTH_PASSWORD=tu_password_seguro
  - WEBHOOK_URL=https://tu-dominio.com/
```

### Webhook en Producción

1. Configura un dominio
2. Usa HTTPS
3. Agrega autenticación al webhook (Header API Key)
4. Usa rate limiting

## 📊 Casos de Uso

### 1. Lead desde Landing Page

```
Landing Page Form → n8n Webhook → API → Airtable → Email Alert
```

### 2. Lead desde Facebook Ads

```
Facebook Lead Ad → n8n Webhook → API → Airtable → Slack + Email
```

### 3. Lead desde Chat

```
Chatbot → n8n Webhook → API → Airtable → Assign to Sales Rep
```

## 🐛 Troubleshooting

### Webhook no responde

```bash
# Ver logs de n8n
docker-compose logs -f n8n

# Verificar que n8n esté corriendo
docker-compose ps
```

### Error al llamar a la API

- Verifica que el backend esté corriendo
- URL debe ser `http://backend:8000` (nombre del servicio en Docker)
- No uses `localhost` dentro del workflow

### Workflow no se activa

- Click en el toggle "Active" ("Save")en la esquina superior derecha y luego en "Publish"
- Verifica que no haya errores en los nodos (ícono rojo)

## 📚 Recursos

- [Documentación n8n](https://docs.n8n.io/)
- [n8n Community](https://community.n8n.io/)
- [Webhook Node Docs](https://docs.n8n.io/integrations/builtin/core-nodes/n8n-nodes-base.webhook/)
