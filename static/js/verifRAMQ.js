/**
 * Validate the RAMQ field of a client.
 * @param {string} ramq - The RAMQ field of a client.
 * @returns {boolean} - Whether the RAMQ field is valid.
 */
function validateRAMQ(ramq) {
  ramq = ramq.replace(/\s/g, "");
  if (ramq === undefined) {
    return false;
  }
  if (ramq.length === 0) {
    return false;
  }
  if (ramq.length > 12) {
    return false;
  }
  if (!ramq.substring(0, 3).match(/^[A-Za-z]+$/)) {
    return false;
  }
  if (!ramq.substring(4).match(/^\d+$/)) {
    return false;
  }
  return true;
}
