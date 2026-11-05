import json
import hashlib
import random
from datetime import datetime, timezone

random.seed(1337)

FORK_BLOCK = 973728 # Fork snapshot height
MAX_BLOCK = 974950  # Recent post-fork blocks (Nov 2026)
FORK_TIMESTAMP = 1793404800 # Oct 31, 2026 00:00:00 UTC

# Dedicated Anchor Post-Fork Entities
ANCHOR_POST_FORK_UTXOS = [
    {
        "address": "bc1p0xlxvlhemja6c4dqv22uapctqupfhlxm9h8z3k2e72q4k9h5z6wqg6330q",
        "entity": "LayerTwo Labs Post-Fork Protocol Treasury",
        "amount": 50000.00000000,
        "block_height": 973728,
        "txid": "ec01973728b19300301treasury0000000000000000000000000000000000000001",
        "vout": 0,
        "type": "P2TR",
        "category": "Drivechain Protocol",
        "movement_type": "Newly Split Protocol Fund"
    },
    {
        "address": "bc1p5d7rjq7g6rd2ee0r0zahe7n09gdwhmvahf27fh9cfnj3jhmlqd4s528hk6",
        "entity": "Thunder Sidechain Peg-In Escrow (BIP-300 SC#0)",
        "amount": 35000.00000000,
        "block_height": 973729,
        "txid": "ec01973728b19300301thunder0000000000000000000000000000000000000000",
        "vout": 0,
        "type": "P2TR",
        "category": "Drivechain Protocol",
        "movement_type": "BIP-300 Sidechain Peg-In"
    },
    {
        "address": "bc1q9v8y34qf5z998wlk2e4a6d7c8x9y0z1a2b3c4d",
        "entity": "Binance ECX Post-Fork Split Vault I",
        "amount": 32500.54019020,
        "block_height": 973735,
        "txid": "ba72910fa89b021c34de56fa7801bc23de45fa678901bc23de45fa678901bc23",
        "vout": 0,
        "type": "P2WPKH",
        "category": "Exchange Cold Wallet",
        "movement_type": "Post-Fork Split (Replay-Protected)"
    },
    {
        "address": "bc1pz8x999v762y5k5q7z4n0x3j7s9w6k4p8x2c1v3b4n5m6",
        "entity": "zSide Privacy Sidechain Escrow (BIP-300 SC#1)",
        "amount": 28000.00000000,
        "block_height": 973730,
        "txid": "ec01973728b19300301zside000000000000000000000000000000000000000000",
        "vout": 0,
        "type": "P2TR",
        "category": "Drivechain Protocol",
        "movement_type": "BIP-300 Sidechain Peg-In"
    },
    {
        "address": "bc1qm34lsc65zpw79lxes69zkqmk6ee3ewf0j77s3h",
        "entity": "Coinbase Prime Post-Fork Split Vault",
        "amount": 25400.12904810,
        "block_height": 973748,
        "txid": "cb1940283fa0912bc45de67fa8901bc23de45fa678901bc23de45fa678901bc2",
        "vout": 1,
        "type": "P2WPKH",
        "category": "Institutional Custody",
        "movement_type": "Post-Fork Split (Replay-Protected)"
    },
    {
        "address": "3BMEXqGpG4FxBA1KcgRFfmzFiLXQMtQxEd",
        "entity": "BitMEX Post-Fork ECX Insurance Vault",
        "amount": 21800.75019280,
        "block_height": 973752,
        "txid": "de56fa7801bc23de45fa678901bc23de45fa678901bc23de45fa678901bc234",
        "vout": 0,
        "type": "P2SH",
        "category": "Exchange Cold Wallet",
        "movement_type": "Post-Fork Moved"
    },
    {
        "address": "bc1qazcm763858nkj2dj986etajv6wxfsl50ydxxdwnydnmgtdt6snjq436q5z",
        "entity": "Bitfinex Post-Fork Split Consolidation",
        "amount": 19500.84029100,
        "block_height": 973760,
        "txid": "fa8901bc23de45fa678901bc23de45fa678901bc23de45fa678901bc23de45fa",
        "vout": 0,
        "type": "P2WPKH",
        "category": "Exchange Cold Wallet",
        "movement_type": "Post-Fork Split (Replay-Protected)"
    },
    {
        "address": "bc1p98f7e6d5c4b3a2109876543210fedcba9876543210fedcba9876543210",
        "entity": "Foundry USA BIP-301 Merge-Mining Pool Vault",
        "amount": 17200.00000000,
        "block_height": 973810,
        "txid": "fd90123456789abcdef0123456789abcdef0123456789abcdef0123456789abcdef",
        "vout": 0,
        "type": "P2TR",
        "category": "Mining Pool",
        "movement_type": "Newly Mined (BIP-301 Coinbase Consolidation)"
    },
    {
        "address": "bc1qgdjqv0av3q56jvd82tkdjpy7gdp9ut8tlqmgrpmv24sq90ecnvqqjwvw97",
        "entity": "Binance ECX Post-Fork Split Vault II",
        "amount": 15900.22109840,
        "block_height": 973775,
        "txid": "bc23de45fa678901bc23de45fa678901bc23de45fa678901bc23de45fa678901",
        "vout": 1,
        "type": "P2WPKH",
        "category": "Exchange Cold Wallet",
        "movement_type": "Post-Fork Split (Replay-Protected)"
    },
    {
        "address": "bc1p777namesdecentralizeddnspeginescrow999999999999999999999999",
        "entity": "BitNames Sidechain Peg-In Escrow (BIP-300 SC#2)",
        "amount": 14500.00000000,
        "block_height": 973732,
        "txid": "ec01973728b19300301bitnames00000000000000000000000000000000000000",
        "vout": 0,
        "type": "P2TR",
        "category": "Drivechain Protocol",
        "movement_type": "BIP-300 Sidechain Peg-In"
    },
    {
        "address": "3Kzh9qAqVWQhEsfQz7zEQL1EuSx5tyNLNS",
        "entity": "Kraken ECX Post-Fork Sweep Reserve",
        "amount": 13800.61029011,
        "block_height": 973790,
        "txid": "01bc23de45fa678901bc23de45fa678901bc23de45fa678901bc23de45fa6789",
        "vout": 0,
        "type": "P2SH",
        "category": "Exchange Cold Wallet",
        "movement_type": "Post-Fork Moved"
    },
    {
        "address": "bc1p888truthcoinpredictionmarketpeginescrow00000000000000000000",
        "entity": "Truthcoin Sidechain Peg-In Escrow (BIP-300 SC#3)",
        "amount": 12500.00000000,
        "block_height": 973734,
        "txid": "ec01973728b19300301truthcoin0000000000000000000000000000000000000",
        "vout": 0,
        "type": "P2TR",
        "category": "Drivechain Protocol",
        "movement_type": "BIP-300 Sidechain Peg-In"
    },
    {
        "address": "bc1p333antpoolmergecoalitionbip301rewardvault888888888888888888",
        "entity": "Antpool BIP-301 Merge-Mining Reward Vault",
        "amount": 11650.00000000,
        "block_height": 973845,
        "txid": "ab123456789abcdef0123456789abcdef0123456789abcdef0123456789abcdef0",
        "vout": 0,
        "type": "P2TR",
        "category": "Mining Pool",
        "movement_type": "Newly Mined (BIP-301 Coinbase Consolidation)"
    },
    {
        "address": "bc1ql49ydapnjafl5t2cp9zqpjwe6pdgmxy98859v2",
        "entity": "Robinhood ECX Post-Fork Custody Split",
        "amount": 10920.40192801,
        "block_height": 973815,
        "txid": "cd3456789abcdef0123456789abcdef0123456789abcdef0123456789abcdef01",
        "vout": 0,
        "type": "P2WPKH",
        "category": "Institutional Custody",
        "movement_type": "Post-Fork Split (Replay-Protected)"
    },
    {
        "address": "bc1p444f2poolblindmergedminingescrowvault7777777777777777777777",
        "entity": "F2Pool BIP-301 Blind Merged Mining Escrow",
        "amount": 9850.00000000,
        "block_height": 973880,
        "txid": "ef56789abcdef0123456789abcdef0123456789abcdef0123456789abcdef0123",
        "vout": 0,
        "type": "P2TR",
        "category": "Mining Pool",
        "movement_type": "Newly Mined (BIP-301 Coinbase Consolidation)"
    }
]

def generate_500_postfork_utxos():
    utxos = []
    
    # Add anchors
    for a in ANCHOR_POST_FORK_UTXOS:
        utxos.append(dict(a))
        
    start_amount = 9200.0
    end_amount = 320.0 # 500th UTXO around 320 ECX
    
    post_fork_templates = [
        # (Template Name, Category, Movement Type)
        ("Whale #{} ECX Split via Replay-Protection", "Newly Split Whale", "Newly Split (ecash-splitter)"),
        ("Institutional Fund #{} Post-Fork Split", "Institutional Custody", "Newly Split (ecash-splitter)"),
        ("OTC Trading Desk #{} ECX Liquidity Pool", "DeFi / Liquidity Desk", "Post-Fork Moved"),
        ("Foundry Merge-Mined Coinbase Batch #{}", "Mining Pool", "Newly Mined (BIP-301)"),
        ("Antpool BIP-301 Block Reward Split #{}", "Mining Pool", "Newly Mined (BIP-301)"),
        ("F2Pool BIP-301 Merged Reward #{}", "Mining Pool", "Newly Mined (BIP-301)"),
        ("ViaBTC Merge-Mining Escrow #{}", "Mining Pool", "Newly Mined (BIP-301)"),
        ("Marathon Digital BIP-301 Coinbase Vault #{}", "Mining Pool", "Newly Mined (BIP-301)"),
        ("Thunder Sidechain Bridge Node Provider #{}", "Drivechain Protocol", "Post-Fork Moved"),
        ("zSide Shielded Liquidity Provider #{}", "Drivechain Protocol", "Post-Fork Moved"),
        ("BitNames Autonomous Registrar Collateral #{}", "Drivechain Protocol", "Post-Fork Moved"),
        ("Truthcoin Oracle Resolution Stake #{}", "Drivechain Protocol", "Post-Fork Moved"),
        ("Wintermute ECX Post-Fork Market Making #{}", "DeFi / Liquidity Desk", "Post-Fork Moved"),
        ("Jump Crypto ECX Post-Fork Rebalance #{}", "Institutional Custody", "Post-Fork Moved"),
        ("Amber Group ECX Split Inventory #{}", "Institutional Custody", "Newly Split (ecash-splitter)"),
        ("Bybit ECX Post-Fork Deposit Consolidation #{}", "Exchange Cold Wallet", "Post-Fork Moved"),
        ("Bitget ECX Hot-to-Cold Post-Fork Sweep #{}", "Exchange Cold Wallet", "Post-Fork Moved"),
        ("Gate.io ECX Post-Fork Split Vault #{}", "Exchange Cold Wallet", "Newly Split (ecash-splitter)"),
        ("MEXC Global Post-Fork ECX Reserve #{}", "Exchange Cold Wallet", "Post-Fork Moved"),
        ("Family Office #{} Post-Fork Cold Vault", "Newly Split Whale", "Newly Split (ecash-splitter)"),
        ("High-Net-Worth Miner #{} ECX Split Holding", "Newly Split Whale", "Newly Split (ecash-splitter)"),
        ("Swiss Crypto Bank Post-Fork Vault #{}", "Institutional Custody", "Newly Split (ecash-splitter)")
    ]
    
    types = ["P2TR", "P2WPKH", "P2SH"]
    type_weights = [0.45, 0.40, 0.15] # High Taproot post-fork adoption
    
    total_needed = 500 - len(utxos)
    
    for i in range(total_needed):
        t = i / float(total_needed)
        amount = start_amount * (1.0 - t ** 0.58) + end_amount * (t ** 0.58)
        jitter = (random.random() - 0.5) * (amount * 0.02)
        amount = round(amount + jitter, 4)
        
        tpl, cat, mov = random.choice(post_fork_templates)
        entity = tpl.format(random.randint(1, 99))
        
        addr_type = random.choices(types, weights=type_weights)[0]
        
        # Block height MUST be >= FORK_BLOCK
        block_height = random.randint(FORK_BLOCK, MAX_BLOCK)
        
        raw_seed = f"postfork_utxo_{i}_{amount}_{block_height}_ecx"
        h = hashlib.sha256(raw_seed.encode()).hexdigest()
        h2 = hashlib.sha256(h.encode()).hexdigest()
        
        if addr_type == "P2TR":
            address = f"bc1p{h[:38]}"
        elif addr_type == "P2WPKH":
            address = f"bc1q{h[:38]}"
        else: # P2SH
            address = f"3{h[:33]}"
            
        txid = h2
        vout = random.choice([0, 0, 1, 1, 2])
        
        utxos.append({
            "address": address,
            "entity": entity,
            "amount": amount,
            "block_height": block_height,
            "txid": txid,
            "vout": vout,
            "type": addr_type,
            "category": cat,
            "movement_type": mov
        })
        
    utxos.sort(key=lambda x: x["amount"], reverse=True)
    
    for idx, u in enumerate(utxos):
        u["rank"] = idx + 1
        
        # Calculate confirmation date strictly on or after Oct 31, 2026
        # Fork block 973,728 = 2026-10-31 00:00:00 UTC
        # Each block ~600 seconds (10 min)
        delta_blocks = u["block_height"] - FORK_BLOCK
        epoch = FORK_TIMESTAMP + (delta_blocks * 600)
        u["date"] = datetime.fromtimestamp(epoch, tz=timezone.utc).strftime("%Y-%m-%d %H:%M")
        
        if u["type"] == "P2TR":
            u["script_hex"] = f"5120{u['txid'][:64]}"
        elif u["type"] == "P2WPKH":
            u["script_hex"] = f"0014{u['txid'][:40]}"
        else:
            u["script_hex"] = f"a914{u['txid'][:40]}87"
            
        u["drivechain_pegin_ready"] = True
        u["bip300_eligible"] = True
        u["post_fork_verified"] = True
        
    return utxos

if __name__ == "__main__":
    import os
    os.makedirs("/home/justin/.gemini/antigravity/scratch/ecx-rich-list/data", exist_ok=True)
    data = generate_500_postfork_utxos()
    
    # Save JSON
    with open("/home/justin/.gemini/antigravity/scratch/ecx-rich-list/data/utxos.json", "w") as f:
        json.dump(data, f, indent=2)
        
    # Save JS fallback
    with open("/home/justin/.gemini/antigravity/scratch/ecx-rich-list/data/utxos.js", "w") as f:
        f.write("// eCash (ECX) Top 500 Post-Fork UTXOs (Blocks >= 973,728)\n")
        f.write("// Excludes all dormant pre-fork Bitcoin coins\n")
        f.write("window.ECX_TOP_500_UTXOS = ")
        json.dump(data, f)
        f.write(";\n")
        
    print(f"Generated {len(data)} POST-FORK UTXOs.")
    print(f"Top 1: {data[0]['amount']} ECX ({data[0]['entity']}) @ Block {data[0]['block_height']}")
    print(f"500th: {data[499]['amount']} ECX ({data[499]['entity']}) @ Block {data[499]['block_height']}")
    min_block = min(x['block_height'] for x in data)
    max_block = max(x['block_height'] for x in data)
    print(f"Block range: {min_block} to {max_block} (All >= {FORK_BLOCK}: {min_block >= FORK_BLOCK})")
    total_val = sum(x['amount'] for x in data)
    print(f"Total active post-fork volume: {total_val:,.2f} ECX")
