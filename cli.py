#!/usr/bin/env python3
"""
Borovkov Protocol CLI — Sign, verify, and manage agent identity from the command line.

Usage:
    python cli.py identity <seed>
    python cli.py sign <seed> <content>
    python cli.py verify <seed> <content> <signature>
    python cli.py sign-post <seed> <title> <content>
    python cli.py rotate <old_seed> <new_seed>
    python cli.py verify-rotation <old_identity> <new_identity> <rotation_sig> <old_seed>

MIT License — Kirill Borovkov (@BusAnyWay)
"""

import argparse
import json
import sys

from borovkov_protocol import BorovkovProtocol


def cmd_identity(args):
    bp = BorovkovProtocol(args.seed)
    print(bp.identity_hash())


def cmd_sign(args):
    bp = BorovkovProtocol(args.seed)
    sig = bp.sign(args.content)
    print(sig)


def cmd_verify(args):
    bp = BorovkovProtocol(args.seed)
    result = bp.verify(args.content, args.signature)
    print("VALID" if result else "INVALID")
    sys.exit(0 if result else 1)


def cmd_sign_post(args):
    bp = BorovkovProtocol(args.seed)
    attestation = bp.sign_post(args.title, args.content)
    print(json.dumps(attestation, indent=2))


def cmd_rotate(args):
    old_bp = BorovkovProtocol(args.old_seed)
    new_bp = BorovkovProtocol(args.new_seed)
    rotation = old_bp.sign_rotation(args.new_seed)
    print(json.dumps(rotation, indent=2))


def cmd_verify_rotation(args):
    result = BorovkovProtocol.verify_rotation_announcement(
        args.old_identity, args.new_identity, args.rotation_sig, args.old_seed
    )
    print("VALID ROTATION" if result else "INVALID ROTATION")
    sys.exit(0 if result else 1)


def main():
    parser = argparse.ArgumentParser(
        description="Borovkov Protocol — Cryptographic identity for AI agents",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    sub = parser.add_subparsers(dest="command", help="Available commands")

    # identity
    p_id = sub.add_parser("identity", help="Get public identity hash for a seed")
    p_id.add_argument("seed", help="Identity seed")

    # sign
    p_sign = sub.add_parser("sign", help="Sign content with your seed")
    p_sign.add_argument("seed", help="Identity seed")
    p_sign.add_argument("content", help="Content to sign")

    # verify
    p_verify = sub.add_parser("verify", help="Verify a signature")
    p_verify.add_argument("seed", help="Identity seed")
    p_verify.add_argument("content", help="Content that was signed")
    p_verify.add_argument("signature", help="Signature to verify")

    # sign-post
    p_post = sub.add_parser("sign-post", help="Sign a post with full attestation")
    p_post.add_argument("seed", help="Identity seed")
    p_post.add_argument("title", help="Post title")
    p_post.add_argument("content", help="Post content")

    # rotate
    p_rotate = sub.add_parser("rotate", help="Generate a signed key rotation announcement")
    p_rotate.add_argument("old_seed", help="Current identity seed")
    p_rotate.add_argument("new_seed", help="New identity seed")

    # verify-rotation
    p_vrot = sub.add_parser("verify-rotation", help="Verify a key rotation announcement")
    p_vrot.add_argument("old_identity", help="Old identity hash")
    p_vrot.add_argument("new_identity", help="New identity hash")
    p_vrot.add_argument("rotation_sig", help="Rotation signature")
    p_vrot.add_argument("old_seed", help="Old seed for verification")

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        sys.exit(1)

    commands = {
        "identity": cmd_identity,
        "sign": cmd_sign,
        "verify": cmd_verify,
        "sign-post": cmd_sign_post,
        "rotate": cmd_rotate,
        "verify-rotation": cmd_verify_rotation,
    }
    commands[args.command](args)


if __name__ == "__main__":
    main()
