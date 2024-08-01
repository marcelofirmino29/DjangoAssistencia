document.addEventListener('DOMContentLoaded', (event) => {
    document.querySelectorAll('.qty .minus').forEach(button => {
        button.addEventListener('click', () => {
            let input = button.nextElementSibling;
            let value = parseInt(input.value, 10);
            if (value > 0) {
                input.value = value - 1;
            }
        });
    });

    document.querySelectorAll('.qty .plus').forEach(button => {
        button.addEventListener('click', () => {
            let input = button.previousElementSibling;
            let value = parseInt(input.value, 10);
            input.value = value + 1;
        });
    });
});
