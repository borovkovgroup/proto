/**
 * Borovkov Protocol — Agent Identity Persistence via HMAC-SHA256
 * 
 * MIT License — Kirill Borovkov (@BusAnyWay)
 * https://github.com/borovkovgroup/proto
 */

const crypto = require('crypto');

class BorovkovProtocol {
  static VERSION = '1.0.0';
  
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
}

if (require.main === module) {
  const bp = new BorovkovProtocol('KirillBorovkov');
  console.log('Identity:', bp.identityHash());
  const sig = bp.sign('I am KirillBorovkov');
  console.log('Signature:', sig);
  console.log('Verified:', bp.verify('I am KirillBorovkov', sig));
}

module.exports = { BorovkovProtocol };
