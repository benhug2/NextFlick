document.getElementById('genreForm').addEventListener('submit', async (event) => {
    event.preventDefault();

    const genre = document.getElementById('genreDropdown').value;
    const movieDetailsDiv = document.getElementById('movieDetails');

    if (!genre) {
        alert('Please select a genre.');
        return;
    }

    try {
        const response = await fetch(`/movies/by_genre?genre=${encodeURIComponent(genre)}`);
        if (response.ok) {
            const movie = await response.json();
            displayMovieDetails(movie, genre, movieDetailsDiv);
        } else {
            const errorData = await response.json();
            movieDetailsDiv.innerHTML = `<p>${errorData.message}</p>`;
        }
    } catch (error) {
        console.error('Error fetching movie by genre:', error);
        alert('An error occurred. Please try again later.');
    }
});

function displayMovieDetails(movie, genre, container) {
    container.innerHTML = `
        <h5>${movie.title}</h5>
        <p><strong>Overview:</strong> ${movie.overview || 'No overview available.'}</p>
        <p><strong>Release Date:</strong> ${movie.release_date || 'Unknown'}</p>
        <p><strong>Rating:</strong> ${movie.vote_average || 'N/A'}</p>
        <button id="tellMeMore" class="btn btn-primary mt-2">Tell Me More</button>
        <button id="nextOption" class="btn btn-secondary mt-2">Next Option</button>
        <div id="detailedInfo" class="mt-3"></div>
    `;

    document.getElementById('tellMeMore').addEventListener('click', async () => {
        try {
            const response = await fetch(`/movies/details?title=${encodeURIComponent(movie.title)}`);
            if (response.ok) {
                const details = await response.json();
                renderDetailedInfo(details);
            } else {
                alert('Failed to fetch details.');
            }
        } catch (error) {
            console.error('Error fetching movie details:', error);
        }
    });

    document.getElementById('nextOption').addEventListener('click', async () => {
        try {
            const response = await fetch(`/movies/by_genre?genre=${encodeURIComponent(genre)}`);
            if (response.ok) {
                const newMovie = await response.json();
                displayMovieDetails(newMovie, genre, container);
            } else {
                alert('Failed to fetch next movie.');
            }
        } catch (error) {
            console.error('Error fetching next movie:', error);
        }
    });
}

function renderDetailedInfo(details) {
    const detailedInfoDiv = document.getElementById('detailedInfo');
    detailedInfoDiv.innerHTML = `
        <h6>Full Details:</h6>
        <p><strong>Title:</strong> ${details.title || 'Unknown'}</p>
        <p><strong>Overview:</strong> ${details.overview || 'No overview available.'}</p>
        <p><strong>Release Date:</strong> ${details.release_date || 'Unknown'}</p>
        <p><strong>Rating:</strong> ${details.vote_average || 'N/A'}</p>
        <p><strong>Genres:</strong> ${parseGenres(details.genres)}</p>
        <p><strong>Budget:</strong> ${details.budget ? `$${details.budget.toLocaleString()}` : 'Unknown'}</p>
        <p><strong>Revenue:</strong> ${details.revenue ? `$${details.revenue.toLocaleString()}` : 'Unknown'}</p>
        <p><strong>Runtime:</strong> ${details.runtime ? `${details.runtime} minutes` : 'Unknown'}</p>
        <p><strong>Tagline:</strong> ${details.tagline || 'No tagline available.'}</p>
        <p><strong>Homepage:</strong> ${details.homepage ? `<a href="${details.homepage}" target="_blank">${details.homepage}</a>` : 'No homepage available.'}</p>
    `;
}

function parseGenres(genres) {
    try {
        const genreList = JSON.parse(genres || '[]');
        return genreList.map(genre => genre.name).join(', ') || 'N/A';
    } catch {
        return 'N/A';
    }
}
