const copyButton = document.querySelector('.copy-link-button');
const shortenedInput = document.querySelector('.url-input');

// Time (in milliseconds) after which the "Copy"-button text will return from "Copied!" to "Copy"
const copyNotifierTimout = 2000

copyButton.addEventListener('click', () => {
    const inputValue = shortenedInput.value.trim();
    if (inputValue) {
        navigator.clipboard.writeText(inputValue)
            .then(() => {
            if (copyButton.innerText !== 'Copied!') {
                const originalText = copyButton.innerText;
                copyButton.innerText = 'Copied!';
                setTimeout(() => {
                    copyButton.innerText = originalText;
                }, copyNotifierTimout);
            }
        })
    }
});
