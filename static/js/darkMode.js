document.addEventListener("DOMContentLoaded", /**
 * This function sets the theme of the document based on the value stored in localStorage.
 *
 * @param {string} [theme] - Optional parameter to set the theme explicitly.
 * @returns {void} - This function does not return any value.
 */
document.addEventListener("DOMContentLoaded", function () {
    if (localStorage.getItem('color-theme') === 'dark' || (!('color-theme' in localStorage) && window.matchMedia('(prefers-color-scheme: dark)').matches)) {
        document.documentElement.classList.add('dark');
    } else {
        document.documentElement.classList.remove('dark')
    }
}));
