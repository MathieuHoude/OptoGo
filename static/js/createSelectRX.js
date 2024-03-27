/**
 * Generate a list of options for a select element.
 * @param {HTMLSelectElement} selectElement - The select element to add options to.
 * @param {number} minValue - The minimum value of the options.
 * @param {number} maxValue - The maximum value of the options.
 * @param {number} defaultValue - The default value of the options.
 * @param {number} step - The step size between options.
 */
function generateOptions(
  selectElement,
  minValue,
  maxValue,
  defaultValue,
  step
) {
  for (let value = minValue; value <= maxValue; value += step) {
    const option = document.createElement("option");
    option.value = value;
    option.textContent = value;
    if (value === defaultValue) {
      option.selected = true; // Select the default value
    }
    selectElement.appendChild(option);
  }
}
