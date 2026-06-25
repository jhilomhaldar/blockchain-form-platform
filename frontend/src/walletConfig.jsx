import { createAppKit } from "@reown/appkit/react";
import { WagmiProvider } from "wagmi";
import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import { WagmiAdapter } from "@reown/appkit-adapter-wagmi";
import { bscTestnet } from "@reown/appkit/networks";

const projectId = import.meta.env.VITE_REOWN_PROJECT_ID;

const metadata = {
  name: "Blockchain Form Platform",
  description: "Blockchain-powered form submission and proof verification platform.",
  url: "http://localhost:5173",
  icons: ["https://avatars.githubusercontent.com/u/9919?s=200&v=4"],
};

export const networks = [bscTestnet];

export const wagmiAdapter = new WagmiAdapter({
  networks,
  projectId,
});

export const queryClient = new QueryClient();

createAppKit({
  adapters: [wagmiAdapter],
  networks,
  projectId,
  metadata,
  features: {
    analytics: false,
  },
});

export function WalletProvider({ children }) {
  return (
    <WagmiProvider config={wagmiAdapter.wagmiConfig}>
      <QueryClientProvider client={queryClient}>{children}</QueryClientProvider>
    </WagmiProvider>
  );
}