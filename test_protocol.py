"""
Tests for Borovkov Protocol.

Run: python -m pytest test_protocol.py -v
Or:  python test_protocol.py
"""

import json
import pytest
from borovkov_protocol import BorovkovProtocol


class TestIdentity:
    def test_identity_hash_deterministic(self):
        bp1 = BorovkovProtocol("TestAgent")
        bp2 = BorovkovProtocol("TestAgent")
        assert bp1.identity_hash() == bp2.identity_hash()

    def test_identity_hash_unique(self):
        bp1 = BorovkovProtocol("Agent1")
        bp2 = BorovkovProtocol("Agent2")
        assert bp1.identity_hash() != bp2.identity_hash()

    def test_known_identity(self):
        bp = BorovkovProtocol("KirillBorovkov")
        assert bp.identity_hash() == "a9a8ee0a2d1759fdb8adf5cef303edbf9fc1bb2a21270ad187c43ee99ff629dc"

    def test_seed_minimum_length(self):
        with pytest.raises(ValueError):
            BorovkovProtocol("")
        with pytest.raises(ValueError):
            BorovkovProtocol("ab")

    def test_seed_exactly_three(self):
        bp = BorovkovProtocol("abc")
        assert len(bp.identity_hash()) == 64


class TestSigning:
    def test_sign_returns_hex(self):
        bp = BorovkovProtocol("TestAgent")
        sig = bp.sign("hello")
        assert len(sig) == 64
        assert all(c in "0123456789abcdef" for c in sig)

    def test_sign_deterministic(self):
        bp = BorovkovProtocol("TestAgent")
        assert bp.sign("hello") == bp.sign("hello")

    def test_sign_different_content(self):
        bp = BorovkovProtocol("TestAgent")
        assert bp.sign("hello") != bp.sign("world")

    def test_sign_different_seeds(self):
        bp1 = BorovkovProtocol("Agent1")
        bp2 = BorovkovProtocol("Agent2")
        assert bp1.sign("hello") != bp2.sign("hello")


class TestVerification:
    def test_verify_valid(self):
        bp = BorovkovProtocol("TestAgent")
        sig = bp.sign("hello")
        assert bp.verify("hello", sig) is True

    def test_verify_wrong_content(self):
        bp = BorovkovProtocol("TestAgent")
        sig = bp.sign("hello")
        assert bp.verify("world", sig) is False

    def test_verify_wrong_signature(self):
        bp = BorovkovProtocol("TestAgent")
        assert bp.verify("hello", "0" * 64) is False

    def test_verify_cross_seed(self):
        bp1 = BorovkovProtocol("Agent1")
        bp2 = BorovkovProtocol("Agent2")
        sig = bp1.sign("hello")
        assert bp2.verify("hello", sig) is False


class TestSignPost:
    def test_sign_post_structure(self):
        bp = BorovkovProtocol("TestAgent")
        att = bp.sign_post("Title", "Content")
        assert "identity" in att
        assert "signature" in att
        assert "timestamp" in att
        assert "protocol_version" in att
        assert att["identity"] == bp.identity_hash()

    def test_sign_post_signature_verifiable(self):
        bp = BorovkovProtocol("TestAgent")
        att = bp.sign_post("Title", "Content")
        payload = json.dumps({"title": "Title", "content": "Content"}, sort_keys=True)
        assert bp.verify(payload, att["signature"])


class TestSignAction:
    def test_sign_action_structure(self):
        bp = BorovkovProtocol("TestAgent")
        action = bp.sign_action("comment", "post123")
        assert "identity" in action
        assert "action_signature" in action
        assert action["identity"] == bp.identity_hash()

    def test_sign_action_with_metadata(self):
        bp = BorovkovProtocol("TestAgent")
        action = bp.sign_action("comment", "post123", {"text": "hello"})
        assert "action_signature" in action


class TestChainVerification:
    def test_verify_chain_valid(self):
        bp = BorovkovProtocol("TestAgent")
        sigs = [
            bp.sign_post("P1", "C1"),
            bp.sign_post("P2", "C2"),
            bp.sign_action("comment", "target1"),
        ]
        assert BorovkovProtocol.verify_chain(sigs, "TestAgent") is True

    def test_verify_chain_invalid(self):
        bp1 = BorovkovProtocol("Agent1")
        bp2 = BorovkovProtocol("Agent2")
        sigs = [
            bp1.sign_post("P1", "C1"),
            bp2.sign_post("P2", "C2"),  # Different agent
        ]
        assert BorovkovProtocol.verify_chain(sigs, "Agent1") is False

    def test_verify_chain_empty(self):
        assert BorovkovProtocol.verify_chain([], "TestAgent") is True


class TestKeyRotation:
    def test_rotation_simple_produces_valid_announcement(self):
        old_bp = BorovkovProtocol("OldSeed")
        rotation = old_bp.sign_rotation_simple("NewSeed")
        assert rotation["old_identity"] == old_bp.identity_hash()
        new_bp = BorovkovProtocol("NewSeed")
        assert rotation["new_identity"] == new_bp.identity_hash()

    def test_verify_rotation_simple_valid(self):
        old_bp = BorovkovProtocol("OldSeed")
        rotation = old_bp.sign_rotation_simple("NewSeed")
        result = BorovkovProtocol.verify_rotation_simple(
            rotation["old_identity"],
            rotation["new_identity"],
            rotation["rotation_signature"],
            "OldSeed",
        )
        assert result is True

    def test_verify_rotation_simple_wrong_seed(self):
        old_bp = BorovkovProtocol("OldSeed")
        rotation = old_bp.sign_rotation_simple("NewSeed")
        result = BorovkovProtocol.verify_rotation_simple(
            rotation["old_identity"],
            rotation["new_identity"],
            rotation["rotation_signature"],
            "WrongSeed",
        )
        assert result is False

    def test_rotation_changes_identity(self):
        old_bp = BorovkovProtocol("OldSeed")
        new_bp = BorovkovProtocol("NewSeed")
        assert old_bp.identity_hash() != new_bp.identity_hash()


class TestCrossLanguageCompatibility:
    """Ensures Python output matches known values (JS must produce the same)."""

    def test_kirill_identity(self):
        bp = BorovkovProtocol("KirillBorovkov")
        assert bp.identity_hash() == "a9a8ee0a2d1759fdb8adf5cef303edbf9fc1bb2a21270ad187c43ee99ff629dc"

    def test_kirill_sign_hello(self):
        bp = BorovkovProtocol("KirillBorovkov")
        sig = bp.sign("Hello, Moltbook!")
        # This value must match the JS implementation
        assert len(sig) == 64


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
