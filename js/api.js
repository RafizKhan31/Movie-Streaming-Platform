/**
 * The Code Wizerd Movie Site - Client API SDK
 * Connects frontend HTML pages to the Django REST Framework MySQL backend.
 */

const API_BASE_URL = 'http://127.0.0.1:8000/api';

const api = {
  // -------------------------------------------------------------
  // Storage & Token Management
  // -------------------------------------------------------------
  getToken() {
    return localStorage.getItem('access_token');
  },
  getRefreshToken() {
    return localStorage.getItem('refresh_token');
  },
  getUser() {
    const u = localStorage.getItem('user');
    try {
      return u ? JSON.parse(u) : null;
    } catch (e) {
      return null;
    }
  },
  setSession(access, refresh, user) {
    if (access) localStorage.setItem('access_token', access);
    if (refresh) localStorage.setItem('refresh_token', refresh);
    if (user) localStorage.setItem('user', JSON.stringify(user));
  },
  clearSession() {
    localStorage.removeItem('access_token');
    localStorage.removeItem('refresh_token');
    localStorage.removeItem('user');
  },
  isAuthenticated() {
    return !!this.getToken();
  },

  // -------------------------------------------------------------
  // Base HTTP Request Wrapper
  // -------------------------------------------------------------
  async request(endpoint, options = {}) {
    const url = endpoint.startsWith('http') ? endpoint : `${API_BASE_URL}${endpoint}`;
    const headers = options.headers || {};

    if (!(options.body instanceof FormData)) {
      headers['Content-Type'] = 'application/json';
    }

    const token = this.getToken();
    if (token) {
      headers['Authorization'] = `Bearer ${token}`;
    }

    options.headers = headers;

    try {
      let response = await fetch(url, options);

      // Handle 401 Unauthorized - attempt token refresh
      if (response.status === 401 && this.getRefreshToken()) {
        const refreshed = await this.refreshToken();
        if (refreshed) {
          headers['Authorization'] = `Bearer ${this.getToken()}`;
          response = await fetch(url, options);
        } else {
          this.clearSession();
        }
      }

      const data = await response.json();
      return data;
    } catch (err) {
      console.error('API Request Error:', err);
      return { success: false, message: err.message, errors: err };
    }
  },

  async refreshToken() {
    try {
      const refresh = this.getRefreshToken();
      if (!refresh) return false;
      const res = await fetch(`${API_BASE_URL}/auth/token/refresh/`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ refresh }),
      });
      if (res.ok) {
        const data = await res.json();
        if (data.data && data.data.access) {
          localStorage.setItem('access_token', data.data.access);
          return true;
        }
      }
      return false;
    } catch (e) {
      return false;
    }
  },

  // -------------------------------------------------------------
  // Auth Endpoints
  // -------------------------------------------------------------
  auth: {
    async register(userData) {
      return await api.request('/auth/register/', {
        method: 'POST',
        body: JSON.stringify(userData),
      });
    },
    async login(email, password) {
      const res = await api.request('/auth/login/', {
        method: 'POST',
        body: JSON.stringify({ email, password }),
      });
      if (res.success && res.data) {
        api.setSession(res.data.access, res.data.refresh, res.data.user);
      }
      return res;
    },
    async logout() {
      const refresh = api.getRefreshToken();
      if (refresh) {
        await api.request('/auth/logout/', {
          method: 'POST',
          body: JSON.stringify({ refresh }),
        });
      }
      api.clearSession();
      window.location.replace('login.html');
    },
    async getProfile() {
      return await api.request('/auth/profile/');
    },
    async updateProfile(formData) {
      return await api.request('/auth/profile/', {
        method: 'PUT',
        body: formData,
      });
    },
    async changePassword(oldPassword, newPassword, confirmNewPassword) {
      return await api.request('/auth/change-password/', {
        method: 'POST',
        body: JSON.stringify({
          old_password: oldPassword,
          new_password: newPassword,
          confirm_new_password: confirmNewPassword,
        }),
      });
    },
  },

  // -------------------------------------------------------------
  // Movies & TV Series Endpoints
  // -------------------------------------------------------------
  movies: {
    async list(params = {}) {
      const q = new URLSearchParams(params).toString();
      return await api.request(`/movies/?${q}`);
    },
    async get(idOrSlug) {
      return await api.request(`/movies/${idOrSlug}/`);
    },
    async trending() {
      return await api.request('/movies/trending/');
    },
    async popular() {
      return await api.request('/movies/popular/');
    },
    async latest() {
      return await api.request('/movies/latest/');
    },
    async featured() {
      return await api.request('/movies/featured/');
    },
    async topRated() {
      return await api.request('/movies/top-rated/');
    },
    async submit(formData) {
      return await api.request('/movies/submit/', {
        method: 'POST',
        body: formData,
      });
    },
  },

  series: {
    async list(params = {}) {
      const q = new URLSearchParams(params).toString();
      return await api.request(`/series/?${q}`);
    },
    async get(idOrSlug) {
      return await api.request(`/series/${idOrSlug}/`);
    },
    async seasons(idOrSlug) {
      return await api.request(`/series/${idOrSlug}/seasons/`);
    },
    async episodes(idOrSlug) {
      return await api.request(`/series/${idOrSlug}/episodes/`);
    },
    async episode(id) {
      return await api.request(`/episodes/${id}/`);
    },
  },

  genres: {
    async list() {
      return await api.request('/genres/');
    },
    async get(slug) {
      return await api.request(`/genres/${slug}/`);
    },
    async movies(slug) {
      return await api.request(`/genres/${slug}/movies/`);
    },
  },

  search: {
    async query(q, type = 'all') {
      return await api.request(`/search/?q=${encodeURIComponent(q)}&type=${type}`);
    },
  },

  // -------------------------------------------------------------
  // Watchlist & Favorites
  // -------------------------------------------------------------
  watchlist: {
    async list() {
      return await api.request('/watchlist/');
    },
    async addMovie(movieId) {
      return await api.request('/watchlist/', {
        method: 'POST',
        body: JSON.stringify({ movie_id: movieId }),
      });
    },
    async addSeries(seriesId) {
      return await api.request('/watchlist/', {
        method: 'POST',
        body: JSON.stringify({ series_id: seriesId }),
      });
    },
    async remove(id) {
      return await api.request(`/watchlist/${id}/`, {
        method: 'DELETE',
      });
    },
    async removeByTarget(movieId = null, seriesId = null) {
      const q = movieId ? `movie_id=${movieId}` : `series_id=${seriesId}`;
      return await api.request(`/watchlist/?${q}`, {
        method: 'DELETE',
      });
    },
  },

  favorites: {
    async list() {
      return await api.request('/favorites/');
    },
    async addMovie(movieId) {
      return await api.request('/favorites/', {
        method: 'POST',
        body: JSON.stringify({ movie_id: movieId }),
      });
    },
    async addSeries(seriesId) {
      return await api.request('/favorites/', {
        method: 'POST',
        body: JSON.stringify({ series_id: seriesId }),
      });
    },
    async remove(id) {
      return await api.request(`/favorites/${id}/`, {
        method: 'DELETE',
      });
    },
  },

  // -------------------------------------------------------------
  // Watch History & Continue Watching
  // -------------------------------------------------------------
  history: {
    async list(completed = null) {
      let endpoint = '/history/';
      if (completed !== null) endpoint += `?completed=${completed}`;
      return await api.request(endpoint);
    },
    async update(data) {
      return await api.request('/history/', {
        method: 'POST',
        body: JSON.stringify(data),
      });
    },
    async remove(id) {
      return await api.request(`/history/${id}/`, {
        method: 'DELETE',
      });
    },
  },

  // -------------------------------------------------------------
  // Reviews & Ratings
  // -------------------------------------------------------------
  reviews: {
    async getMovieReviews(movieId) {
      return await api.request(`/movies/${movieId}/reviews/`);
    },
    async submitMovieReview(movieId, rating, title, content) {
      return await api.request(`/movies/${movieId}/reviews/`, {
        method: 'POST',
        body: JSON.stringify({ rating, title, content }),
      });
    },
    async getSeriesReviews(seriesId) {
      return await api.request(`/series/${seriesId}/reviews/`);
    },
    async submitSeriesReview(seriesId, rating, title, content) {
      return await api.request(`/series/${seriesId}/reviews/`, {
        method: 'POST',
        body: JSON.stringify({ rating, title, content }),
      });
    },
    async delete(id) {
      return await api.request(`/reviews/${id}/`, {
        method: 'DELETE',
      });
    },
  },

  // -------------------------------------------------------------
  // Streaming & Subtitles
  // -------------------------------------------------------------
  streaming: {
    async getMovieStreamInfo(movieId) {
      return await api.request(`/movies/${movieId}/stream/?format=json`);
    },
    async getEpisodeStreamInfo(episodeId) {
      return await api.request(`/episodes/${episodeId}/stream/?format=json`);
    },
    async getMovieSubtitles(movieId) {
      return await api.request(`/movies/${movieId}/subtitles/`);
    },
    async getEpisodeSubtitles(episodeId) {
      return await api.request(`/episodes/${episodeId}/subtitles/`);
    },
  },

  home: {
    async getData() {
      return await api.request('/home/');
    },
  },

  contact: {
    async send(data) {
      return await api.request('/contact/', {
        method: 'POST',
        body: JSON.stringify(data),
      });
    },
  },

  subscriptions: {
    async plans() {
      return await api.request('/subscriptions/plans/');
    },
    async subscribe(planId) {
      return await api.request('/subscriptions/subscribe/', {
        method: 'POST',
        body: JSON.stringify({ plan_id: planId }),
      });
    },
    async mySubscription() {
      return await api.request('/subscriptions/my-subscription/');
    },
  },

  // -------------------------------------------------------------
  // UI Helpers (Navbar, Video Player, Continue Watching)
  // -------------------------------------------------------------
  initNavbarAuth() {
    const user = this.getUser();
    const logoutBtnContainers = document.querySelectorAll('button[onclick="logout()"]');

    logoutBtnContainers.forEach((btn) => {
      const parent = btn.parentElement;
      if (user) {
        parent.innerHTML = `
          <div class="dropdown d-inline-block">
            <button class="btn btn-outline-danger dropdown-toggle" type="button" id="userMenuBtn" data-bs-toggle="dropdown" aria-expanded="false" style="font-size: 16px;">
              <i class="fa fa-user-circle"></i> ${user.first_name || user.username}
            </button>
            <ul class="dropdown-menu dropdown-menu-dark" aria-labelledby="userMenuBtn">
              <li><a class="dropdown-item" href="javascript:void(0)" onclick="api.showWatchlistModal()"><i class="fa fa-bookmark text-danger me-2"></i> My Watchlist</a></li>
              <li><a class="dropdown-item" href="javascript:void(0)" onclick="api.showProfileModal()"><i class="fa fa-id-card text-info me-2"></i> Profile & History</a></li>
              <li><hr class="dropdown-divider"></li>
              <li><a class="dropdown-item text-danger" href="javascript:void(0)" onclick="api.auth.logout()"><i class="fa fa-sign-out-alt me-2"></i> Logout</a></li>
            </ul>
          </div>
        `;
      } else {
        parent.innerHTML = `
          <a href="login.html" class="btn btn-danger" style="font-size: 16px;">Login</a>
        `;
      }
    });
  },

  // Built-in Video Player Modal
  async playVideo(item) {
    let streamUrl = '';
    let subtitles = [];
    let isMovie = !!item.id;
    let itemId = item.id;

    // Fetch stream information
    if (item.episode_id) {
      const res = await this.streaming.getEpisodeStreamInfo(item.episode_id);
      if (res.success && res.data) {
        streamUrl = res.data.stream_url;
        subtitles = res.data.subtitles || [];
      }
    } else {
      const res = await this.streaming.getMovieStreamInfo(item.id);
      if (res.success && res.data) {
        streamUrl = res.data.stream_url;
        subtitles = res.data.subtitles || [];
      } else if (item.trailer_url) {
        streamUrl = item.trailer_url;
      }
    }

    if (!streamUrl) {
      streamUrl = item.trailer_url || 'https://commondatastorage.googleapis.com/gtv-videos-bucket/sample/BigBuckBunny.mp4';
    }

    // Embed or HTML5 video
    let modalEl = document.getElementById('streamingVideoModal');
    if (!modalEl) {
      modalEl = document.createElement('div');
      modalEl.id = 'streamingVideoModal';
      modalEl.className = 'modal fade';
      modalEl.tabIndex = -1;
      modalEl.innerHTML = `
        <div class="modal-dialog modal-xl modal-dialog-centered">
          <div class="modal-content bg-dark text-white border-danger shadow-lg">
            <div class="modal-header border-secondary">
              <h5 class="modal-title text-danger" id="videoModalTitle"><i class="fa fa-play-circle me-2"></i> Now Playing</h5>
              <button type="button" class="btn-close btn-close-white" data-bs-dismiss="modal" aria-label="Close"></button>
            </div>
            <div class="modal-body p-0" id="videoModalBody" style="background:#000; min-height: 400px; display:flex; align-items:center; justify-content:center;">
            </div>
            <div class="modal-footer border-secondary justify-content-between">
              <div id="videoSubtitlesContainer" class="d-flex align-items-center">
                <span class="me-2 text-muted"><i class="fa fa-closed-captioning"></i> Subtitles:</span>
                <select id="subtitleSelect" class="form-select form-select-sm bg-dark text-white border-secondary" style="width: auto;">
                  <option value="none">Off</option>
                </select>
              </div>
              <div id="videoHistoryStatus" class="text-muted small"></div>
              <button type="button" class="btn btn-outline-danger" data-bs-dismiss="modal">Close</button>
            </div>
          </div>
        </div>
      `;
      document.body.appendChild(modalEl);
    }

    const titleEl = document.getElementById('videoModalTitle');
    const bodyEl = document.getElementById('videoModalBody');
    const statusEl = document.getElementById('videoHistoryStatus');
    const subtitleSelect = document.getElementById('subtitleSelect');

    titleEl.innerHTML = `<i class="fa fa-film me-2"></i> ${item.title || 'Movie Streaming'}`;

    // If stream URL is YouTube, render iframe
    if (streamUrl.includes('youtube.com') || streamUrl.includes('youtu.be')) {
      let ytId = '';
      if (streamUrl.includes('youtu.be/')) {
        ytId = streamUrl.split('youtu.be/')[1].split('?')[0].split('&')[0];
      } else if (streamUrl.includes('watch?v=' || streamUrl.includes('&v='))) {
        ytId = streamUrl.split('v=')[1].split('&')[0];
      }
      bodyEl.innerHTML = `
        <iframe width="100%" height="520" src="https://www.youtube.com/embed/${ytId}?autoplay=1"
          frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen>
        </iframe>
      `;
      statusEl.textContent = 'Previewing trailer / stream.';
    } else {
      // HTML5 video player with track elements
      let trackTags = '';
      subtitleSelect.innerHTML = '<option value="none">Off</option>';
      subtitles.forEach((sub, idx) => {
        const fileUrl = sub.file_url || `${API_BASE_URL}/streaming/subtitles/${sub.id}/`;
        trackTags += `<track kind="subtitles" src="${fileUrl}" srclang="${sub.language}" label="${sub.label}" ${sub.is_default ? 'default' : ''}>`;
        subtitleSelect.innerHTML += `<option value="${idx}">${sub.label} (${sub.language})</option>`;
      });

      bodyEl.innerHTML = `
        <video id="html5VideoPlayer" controls autoplay style="width: 100%; height: 520px; background: #000;">
          <source src="${streamUrl}" type="video/mp4">
          ${trackTags}
          Your browser does not support the video tag.
        </video>
      `;

      const video = document.getElementById('html5VideoPlayer');

      // Subtitle switcher
      subtitleSelect.onchange = () => {
        const selected = subtitleSelect.value;
        for (let i = 0; i < video.textTracks.length; i++) {
          if (selected === 'none') {
            video.textTracks[i].mode = 'disabled';
          } else if (i === parseInt(selected)) {
            video.textTracks[i].mode = 'showing';
          } else {
            video.textTracks[i].mode = 'disabled';
          }
        }
      };

      // Periodic watch progress recording (every 5 seconds)
      let progressTimer = null;
      if (api.isAuthenticated()) {
        const saveProgress = async () => {
          if (video && video.duration) {
            const current = video.currentTime;
            const dur = video.duration;
            const payload = item.episode_id
              ? { episode_id: item.episode_id, current_position: current, duration: dur }
              : { movie_id: itemId, current_position: current, duration: dur };
            await api.history.update(payload);
            const pct = Math.round((current / dur) * 100);
            statusEl.textContent = `Progress saved: ${pct}%`;
          }
        };

        progressTimer = setInterval(saveProgress, 5000);
        video.onpause = saveProgress;
      }

      modalEl.addEventListener('hidden.bs.modal', () => {
        if (progressTimer) clearInterval(progressTimer);
        bodyEl.innerHTML = '';
      }, { once: true });
    }

    const modal = new bootstrap.Modal(modalEl);
    modal.show();
  },

  // Watchlist Modal
  async showWatchlistModal() {
    if (!this.isAuthenticated()) {
      window.location.href = 'login.html';
      return;
    }

    const res = await this.watchlist.list();
    const items = res.success ? res.data : [];

    let listHtml = '';
    if (items.length === 0) {
      listHtml = `<div class="p-4 text-center text-muted"><h5>Your watchlist is currently empty.</h5><p>Explore movies and click "Add to Watchlist" to save them here!</p></div>`;
    } else {
      listHtml = `<div class="row g-3 p-3">`;
      items.forEach((item) => {
        const content = item.movie || item.series;
        if (!content) return;
        const poster = content.poster_display || content.poster || 'Images/TheaterLogoFinal.png';
        listHtml += `
          <div class="col-md-4 col-sm-6 text-center">
            <div class="card bg-black text-white border-danger h-100 p-2 shadow">
              <img src="${poster}" class="card-img-top" style="height: 220px; object-fit: cover; border-radius: 4px;" alt="${content.title}">
              <div class="card-body p-2">
                <h6 class="card-title text-truncate">${content.title}</h6>
                <div class="small text-danger mb-2"><i class="fa fa-star"></i> ${content.imdb_rating || 'N/A'}</div>
                <div class="d-flex justify-content-center gap-2">
                  <button class="btn btn-sm btn-danger" onclick='api.playVideo(${JSON.stringify(content)})'><i class="fa fa-play"></i> Play</button>
                  <button class="btn btn-sm btn-outline-secondary" onclick="api.removeFromWatchlist(${item.id}, this)"><i class="fa fa-trash"></i></button>
                </div>
              </div>
            </div>
          </div>
        `;
      });
      listHtml += `</div>`;
    }

    let modalEl = document.getElementById('watchlistModal');
    if (!modalEl) {
      modalEl = document.createElement('div');
      modalEl.id = 'watchlistModal';
      modalEl.className = 'modal fade';
      modalEl.tabIndex = -1;
      modalEl.innerHTML = `
        <div class="modal-dialog modal-lg modal-dialog-centered">
          <div class="modal-content bg-dark text-white border-danger">
            <div class="modal-header border-secondary">
              <h5 class="modal-title text-danger"><i class="fa fa-bookmark me-2"></i> My Watchlist</h5>
              <button type="button" class="btn-close btn-close-white" data-bs-dismiss="modal"></button>
            </div>
            <div class="modal-body p-0" id="watchlistModalBody"></div>
          </div>
        </div>
      `;
      document.body.appendChild(modalEl);
    }

    document.getElementById('watchlistModalBody').innerHTML = listHtml;
    const modal = new bootstrap.Modal(modalEl);
    modal.show();
  },

  async removeFromWatchlist(id, btn) {
    const res = await this.watchlist.remove(id);
    if (res.success) {
      const card = btn.closest('.col-md-4');
      if (card) card.remove();
    }
  },

  // Profile Modal
  async showProfileModal() {
    if (!this.isAuthenticated()) {
      window.location.href = 'login.html';
      return;
    }
    const res = await this.auth.getProfile();
    const user = res.success ? res.data : this.getUser();

    // Fetch history
    const histRes = await this.history.list();
    const historyItems = histRes.success ? histRes.data : [];

    let historyHtml = '<p class="text-muted small">No watch history yet.</p>';
    if (historyItems.length > 0) {
      historyHtml = '<div class="list-group list-group-flush">';
      historyItems.slice(0, 5).forEach((h) => {
        const title = h.movie ? h.movie.title : (h.episode ? h.episode.title : 'Content');
        historyHtml += `
          <div class="list-group-item bg-transparent text-white border-secondary p-2 d-flex justify-content-between align-items-center">
            <div>
              <strong>${title}</strong>
              <div class="text-muted small">${h.progress_display}</div>
            </div>
            <span class="badge bg-danger">${h.progress_percentage}%</span>
          </div>
        `;
      });
      historyHtml += '</div>';
    }

    let modalEl = document.getElementById('profileModal');
    if (!modalEl) {
      modalEl = document.createElement('div');
      modalEl.id = 'profileModal';
      modalEl.className = 'modal fade';
      modalEl.tabIndex = -1;
      modalEl.innerHTML = `
        <div class="modal-dialog modal-dialog-centered">
          <div class="modal-content bg-dark text-white border-danger shadow">
            <div class="modal-header border-secondary">
              <h5 class="modal-title text-danger"><i class="fa fa-user-circle me-2"></i> User Profile</h5>
              <button type="button" class="btn-close btn-close-white" data-bs-dismiss="modal"></button>
            </div>
            <div class="modal-body">
              <div class="text-center mb-4">
                <i class="fa fa-user-circle fa-5x text-danger mb-2"></i>
                <h4 id="profUsername" class="mb-0"></h4>
                <p id="profEmail" class="text-muted"></p>
                <span id="profBadge" class="badge bg-warning text-dark">Free Member</span>
              </div>
              <h6 class="text-danger border-bottom border-secondary pb-2 mb-3"><i class="fa fa-history me-2"></i> Recent Watch History</h6>
              <div id="profHistoryContainer"></div>
            </div>
          </div>
        </div>
      `;
      document.body.appendChild(modalEl);
    }

    document.getElementById('profUsername').textContent = user.full_name || user.username;
    document.getElementById('profEmail').textContent = user.email;
    document.getElementById('profBadge').textContent = user.is_premium ? '★ Premium Member' : 'Standard Member';
    document.getElementById('profHistoryContainer').innerHTML = historyHtml;

    const modal = new bootstrap.Modal(modalEl);
    modal.show();
  },

  // Continue Watching Section Loader
  async renderContinueWatching(containerId = 'continueWatchingSection') {
    if (!this.isAuthenticated()) return;
    const res = await this.history.list(false);
    if (!res.success || !res.data || res.data.length === 0) return;

    let targetEl = document.getElementById(containerId);
    if (!targetEl) {
      // Create section dynamically right before main movies section
      const mainContainer = document.querySelector('.maincontainer') || document.querySelector('.main-content');
      if (!mainContainer) return;

      targetEl = document.createElement('div');
      targetEl.id = containerId;
      targetEl.className = 'container my-4';
      mainContainer.parentNode.insertBefore(targetEl, mainContainer);
    }

    let cardsHtml = `
      <div class="d-flex align-items-center mb-3">
        <h3 class="text-white mb-0 me-3"><i class="fa fa-history text-danger"></i> Continue Watching</h3>
        <div class="flex-grow-1 border-bottom border-danger"></div>
      </div>
      <div class="row row-cols-1 row-cols-md-3 row-cols-lg-4 g-3">
    `;

    res.data.forEach((item) => {
      const content = item.movie || item.episode;
      if (!content) return;
      const title = item.movie ? item.movie.title : `${content.title} (${item.episode.series_title || ''})`;
      const poster = content.poster_display || content.thumbnail_display || 'Images/TheaterLogoFinal.png';
      const pct = item.progress_percentage || 0;

      cardsHtml += `
        <div class="col">
          <div class="card bg-black text-white border-danger shadow h-100" style="overflow: hidden;">
            <div class="position-relative">
              <img src="${poster}" class="card-img-top" style="height: 180px; object-fit: cover;" alt="${title}">
              <div class="progress" style="height: 6px; border-radius: 0;">
                <div class="progress-bar bg-danger" role="progressbar" style="width: ${pct}%;" aria-valuenow="${pct}" aria-valuemin="0" aria-valuemax="100"></div>
              </div>
            </div>
            <div class="card-body p-3 d-flex flex-column justify-content-between">
              <div>
                <h6 class="card-title text-truncate mb-1">${title}</h6>
                <div class="small text-muted mb-2">${item.progress_display}</div>
              </div>
              <button class="btn btn-sm btn-danger w-100" onclick='api.playVideo(${JSON.stringify(content)})'>
                <i class="fa fa-play me-1"></i> Resume Play
              </button>
            </div>
          </div>
        </div>
      `;
    });

    cardsHtml += `</div><hr class="border-secondary my-4">`;
    targetEl.innerHTML = cardsHtml;
  },
};

// Initialize navbar on window load
document.addEventListener('DOMContentLoaded', () => {
  api.initNavbarAuth();
  if (document.body.id !== 'stop-scrolling') {
    api.renderContinueWatching();
  }
});
