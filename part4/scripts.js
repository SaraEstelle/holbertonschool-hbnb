/*
  scripts.js — HBnB Part 4
  Toute la logique JavaScript de l'application.
  Organisé par task pour la lisibilité.

  URL de l'API Flask (Part 3) — toujours lancée sur le port 5000
*/
const API_URL = 'http://127.0.0.1:5000/api/v1';

/*
  Variable globale — toutes les places récupérées de l'API.
  Stockée ici pour le filtre par prix (on ne re-fetch pas, on filtre localement).
*/
let allPlaces = [];

// ============================================================
// UTILITAIRES — réutilisés dans toutes les tasks
// ============================================================

/*
  getCookie(name)
  Lit un cookie par son nom depuis document.cookie.
  Retourne la valeur ou null si absent.

  Pourquoi ?
  document.cookie retourne une chaîne "token=abc; autre=xyz".
  Il faut splitter et chercher manuellement.
*/
function getCookie(name) {
    const cookies = document.cookie.split('; ');
    for (const cookie of cookies) {
        const [key, val] = cookie.split('=');
        if (key === name) return val;
    }
    return null;
}

/*
  getPlaceIdFromURL()
  Extrait ?id=<uuid> depuis l'URL courante.
  Utilisé dans place.html et add_review.html.
*/
function getPlaceIdFromURL() {
    const params = new URLSearchParams(window.location.search);
    return params.get('id');
}

/*
  showToast(message, type)
  Affiche une notification temporaire en bas à droite.
  type : 'success' | 'error'
*/
function showToast(message, type = 'success') {
    const toast = document.getElementById('toast');
    if (!toast) return;
    toast.textContent = message;
    toast.className = `toast toast-${type} show`;
    setTimeout(() => { toast.className = 'toast'; }, 3500);
}

/*
  updateLoginButton()
  Lit le cookie 'token'.
  Si connecté : remplace le bouton Login par "Logout".
  Si déconnecté : affiche le bouton Login.

  Appelé au chargement de chaque page.
*/
function updateLoginButton() {
    const token = getCookie('token');
    const loginLink = document.getElementById('login-link');
    if (!loginLink) return;

    if (token) {
        /* Connecté : transformer le lien en bouton Logout */
        loginLink.textContent = 'Logout';
        loginLink.className = 'logout-button';
        loginLink.href = '#';
        loginLink.onclick = (e) => {
            e.preventDefault();
            /* Supprimer le cookie en le faisant expirer immédiatement */
            document.cookie = 'token=; path=/; expires=Thu, 01 Jan 1970 00:00:00 GMT';
            window.location.href = 'index.html';
        };
    } else {
        /* Déconnecté : bouton Login standard */
        loginLink.textContent = 'Login';
        loginLink.className = 'login-button';
        loginLink.href = 'login.html';
        loginLink.onclick = null;
    }
}

// ============================================================
// TASK 1 — LOGIN
// ============================================================

/*
  loginUser(email, password)
  POST /api/v1/auth/login avec email + password.
  Si succès → stocke le token dans un cookie et redirige vers index.html.
  Si échec → affiche un message d'erreur dans le formulaire.
*/
async function loginUser(email, password) {
    const response = await fetch(`${API_URL}/auth/login`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ email, password })
    });

    if (response.ok) {
        const data = await response.json();
        /* Stocker le token en cookie accessible sur toutes les pages (path=/) */
        document.cookie = `token=${data.access_token}; path=/`;
        window.location.href = 'index.html';
    } else {
        /* Afficher le message d'erreur dans le formulaire */
        const errorDiv = document.getElementById('login-error');
        if (errorDiv) errorDiv.style.display = 'block';
    }
}

// ============================================================
// TASK 2 — INDEX (liste des places)
// ============================================================

/*
  setupPriceFilter()
  Ajoute les options au <select id="price-filter">.
  Options imposées par le correcteur : All, $10, $50, $100.
*/
function setupPriceFilter() {
    const select = document.getElementById('price-filter');
    if (!select) return;

    const options = [
        { value: 'all', label: 'All' },
        { value: '10',  label: '$10' },
        { value: '50',  label: '$50' },
        { value: '100', label: '$100' }
    ];

    options.forEach(({ value, label }) => {
        const option = document.createElement('option');
        option.value = value;
        option.textContent = label;
        select.appendChild(option);
    });
}

/*
  fetchPlaces(token)
  GET /api/v1/places/ — endpoint public, token optionnel.
  Stocke les places dans allPlaces et appelle displayPlaces().
*/
async function fetchPlaces(token) {
    const placesList = document.getElementById('places-list');
    if (placesList) {
        placesList.innerHTML = '<p class="loading-msg">Loading places...</p>';
    }

    const headers = {};
    if (token) headers['Authorization'] = `Bearer ${token}`;

    const response = await fetch(`${API_URL}/places/`, { headers });

    if (response.ok) {
        const places = await response.json();
        allPlaces = places;
        displayPlaces(places);
    } else {
        if (placesList) {
            placesList.innerHTML = '<p class="no-places-msg">Unable to load places. Is the API running?</p>';
        }
    }
}

/*
  displayPlaces(places)
  Crée les div.place-card pour chaque place et les ajoute dans #places-list.
  Chaque carte a : titre, prix formaté, bouton "View Details" qui pointe vers place.html?id=<uuid>
*/
function displayPlaces(places) {
    const placesList = document.getElementById('places-list');
    if (!placesList) return;

    placesList.innerHTML = '';

    if (places.length === 0) {
        placesList.innerHTML = '<p class="no-places-msg">No places available for this price range.</p>';
        return;
    }

    places.forEach(place => {
        const card = document.createElement('div');
        card.className = 'place-card';           /* classe obligatoire */
        card.dataset.price = place.price;         /* pour le filtre par prix */

        card.innerHTML = `
            <h2>${place.title}</h2>
            <span class="price-tag">$${place.price} / night</span>
            <a href="place.html?id=${place.id}" class="details-button">View Details</a>
        `;

        placesList.appendChild(card);
    });
}

/*
  filterByPrice(maxPrice)
  Affiche/cache les .place-card selon le prix maximum sélectionné.
  Ne re-fetch pas l'API — travaille sur les cartes déjà dans le DOM.
  Utilise dataset.price pour comparer (en Float).
*/
function filterByPrice(maxPrice) {
    const cards = document.querySelectorAll('.place-card');

    cards.forEach(card => {
        const price = parseFloat(card.dataset.price); /* convertir en nombre ! */

        if (maxPrice === 'all' || price <= parseFloat(maxPrice)) {
            card.style.display = 'flex';
        } else {
            card.style.display = 'none';
        }
    });
}

// ============================================================
// TASK 3 — PLACE DETAILS
// ============================================================

/*
  checkAuthForPlacePage(placeId)
  Vérifie le token et affiche/cache la section #add-review.
  Lance ensuite fetchPlaceDetails().
*/
function checkAuthForPlacePage(placeId) {
    const token = getCookie('token');
    const addReviewSection = document.getElementById('add-review');

    if (addReviewSection) {
        /* Montrer le formulaire review seulement si connecté */
        addReviewSection.style.display = token ? 'block' : 'none';
    }

    if (!placeId) {
        /* Pas d'ID dans l'URL → retour à l'accueil */
        window.location.href = 'index.html';
        return;
    }

    fetchPlaceDetails(token, placeId);
}

/*
  fetchPlaceDetails(token, placeId)
  Deux appels en parallèle :
  1. GET /places/<id>             → infos place (host, prix, desc, amenities)
  2. GET /places/<id>/reviews     → liste des reviews
*/
async function fetchPlaceDetails(token, placeId) {
    const headers = {};
    if (token) headers['Authorization'] = `Bearer ${token}`;

    /* Les deux fetches en parallèle — plus rapide qu'en séquence */
    const [placeRes, reviewsRes] = await Promise.all([
        fetch(`${API_URL}/places/${placeId}`, { headers }),
        fetch(`${API_URL}/places/${placeId}/reviews`, { headers })
    ]);

    if (!placeRes.ok) {
        const detailsSection = document.getElementById('place-details');
        if (detailsSection) {
            detailsSection.innerHTML = '<p style="color:#999;padding:40px;text-align:center">Place not found.</p>';
        }
        return;
    }

    const place = await placeRes.json();
    const reviews = reviewsRes.ok ? await reviewsRes.json() : [];

    displayPlaceDetails(place, reviews);
}

/*
  displayPlaceDetails(place, reviews)
  Injecte le HTML de la place et ses reviews dans le DOM.
  Classes obligatoires utilisées : place-info, review-card.
*/
function displayPlaceDetails(place, reviews) {
    const detailsSection = document.getElementById('place-details');
    const reviewsSection = document.getElementById('reviews');

    if (!detailsSection) return;

    /* Mettre à jour le titre de la page */
    document.title = `HBnB — ${place.title}`;

    /* Construire les amenities */
    const amenitiesHTML = place.amenities && place.amenities.length > 0
        ? place.amenities.map(a => `<span class="amenity-tag">${a.name}</span>`).join('')
        : '<span style="color:#999">None listed</span>';

    /* Infos de l'hôte */
    const ownerName = place.owner
        ? `${place.owner.first_name} ${place.owner.last_name}`
        : 'Unknown host';

    /* Injecter les détails — classe obligatoire : place-info */
    detailsSection.innerHTML = `
        <h1>${place.title}</h1>
        <div class="place-info">
            <div class="place-info-item">
                <span class="place-info-label">Host</span>
                <span class="place-info-value">${ownerName}</span>
            </div>
            <div class="place-info-item">
                <span class="place-info-label">Price per night</span>
                <span class="place-info-value price">$${place.price}</span>
            </div>
            <div class="place-info-item" style="grid-column: 1 / -1">
                <span class="place-info-label">Description</span>
                <span class="place-info-value" style="font-weight:600">${place.description || 'No description provided.'}</span>
            </div>
            <div class="place-info-item" style="grid-column: 1 / -1">
                <span class="place-info-label">Amenities</span>
                <div class="amenities-list">${amenitiesHTML}</div>
            </div>
        </div>
    `;

    /* Injecter les reviews — classe obligatoire : review-card */
    if (reviewsSection) {
        reviewsSection.innerHTML = `<h2>Reviews (${reviews.length})</h2>`;

        if (reviews.length === 0) {
            reviewsSection.innerHTML += '<p style="color:#999;padding:10px 0">No reviews yet. Be the first!</p>';
        } else {
            reviews.forEach(review => {
                /* Générer les étoiles */
                const stars = '★'.repeat(review.rating) + '☆'.repeat(5 - review.rating);
                const card = document.createElement('div');
                card.className = 'review-card';    /* classe obligatoire */
                card.innerHTML = `
                    <p class="reviewer-name">${review.user_id || 'Anonymous'}</p>
                    <p class="review-text">${review.text}</p>
                    <span class="stars">${stars}</span>
                `;
                reviewsSection.appendChild(card);
            });
        }
    }

    /* Stocker l'ID de la place sur le formulaire pour la soumission */
    const reviewForm = document.getElementById('review-form');
    if (reviewForm) reviewForm.dataset.placeId = place.id;
}

// ============================================================
// TASK 4 — ADD REVIEW FORM
// ============================================================

/*
  submitReview(token, placeId, text, rating)
  POST /api/v1/reviews/ avec le token JWT.
  Retourne la réponse brute pour que l'appelant la gère.
*/
async function submitReview(token, placeId, text, rating) {
    return fetch(`${API_URL}/reviews/`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${token}`
        },
        body: JSON.stringify({
            text: text,
            rating: parseInt(rating, 10),   /* toujours convertir en entier */
            place_id: placeId
        })
    });
}

/*
  handleReviewResponse(response, form)
  Gère la réponse après soumission.
  Succès → toast + reset + redirection.
  Échec → toast erreur.
*/
async function handleReviewResponse(response, form) {
    if (response.ok) {
        showToast('Review submitted! Thank you.', 'success');
        if (form) form.reset();
        /* Courte pause pour que le toast soit visible avant la redirection */
        setTimeout(() => { window.location.href = 'index.html'; }, 1500);
    } else {
        const data = await response.json().catch(() => ({}));
        const msg = data.error || 'Failed to submit review.';
        showToast(msg, 'error');
    }
}

/*
  loadPlaceTitleForReviewPage(placeId, token)
  Sur add_review.html, récupère le nom de la place pour l'afficher en titre.
*/
async function loadPlaceTitleForReviewPage(placeId, token) {
    const titleEl = document.getElementById('place-title');
    if (!titleEl || !placeId) return;

    const headers = token ? { 'Authorization': `Bearer ${token}` } : {};
    const res = await fetch(`${API_URL}/places/${placeId}`, { headers });
    if (res.ok) {
        const place = await res.json();
        titleEl.textContent = `Reviewing: ${place.title}`;
        document.title = `HBnB — Review: ${place.title}`;
    }
}

// ============================================================
// POINT D'ENTRÉE — exécuté quand la page est complètement chargée
// ============================================================

document.addEventListener('DOMContentLoaded', () => {

    /* Mettre à jour le bouton Login/Logout sur toutes les pages */
    updateLoginButton();

    // ----------------------------------------------------------
    // TASK 1 : page login.html
    // ----------------------------------------------------------
    const loginForm = document.getElementById('login-form');
    if (loginForm) {
        /* Si déjà connecté → pas besoin d'être sur login.html */
        if (getCookie('token')) {
            window.location.href = 'index.html';
            return;
        }

        loginForm.addEventListener('submit', async (event) => {
            event.preventDefault(); /* bloque le rechargement de page */
            const email    = document.getElementById('email').value.trim();
            const password = document.getElementById('password').value;
            await loginUser(email, password);
        });
    }

    // ----------------------------------------------------------
    // TASK 2 : page index.html
    // ----------------------------------------------------------
    if (document.getElementById('places-list')) {
        const token = getCookie('token');

        /* Remplir les options du filtre prix */
        setupPriceFilter();

        /* Charger les places */
        fetchPlaces(token);

        /* Écouter le changement de filtre */
        const priceFilter = document.getElementById('price-filter');
        if (priceFilter) {
            priceFilter.addEventListener('change', (e) => {
                filterByPrice(e.target.value);
            });
        }
    }

    // ----------------------------------------------------------
    // TASK 3 : page place.html
    // ----------------------------------------------------------
    if (document.getElementById('place-details')) {
        const placeId = getPlaceIdFromURL();
        checkAuthForPlacePage(placeId);

        /* Écouter le formulaire de review intégré dans place.html */
        const inlineForm = document.getElementById('review-form');
        if (inlineForm) {
            inlineForm.addEventListener('submit', async (event) => {
                event.preventDefault();
                const token   = getCookie('token');
                const pid     = inlineForm.dataset.placeId || placeId;
                const text    = document.getElementById('review-text').value.trim();
                const rating  = document.getElementById('rating').value;

                if (!token) { showToast('Please log in to submit a review.', 'error'); return; }
                if (!text)  { showToast('Please write your review.', 'error'); return; }
                if (!rating) { showToast('Please select a rating.', 'error'); return; }

                const response = await submitReview(token, pid, text, rating);
                await handleReviewResponse(response, inlineForm);
            });
        }
    }

    // ----------------------------------------------------------
    // TASK 4 : page add_review.html
    // ----------------------------------------------------------
    const reviewPageForm = document.getElementById('review-form');
    const isAddReviewPage = reviewPageForm
        && !document.getElementById('places-list')
        && !document.getElementById('place-details');

    if (isAddReviewPage) {
        const token   = getCookie('token');
        const placeId = getPlaceIdFromURL();

        /* Si pas connecté → redirection immédiate */
        if (!token) {
            window.location.href = 'index.html';
            return;
        }

        /* Charger le nom de la place pour l'afficher en titre */
        loadPlaceTitleForReviewPage(placeId, token);

        reviewPageForm.addEventListener('submit', async (event) => {
            event.preventDefault();
            const text   = document.getElementById('review').value.trim();
            const rating = document.getElementById('rating').value;

            if (!text)   { showToast('Please write your review.', 'error'); return; }
            if (!rating) { showToast('Please select a rating.', 'error'); return; }

            const response = await submitReview(token, placeId, text, rating);
            await handleReviewResponse(response, reviewPageForm);
        });
    }

});
