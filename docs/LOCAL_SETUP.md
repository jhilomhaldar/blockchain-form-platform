# Local Setup Guide

This guide explains how to set up and run the **Blockchain-Powered Form Submission Platform** on a local Windows machine.

The project contains:

```text
backend/           Django REST Framework backend
frontend/          React + Vite frontend
smart-contracts/   Solidity + Hardhat smart contract
docs/              Project documentation
```

The complete local flow is:

```text
React Frontend
→ Django REST API
→ PostgreSQL Database
→ SHA-256 Hash Generation
→ Local Hardhat Blockchain
→ Solidity Smart Contract Proof Registry
→ Verification API
```

---

## 1. Prerequisites

Install these tools before starting:

```text
Python 3.11+
Node.js 20+
npm
Git
PostgreSQL
Git Bash
VS Code
```

Recommended local versions used during development:

```text
Python: 3.13.x
Node.js: 22.x
npm: 11.x
PostgreSQL: 16 / 18
```

---

## 2. Clone the Repository

```bash
git clone git@github.com:jhilomhaldar/blockchain-form-platform.git
cd blockchain-form-platform
git checkout development
git pull origin development
```

Check status:

```bash
git status
```

Expected:

```text
On branch development
nothing to commit, working tree clean
```

---

## 3. PostgreSQL Setup

This project uses local PostgreSQL.

### 3.1 Check PostgreSQL

```bash
psql --version
pg_isready -h 127.0.0.1 -p 5432
```

If `psql` is not found, add PostgreSQL to Git Bash PATH.

For PostgreSQL 16:

```bash
export PATH="/c/Program Files/PostgreSQL/16/bin:$PATH"
echo 'export PATH="/c/Program Files/PostgreSQL/16/bin:$PATH"' >> ~/.bashrc
source ~/.bashrc
```

For PostgreSQL 18:

```bash
export PATH="/c/Program Files/PostgreSQL/18/bin:$PATH"
echo 'export PATH="/c/Program Files/PostgreSQL/18/bin:$PATH"' >> ~/.bashrc
source ~/.bashrc
```

Check again:

```bash
psql --version
pg_isready -h 127.0.0.1 -p 5432
```

Expected:

```text
127.0.0.1:5432 - accepting connections
```

### 3.2 Create Database

This guide assumes the local PostgreSQL username and password are:

```text
User: postgres
Password: postgres
Database: blockchain_forms
Host: 127.0.0.1
Port: 5432
```

Create the database:

```bash
PGPASSWORD=postgres psql -U postgres -h 127.0.0.1 -p 5432 -d postgres -c "CREATE DATABASE blockchain_forms;"
```

If the database already exists, the error can be ignored.

Check databases:

```bash
PGPASSWORD=postgres psql -U postgres -h 127.0.0.1 -p 5432 -d postgres -c "\l"
```

You should see:

```text
blockchain_forms
```

---

## 4. Backend Setup

Go to the backend folder:

```bash
cd backend
```

Create virtual environment:

```bash
python -m venv venv
```

Activate virtual environment:

```bash
source venv/Scripts/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Create backend `.env` file:

```bash
cat > .env <<'EOF'
DEBUG=True
SECRET_KEY=change-this-secret-key-later

DB_NAME=blockchain_forms
DB_USER=postgres
DB_PASSWORD=postgres
DB_HOST=127.0.0.1
DB_PORT=5432

CORS_ALLOWED_ORIGINS=http://localhost:5173

BLOCKCHAIN_ENABLED=True
BLOCKCHAIN_NETWORK=LOCAL_HARDHAT
BLOCKCHAIN_RPC_URL=http://127.0.0.1:8545
BLOCKCHAIN_CHAIN_ID=31337
CONTRACT_ADDRESS=PUT_LOCAL_CONTRACT_ADDRESS_HERE
BACKEND_WALLET_PRIVATE_KEY=0xac0974bec39a17e36ba4a6b4d238ff944bacb478cbed5efcae784d7bf4f2ff80
EOF
```

Run migrations:

```bash
python manage.py migrate
```

Create admin user:

```bash
winpty python manage.py createsuperuser
```

If `winpty` does not work, use PowerShell:

```powershell
cd E:\work\blockchain-form-platform\backend
.\venv\Scripts\activate
python manage.py createsuperuser
```

Do not start the backend yet. First deploy the smart contract and update the contract address in `.env`.

---

## 5. Smart Contract Setup

Open a new Git Bash terminal.

Go to the smart contract folder:

```bash
cd smart-contracts
```

Install dependencies:

```bash
npm install
```

Compile contract:

```bash
npm run compile
```

Run tests:

```bash
npm test
```

Expected result:

```text
8 passing
```

---

## 6. Start Local Hardhat Blockchain

In the smart contract terminal:

```bash
npm run node
```

Keep this terminal running.

This starts the local blockchain at:

```text
http://127.0.0.1:8545
```

Hardhat provides local test accounts and private keys. The project uses the first Hardhat account private key locally:

```text
0xac0974bec39a17e36ba4a6b4d238ff944bacb478cbed5efcae784d7bf4f2ff80
```

This private key is only for local Hardhat development.

Never use a real wallet private key in this project.

---

## 7. Deploy Smart Contract Locally

Open another Git Bash terminal.

Go to the smart contract folder:

```bash
cd smart-contracts
```

Deploy the contract:

```bash
npm run deploy:local
```

Expected output:

```text
FormProofRegistry deployed successfully.
Contract address: 0x...
Network: localhost
```

Copy the contract address.

Example:

```text
0x5FbDB2315678afecb367f032d93F642f64180aa3
```

---

## 8. Update Backend Contract Address

Open:

```text
backend/.env
```

Replace:

```env
CONTRACT_ADDRESS=PUT_LOCAL_CONTRACT_ADDRESS_HERE
```

with the deployed contract address:

```env
CONTRACT_ADDRESS=0xYourLocalContractAddressHere
```

Important:

Every time the Hardhat node is restarted, local blockchain state may reset. If that happens, deploy the contract again and update the backend `.env` contract address.

---

## 9. Run Django Backend

Open a backend terminal:

```bash
cd backend
source venv/Scripts/activate
python manage.py runserver
```

Backend runs at:

```text
http://127.0.0.1:8000
```

Useful backend URLs:

```text
Admin Panel:
http://127.0.0.1:8000/admin/

Forms API:
http://127.0.0.1:8000/api/forms/

Submission API:
http://127.0.0.1:8000/api/submissions/
```

The root URL `http://127.0.0.1:8000/` may show 404. That is normal because this backend currently exposes `/admin/` and `/api/`.

---

## 10. Seed Demo Form Template

Instead of manually creating the form from Django admin, run:

```bash
cd backend
source venv/Scripts/activate
python manage.py seed_demo_data
```

This creates:

```text
Contact Verification Form
Name field
Email field
Phone field
Message field
```

Now test the form API:

```text
http://127.0.0.1:8000/api/forms/contact-verification-form/
```

You should see the form template and fields in JSON format.

### Optional Manual Fallback

If the seed command is not available, create the form manually from Django admin.

Open:

```text
http://127.0.0.1:8000/admin/
```

Go to:

```text
Submissions → Form templates → Add
```

Create this form:

```text
Title: Contact Verification Form
Slug: contact-verification-form
Description: A sample blockchain-ready contact form for secure submission verification.
Status: ACTIVE
```

Add these form fields:

```text
Label: Name
Key: name
Field type: TEXT
Required: Yes
Sort order: 1
Active: Yes
```

```text
Label: Email
Key: email
Field type: EMAIL
Required: Yes
Sort order: 2
Active: Yes
```

```text
Label: Phone
Key: phone
Field type: PHONE
Required: No
Sort order: 3
Active: Yes
```

```text
Label: Message
Key: message
Field type: TEXTAREA
Required: No
Sort order: 4
Active: Yes
```

Save the form template.

---

## 11. Frontend Setup

Open a new Git Bash terminal.

Go to the frontend folder:

```bash
cd frontend
```

Install dependencies:

```bash
npm install
```

Create frontend `.env`:

```bash
cat > .env <<'EOF'
VITE_API_BASE_URL=http://127.0.0.1:8000/api
EOF
```

Run frontend:

```bash
npm run dev
```

Frontend runs at:

```text
http://localhost:5173
```

Open:

```text
http://localhost:5173/forms/contact-verification-form
```

---

## 12. Required Running Terminals

For the complete application to work, keep three terminals running.

### Terminal 1: Local Blockchain

```bash
cd smart-contracts
npm run node
```

### Terminal 2: Django Backend

```bash
cd backend
source venv/Scripts/activate
python manage.py runserver
```

### Terminal 3: React Frontend

```bash
cd frontend
npm run dev
```

---

## 13. Test Full Form Submission Flow

Open:

```text
http://localhost:5173/forms/contact-verification-form
```

Fill the form and submit.

Expected result:

```text
Submission Ref: SUB-...
Data Hash: 0x...
Blockchain Status: BLOCKCHAIN_CONFIRMED
Transaction Hash: 0x...
Blockchain Message: Proof stored on blockchain.
```

Then click:

```text
Verify this submission
```

Expected verification result:

```text
Verified Successfully
Database Verified: true
Blockchain Verified: true
Final Verification: true
```

---

## 14. API Testing

### Get Form

```http
GET http://127.0.0.1:8000/api/forms/contact-verification-form/
```

### Submit Form

```http
POST http://127.0.0.1:8000/api/submissions/
Content-Type: application/json
```

Request body:

```json
{
  "form_slug": "contact-verification-form",
  "wallet_address": "0x1234567890abcdef1234567890abcdef12345678",
  "submitted_data": {
    "name": "Jhilom Haldar",
    "email": "test@example.com",
    "phone": "9007068919",
    "message": "This is a blockchain verified form submission."
  }
}
```

### Verify Submission

```http
GET http://127.0.0.1:8000/api/submissions/SUB-YYYYMMDD-000001/verify/
```

Replace `SUB-YYYYMMDD-000001` with the actual submission reference.

---

## 15. Troubleshooting

### `psql: command not found`

Add PostgreSQL bin folder to Git Bash PATH.

For PostgreSQL 18:

```bash
export PATH="/c/Program Files/PostgreSQL/18/bin:$PATH"
```

For PostgreSQL 16:

```bash
export PATH="/c/Program Files/PostgreSQL/16/bin:$PATH"
```

### PostgreSQL password failed

Make sure the backend `.env` uses the correct local PostgreSQL password.

Default expected by this guide:

```env
DB_PASSWORD=postgres
```

If you forgot the local PostgreSQL password, reset it locally and update the `.env` file.

### `Unable to connect to blockchain RPC`

Make sure Hardhat node is running:

```bash
cd smart-contracts
npm run node
```

### Blockchain transaction failed

Check:

```text
1. Hardhat node is running.
2. Smart contract is deployed.
3. backend/.env has the correct CONTRACT_ADDRESS.
4. Django backend was restarted after changing .env.
5. BACKEND_WALLET_PRIVATE_KEY is the first Hardhat account private key.
```

### Frontend cannot load form

Check:

```text
1. Django backend is running.
2. Demo data was seeded using python manage.py seed_demo_data.
3. Form slug is exactly contact-verification-form.
4. frontend/.env has VITE_API_BASE_URL=http://127.0.0.1:8000/api.
5. CORS_ALLOWED_ORIGINS=http://localhost:5173 exists in backend/.env.
```

### Django admin CSS looks broken

Run:

```bash
python manage.py collectstatic
```

Then restart backend and hard refresh browser:

```text
CTRL + F5
```

---

## 16. Files Not Committed to GitHub

The following files and folders are intentionally ignored and must be created locally:

```text
backend/.env
backend/venv/
frontend/.env
frontend/node_modules/
smart-contracts/node_modules/
smart-contracts/cache/
smart-contracts/artifacts/
```

Never commit private keys, real wallet secrets, `.env`, or local virtual environments.

---

## 17. Current Local Development Stack

```text
Frontend: React + Vite
Backend: Django REST Framework
Database: PostgreSQL
Blockchain: Local Hardhat Network
Smart Contract: Solidity FormProofRegistry
Wallet: Demo wallet address currently
Future Wallet Support: WalletConnect + Trust Wallet
```

---

## 18. Future Improvements

Planned improvements:

```text
1. WalletConnect integration
2. Trust Wallet support
3. BSC Testnet deployment
4. Frontend dashboard for submissions
5. Public verification certificate page
6. Screenshots in README
7. Production deployment documentation
8. GitHub Actions workflow
```
