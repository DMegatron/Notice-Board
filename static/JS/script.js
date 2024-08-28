const darkModeToggle = document.getElementById('dark-mode-toggle');
const body = document.body;
const navbar = document.querySelector('.navbar');
const sections = document.querySelectorAll('.section');
const bottomSectionsDivs = document.querySelectorAll('.bottom-sections div');

if (localStorage.getItem('darkMode') === 'enabled') {
    enableDarkMode();
} else {
    disableDarkMode();
}

darkModeToggle.addEventListener('click', () => {
    if (localStorage.getItem('darkMode') !== 'enabled') {
        enableDarkMode();
    } else {
        disableDarkMode();
    }
});

function enableDarkMode() {
    darkModeToggle.innerHTML = '☀️';
    body.classList.add('dark-mode');
    navbar.classList.add('dark-mode');
    sections.forEach(section => section.classList.add('dark-mode'));
    bottomSectionsDivs.forEach(div => div.classList.add('dark-mode'));
    localStorage.setItem('darkMode', 'enabled');
}

function disableDarkMode() {
    darkModeToggle.innerHTML = '🌙';
    body.classList.remove('dark-mode');
    navbar.classList.remove('dark-mode');
    sections.forEach(section => section.classList.remove('dark-mode'));
    bottomSectionsDivs.forEach(div => div.classList.remove('dark-mode'));
    localStorage.setItem('darkMode', 'disabled');
}
