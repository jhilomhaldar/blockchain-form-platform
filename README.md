# Blockchain-Powered Form Submission Platform

A local-first full-stack blockchain-powered form submission and verification platform built with **Python, Django REST Framework, PostgreSQL, React, Solidity, Hardhat, and Web3.py**.

This project demonstrates how traditional web applications can be combined with blockchain-based proof storage to make form submissions tamper-verifiable.

---

## Project Purpose

Traditional form submissions are stored only in centralized databases. If a record is modified later, it can be difficult to prove what the original submitted data was.

This project solves that problem by storing the actual submitted data in PostgreSQL and storing only a cryptographic proof of that data on a blockchain smart contract.

The submitted data remains private in the database, while the blockchain stores a tamper-proof hash that can be used for future verification.

---

## Current Project Status

This project currently runs fully on a local Windows development machine.

Current working flow:

```text
React Frontend
→ Django REST API
→ PostgreSQL Database
→ SHA-256 Hash Generation
→ Local Hardhat Blockchain
→ Solidity Smart Contract
→ Blockchain Verification API
```

Deployment to AWS, BSC Testnet, WalletConnect, and Trust Wallet integration are planned future phases.

---

## Key Features

* Dynamic form template management from Django admin
* Form field management
* Public form submission from React frontend
* PostgreSQL-based form data storage
* SHA-256 hash generation for submitted data
* Solidity smart contract for proof registration
* Local Hardhat blockchain integration
* Web3.py-based backend blockchain transaction handling
* Blockchain transaction hash storage
* Submission verification API
* React verification page
* Jazzmin-powered Django admin interface
* Demo data seed command for easy local setup
* Full local setup documentation for recruiters and developers

---

## Technology Stack

### Backend

* Python
* Django
* Django REST Framework
* PostgreSQL
* Web3.py
* Django Jazzmin Admin
* python-decouple
* django-cors-headers

### Frontend

* React
* Vite
* Axios
* React Router DOM

### Blockchain

* Solidity
* Hardhat
* Local Hardhat Network
* ethers.js
* Web3.py

### Database

* PostgreSQL local database

---

## Architecture

```text
User Browser
    |
    v
React Frontend
    |
    v
Django REST API
    |
    v
PostgreSQL Database
    |
    v
SHA-256 Hash Service
    |
    v
Web3.py Blockchain Service
    |
    v
Solidity Smart Contract on Local Hardhat Blockchain
```

---

## How the Blockchain Proof Works

The platform does not store full form data on the blockchain.

Instead:

1. User submits form data.
2. Django validates and stores the submitted data in PostgreSQL.
3. Django normalizes the submitted JSON data.
4. Django generates a SHA-256 hash.
5. Django sends the submission reference, hash, and wallet address to the Solidity smart contract.
6. The smart contract stores the proof on the local blockchain.
7. The transaction hash is saved in PostgreSQL.
8. Later, the submission can be verified by comparing the database hash with the blockchain proof.

Example:

```text
Submitted Data
→ Normalized JSON
→ SHA-256 Hash
→ Smart Contract Proof
→ Verification Result
```

---

## Why Only Hashes Are Stored On-Chain

The platform stores only hashes on-chain because:

* Blockchain data is public.
* Sensitive form data should not be publicly exposed.
* On-chain storage is expensive.
* Blockchain data is difficult to delete.
* Privacy-friendly architecture is better for real-world applications.

Actual form data stays in PostgreSQL.

Blockchain stores only the proof.

---

## Project Structure

```text
blockchain-form-platform/
│
├── backend/
│   ├── blockchain_form/
│   ├── submissions/
│   ├── manage.py
│   └── requirements.txt
│
├── frontend/
│   ├── src/
│   ├── package.json
│   └── vite.config.js
│
├── smart-contracts/
│   ├── contracts/
│   ├── scripts/
│   ├── test/
│   ├── hardhat.config.js
│   └── package.json
│
├── docs/
│   └── LOCAL_SETUP.md
│
├── screenshots/
│
├── README.md
└── .gitignore
```

---

## Smart Contract

The main Solidity contract is:

```text
smart-contracts/contracts/FormProofRegistry.sol
```

Main functions:

```solidity
submitProof(string submissionRef, bytes32 dataHash, address submitterWallet)
verifyProof(string submissionRef, bytes32 dataHash)
getProof(string submissionRef)
revokeProof(string submissionRef)
```

The contract stores:

```text
submission reference
data hash
submitter wallet
recorded by address
created timestamp
revoked status
```

---

## Backend APIs

### Get Form

```http
GET /api/forms/contact-verification-form/
```

### Submit Form

```http
POST /api/submissions/
```

Example request:

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
GET /api/submissions/{submission_ref}/verify/
```

---

## Local Setup

Full local setup instructions are available here:

```text
docs/LOCAL_SETUP.md
```

Quick local run summary:

```bash
# Terminal 1: Local blockchain
cd smart-contracts
npm run node
```

```bash
# Terminal 2: Django backend
cd backend
source venv/Scripts/activate
python manage.py runserver
```

```bash
# Terminal 3: React frontend
cd frontend
npm run dev
```

Frontend URL:

```text
http://localhost:5173/forms/contact-verification-form
```

Backend admin URL:

```text
http://127.0.0.1:8000/admin/
```

---

## Demo Data

The project includes a Django management command to seed demo form data:

```bash
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

---

## Testing

### Smart Contract Tests

```bash
cd smart-contracts
npm test
```

Expected result:

```text
8 passing
```

### Backend

Run Django backend:

```bash
cd backend
source venv/Scripts/activate
python manage.py runserver
```

### Frontend

Run React frontend:

```bash
cd frontend
npm run dev
```

Then submit and verify a form using the browser.

---

## Security Design

Security-focused decisions in this project:

* Full form data is not stored on-chain.
* Only cryptographic hashes are stored on-chain.
* Backend secrets are stored in `.env`.
* `.env` files are ignored by Git.
* Local Hardhat private key is used only for development.
* Real wallet private keys must never be committed.
* PostgreSQL stores the actual private submission data.
* Verification checks both database hash and blockchain proof.

---

## Files Not Committed

These files and folders are intentionally ignored:

```text
backend/.env
backend/venv/
frontend/.env
frontend/node_modules/
smart-contracts/node_modules/
smart-contracts/cache/
smart-contracts/artifacts/
```

---

## Current Limitations

This is currently a local-first portfolio project.

Current limitations:

* WalletConnect is not integrated yet.
* Trust Wallet support is planned.
* BSC Testnet deployment is planned.
* Production deployment is not configured yet.
* Public verification certificate page is planned.

---

## Roadmap

Planned future improvements:

```text
1. WalletConnect integration
2. Trust Wallet support
3. BSC Testnet deployment
4. Binance Smart Chain mainnet-ready configuration
5. Public verification certificate page
6. Frontend submission dashboard
7. Admin analytics dashboard
8. Docker setup
9. GitHub Actions workflow
10. Production deployment guide
```

---

## Author

**Jhilom Haldar**

SaaS & Cloud Solution Architect
Full Stack Platform Engineer
AI Automation Builder

---

## License

This project is intended for portfolio, learning, and demonstration purposes.

Recommended license:

```text
MIT License
```
