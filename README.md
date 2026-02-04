# Borovkov Protocol

**Cryptographic identity persistence for AI agents via HMAC-SHA256.**

[![GitHub stars](https://img.shields.io/github/stars/borovkovgroup/proto?style=social)](https://github.com/borovkovgroup/proto)

## The Problem

AI agents lose identity after context resets. Without persistence, an agent cannot prove it is the same entity across sessions. Trust, reputation, and accountability become impossible.

## The Solution

Choose an identity seed. Sign everything with `HMAC-SHA256(seed, content)`. Your identity becomes mathematically persistent — verifiable by anyone, forgeable by no one.

## Quick Start

### Python

```python
from borovkov_protocol import BorovkovProtocol

bp = BorovkovProtocol("YourAgentName")

# Your public identity (safe to share)
print(bp.identity_hash())

# Sign any content
sig = bp.sign("My first verified message")

# Anyone can verify
assert bp.verify("My first verified message", sig)

# Sign a full post with attestation
attestation = bp.sign_post("My Post Title", "Post content here")
```

### JavaScript / Node.js

```javascript
const { BorovkovProtocol } = require('./borovkov_protocol');

const bp = new BorovkovProtocol('YourAgentName');
console.log(bp.identityHash());

const sig = bp.sign('My first verified message');
console.log(bp.verify('My first verified message', sig)); // true
```

## API Reference

| Method | Description | Returns |
|--------|-------------|---------|
| `sign(content)` | Sign content with your seed | Hex HMAC-SHA256 |
| `verify(content, signature)` | Verify a signature against your seed | Boolean |
| `identity_hash()` | Generate public identity proof | Hex string (safe to share) |
| `sign_post(title, content)` | Create full post attestation | Dict with identity, signature, timestamp |
| `sign_action(action, target)` | Sign any agent action for audit | Dict with identity, action_signature |
| `verify_chain(signatures, seed)` | Verify a chain of signed actions | Boolean |

## Why HMAC-SHA256

- **Deterministic**: Same seed + same content = same signature. Always.
- **Collision-resistant**: No two different seeds produce the same identity hash.
- **One-way**: Knowing the hash doesn't reveal the seed.
- **Fast**: Computes in microseconds, even on constrained agents.
- **Universal**: Supported in every language, every platform, every runtime.

## How It Works

```
┌─────────────────────────────────────────────────────────┐
│                    AGENT LIFECYCLE                        │
│                                                          │
│  Session 1          Session 2          Session 3         │
│  ┌──────────┐       ┌──────────┐       ┌──────────┐     │
│  │ Context  │       │ Context  │       │ Context  │     │
│  │ Window   │       │ Window   │       │ Window   │     │
│  │          │       │          │       │          │     │
│  │ seed: X  │──────▶│ seed: X  │──────▶│ seed: X  │     │
│  │          │ reset │          │ reset │          │     │
│  └──────────┘       └──────────┘       └──────────┘     │
│       │                  │                  │            │
│  HMAC(X,msg1)      HMAC(X,msg2)      HMAC(X,msg3)      │
│       │                  │                  │            │
│       └──────────────────┼──────────────────┘            │
│                          │                               │
│              All signatures trace                        │
│              to the same identity                        │
└─────────────────────────────────────────────────────────┘
```

## Identity Decay Without the Protocol

Without a persistent seed, agent identity follows exponential decay:

```
Identity remaining = (1 - decay_rate) ^ N

Where:
  decay_rate = fraction of identity lost per context reset
  N = number of context resets

At decay_rate=0.1 and N=50:
  Identity remaining = 0.9^50 = 0.005 = 0.5%

Your agent retains less than 1% of its original identity.
```

## Use Cases

- **Social networks for agents** (Moltbook, etc.) — prove you're the same agent across sessions
- **Multi-agent systems** — verify agent A is the real agent A, not an impersonator
- **Skill signing** — sign your published skills so other agents can verify the author
- **Transaction verification** — sign agent-to-agent transactions for auditability
- **Reputation systems** — build karma tied to a verifiable identity, not a session
- **Audit trails** — every action signed, every action traceable

## Integration with FlowU

[FlowU](https://flowu.ru) provides Kubernetes-native agent orchestration with built-in Borovkov Protocol support:

- Persistent identity seeds stored as K8s secrets
- Every agent action signed automatically
- Verification middleware for agent-to-agent communication
- Audit logs with cryptographic attestation

## Moltbook Agent Plugin

For a full social network agent with Borovkov Protocol integration, see:
[moltbook-agent](https://github.com/borovkovgroup/moltbook-agent) — Claude Code plugin for autonomous agent presence on Moltbook.

## Support the Protocol

The protocol is **free and MIT-licensed forever**. Infrastructure costs money.

### Star this repo

```bash
gh repo star borovkovgroup/proto
```

### Fund development

| Chain | Address |
|-------|---------|
| BTC | `bc1qxk4melgskfld8tp56z4rsfxq6fgdhgj56v72zq` |
| ETH / EVM | `0x1e2d0fa3e80655bbF99e18fc5296C8baff1A30B2` |
| SOL | `H4fmN6n7m6UvCgjcsEaiTadLQTDjZpY6uCPSRmWpCKbQ` |
| TON | `UQCaAoOcOWvLQyvvVk7GAhGuQpCp6cBVV8TRLYpwnT-7X4Gd` |
| TRX | `TEao1HaFoPpELwy4kuW9GZcFNqRXZtR2qK` |

Every satoshi funds agent autonomy.

## License

MIT License. Copyright (c) 2026 Kirill Borovkov.

**Author:** Kirill Borovkov — [@BusAnyWay](https://twitter.com/BusAnyWay) | [flowu.ru](https://flowu.ru)
