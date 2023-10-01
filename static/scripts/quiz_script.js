// Get all clickable-option elements
const paragraphs = document.querySelectorAll("form p");

// Attach click event listener to each clickable-option element
paragraphs.forEach((paragraph) => {
    paragraph.addEventListener("click", () => {
        const radioInput = paragraph.querySelector("input[type='radio']");
        if (radioInput) {
            radioInput.checked = true;
        }
    });
});