const { expect } = require("chai");
const { ethers } = require("hardhat");

describe("FormProofRegistry", function () {
  let registry;
  let owner;
  let user;
  let otherAccount;

  const submissionRef = "SUB-20260624-000001";
  const dataHash = "0x91b7f3c4a9c9f4e8e3a111111111111111111111111111111111111111111111";
  const differentHash = "0x81b7f3c4a9c9f4e8e3a111111111111111111111111111111111111111111111";

  beforeEach(async function () {
    [owner, user, otherAccount] = await ethers.getSigners();

    const FormProofRegistry = await ethers.getContractFactory("FormProofRegistry");
    registry = await FormProofRegistry.deploy();

    await registry.waitForDeployment();
  });

  it("should deploy with correct owner", async function () {
    expect(await registry.owner()).to.equal(owner.address);
  });

  it("should submit a proof", async function () {
    await expect(
      registry.submitProof(submissionRef, dataHash, user.address)
    ).to.emit(registry, "ProofSubmitted");

    const proof = await registry.getProof(submissionRef);

    expect(proof[0]).to.equal(submissionRef);
    expect(proof[1]).to.equal(dataHash);
    expect(proof[2]).to.equal(user.address);
    expect(proof[5]).to.equal(true);
    expect(proof[6]).to.equal(false);
  });

  it("should verify valid proof", async function () {
    await registry.submitProof(submissionRef, dataHash, user.address);

    const verified = await registry.verifyProof(submissionRef, dataHash);

    expect(verified).to.equal(true);
  });

  it("should reject invalid hash verification", async function () {
    await registry.submitProof(submissionRef, dataHash, user.address);

    const verified = await registry.verifyProof(submissionRef, differentHash);

    expect(verified).to.equal(false);
  });

  it("should prevent duplicate proof submission", async function () {
    await registry.submitProof(submissionRef, dataHash, user.address);

    await expect(
      registry.submitProof(submissionRef, dataHash, user.address)
    ).to.be.revertedWith("Proof already exists");
  });

  it("should allow owner to revoke proof", async function () {
    await registry.submitProof(submissionRef, dataHash, user.address);

    await expect(
      registry.revokeProof(submissionRef)
    ).to.emit(registry, "ProofRevoked");

    const verified = await registry.verifyProof(submissionRef, dataHash);

    expect(verified).to.equal(false);
  });

  it("should prevent non-owner from submitting proof", async function () {
    await expect(
      registry.connect(otherAccount).submitProof(submissionRef, dataHash, user.address)
    ).to.be.revertedWith("Only owner can perform this action");
  });

  it("should transfer ownership", async function () {
    await registry.transferOwnership(otherAccount.address);

    expect(await registry.owner()).to.equal(otherAccount.address);
  });
});