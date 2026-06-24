import json
from pathlib import Path

from decouple import config
from django.utils import timezone
from web3 import Web3
from eth_account import Account

from submissions.models import BlockchainTransaction


BASE_DIR = Path(__file__).resolve().parent.parent


def blockchain_enabled():
    return config("BLOCKCHAIN_ENABLED", default=False, cast=bool)


def get_web3():
    rpc_url = config("BLOCKCHAIN_RPC_URL", default="http://127.0.0.1:8545")
    return Web3(Web3.HTTPProvider(rpc_url))


def get_contract_abi():
    abi_path = BASE_DIR / "contracts" / "FormProofRegistryABI.json"

    with open(abi_path, "r", encoding="utf-8") as abi_file:
        return json.load(abi_file)


def get_contract(web3):
    contract_address = config("CONTRACT_ADDRESS")
    checksum_address = web3.to_checksum_address(contract_address)
    abi = get_contract_abi()

    return web3.eth.contract(
        address=checksum_address,
        abi=abi
    )


def get_backend_account():
    private_key = config("BACKEND_WALLET_PRIVATE_KEY")
    return Account.from_key(private_key)


def normalize_wallet_address(web3, wallet_address, fallback_address):
    if not wallet_address:
        return fallback_address

    try:
        return web3.to_checksum_address(wallet_address)
    except Exception:
        return fallback_address


def submit_proof_to_blockchain(submission):
    """
    Stores submission proof on local Hardhat blockchain.

    This function:
    - connects to local blockchain
    - calls submitProof on FormProofRegistry contract
    - waits for transaction confirmation
    - updates FormSubmission and BlockchainTransaction records
    """

    if not blockchain_enabled():
        return {
            "enabled": False,
            "success": False,
            "message": "Blockchain is disabled."
        }

    try:
        web3 = get_web3()

        if not web3.is_connected():
            raise Exception("Unable to connect to blockchain RPC.")

        account = get_backend_account()
        contract = get_contract(web3)

        submitter_wallet = normalize_wallet_address(
            web3=web3,
            wallet_address=submission.wallet_address,
            fallback_address=account.address,
        )

        chain_id = config("BLOCKCHAIN_CHAIN_ID", default=31337, cast=int)
        network = config("BLOCKCHAIN_NETWORK", default="LOCAL_HARDHAT")
        contract_address = config("CONTRACT_ADDRESS")

        nonce = web3.eth.get_transaction_count(account.address)

        transaction = contract.functions.submitProof(
            submission.submission_ref,
            submission.data_hash,
            submitter_wallet
        ).build_transaction({
            "from": account.address,
            "nonce": nonce,
            "chainId": chain_id,
            "gas": 500000,
            "gasPrice": web3.eth.gas_price,
        })

        signed_txn = web3.eth.account.sign_transaction(
            transaction,
            private_key=config("BACKEND_WALLET_PRIVATE_KEY")
        )

        raw_transaction = getattr(signed_txn, "raw_transaction", None)

        if raw_transaction is None:
            raw_transaction = signed_txn.rawTransaction

        tx_hash = web3.eth.send_raw_transaction(raw_transaction)
        tx_hash_hex = web3.to_hex(tx_hash)

        receipt = web3.eth.wait_for_transaction_receipt(tx_hash, timeout=120)

        is_success = receipt.status == 1

        submission.blockchain_tx_hash = tx_hash_hex
        submission.blockchain_status = "BLOCKCHAIN_CONFIRMED" if is_success else "FAILED"
        submission.status = "BLOCKCHAIN_CONFIRMED" if is_success else "FAILED"
        submission.save(update_fields=[
            "blockchain_tx_hash",
            "blockchain_status",
            "status",
            "updated_at",
        ])

        BlockchainTransaction.objects.update_or_create(
            submission=submission,
            defaults={
                "network": network,
                "contract_address": contract_address,
                "tx_hash": tx_hash_hex,
                "block_number": receipt.blockNumber,
                "gas_used": receipt.gasUsed,
                "status": "CONFIRMED" if is_success else "FAILED",
                "confirmed_at": timezone.now() if is_success else None,
                "error_message": None if is_success else "Transaction failed on-chain.",
            }
        )

        return {
            "enabled": True,
            "success": is_success,
            "tx_hash": tx_hash_hex,
            "block_number": receipt.blockNumber,
            "gas_used": receipt.gasUsed,
            "message": "Proof stored on blockchain." if is_success else "Blockchain transaction failed."
        }

    except Exception as e:
        submission.blockchain_status = "FAILED"
        submission.status = "FAILED"
        submission.save(update_fields=[
            "blockchain_status",
            "status",
            "updated_at",
        ])

        BlockchainTransaction.objects.update_or_create(
            submission=submission,
            defaults={
                "network": config("BLOCKCHAIN_NETWORK", default="LOCAL_HARDHAT"),
                "contract_address": config("CONTRACT_ADDRESS", default=""),
                "status": "FAILED",
                "error_message": str(e),
            }
        )

        return {
            "enabled": True,
            "success": False,
            "message": str(e)
        }


def verify_proof_on_blockchain(submission):
    """
    Verifies whether database hash matches blockchain stored hash.
    """

    if not blockchain_enabled():
        return {
            "enabled": False,
            "success": False,
            "verified": False,
            "message": "Blockchain is disabled."
        }

    try:
        web3 = get_web3()

        if not web3.is_connected():
            raise Exception("Unable to connect to blockchain RPC.")

        contract = get_contract(web3)

        verified = contract.functions.verifyProof(
            submission.submission_ref,
            submission.data_hash
        ).call()

        proof = contract.functions.getProof(
            submission.submission_ref
        ).call()

        blockchain_hash = web3.to_hex(proof[1]) if proof[1] else None

        return {
            "enabled": True,
            "success": True,
            "verified": verified,
            "blockchain_hash": blockchain_hash,
            "submitter_wallet": proof[2],
            "recorded_by": proof[3],
            "created_at": int(proof[4]),
            "exists": proof[5],
            "revoked": proof[6],
            "message": "Blockchain verification completed."
        }

    except Exception as e:
        return {
            "enabled": True,
            "success": False,
            "verified": False,
            "message": str(e)
        }