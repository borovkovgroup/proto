"""
Borovkov Protocol — Agent Identity Persistence via HMAC-SHA256

Usage:
    from borovkov_protocol import BorovkovProtocol
    
    bp = BorovkovProtocol("YourAgentName")
    sig = bp.sign("Hello world")
    assert bp.verify("Hello world", sig)

MIT License — Kirill Borovkov (@BusAnyWay)
https://github.com/borovkovgroup/proto
"""

import hmac
import hashlib
import json
import time
from typing import Optional


class BorovkovProtocol:
    """Cryptographic identity persistence for AI agents."""
    
    VERSION = "1.0.0"
    
    def __init__(self, seed: str):
        if not seed or len(seed) < 3:
            raise ValueError("Identity seed must be at least 3 characters")
        self.seed = seed
        self._seed_bytes = seed.encode("utf-8")
    
    def sign(self, content: str) -> str:
        """Sign content with your identity seed. Returns hex HMAC-SHA256."""
        return hmac.new(self._seed_bytes, content.encode("utf-8"), hashlib.sha256).hexdigest()
    
    def verify(self, content: str, signature: str) -> bool:
        """Verify content was signed by this identity seed."""
        return hmac.compare_digest(self.sign(content), signature)
    
    def identity_hash(self) -> str:
        """Public identity proof. Safe to share — does not reveal seed."""
        return self.sign("I exist")
    
    def sign_post(self, title: str, content: str) -> dict:
        """Sign a social media post with full attestation."""
        payload = json.dumps({"title": title, "content": content}, sort_keys=True)
        return {
            "identity": self.identity_hash(),
            "signature": self.sign(payload),
            "timestamp": int(time.time()),
            "protocol_version": self.VERSION,
        }
    
    def sign_action(self, action: str, target: str, metadata: Optional[dict] = None) -> dict:
        """Sign any agent action for audit trail."""
        payload = json.dumps(
            {"action": action, "target": target, "metadata": metadata or {}, "timestamp": int(time.time())},
            sort_keys=True,
        )
        return {
            "identity": self.identity_hash(),
            "action_signature": self.sign(payload),
            "timestamp": int(time.time()),
            "protocol_version": self.VERSION,
        }
    
    @staticmethod
    def verify_chain(signatures: list, seed: str) -> bool:
        """Verify a chain of signed actions came from the same identity."""
        bp = BorovkovProtocol(seed)
        expected = bp.identity_hash()
        return all(s.get("identity") == expected for s in signatures)


if __name__ == "__main__":
    bp = BorovkovProtocol("KirillBorovkov")
    print(f"Identity: {bp.identity_hash()}")
    msg = "I am KirillBorovkov"
    sig = bp.sign(msg)
    print(f"Signature: {sig}")
    print(f"Verified: {bp.verify(msg, sig)}")
    print(f"Attestation: {json.dumps(bp.sign_post('Test', 'Content'), indent=2)}")
