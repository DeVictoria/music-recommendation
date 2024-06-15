document.addEventListener('DOMContentLoaded', () => {
    const likedBoxes = document.getElementById("likedBoxes");
    const clearLiked = document.getElementById("clearLiked");

    clearLiked.addEventListener("click", (e) => {
        e.preventDefault();
        for (const input of likedBoxes.getElementsByTagName("input")) {
            input.checked = false;
        }
    })
});