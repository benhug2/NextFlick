document.getElementById('moodForm').addEventListener('submit', async (event) => {
    event.preventDefault();

    const mood = document.getElementById('moodDropdown').value;
    const moodMovieDetailsDiv = document.getElementById('moodMovieDetails');

    if (!mood) {
        alert('Please select your mood.');
        return;
    }

    try {
        const response = await fetch(`/movies/by_mood?mood=${encodeURIComponent(mood)}`);
        if (response.ok) {
            const movie = await response.json();
            moodMovieDetailsDiv.innerHTML = `
                <h5>${movie.title}</h5>
                <p><strong>Overview:</strong> ${movie.overview || 'No overview available.'}</p>
                <p><strong>Release Date:</strong> ${movie.release_date || 'Unknown'}</p>
                <p><strong>Rating:</strong> ${movie.vote_average || 'N/A'}</p>
            `;
        } else {
            const errorData = await response.json();
            moodMovieDetailsDiv.innerHTML = `<p>${errorData.message}</p>`;
        }
    } catch (error) {
        console.error('Error fetching movie by mood:', error);
        alert('An error occurred. Please try again later.');
    }
});
