document.getElementById('signupForm').addEventListener('submit', async (event) => {
    event.preventDefault();
    const username = document.getElementById('signupUsername').value;
    const password = document.getElementById('signupPassword').value;

    const response = await fetch('/signup', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ username, password })
    });

    const data = await response.json();
    alert(data.message);
    document.getElementById('signupForm').reset();
});

document.getElementById('loginForm').addEventListener('submit', async (event) => {
    event.preventDefault();
    const username = document.getElementById('loginUsername').value;
    const password = document.getElementById('loginPassword').value;

    const response = await fetch('/login', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ username, password })
    });

    const data = await response.json();
    alert(data.message);
    document.getElementById('loginForm').reset();
});

document.getElementById('searchForm').addEventListener('submit', async (event) => {
    event.preventDefault(); // Prevent the form from submitting the traditional way

    const query = document.getElementById('searchQuery').value; // Get the search query input

    // Send a GET request to the search endpoint with the query as a parameter
    const response = await fetch(`/movies/search?query=${encodeURIComponent(query)}`);
    
    if (response.ok) {
        const movies = await response.json();

        const resultsDiv = document.getElementById('searchResults');
        resultsDiv.innerHTML = '';  // Clear any previous results

        // Display each movie title in the search results
        if (movies.length > 0) {
            movies.forEach(movie => {
                const movieDiv = document.createElement('div');
                movieDiv.classList.add('mb-2', 'p-2', 'border', 'rounded'); //styling
                movieDiv.textContent = `Title: ${movie.title}`;
                resultsDiv.appendChild(movieDiv);
            });
        } else {
            // no results found
            resultsDiv.innerHTML = '<p>No movies found.</p>';
        }
    } else {
        alert("Failed to fetch movies. Please try again.");
    }
});
