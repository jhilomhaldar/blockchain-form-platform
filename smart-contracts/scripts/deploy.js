const hre = require("hardhat");

async function main() {
  console.log("Deploying FormProofRegistry contract...");

  const FormProofRegistry = await hre.ethers.getContractFactory("FormProofRegistry");
  const formProofRegistry = await FormProofRegistry.deploy();

  await formProofRegistry.waitForDeployment();

  const contractAddress = await formProofRegistry.getAddress();

  console.log("FormProofRegistry deployed successfully.");
  console.log("Contract address:", contractAddress);
  console.log("Network:", hre.network.name);
}

main().catch((error) => {
  console.error(error);
  process.exitCode = 1;
});
