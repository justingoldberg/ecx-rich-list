import json
import hashlib
import random
from datetime import datetime, timezone

# Seed for reproducible realistic data
random.seed(42)

FORK_BLOCK = 973728
FORK_DATE = "2026-10-31T00:00:00Z"

# Known top entities and anchor UTXOs in Bitcoin/ECX history
ANCHOR_UTXOS = [
    {
        "address": "34xp4vRoCGJym3xR7yCVPFHoCNxv4Twseo",
        "entity": "Binance Cold Storage I",
        "amount": 248597.38821045,
        "block_height": 554320,
        "txid": "76c5f72688009149457221e3ca6f65beac5500e3f847f978028ff55fc6dff5a1",
        "vout": 0,
        "type": "P2SH",
        "category": "Exchange Cold Wallet"
    },
    {
        "address": "bc1qgdjqv0av3q56jvd82tkdjpy7gdp9ut8tlqmgrpmv24sq90ecnvqqjwvw97",
        "entity": "Binance Cold Storage II",
        "amount": 178010.55120341,
        "block_height": 778942,
        "txid": "1d8b9e63e23072b2170356bf1fbf29a1b069d300e84b80e81c00bb2539ff85a9",
        "vout": 1,
        "type": "P2WPKH",
        "category": "Exchange Cold Wallet"
    },
    {
        "address": "bc1qazcm763858nkj2dj986etajv6wxfsl50ydxxdwnydnmgtdt6snjq436q5z",
        "entity": "Bitfinex Cold Storage",
        "amount": 122078.19045812,
        "block_height": 621045,
        "txid": "4020a65e771eef8d523678cdb8d00ee3b9dc90610f438a3ddcfdb9a8ee1b7522",
        "vout": 0,
        "type": "P2WPKH",
        "category": "Exchange Cold Wallet"
    },
    {
        "address": "bc1ql49ydapnjafl5t2cp9zqpjwe6pdgmxy98859v2",
        "entity": "Robinhood Custody",
        "amount": 118300.20149022,
        "block_height": 795410,
        "txid": "6df6d38e04b407a4a2f8d38bf030438cf34eb3c0e3a62886f34e6e00135b3e6e",
        "vout": 0,
        "type": "P2WPKH",
        "category": "Institutional Custody"
    },
    {
        "address": "bc1qf2epzhwmdccap94nwsc5xrc5mnm6urm7pqfd2",
        "entity": "US Dept of Justice (Silk Road Seizure)",
        "amount": 94643.29841050,
        "block_height": 718390,
        "txid": "893c5d6f3e0984a92c34df0028a31e847c01bfe546e921d74128f73b889311e2",
        "vout": 0,
        "type": "P2WPKH",
        "category": "Government Seizure"
    },
    {
        "address": "1FeexV6bAHb8ybZjqQMjJrcCrHGW9sb6uF",
        "entity": "Mt. Gox Hack Drainer (Dormant 2011)",
        "amount": 79957.21004128,
        "block_height": 113400,
        "txid": "3a9e64e520023ee09918bc289be982d622a59a9bf97e3a96898d9a44955c4d6a",
        "vout": 0,
        "type": "P2PKH",
        "category": "Dormant Whale"
    },
    {
        "address": "1HQ3Go3ggje8pYsttfhmhh6o5WahCazvd1",
        "entity": "US Marshals Service Seized Funds",
        "amount": 69370.11902401,
        "block_height": 655420,
        "txid": "0e3e2357e806b6cdb1f70b54c3a3a17b6714ee1f0e241c0246f53016a3097e32",
        "vout": 0,
        "type": "P2PKH",
        "category": "Government Seizure"
    },
    {
        "address": "bc1qjasf9z3wt7mgnngwhrw9734448xx3qcvmunv06",
        "entity": "Binance Cold Storage III",
        "amount": 68200.00512890,
        "block_height": 780120,
        "txid": "f58d9283a0058b8849bca021798369ff16104bcddb54e3d646beee92a104085f",
        "vout": 2,
        "type": "P2WPKH",
        "category": "Exchange Cold Wallet"
    },
    {
        "address": "1P5ZEDWTKTFGxQjZphgWPQUpe554WKDfHQ",
        "entity": "Tier-1 Whale Accumulator",
        "amount": 62450.84001923,
        "block_height": 605110,
        "txid": "b182cb979d6fbb6b8ec749e75c6bf23d8c1157f12e8471183182ee2be42566c7",
        "vout": 1,
        "type": "P2PKH",
        "category": "Dormant Whale"
    },
    {
        "address": "3BMEXqGpG4FxBA1KcgRFfmzFiLXQMtQxEd",
        "entity": "BitMEX Multi-Sig Cold Storage",
        "amount": 58920.14920033,
        "block_height": 690220,
        "txid": "270db2b449195e347fcf7c7c34b3f885df0db0a11e86b03884ffb23b1a8d0527",
        "vout": 0,
        "type": "P2SH",
        "category": "Exchange Cold Wallet"
    },
    {
        "address": "bc1qm34lsc65zpw79lxes69zkqmk6ee3ewf0j77s3h",
        "entity": "Coinbase Prime Custody",
        "amount": 53890.62100412,
        "block_height": 812900,
        "txid": "921820d2ba7bc09e995a92a514d0251fb87a9c8b7cf7232230113c4e5781a520",
        "vout": 1,
        "type": "P2WPKH",
        "category": "Institutional Custody"
    },
    {
        "address": "3Kzh9qAqVWQhEsfQz7zEQL1EuSx5tyNLNS",
        "entity": "Kraken Cold Storage",
        "amount": 47210.45012390,
        "block_height": 710430,
        "txid": "1a2b3c4d5e6f708192a3b4c5d6e7f8091a2b3c4d5e6f708192a3b4c5d6e7f809",
        "vout": 0,
        "type": "P2SH",
        "category": "Exchange Cold Wallet"
    },
    {
        "address": "bc1p0xlxvlhemja6c4dqv22uapctqupfhlxm9h8z3k2e72q4k9h5z6wqg6330q",
        "entity": "LayerTwo Labs Ecosystem Reserve",
        "amount": 45000.00000000,
        "block_height": 973728,
        "txid": "c0ffee0000b19300301ecxmainnet0000000000000000000000000000000000001",
        "vout": 0,
        "type": "P2TR",
        "category": "Drivechain Protocol"
    },
    {
        "address": "3D2oetdNuZUqQHPJmcMDDHYoqkyNVsFk9r",
        "entity": "OKX Cold Wallet Reserve",
        "amount": 41850.32049012,
        "block_height": 745120,
        "txid": "a1f94c0293ee0912cb84ef701389cb4019a58b09332eec489d71c1b90321a501",
        "vout": 0,
        "type": "P2SH",
        "category": "Exchange Cold Wallet"
    },
    {
        "address": "1L2VaD87v32s8aU5p1v5vFwB2N4zR6u7y9",
        "entity": "Tether USD₮ Treasury Collateral",
        "amount": 39500.00000000,
        "block_height": 830150,
        "txid": "d0498a129ef310486c91a03e1b7c3d2e99f01ab67382c401589da015e128b940",
        "vout": 0,
        "type": "P2PKH",
        "category": "Institutional Custody"
    },
    {
        "address": "bc1q5p6h345w2y5k5q7z4n0x3j7s9w6k4p8x2c1v3b",
        "entity": "Fidelity Wise Origin Custody",
        "amount": 37200.75102944,
        "block_height": 841200,
        "txid": "e4589a1b023f990145c7198ea013df8291a0c49156efb902183cba491024e129",
        "vout": 1,
        "type": "P2WPKH",
        "category": "Institutional Custody"
    },
    {
        "address": "3LQUu4v9z6KN2vsvRxjvPR83R3RBw3x5yZ",
        "entity": "Gemini Trust Custody",
        "amount": 32150.91040182,
        "block_height": 715000,
        "txid": "78201a093e1b9f4852c019dae491025b3901a8f30948ec190283b4c1029348fa",
        "vout": 0,
        "type": "P2SH",
        "category": "Exchange Cold Wallet"
    },
    {
        "address": "12tkqA9xSo9qFXzrBtQ4CGVaTXU4mA4kCe",
        "entity": "Early Miner (Satoshi Era 2010)",
        "amount": 28151.00000000,
        "block_height": 72400,
        "txid": "1182a930fb01928374a5c6d7e8f901a2b3c4d5e6f7a8b9c0d1e2f3a4b5c6d7e8",
        "vout": 0,
        "type": "P2PKH",
        "category": "Dormant Whale"
    },
    {
        "address": "bc1p5d7rjq7g6rd2ee0r0zahe7n09gdwhmvahf27fh9cfnj3jhmlqd4s528hk6",
        "entity": "Thunder Sidechain Peg-In Contract (BIP-300 SC#0)",
        "amount": 25000.00000000,
        "block_height": 973728,
        "txid": "0000000000000000000bip300peg00000000000000000000000000000000000000",
        "vout": 0,
        "type": "P2TR",
        "category": "Drivechain Protocol"
    },
    {
        "address": "bc1pz8x999v762y5k5q7z4n0x3j7s9w6k4p8x2c1v3b4n5m6",
        "entity": "zSide Privacy Sidechain Peg-In (BIP-300 SC#1)",
        "amount": 20000.00000000,
        "block_height": 973728,
        "txid": "0000000000000000000bip300peg00000000000000000000000000000000000001",
        "vout": 0,
        "type": "P2TR",
        "category": "Drivechain Protocol"
    }
]

# Generate realistic continuous descending curve for remaining UTXOs
def generate_500_utxos():
    utxos = []
    
    # Add anchors first
    for a in ANCHOR_UTXOS:
        utxos.append(dict(a))
        
    start_amount = 19500.0
    end_amount = 1250.0 # 500th UTXO around 1,250 ECX
    
    categories = [
        ("Institutional Custody", 0.25),
        ("Exchange Cold Wallet", 0.30),
        ("Dormant Whale (Pre-2016)", 0.20),
        ("BIP-300 Drivechain Peg Ready", 0.15),
        ("DeFi / Sidechain Liquidity Provider", 0.10)
    ]
    
    types = ["P2WPKH", "P2TR", "P2SH", "P2PKH"]
    type_weights = [0.45, 0.25, 0.20, 0.10]
    
    entities_pool = [
        "Bitwise ECX ETP Vault", "Galaxy Digital Custody", "Copper.co ClearLoop",
        "Anchorage Digital Treasury", "Cumberland Mining Vault", "Jump Crypto Reserve",
        "Wintermute ECX Market Making", "FalconX Institutional Pool", "Fireblocks Vault #{}",
        "BitGo Trust Multi-Sig #{}", "CoinShares Physical Stash", "Amber Group Treasury",
        "Foundry Digital Mining Pool", "Antpool Consolidated Reward", "F2Pool Coinbase Vault",
        "Marathon Digital Treasury", "Riot Platforms Reserve", "CleanSpark ECX Stash",
        "Bitfarms Cold Storage", "Deribit Margin Cold Reserve", "Bybit Institutional Reserve #{}",
        "Bitstamp Vault", "Gate.io Cold Wallet #{}", "MEXC Global Reserve #{}",
        "Drivechain Merge-Mining Pool Alpha", "Drivechain Validator Stash #{}",
        "Truthcoin Prediction Market Liquidity", "BitNames Registry Reserve",
        "Satoshi Era Early HODLer (2011)", "Ancient Block Reward Consolidation #{}",
        "Anonymous Whale #{}", "Swiss Private Bank Vault #{}", "Family Office Trust #{}"
    ]
    
    total_needed = 500 - len(utxos)
    
    # Exponential decay curve for whale distribution
    decay_factor = 2.8
    for i in range(total_needed):
        t = i / float(total_needed)
        # Power curve for natural distribution
        amount = start_amount * (1.0 - t ** 0.55) + end_amount * (t ** 0.55)
        # Add slight natural jitter
        jitter = (random.random() - 0.5) * (amount * 0.015)
        amount = round(amount + jitter, 4)
        
        # Pick category
        cat = random.choices([c[0] for c in categories], weights=[c[1] for c in categories])[0]
        
        # Pick address type
        addr_type = random.choices(types, weights=type_weights)[0]
        
        # Generate hash-based address & txid
        raw_seed = f"utxo_{i}_{amount}_ecx_mainnet"
        h = hashlib.sha256(raw_seed.encode()).hexdigest()
        h2 = hashlib.sha256(h.encode()).hexdigest()
        
        if addr_type == "P2TR":
            address = f"bc1p{h[:38]}"
        elif addr_type == "P2WPKH":
            address = f"bc1q{h[:38]}"
        elif addr_type == "P2SH":
            address = f"3{h[:33]}"
        else: # P2PKH
            address = f"1{h[:33]}"
            
        txid = h2
        vout = random.choice([0, 0, 0, 1, 1, 2])
        block_height = random.randint(120000, FORK_BLOCK)
        
        # Select entity
        ent_template = random.choice(entities_pool)
        if "{}" in ent_template:
            entity = ent_template.format(random.randint(1, 99))
        else:
            entity = ent_template
            
        utxos.append({
            "address": address,
            "entity": entity,
            "amount": amount,
            "block_height": block_height,
            "txid": txid,
            "vout": vout,
            "type": addr_type,
            "category": cat
        })
        
    # Sort descending by amount
    utxos.sort(key=lambda x: x["amount"], reverse=True)
    
    # Assign ranks and metadata
    current_time_epoch = 1793404800 # Oct 2026 epoch approx
    for idx, u in enumerate(utxos):
        u["rank"] = idx + 1
        # Calculate block time estimate (average 10 min per block from genesis 2009-01-03)
        block_epoch = 1231006505 + (u["block_height"] * 600)
        u["date"] = datetime.fromtimestamp(min(block_epoch, 1793404800), tz=timezone.utc).strftime("%Y-%m-%d")
        
        # Derive script hex representation
        if u["type"] == "P2TR":
            u["script_hex"] = f"5120{u['txid'][:64]}"
        elif u["type"] == "P2WPKH":
            u["script_hex"] = f"0014{u['txid'][:40]}"
        elif u["type"] == "P2SH":
            u["script_hex"] = f"a914{u['txid'][:40]}87"
        else:
            u["script_hex"] = f"76a914{u['txid'][:40]}88ac"
            
        # Drivechain compatibility tag
        u["drivechain_pegin_ready"] = True
        u["bip300_eligible"] = True
        
    return utxos

if __name__ == "__main__":
    import os
    os.makedirs("/home/justin/.gemini/antigravity/scratch/ecx-rich-list/data", exist_ok=True)
    data = generate_500_utxos()
    with open("/home/justin/.gemini/antigravity/scratch/ecx-rich-list/data/utxos.json", "w") as f:
        json.dump(data, f, indent=2)
    print(f"Generated {len(data)} UTXOs successfully.")
    print(f"Top 1: {data[0]['amount']} ECX ({data[0]['entity']})")
    print(f"500th: {data[499]['amount']} ECX ({data[499]['entity']})")
    total_val = sum(x['amount'] for x in data)
    print(f"Total in top 500: {total_val:,.2f} ECX")
