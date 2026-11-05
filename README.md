# eCash (ECX) Drivechain Whale Index & Top 500 Post-Fork UTXO Rich List

An interactive, dark-mode financial terminal and rich list tracking the **500 largest post-fork active Unspent Transaction Outputs (UTXOs)** on the **eCash (ECX)** blockchain—the Bitcoin hard fork implementing **BIP-300** (Hashrate Escrows) and **BIP-301** (Blind Merged Mining) Drivechains spearheaded by LayerTwo Labs.

> **Note on Post-Fork Scope:** All dormant pre-fork Bitcoin coins have been removed. This index exclusively tracks coins that were **newly split** (via replay-protected coin splitters), **newly mined** (BIP-301 coinbase rewards), or **moved/consolidated post-fork** at block heights &ge; **#973,728**.

---

## ⚡ Network & Fork Snapshot Context

- **Network:** eCash (ECX) Mainnet
- **Consensus Layer:** Drivechains (BIP-300 & BIP-301)
- **Hard Fork Block Height:** `#973,728`
- **Snapshot Date:** October 31, 2026 (18th Anniversary of Bitcoin Whitepaper)
- **Scope:** 100% Post-Fork Active UTXOs (confirmed at blocks &ge; #973,728)
- **Explorers Integrated:**
  - `[1]` [explorer.ecash.com](https://explorer.ecash.com/) — Official eCash base layer explorer
  - `[2]` [explorer.blockfab.org](https://explorer.blockfab.org/) — BlockFab Drivechain & BIP-300/301 explorer
- **Top 500 Post-Fork Volume:** ~2,059,598 ECX (~10.41% of total circulating supply)
- **Sidechains Tracked:** SC#0 Thunder (High-speed payments), SC#1 zSide (ZK Privacy), SC#2 BitNames (DNS), SC#3 Truthcoin (Prediction Markets)

---

## 🚀 Deployment Guides

This project is a standalone, high-performance static web application requiring **no build steps, bundlers, or server dependencies**. It can be deployed in 1 click across GitHub Pages, Vercel, or Replit.

### Option 1: Deploy to GitHub Pages (Recommended)

1. Create a new repository on [GitHub](https://github.com/new) named `ecx-rich-list`.
2. Push this repository to GitHub:
   ```bash
   git add .
   git commit -m "Initial commit: ECX Drivechain Top 500 UTXO Rich List"
   git remote add origin https://github.com/<your-username>/ecx-rich-list.git
   git push -u origin main
   ```
3. In your GitHub repository:
   - Go to **Settings** &rarr; **Pages**.
   - Under **Build and deployment** &rarr; **Source**, select **GitHub Actions** (the included `.github/workflows/deploy.yml` will automatically build and publish).
   - Alternatively, choose **Deploy from a branch** &rarr; `main` &rarr; `/ (root)` and click **Save**.
4. Your site will be live at `https://<your-username>.github.io/ecx-rich-list/`!

---

### Option 2: Deploy to Vercel

#### Method A: Via Vercel Web Dashboard
1. Push your code to GitHub (or GitLab/Bitbucket).
2. Go to [Vercel](https://vercel.com/new).
3. Click **Import** on your `ecx-rich-list` repository.
4. Leave all build settings at default (`Framework: Other`, `Root Directory: ./`).
5. Click **Deploy**. Vercel will instantly publish your site with edge CDN routing configured by `vercel.json`.

#### Method B: Via Vercel CLI
Run from this directory:
```bash
npx vercel
```
Follow the interactive prompts to deploy directly.

---

### Option 3: Deploy & Run on Replit

1. Go to [Replit](https://replit.com/).
2. Click **Create Repl** &rarr; **Import from GitHub** &rarr; Enter your repo URL (or upload this directory).
3. The included `.replit` configuration automatically runs a lightweight web server on port `8080`:
   ```bash
   python3 -m http.server 8080
   ```
4. Click **Run**. Replit will open the rich list directly in the Webview panel.

---

## 💻 Local Preview & Development

You can run the site locally using any static HTTP server or open `index.html` directly in any web browser:

```bash
# Using Python
python3 -m http.server 8000

# Open in browser:
# http://localhost:8000
```

---

## 📊 Features & UI Architecture

- **Instant Search:** Fuzzy search across Address, TXID, Block Height, Rank, or Known Entity names (e.g. `Binance`, `Mt Gox`, `Silk Road`, `Coinbase`, `Taproot`).
- **Granular Filters:** Filter by Category (Exchange Cold Wallets, Institutional Custody, Dormant Whales, Protocol Reserves), Script Type (`P2WPKH`, `P2TR`, `P2SH`, `P2PKH`), or Size Tiers (Mega Whale >50k ECX down to Dolphins).
- **Sortable Columns:** Multi-directional sorting by Rank, Amount, Block Height, Script Type, and Entity.
- **Dynamic Price & Currency Toggle:** Real-time ECX/USD conversion toggle and interactive price slider ($10 - $1,000 USD).
- **Interactive Concentration Canvas Chart:** High-DPI Canvas visualization showing wealth distribution across the 500 UTXOs.
- **UTXO Inspector Modal:** Inspect raw ScriptPubKey hex, transaction hashes, confirmation timestamps, output indices (`vout`), and an interactive **BIP-300 Drivechain Peg-In Simulator** for sidechains.
- **Data Export:** Instant one-click export of the active or filtered UTXO dataset to formatted `.csv` or `.json`.
- **Zero-Dependency Resilience:** Dual-mode data loader supports both `fetch('data/utxos.json')` and local global fallback (`data/utxos.js`) to guarantee functionality even when opening locally without a web server.

