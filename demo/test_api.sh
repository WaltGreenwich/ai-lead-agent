#!/bin/bash

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

API_URL="http://localhost:8000"

echo -e "${YELLOW}🧪 Testing AI Lead Agent API${NC}\n"

# Test 1: Health Check
echo -e "${YELLOW}Test 1: Health Check${NC}"
curl -s $API_URL/health | python -m json.tool
echo -e "\n"

# Test 2: High-Quality Lead
echo -e "${YELLOW}Test 2: High-Quality Lead (Hot)${NC}"
curl -s -X POST $API_URL/leads \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Sarah Johnson",
    "email": "sarah@bigcorp.com",
    "company": "BigCorp Inc",
    "phone": "+1234567890",
    "website": "https://bigcorp.com",
    "message": "We urgently need a CRM solution for our 200-person sales team. We have budget approved for $100k and need to implement ASAP. Our current system is failing and costing us deals.",
    "source": "referral"
  }' | python -m json.tool
echo -e "\n"

# Test 3: Medium-Quality Lead
echo -e "${YELLOW}Test 3: Medium-Quality Lead (Warm)${NC}"
curl -s -X POST $API_URL/leads \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Mike Chen",
    "email": "mike@startup.io",
    "company": "Startup Inc",
    "message": "We are a small team looking into CRM options. We would like to schedule a demo sometime next month to see if it fits our needs.",
    "source": "web_form"
  }' | python -m json.tool
echo -e "\n"

# Test 4: Low-Quality Lead
echo -e "${YELLOW}Test 4: Low-Quality Lead (Cold)${NC}"
curl -s -X POST $API_URL/leads \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Bob Smith",
    "email": "bob@personal.com",
    "message": "Just browsing, maybe interested in learning more someday.",
    "source": "web_form"
  }' | python -m json.tool
echo -e "\n"

echo -e "${GREEN}✅ All tests completed!${NC}"