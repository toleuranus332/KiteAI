# KiteAI
Automated multi-account farming tool for Kite AI decentralized payment network with faucet claims, token staking, DEX swaps, daily quiz completion, cross-chain bridging, proxy rotation, and configurable task scheduling
# Kite AI Bot

Automated multi-account interaction tool for the **Kite AI** decentralized payment network testnet.

## Features

- **Multi-account management** — load multiple wallets from `accounts.txt`
- **Proxy rotation** — supports HTTP/SOCKS5 proxies with automatic rotation
- **Faucet claims** — auto-claim testnet KITE tokens
- **Token staking** — automated staking of available balance
- **DEX swaps** — random token swap execution
- **Daily quiz** — automatic quiz completion for rewards
- **Cross-chain bridge** — bridge tokens to Ethereum, Arbitrum, Base
- **Configurable delays** — randomized intervals between tasks

## Requirements

- Python 3.9+
- pip

## Installation

```bash
git clone https://github.com/vonssy/KiteAi-BOT.git
cd KiteAi-BOT
pip install -r requirements.txt
```

## Configuration

1. Add private keys to `accounts.txt` (one per line)
2. Add proxies to `proxy.txt` (optional, one per line)
3. Run the bot and use the interactive configuration menu, or edit `config.json` directly

### Config options

| Parameter | Default | Description |
|-----------|---------|-------------|
| `rpc_url` | `https://rpc.kiteai.top` | RPC endpoint |
| `chain_id` | `2368` | Network chain ID |
| `max_concurrent` | `5` | Parallel worker threads |
| `task_delay_min` | `3` | Minimum delay between tasks (sec) |
| `task_delay_max` | `10` | Maximum delay between tasks (sec) |
| `auto_claim_faucet` | `true` | Enable faucet auto-claim |
| `auto_stake` | `true` | Enable auto-staking |
| `auto_swap` | `true` | Enable DEX swap execution |
| `auto_quiz` | `true` | Enable daily quiz completion |
| `auto_bridge` | `true` | Enable cross-chain bridge |

## Usage

```bash
python main.py
```

## Proxy format

```
ip:port
http://ip:port
http://user:pass@ip:port
socks5://ip:port
```

## Disclaimer

This tool is for educational and testnet purposes only. Use at your own risk.

## License

MIT
