/**
 * Verify the RAMQ number of a user
 * @param {string} ramq - The RAMQ number of the user
 * @returns {Promise<object>} - A JSON object containing the user's information
 */
const verifRamq = async (ramq) => {
  const response = await fetch('/verif_ramq', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({
      ramq : ramq,
    }),
  });

  if (response.ok) {
    return response.json();
  }

  throw new Error(response.statusText);
};