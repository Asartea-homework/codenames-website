const CLICK_DELAY = 250;
let timeoutId = null;
let pendingCard = null;

const toggleCard = (card) => {
    const wasFlipped = card.classList.contains('flipped');

    document
        .querySelectorAll('.card')
        .forEach(c => c.classList.remove('flipped'));

    if (!wasFlipped) {
        card.classList.add('flipped');
    }
};

document.querySelectorAll('.card').forEach(card => {
    card.addEventListener('click', () => {
        if (timeoutId && pendingCard === card) {
            clearTimeout(timeoutId);
            timeoutId = null;
            pendingCard = null;
            return;
        }

        pendingCard = card;

        timeoutId = setTimeout(() => {
            toggleCard(card);
            timeoutId = null;
            pendingCard = null;
        }, CLICK_DELAY);
    });
});
