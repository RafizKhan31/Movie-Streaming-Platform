/**
 * The Code Wizerd Movie Site - Main Search & Detail Handler
 * Connected to Django REST API (Replaces OMDB static data)
 */

function getMovies(query) {
  if (!query || !query.trim()) return;

  const endpoint = `http://127.0.0.1:8000/api/movies/?search=${encodeURIComponent(query.trim())}`;

  fetch(endpoint)
    .then((res) => res.json())
    .then((res) => {
      let results = [];
      if (res.data && res.data.results) {
        results = res.data.results;
      } else if (Array.isArray(res.data)) {
        results = res.data;
      }

      let html = '';
      if (results.length === 0) {
        html = `
          <div class="col-12 text-center py-4">
            <h4 class="text-white">No movies found matching "${query}"</h4>
            <p class="text-muted">Try searching for other titles like Inception, Batman, 3 Idiots, or Breaking Bad.</p>
          </div>
        `;
      } else {
        results.forEach((movie) => {
          const poster = movie.poster_display || movie.poster || './Images/TheaterLogoFinal.png';
          const rating = movie.imdb_rating ? `<span class="badge bg-danger mb-2"><i class="fa fa-star"></i> ${movie.imdb_rating}</span>` : '';
          const genres = movie.genres && movie.genres.length > 0 ? movie.genres.map(g => g.name).join(', ') : '';

          html += `
            <div class="col-md-3 col-sm-6 mb-4">
              <div class="card bg-dark text-white border-danger h-100 shadow-lg text-center p-2" style="border-radius: 8px;">
                <img src="${poster}" class="card-img-top mb-2" style="height: 320px; object-fit: cover; border-radius: 6px;" alt="${movie.title}">
                <div class="card-body p-2 d-flex flex-column justify-content-between">
                  <div>
                    <h5 class="card-title text-truncate mb-1" title="${movie.title}">${movie.title}</h5>
                    <div class="text-muted small mb-1">${movie.release_year || ''} ${genres ? '• ' + genres : ''}</div>
                    ${rating}
                  </div>
                  <div class="d-flex justify-content-center gap-2 mt-2">
                    <a onclick="movieSelected('${movie.slug || movie.id}')" class="btn btn-sm btn-danger text-white" href="javascript:void(0)">Details</a>
                    <button class="btn btn-sm btn-outline-light" onclick='api.playVideo(${JSON.stringify(movie)})'><i class="fa fa-play"></i> Play</button>
                  </div>
                </div>
              </div>
            </div>
          `;
        });
      }

      $('#movies').html(html);

      // Smooth scroll down to results
      const moviesElem = document.getElementById('movies');
      if (moviesElem) {
        moviesElem.scrollIntoView({ behavior: 'smooth', block: 'start' });
      }
    })
    .catch((err) => {
      console.error('Search error:', err);
      $('#movies').html(`<div class="col-12 text-center text-danger py-4">Error connecting to movie database.</div>`);
    });
}

function movieSelected(identifier) {
  sessionStorage.setItem('movieID', identifier);
  window.location = 'movie-min.html';
  return false;
}

function getMovie() {
  const movieID = sessionStorage.getItem('movieID') || 'inception';
  const endpoint = `http://127.0.0.1:8000/api/movies/${movieID}/`;

  fetch(endpoint)
    .then((res) => res.json())
    .then((res) => {
      if (!res.success || !res.data) {
        $('#movie').html(`<div class="alert alert-danger text-center">Movie not found.</div>`);
        return;
      }

      const movie = res.data;
      const poster = movie.poster_display || movie.poster || './Images/TheaterLogoFinal.png';
      const genres = movie.genres ? movie.genres.map(g => g.name).join(', ') : 'N/A';
      const castNames = movie.movie_cast && movie.movie_cast.length > 0
        ? movie.movie_cast.map(c => `${c.person.name} (${c.character_name || 'Cast'})`).join(', ')
        : (movie.cast && movie.cast.length > 0 ? movie.cast.map(c => c.name).join(', ') : 'N/A');
      const directors = movie.directors && movie.directors.length > 0
        ? movie.directors.map(d => d.name).join(', ')
        : 'N/A';
      const writers = movie.writers && movie.writers.length > 0
        ? movie.writers.map(w => w.name).join(', ')
        : 'N/A';

      const inWatchlist = movie.in_watchlist;
      const isFav = movie.is_favorite;

      const html = `
        <div class="row align-items-center mb-4 p-4 text-white" style="background: rgba(0,0,0,0.85); border-radius: 10px; border: 1px solid #dc3545;">
          <div class="col-md-4 text-center mb-3 mb-md-0">
            <img src="${poster}" class="img-fluid rounded shadow-lg" style="max-height: 440px; object-fit: cover; border: 2px solid #dc3545;" alt="${movie.title}">
          </div>
          <div class="col-md-8">
            <h1 class="display-5 fw-bold text-white mb-2">${movie.title}</h1>
            <p class="text-muted mb-3"><i class="fa fa-calendar-alt text-danger me-1"></i> Released: ${movie.release_year || movie.release_date || 'N/A'} | <i class="fa fa-clock text-danger me-1"></i> ${movie.duration || 'N/A'} | <i class="fa fa-certificate text-danger me-1"></i> ${movie.age_rating || 'PG-13'}</p>

            <ul class="list-group list-group-flush mb-4" style="background: transparent;">
              <li class="list-group-item bg-transparent text-white border-secondary"><strong>Genre:</strong> <span class="badge bg-danger ms-2">${genres}</span></li>
              <li class="list-group-item bg-transparent text-white border-secondary"><strong>IMDb Rating:</strong> <span class="text-warning fw-bold"><i class="fa fa-star"></i> ${movie.imdb_rating || 'N/A'} / 10</span></li>
              <li class="list-group-item bg-transparent text-white border-secondary"><strong>Director:</strong> ${directors}</li>
              <li class="list-group-item bg-transparent text-white border-secondary"><strong>Writers:</strong> ${writers}</li>
              <li class="list-group-item bg-transparent text-white border-secondary"><strong>Actors / Cast:</strong> ${castNames}</li>
            </ul>

            <div class="d-flex flex-wrap gap-2 mb-2">
              <button class="btn btn-danger btn-lg px-4" onclick='api.playVideo(${JSON.stringify(movie)})'>
                <i class="fa fa-play me-2"></i> Play Movie
              </button>
              ${movie.trailer_url ? `
                <a href="${movie.trailer_url}" target="_blank" class="btn btn-outline-light btn-lg">
                  <i class="fa fa-play-circle me-1"></i> Watch Trailer
                </a>
              ` : ''}
              <button id="detailWatchlistBtn" class="btn ${inWatchlist ? 'btn-success' : 'btn-outline-danger'} btn-lg" onclick="toggleMovieWatchlist(${movie.id}, this)">
                <i class="fa ${inWatchlist ? 'fa-check' : 'fa-bookmark'} me-1"></i> ${inWatchlist ? 'In Watchlist' : 'Add to Watchlist'}
              </button>
              <button id="detailFavoriteBtn" class="btn ${isFav ? 'btn-danger' : 'btn-outline-danger'} btn-lg" onclick="toggleMovieFavorite(${movie.id}, this)">
                <i class="fa fa-heart me-1"></i> ${isFav ? 'Favorited' : 'Favorite'}
              </button>
            </div>
          </div>
        </div>

        <div class="row mb-4">
          <div class="col-12 p-4 text-white" style="background: rgba(20,20,20,0.9); border-radius: 8px; border-left: 4px solid #dc3545;">
            <h3 class="text-danger mb-3">Plot Synopsis</h3>
            <p class="fs-5" style="line-height: 1.8;">${movie.description || 'No description available for this movie.'}</p>
            <hr class="border-secondary">
            <div class="d-flex justify-content-between align-items-center flex-wrap">
              <a href="home.html" class="btn btn-outline-danger"><i class="fa fa-arrow-left me-2"></i> Back to Streaming Home</a>
              <span class="text-muted"><i class="fa fa-eye me-1"></i> ${movie.views || 0} views</span>
            </div>
          </div>
        </div>

        <!-- Ratings and Reviews Section -->
        <div class="row mb-5">
          <div class="col-12 p-4 text-white" style="background: rgba(15,15,15,0.95); border-radius: 8px; border: 1px solid #333;">
            <h3 class="text-danger mb-4"><i class="fa fa-comments me-2"></i> User Ratings & Reviews</h3>

            <div id="reviewSubmissionBox" class="mb-4 p-3 border border-secondary rounded bg-dark">
              <h5 class="text-white mb-3">Leave a Review</h5>
              <div class="row g-3">
                <div class="col-md-3">
                  <label class="form-label text-muted">Rating (1 to 10):</label>
                  <select id="userRatingScore" class="form-select bg-black text-white border-secondary">
                    <option value="10">10 ★ (Masterpiece)</option>
                    <option value="9">9 ★ (Superb)</option>
                    <option value="8" selected>8 ★ (Very Good)</option>
                    <option value="7">7 ★ (Good)</option>
                    <option value="6">6 ★ (Fine)</option>
                    <option value="5">5 ★ (Average)</option>
                    <option value="4">4 ★ (Below Average)</option>
                    <option value="3">3 ★ (Poor)</option>
                    <option value="2">2 ★ (Terrible)</option>
                    <option value="1">1 ★ (Unwatchable)</option>
                  </select>
                </div>
                <div class="col-md-9">
                  <label class="form-label text-muted">Headline:</label>
                  <input type="text" id="userReviewTitle" class="form-control bg-black text-white border-secondary" placeholder="E.g., An absolute masterpiece of modern cinema!">
                </div>
                <div class="col-12">
                  <label class="form-label text-muted">Your Review:</label>
                  <textarea id="userReviewContent" rows="3" class="form-control bg-black text-white border-secondary" placeholder="Write your thoughts about the direction, story, acting..."></textarea>
                </div>
                <div class="col-12">
                  <button class="btn btn-danger px-4" onclick="submitMovieReview(${movie.id})"><i class="fa fa-paper-plane me-1"></i> Submit Review</button>
                  <span id="reviewMsgStatus" class="ms-3 text-info"></span>
                </div>
              </div>
            </div>

            <div id="movieReviewsList">
              <p class="text-muted">Loading reviews...</p>
            </div>
          </div>
        </div>
      `;

      $('#movie').html(html);

      // Load reviews
      loadMovieReviews(movie.id);
    })
    .catch((err) => {
      console.error(err);
      $('#movie').html(`<div class="alert alert-danger text-center">Failed to load movie details.</div>`);
    });
}

async function loadMovieReviews(movieId) {
  const res = await api.reviews.getMovieReviews(movieId);
  const container = document.getElementById('movieReviewsList');
  if (!container) return;

  const reviews = res.success && res.data && res.data.results ? res.data.results : [];
  if (reviews.length === 0) {
    container.innerHTML = `<p class="text-muted">No reviews yet. Be the first to share your thoughts!</p>`;
    return;
  }

  let html = '';
  reviews.forEach((r) => {
    const author = r.user ? (r.user.full_name || r.user.username) : 'Anonymous';
    html += `
      <div class="p-3 mb-3 border-bottom border-secondary bg-transparent">
        <div class="d-flex justify-content-between align-items-center mb-1">
          <strong class="text-danger"><i class="fa fa-user-circle me-1"></i> ${author}</strong>
          <span class="badge bg-warning text-dark"><i class="fa fa-star"></i> ${r.rating} / 10</span>
        </div>
        ${r.title ? `<h6 class="text-white mt-1 mb-1">${r.title}</h6>` : ''}
        <p class="text-light mb-1 small">${r.content || ''}</p>
        <span class="text-muted" style="font-size: 11px;">Posted: ${new Date(r.created_at).toLocaleDateString()}</span>
      </div>
    `;
  });
  container.innerHTML = html;
}

async function submitMovieReview(movieId) {
  if (!api.isAuthenticated()) {
    alert('Please log in first to submit a rating and review.');
    window.location.href = 'login.html';
    return;
  }

  const rating = document.getElementById('userRatingScore').value;
  const title = document.getElementById('userReviewTitle').value;
  const content = document.getElementById('userReviewContent').value;
  const statusEl = document.getElementById('reviewMsgStatus');

  statusEl.textContent = 'Submitting...';
  const res = await api.reviews.submitMovieReview(movieId, rating, title, content);
  if (res.success) {
    statusEl.textContent = 'Review saved!';
    document.getElementById('userReviewContent').value = '';
    loadMovieReviews(movieId);
  } else {
    statusEl.textContent = res.message || 'Error saving review.';
  }
}

async function toggleMovieWatchlist(movieId, btn) {
  if (!api.isAuthenticated()) {
    window.location.href = 'login.html';
    return;
  }
  const isAdded = btn.classList.contains('btn-success');
  if (isAdded) {
    await api.watchlist.removeByTarget(movieId, null);
    btn.className = 'btn btn-outline-danger btn-lg';
    btn.innerHTML = '<i class="fa fa-bookmark me-1"></i> Add to Watchlist';
  } else {
    await api.watchlist.addMovie(movieId);
    btn.className = 'btn btn-success btn-lg';
    btn.innerHTML = '<i class="fa fa-check me-1"></i> In Watchlist';
  }
}

async function toggleMovieFavorite(movieId, btn) {
  if (!api.isAuthenticated()) {
    window.location.href = 'login.html';
    return;
  }
  const isFav = btn.classList.contains('btn-danger') && !btn.classList.contains('btn-outline-danger');
  if (isFav) {
    btn.className = 'btn btn-outline-danger btn-lg';
    btn.innerHTML = '<i class="fa fa-heart me-1"></i> Favorite';
  } else {
    await api.favorites.addMovie(movieId);
    btn.className = 'btn btn-danger btn-lg';
    btn.innerHTML = '<i class="fa fa-heart me-1"></i> Favorited';
  }
}

$(document).ready(() => {
  $('#searchForm').on('submit', (e) => {
    e.preventDefault();
    getMovies($('#searchText').val());
  });
});
