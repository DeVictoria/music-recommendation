document.addEventListener('DOMContentLoaded', () => {
    const recommendations = document.getElementById("recommendation");
    const searchField = document.getElementById('searchField');
    const searchButton = document.getElementById('searchButton');
    const searchBoxes = document.getElementById("searchBoxes");
    let searchCount = 0;

    searchButton.addEventListener('click', async () => {
        const query = searchField.value;

        if (query.trim() === '') {
            return;
        }

        const data = await fetch(`/search?query=${query}`).then(res => res.json());

        searchBoxes.replaceChildren();

        data.forEach(([id, title]) => {
            const li = document.createElement('li');

            const checkbox = document.createElement('input');
            checkbox.type = "checkbox";
            checkbox.id = `search-${searchCount++}`;
            checkbox.value = id;
            checkbox.name = "recommendation"

            checkbox.addEventListener("change", (e) => {
                if (!e.target.checked) {
                    return;
                }

                const same = Array.from(
                    recommendations.getElementsByTagName("input")
                ).find((input) => input.value === e.target.value);

                if (same) {
                    same.checked = true;
                    searchBoxes.removeChild(li);
                    return;
                }

                recommendations.appendChild(li);
            })

            const label = document.createElement('label');
            label.htmlFor = checkbox.id;
            label.textContent = title;

            li.appendChild(checkbox);
            li.appendChild(label);

            searchBoxes.appendChild(li);
        });
    });
});