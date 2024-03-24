/**
 * Modifies the Opto infos in the database.
 * @param {number} newPracticeNumber - The new practice number.
 * @param {string} newAdresse - The new adresse.
 * @param {string} newPhoneNumber - The new phone number.
 * @returns {Promise<void>}
 */
const modifyOptoInfos = async (newPracticeNumber, newAdresse, newPhoneNumber) => {
  const response = await fetch('/update_opto', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({
      practice_number : newPracticeNumber,
      adresse: newAdresse,
      phone_number: newPhoneNumber,
    }),
  });

  if (response.ok) {
    return response.json();
  }

  throw new Error(response.statusText);
};