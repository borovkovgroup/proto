/**
 * Borovkov Protocol — Agent Identity Persistence via HMAC-SHA256
 * 
 * MIT License — Kirill Borovkov (@BusAnyWay)
 * https://github.com/borovkovgroup/proto
 */

const crypto = require('crypto');

class BorovkovProtocol {
  static VERSION = '1.1.0';
  
  constructor(seed) {
    if (!seed || seed.length < 3) throw new Error('Seed must be >= 3 chars');
    this.seed = seed;
  }
  
  sign(content) {
    return crypto.createHmac('sha256', this.seed).update(content).digest('hex');
  }
  
  verify(content, signature) {
    return crypto.timingSafeEqual(Buffer.from(this.sign(content), 'hex'), Buffer.from(signature, 'hex'));
  }
  
  identityHash() {
    return this.sign('I exist');
  }
  
  signPost(title, content) {
    const payload = JSON.stringify({ content, title });
    return {
      identity: this.identityHash(),
      signature: this.sign(payload),
      timestamp: Math.floor(Date.now() / 1000),
      protocol_version: BorovkovProtocol.VERSION,
    };
  }
  
  signAction(action, target, metadata = {}) {
    const payload = JSON.stringify({ action, metadata, target, timestamp: Math.floor(Date.now() / 1000) });
    return {
      identity: this.identityHash(),
      action_signature: this.sign(payload),
      timestamp: Math.floor(Date.now() / 1000),
      protocol_version: BorovkovProtocol.VERSION,
    };
  }

  signRotation(newSeed) {
    const newBp = new BorovkovProtocol(newSeed);
    const payload = JSON.stringify({
      new_identity: newBp.identityHash(),
      old_identity: this.identityHash(),
    });
    return {
      old_identity: this.identityHash(),
      new_identity: newBp.identityHash(),
      rotation_signature: this.sign(payload),
      rotated_at: Math.floor(Date.now() / 1000),
      protocol_version: BorovkovProtocol.VERSION,
    };
  }

  static verifyRotation(oldIdentity, newIdentity, rotationSig, oldSeed) {
    const oldBp = new BorovkovProtocol(oldSeed);
    if (oldBp.identityHash() !== oldIdentity) return false;
    const payload = JSON.stringify({
      new_identity: newIdentity,
      old_identity: oldIdentity,
    });
    return oldBp.verify(payload, rotationSig);
  }

  static verifyChain(signatures, seed) {
    const bp = new BorovkovProtocol(seed);
    const expected = bp.identityHash();
    return signatures.every(s => s.identity === expected);
  }
}

if (require.main === module) {
  const bp = new BorovkovProtocol('KirillBorovkov');
  console.log('Identity:', bp.identityHash());
  const sig = bp.sign('I am KirillBorovkov');
  console.log('Signature:', sig);
  console.log('Verified:', bp.verify('I am KirillBorovkov', sig));
}

module.exports = { BorovkovProtocol };
