// SPDX-License-Identifier: MIT
pragma solidity ^0.8.24;

contract FormProofRegistry {
    address public owner;

    struct FormProof {
        string submissionRef;
        bytes32 dataHash;
        address submitterWallet;
        address recordedBy;
        uint256 createdAt;
        bool exists;
        bool revoked;
    }

    mapping(bytes32 => FormProof) private proofs;

    event ProofSubmitted(
        string indexed submissionRef,
        bytes32 indexed submissionKey,
        bytes32 dataHash,
        address indexed submitterWallet,
        address recordedBy,
        uint256 createdAt
    );

    event ProofRevoked(
        string indexed submissionRef,
        bytes32 indexed submissionKey,
        address indexed revokedBy,
        uint256 revokedAt
    );

    event OwnershipTransferred(
        address indexed previousOwner,
        address indexed newOwner
    );

    modifier onlyOwner() {
        require(msg.sender == owner, "Only owner can perform this action");
        _;
    }

    constructor() {
        owner = msg.sender;
        emit OwnershipTransferred(address(0), msg.sender);
    }

    function generateSubmissionKey(
        string memory submissionRef
    ) public pure returns (bytes32) {
        return keccak256(abi.encodePacked(submissionRef));
    }

    function submitProof(
        string memory submissionRef,
        bytes32 dataHash,
        address submitterWallet
    ) external onlyOwner returns (bool) {
        require(bytes(submissionRef).length > 0, "Submission reference is required");
        require(dataHash != bytes32(0), "Data hash is required");
        require(submitterWallet != address(0), "Submitter wallet is required");

        bytes32 submissionKey = generateSubmissionKey(submissionRef);

        require(!proofs[submissionKey].exists, "Proof already exists");

        proofs[submissionKey] = FormProof({
            submissionRef: submissionRef,
            dataHash: dataHash,
            submitterWallet: submitterWallet,
            recordedBy: msg.sender,
            createdAt: block.timestamp,
            exists: true,
            revoked: false
        });

        emit ProofSubmitted(
            submissionRef,
            submissionKey,
            dataHash,
            submitterWallet,
            msg.sender,
            block.timestamp
        );

        return true;
    }

    function verifyProof(
        string memory submissionRef,
        bytes32 dataHash
    ) external view returns (bool) {
        bytes32 submissionKey = generateSubmissionKey(submissionRef);
        FormProof memory proof = proofs[submissionKey];

        if (!proof.exists || proof.revoked) {
            return false;
        }

        return proof.dataHash == dataHash;
    }

    function getProof(
        string memory submissionRef
    )
        external
        view
        returns (
            string memory storedSubmissionRef,
            bytes32 dataHash,
            address submitterWallet,
            address recordedBy,
            uint256 createdAt,
            bool exists,
            bool revoked
        )
    {
        bytes32 submissionKey = generateSubmissionKey(submissionRef);
        FormProof memory proof = proofs[submissionKey];

        return (
            proof.submissionRef,
            proof.dataHash,
            proof.submitterWallet,
            proof.recordedBy,
            proof.createdAt,
            proof.exists,
            proof.revoked
        );
    }

    function revokeProof(
        string memory submissionRef
    ) external onlyOwner returns (bool) {
        bytes32 submissionKey = generateSubmissionKey(submissionRef);

        require(proofs[submissionKey].exists, "Proof does not exist");
        require(!proofs[submissionKey].revoked, "Proof already revoked");

        proofs[submissionKey].revoked = true;

        emit ProofRevoked(
            submissionRef,
            submissionKey,
            msg.sender,
            block.timestamp
        );

        return true;
    }

    function transferOwnership(address newOwner) external onlyOwner {
        require(newOwner != address(0), "New owner cannot be zero address");

        address previousOwner = owner;
        owner = newOwner;

        emit OwnershipTransferred(previousOwner, newOwner);
    }
}