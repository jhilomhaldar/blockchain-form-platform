import { useAppKit, useAppKitAccount } from "@reown/appkit/react";

function WalletConnectButton({ onWalletChange }) {
  const { open } = useAppKit();
  const { address, isConnected } = useAppKitAccount();

  if (address && onWalletChange) {
    onWalletChange(address);
  }

  return (
    <div className="wallet-box">
      <button type="button" className="wallet-button" onClick={() => open()}>
        {isConnected ? "Change Wallet" : "Connect Trust Wallet / WalletConnect"}
      </button>

      {isConnected && address && (
        <div className="wallet-connected">
          <strong>Connected Wallet</strong>
          <span>{address}</span>
        </div>
      )}

      {!isConnected && (
        <small>
          Connect with Trust Wallet or any WalletConnect-supported EVM wallet.
        </small>
      )}
    </div>
  );
}

export default WalletConnectButton;