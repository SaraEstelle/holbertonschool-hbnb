-- ============================================================
-- HBnB — Tests CRUD complets
-- Organises par type : CRUD, Auth, RBAC, Relations
-- ============================================================
-- Usage : sqlite3 instance/development.db < tests/test_crud.sql
-- ============================================================

PRAGMA foreign_keys = ON;

-- Nettoyage avant les tests (garde les donnees initiales)
DELETE FROM place_amenity;
DELETE FROM reviews;
DELETE FROM places;
DELETE FROM users WHERE id != '36c9050e-ddd3-4c3b-9731-9f487208bbc1';

-- ============================================================
-- SECTION 0 — VERIFICATION DONNEES INITIALES
-- ============================================================

SELECT '========================================' AS separator;
SELECT 'SECTION 0 — DONNEES INITIALES' AS section;
SELECT '========================================' AS separator;

-- TEST 0.1 — Admin existe avec is_admin = TRUE
SELECT '-- TEST 0.1: Admin existe avec is_admin = TRUE' AS test;
SELECT id, first_name, last_name, email, is_admin
FROM users WHERE email = 'admin@hbnb.io';
-- ATTENDU : 1 ligne, is_admin = 1, id = 36c9050e-ddd3-4c3b-9731-9f487208bbc1

-- TEST 0.2 — 3 amenities initiales presentes
SELECT '-- TEST 0.2: 3 amenities initiales (WiFi, Swimming Pool, Air Conditioning)' AS test;
SELECT id, name FROM amenities ORDER BY name;
-- ATTENDU : 3 lignes

-- ============================================================
-- SECTION 1 — CRUD : USERS
-- ============================================================

SELECT '========================================' AS separator;
SELECT 'SECTION 1 — CRUD : USERS' AS section;
SELECT '========================================' AS separator;

-- --------------------------
-- CREATE
-- --------------------------

-- TEST 1.1 — Insertion utilisateur valide
SELECT '-- TEST 1.1: Insertion utilisateur valide (John)' AS test;
INSERT INTO users (id, first_name, last_name, email, password, is_admin, created_at, updated_at)
VALUES (
    '11111111-1111-1111-1111-111111111111',
    'John', 'Doe', 'john@test.com',
    '$2b$12$Z24N6SlkS8E6YEjB5weWseNPC8oPALbIfEIjM/AanPP9JuheGsZFq',
    FALSE, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP
);
SELECT id, first_name, last_name, email, is_admin FROM users
WHERE id = '11111111-1111-1111-1111-111111111111';
-- ATTENDU : 1 ligne avec is_admin = 0

-- TEST 1.2 — Insertion deuxieme utilisateur valide
SELECT '-- TEST 1.2: Insertion deuxieme utilisateur valide (Jane)' AS test;
INSERT INTO users (id, first_name, last_name, email, password, is_admin, created_at, updated_at)
VALUES (
    '22222222-2222-2222-2222-222222222222',
    'Jane', 'Smith', 'jane@test.com',
    '$2b$12$Z24N6SlkS8E6YEjB5weWseNPC8oPALbIfEIjM/AanPP9JuheGsZFq',
    FALSE, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP
);
SELECT id, first_name, email FROM users
WHERE id = '22222222-2222-2222-2222-222222222222';
-- ATTENDU : 1 ligne

-- TEST 1.3 — Doublon email (doit echouer)
SELECT '-- TEST 1.3: Doublon email (doit echouer)' AS test;
INSERT INTO users (id, first_name, last_name, email, password, is_admin, created_at, updated_at)
VALUES (
    'aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa',
    'Dup', 'User', 'john@test.com',
    '$2b$12$Z24N6SlkS8E6YEjB5weWseNPC8oPALbIfEIjM/AanPP9JuheGsZFq',
    FALSE, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP
);
-- ATTENDU : ERREUR UNIQUE constraint failed: users.email

-- TEST 1.4 — Mot de passe stocke hache
SELECT '-- TEST 1.4: Mot de passe stocke en hash bcrypt' AS test;
SELECT password FROM users WHERE email = 'john@test.com';
-- ATTENDU : hash bcrypt commencant par $2b$

-- --------------------------
-- READ
-- --------------------------

-- TEST 1.5 — Lire tous les utilisateurs
SELECT '-- TEST 1.5: Lire tous les utilisateurs' AS test;
SELECT id, first_name, last_name, email, is_admin FROM users ORDER BY email;
-- ATTENDU : 3 lignes (admin, Jane, John)

-- TEST 1.6 — Lire un utilisateur par ID
SELECT '-- TEST 1.6: Lire un utilisateur par ID' AS test;
SELECT id, first_name, last_name, email FROM users
WHERE id = '11111111-1111-1111-1111-111111111111';
-- ATTENDU : 1 ligne (John Doe)

-- --------------------------
-- UPDATE
-- --------------------------

-- TEST 1.7 — Modifier le prenom
SELECT '-- TEST 1.7: Modifier le prenom de John -> Johnny' AS test;
UPDATE users SET first_name = 'Johnny', updated_at = CURRENT_TIMESTAMP
WHERE id = '11111111-1111-1111-1111-111111111111';
SELECT id, first_name FROM users WHERE id = '11111111-1111-1111-1111-111111111111';
-- ATTENDU : first_name = 'Johnny'

-- TEST 1.8 — Modifier l'email avec une valeur valide
SELECT '-- TEST 1.8: Modifier email -> johnny@test.com' AS test;
UPDATE users SET email = 'johnny@test.com', updated_at = CURRENT_TIMESTAMP
WHERE id = '11111111-1111-1111-1111-111111111111';
SELECT email FROM users WHERE id = '11111111-1111-1111-1111-111111111111';
-- ATTENDU : johnny@test.com

-- TEST 1.9 — Modifier email avec doublon (doit echouer)
SELECT '-- TEST 1.9: Modifier email avec doublon (doit echouer)' AS test;
UPDATE users SET email = 'jane@test.com'
WHERE id = '11111111-1111-1111-1111-111111111111';
-- ATTENDU : ERREUR UNIQUE constraint failed: users.email

-- --------------------------
-- DELETE
-- --------------------------

-- TEST 1.10 — Supprimer un user sans places (doit reussir)
SELECT '-- TEST 1.10: Supprimer Jane (pas de places) -> succes' AS test;
DELETE FROM users WHERE id = '22222222-2222-2222-2222-222222222222';
SELECT id FROM users WHERE id = '22222222-2222-2222-2222-222222222222';
-- ATTENDU : 0 lignes (supprime)

-- Reinstaller Jane pour les tests suivants
INSERT INTO users (id, first_name, last_name, email, password, is_admin, created_at, updated_at)
VALUES (
    '22222222-2222-2222-2222-222222222222',
    'Jane', 'Smith', 'jane@test.com',
    '$2b$12$Z24N6SlkS8E6YEjB5weWseNPC8oPALbIfEIjM/AanPP9JuheGsZFq',
    FALSE, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP
);

-- ============================================================
-- SECTION 2 — CRUD : AMENITIES
-- ============================================================

SELECT '========================================' AS separator;
SELECT 'SECTION 2 — CRUD : AMENITIES' AS section;
SELECT '========================================' AS separator;

-- --------------------------
-- CREATE
-- --------------------------

-- TEST 2.1 — Insertion amenity valide
SELECT '-- TEST 2.1: Insertion amenity valide (Parking)' AS test;
INSERT INTO amenities (id, name, created_at, updated_at)
VALUES ('aaaa0001-0000-0000-0000-000000000000', 'Parking', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP);
SELECT id, name FROM amenities WHERE name = 'Parking';
-- ATTENDU : 1 ligne

-- TEST 2.2 — Doublon nom amenity (doit echouer)
SELECT '-- TEST 2.2: Doublon nom amenity (doit echouer)' AS test;
INSERT INTO amenities (id, name, created_at, updated_at)
VALUES ('aaaa0002-0000-0000-0000-000000000000', 'Parking', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP);
-- ATTENDU : ERREUR UNIQUE constraint failed: amenities.name

-- TEST 2.3 — Nom NULL (doit echouer)
SELECT '-- TEST 2.3: Nom NULL (doit echouer)' AS test;
INSERT INTO amenities (id, name, created_at, updated_at)
VALUES ('aaaa0003-0000-0000-0000-000000000000', NULL, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP);
-- ATTENDU : ERREUR NOT NULL constraint failed: amenities.name

-- --------------------------
-- READ
-- --------------------------

-- TEST 2.4 — Lire toutes les amenities
SELECT '-- TEST 2.4: Lire toutes les amenities' AS test;
SELECT id, name FROM amenities ORDER BY name;
-- ATTENDU : 4 lignes (Air Conditioning, Parking, Swimming Pool, WiFi)

-- --------------------------
-- UPDATE
-- --------------------------

-- TEST 2.5 — Modifier le nom d'une amenity
SELECT '-- TEST 2.5: Modifier nom Parking -> Parking prive' AS test;
UPDATE amenities SET name = 'Parking prive', updated_at = CURRENT_TIMESTAMP
WHERE name = 'Parking';
SELECT name FROM amenities WHERE id = 'aaaa0001-0000-0000-0000-000000000000';
-- ATTENDU : Parking prive

-- --------------------------
-- DELETE
-- --------------------------

-- TEST 2.6 — Supprimer une amenity non liee
SELECT '-- TEST 2.6: Supprimer amenity non liee -> succes' AS test;
DELETE FROM amenities WHERE id = 'aaaa0001-0000-0000-0000-000000000000';
SELECT id FROM amenities WHERE id = 'aaaa0001-0000-0000-0000-000000000000';
-- ATTENDU : 0 lignes

-- ============================================================
-- SECTION 3 — CRUD : PLACES
-- ============================================================

SELECT '========================================' AS separator;
SELECT 'SECTION 3 — CRUD : PLACES' AS section;
SELECT '========================================' AS separator;

-- --------------------------
-- CREATE
-- --------------------------

-- TEST 3.1 — Insertion place valide
SELECT '-- TEST 3.1: Insertion place valide (Test Place, owner = John)' AS test;
INSERT INTO places (id, title, description, price, latitude, longitude, owner_id, created_at, updated_at)
VALUES (
    'bbbb0001-0000-0000-0000-000000000000',
    'Test Place', 'Nice place for testing',
    99.99, 48.8566, 2.3522,
    '11111111-1111-1111-1111-111111111111',
    CURRENT_TIMESTAMP, CURRENT_TIMESTAMP
);
SELECT id, title, price, owner_id FROM places
WHERE id = 'bbbb0001-0000-0000-0000-000000000000';
-- ATTENDU : 1 ligne

-- TEST 3.2 — owner_id inexistant (doit echouer)
SELECT '-- TEST 3.2: owner_id inexistant (doit echouer)' AS test;
INSERT INTO places (id, title, description, price, latitude, longitude, owner_id, created_at, updated_at)
VALUES (
    'bbbb0002-0000-0000-0000-000000000000',
    'Ghost Place', 'No owner',
    50.00, 48.00, 2.00,
    'ffffffff-ffff-ffff-ffff-ffffffffffff',
    CURRENT_TIMESTAMP, CURRENT_TIMESTAMP
);
-- ATTENDU : ERREUR FOREIGN KEY constraint failed

-- TEST 3.3 — Prix negatif (doit echouer)
SELECT '-- TEST 3.3: Prix negatif (doit echouer)' AS test;
INSERT INTO places (id, title, description, price, latitude, longitude, owner_id, created_at, updated_at)
VALUES (
    'bbbb0003-0000-0000-0000-000000000000',
    'Bad Price', 'Negative price',
    -10.00, 48.00, 2.00,
    '11111111-1111-1111-1111-111111111111',
    CURRENT_TIMESTAMP, CURRENT_TIMESTAMP
);
-- ATTENDU : ERREUR CHECK constraint failed: price > 0

-- TEST 3.4 — Latitude hors limites (doit echouer)
SELECT '-- TEST 3.4: Latitude hors limites (doit echouer)' AS test;
INSERT INTO places (id, title, description, price, latitude, longitude, owner_id, created_at, updated_at)
VALUES (
    'bbbb0004-0000-0000-0000-000000000000',
    'Bad Latitude', 'Invalid latitude',
    50.00, 999.00, 2.00,
    '11111111-1111-1111-1111-111111111111',
    CURRENT_TIMESTAMP, CURRENT_TIMESTAMP
);
-- ATTENDU : ERREUR CHECK constraint failed

-- TEST 3.5 — Longitude hors limites (doit echouer)
SELECT '-- TEST 3.5: Longitude hors limites (doit echouer)' AS test;
INSERT INTO places (id, title, description, price, latitude, longitude, owner_id, created_at, updated_at)
VALUES (
    'bbbb0005-0000-0000-0000-000000000000',
    'Bad Longitude', 'Invalid longitude',
    50.00, 48.00, 999.00,
    '11111111-1111-1111-1111-111111111111',
    CURRENT_TIMESTAMP, CURRENT_TIMESTAMP
);
-- ATTENDU : ERREUR CHECK constraint failed

-- --------------------------
-- READ
-- --------------------------

-- TEST 3.6 — Lire toutes les places avec leur owner
SELECT '-- TEST 3.6: Lire toutes les places avec owner' AS test;
SELECT p.id, p.title, p.price, u.first_name, u.last_name
FROM places p JOIN users u ON p.owner_id = u.id;
-- ATTENDU : 1 ligne (Test Place, Johnny Doe)

-- TEST 3.7 — Lire les places d'un utilisateur specifique
SELECT '-- TEST 3.7: Lire les places de John' AS test;
SELECT id, title, price FROM places
WHERE owner_id = '11111111-1111-1111-1111-111111111111';
-- ATTENDU : 1 ligne

-- --------------------------
-- UPDATE
-- --------------------------

-- TEST 3.8 — Modifier le prix avec valeur valide
SELECT '-- TEST 3.8: Modifier prix 99.99 -> 149.99' AS test;
UPDATE places SET price = 149.99, updated_at = CURRENT_TIMESTAMP
WHERE id = 'bbbb0001-0000-0000-0000-000000000000';
SELECT price FROM places WHERE id = 'bbbb0001-0000-0000-0000-000000000000';
-- ATTENDU : 149.99

-- TEST 3.9 — Modifier prix avec valeur invalide (doit echouer)
SELECT '-- TEST 3.9: Modifier prix -> 0 (doit echouer)' AS test;
UPDATE places SET price = 0
WHERE id = 'bbbb0001-0000-0000-0000-000000000000';
-- ATTENDU : ERREUR CHECK constraint failed: price > 0

-- TEST 3.10 — Modifier titre
SELECT '-- TEST 3.10: Modifier titre' AS test;
UPDATE places SET title = 'Updated Test Place', updated_at = CURRENT_TIMESTAMP
WHERE id = 'bbbb0001-0000-0000-0000-000000000000';
SELECT title FROM places WHERE id = 'bbbb0001-0000-0000-0000-000000000000';
-- ATTENDU : Updated Test Place

-- --------------------------
-- DELETE
-- --------------------------

-- TEST 3.11 — Supprimer place avec reviews (doit echouer — on cree une review d'abord)
INSERT INTO reviews (id, text, rating, user_id, place_id, created_at, updated_at)
VALUES (
    'cccc0001-0000-0000-0000-000000000000',
    'Test review', 4,
    '22222222-2222-2222-2222-222222222222',
    'bbbb0001-0000-0000-0000-000000000000',
    CURRENT_TIMESTAMP, CURRENT_TIMESTAMP
);

SELECT '-- TEST 3.11: Supprimer place avec reviews (doit echouer)' AS test;
DELETE FROM places WHERE id = 'bbbb0001-0000-0000-0000-000000000000';
-- ATTENDU : ERREUR FOREIGN KEY constraint failed

-- ============================================================
-- SECTION 4 — CRUD : REVIEWS
-- ============================================================

SELECT '========================================' AS separator;
SELECT 'SECTION 4 — CRUD : REVIEWS' AS section;
SELECT '========================================' AS separator;

-- --------------------------
-- CREATE
-- --------------------------

-- TEST 4.1 — Review deja inseree au test 3.11, on verifie
SELECT '-- TEST 4.1: Verifier review inseree (Jane sur Test Place)' AS test;
SELECT id, text, rating, user_id, place_id FROM reviews
WHERE id = 'cccc0001-0000-0000-0000-000000000000';
-- ATTENDU : 1 ligne avec rating = 4

-- TEST 4.2 — Deuxieme review Admin sur Test Place
SELECT '-- TEST 4.2: Insertion review valide (Admin sur Test Place)' AS test;
INSERT INTO reviews (id, text, rating, user_id, place_id, created_at, updated_at)
VALUES (
    'cccc0002-0000-0000-0000-000000000000',
    'Very nice place!', 5,
    '36c9050e-ddd3-4c3b-9731-9f487208bbc1',
    'bbbb0001-0000-0000-0000-000000000000',
    CURRENT_TIMESTAMP, CURRENT_TIMESTAMP
);
SELECT id, text, rating FROM reviews WHERE id = 'cccc0002-0000-0000-0000-000000000000';
-- ATTENDU : 1 ligne avec rating = 5

-- TEST 4.3 — Doublon review meme user meme place (doit echouer)
SELECT '-- TEST 4.3: Doublon review meme user/place (doit echouer)' AS test;
INSERT INTO reviews (id, text, rating, user_id, place_id, created_at, updated_at)
VALUES (
    'cccc0003-0000-0000-0000-000000000000',
    'Second review attempt', 3,
    '22222222-2222-2222-2222-222222222222',
    'bbbb0001-0000-0000-0000-000000000000',
    CURRENT_TIMESTAMP, CURRENT_TIMESTAMP
);
-- ATTENDU : ERREUR UNIQUE constraint failed

-- TEST 4.4 — Rating hors limites (doit echouer)
SELECT '-- TEST 4.4: Rating > 5 (doit echouer)' AS test;
INSERT INTO reviews (id, text, rating, user_id, place_id, created_at, updated_at)
VALUES (
    'cccc0004-0000-0000-0000-000000000000',
    'Bad rating', 10,
    '22222222-2222-2222-2222-222222222222',
    'bbbb0001-0000-0000-0000-000000000000',
    CURRENT_TIMESTAMP, CURRENT_TIMESTAMP
);
-- ATTENDU : ERREUR CHECK constraint failed

-- TEST 4.5 — user_id inexistant (doit echouer)
SELECT '-- TEST 4.5: user_id inexistant (doit echouer)' AS test;
INSERT INTO reviews (id, text, rating, user_id, place_id, created_at, updated_at)
VALUES (
    'cccc0005-0000-0000-0000-000000000000',
    'Ghost review', 3,
    'ffffffff-ffff-ffff-ffff-ffffffffffff',
    'bbbb0001-0000-0000-0000-000000000000',
    CURRENT_TIMESTAMP, CURRENT_TIMESTAMP
);
-- ATTENDU : ERREUR FOREIGN KEY constraint failed

-- TEST 4.6 — place_id inexistant (doit echouer)
SELECT '-- TEST 4.6: place_id inexistant (doit echouer)' AS test;
INSERT INTO reviews (id, text, rating, user_id, place_id, created_at, updated_at)
VALUES (
    'cccc0006-0000-0000-0000-000000000000',
    'Ghost place review', 3,
    '22222222-2222-2222-2222-222222222222',
    'ffffffff-ffff-ffff-ffff-ffffffffffff',
    CURRENT_TIMESTAMP, CURRENT_TIMESTAMP
);
-- ATTENDU : ERREUR FOREIGN KEY constraint failed

-- --------------------------
-- READ
-- --------------------------

-- TEST 4.7 — Lire toutes les reviews avec auteur et lieu
SELECT '-- TEST 4.7: Lire toutes les reviews avec auteur et lieu' AS test;
SELECT r.id, r.text, r.rating, u.first_name, p.title
FROM reviews r
JOIN users u ON r.user_id = u.id
JOIN places p ON r.place_id = p.id;
-- ATTENDU : 2 lignes (Jane + Admin)

-- TEST 4.8 — Lire reviews d'un lieu specifique
SELECT '-- TEST 4.8: Lire reviews du Test Place' AS test;
SELECT r.text, r.rating, u.first_name
FROM reviews r JOIN users u ON r.user_id = u.id
WHERE r.place_id = 'bbbb0001-0000-0000-0000-000000000000';
-- ATTENDU : 2 lignes

-- --------------------------
-- UPDATE
-- --------------------------

-- TEST 4.9 — Modifier le texte d'une review
SELECT '-- TEST 4.9: Modifier texte review' AS test;
UPDATE reviews SET text = 'Updated review text!', updated_at = CURRENT_TIMESTAMP
WHERE id = 'cccc0001-0000-0000-0000-000000000000';
SELECT text FROM reviews WHERE id = 'cccc0001-0000-0000-0000-000000000000';
-- ATTENDU : Updated review text!

-- TEST 4.10 — Modifier rating valide
SELECT '-- TEST 4.10: Modifier rating 4 -> 3' AS test;
UPDATE reviews SET rating = 3, updated_at = CURRENT_TIMESTAMP
WHERE id = 'cccc0001-0000-0000-0000-000000000000';
SELECT rating FROM reviews WHERE id = 'cccc0001-0000-0000-0000-000000000000';
-- ATTENDU : 3

-- TEST 4.11 — Modifier rating invalide (doit echouer)
SELECT '-- TEST 4.11: Modifier rating -> 0 (doit echouer)' AS test;
UPDATE reviews SET rating = 0
WHERE id = 'cccc0001-0000-0000-0000-000000000000';
-- ATTENDU : ERREUR CHECK constraint failed

-- --------------------------
-- DELETE
-- --------------------------

-- TEST 4.12 — Supprimer une review
SELECT '-- TEST 4.12: Supprimer une review -> succes' AS test;
DELETE FROM reviews WHERE id = 'cccc0001-0000-0000-0000-000000000000';
SELECT id FROM reviews WHERE id = 'cccc0001-0000-0000-0000-000000000000';
-- ATTENDU : 0 lignes

-- ============================================================
-- SECTION 5 — RELATIONS
-- ============================================================

SELECT '========================================' AS separator;
SELECT 'SECTION 5 — RELATIONS' AS section;
SELECT '========================================' AS separator;

-- TEST 5.1 — Lier une amenity a une place
SELECT '-- TEST 5.1: Lier WiFi a Test Place' AS test;
INSERT INTO place_amenity (place_id, amenity_id)
VALUES (
    'bbbb0001-0000-0000-0000-000000000000',
    '7c9fdf4d-99be-4b1c-8c2e-5aea5db0d0eb'
);
SELECT a.name FROM amenities a
JOIN place_amenity pa ON a.id = pa.amenity_id
WHERE pa.place_id = 'bbbb0001-0000-0000-0000-000000000000';
-- ATTENDU : WiFi

-- TEST 5.2 — Lier une deuxieme amenity
SELECT '-- TEST 5.2: Lier Swimming Pool a Test Place' AS test;
INSERT INTO place_amenity (place_id, amenity_id)
VALUES (
    'bbbb0001-0000-0000-0000-000000000000',
    'ae5ae8a5-0203-451b-9cb8-6086e5b2f41e'
);
SELECT COUNT(*) AS nb_amenities FROM place_amenity
WHERE place_id = 'bbbb0001-0000-0000-0000-000000000000';
-- ATTENDU : 2

-- TEST 5.3 — Doublon place_amenity (doit echouer)
SELECT '-- TEST 5.3: Doublon place_amenity (doit echouer)' AS test;
INSERT INTO place_amenity (place_id, amenity_id)
VALUES (
    'bbbb0001-0000-0000-0000-000000000000',
    '7c9fdf4d-99be-4b1c-8c2e-5aea5db0d0eb'
);
-- ATTENDU : ERREUR UNIQUE constraint failed

-- TEST 5.4 — place_id inexistant dans place_amenity (doit echouer)
SELECT '-- TEST 5.4: place_id inexistant dans place_amenity (doit echouer)' AS test;
INSERT INTO place_amenity (place_id, amenity_id)
VALUES (
    'ffffffff-ffff-ffff-ffff-ffffffffffff',
    '7c9fdf4d-99be-4b1c-8c2e-5aea5db0d0eb'
);
-- ATTENDU : ERREUR FOREIGN KEY constraint failed

-- TEST 5.5 — amenity_id inexistant dans place_amenity (doit echouer)
SELECT '-- TEST 5.5: amenity_id inexistant dans place_amenity (doit echouer)' AS test;
INSERT INTO place_amenity (place_id, amenity_id)
VALUES (
    'bbbb0001-0000-0000-0000-000000000000',
    'ffffffff-ffff-ffff-ffff-ffffffffffff'
);
-- ATTENDU : ERREUR FOREIGN KEY constraint failed

-- TEST 5.6 — Supprimer amenity liee a une place (doit echouer)
SELECT '-- TEST 5.6: Supprimer amenity liee a une place (doit echouer)' AS test;
DELETE FROM amenities WHERE id = '7c9fdf4d-99be-4b1c-8c2e-5aea5db0d0eb';
-- ATTENDU : ERREUR FOREIGN KEY constraint failed

-- TEST 5.7 — Supprimer user avec place (doit echouer)
SELECT '-- TEST 5.7: Supprimer user proprietaire dune place (doit echouer)' AS test;
DELETE FROM users WHERE id = '11111111-1111-1111-1111-111111111111';
-- ATTENDU : ERREUR FOREIGN KEY constraint failed

-- TEST 5.8 — JOIN Place -> Owner -> Reviews -> Amenities
SELECT '-- TEST 5.8: JOIN complet Place + Owner + Amenities' AS test;
SELECT
    p.title AS place,
    u.first_name || ' ' || u.last_name AS owner,
    a.name AS amenity
FROM places p
JOIN users u ON p.owner_id = u.id
JOIN place_amenity pa ON p.id = pa.place_id
JOIN amenities a ON pa.amenity_id = a.id;
-- ATTENDU : 2 lignes (Test Place + Johnny Doe + WiFi / Swimming Pool)

-- TEST 5.9 — Verifier integrite : pas de places orphelines
SELECT '-- TEST 5.9: Pas de places sans owner' AS test;
SELECT p.* FROM places p
LEFT JOIN users u ON p.owner_id = u.id
WHERE u.id IS NULL;
-- ATTENDU : 0 lignes

-- TEST 5.10 — Verifier integrite : pas de reviews orphelines
SELECT '-- TEST 5.10: Pas de reviews sans user ou place' AS test;
SELECT r.* FROM reviews r
LEFT JOIN users u ON r.user_id = u.id
WHERE u.id IS NULL;
-- ATTENDU : 0 lignes

SELECT r.* FROM reviews r
LEFT JOIN places p ON r.place_id = p.id
WHERE p.id IS NULL;
-- ATTENDU : 0 lignes

-- ============================================================
-- SECTION 6 — RBAC (Role Based Access Control)
-- ============================================================

SELECT '========================================' AS separator;
SELECT 'SECTION 6 — RBAC' AS section;
SELECT '========================================' AS separator;

-- TEST 6.1 — Verifier is_admin de l'admin
SELECT '-- TEST 6.1: Admin a is_admin = TRUE' AS test;
SELECT email, is_admin FROM users WHERE email = 'admin@hbnb.io';
-- ATTENDU : is_admin = 1

-- TEST 6.2 — Verifier is_admin des users normaux
SELECT '-- TEST 6.2: Users normaux ont is_admin = FALSE' AS test;
SELECT email, is_admin FROM users WHERE email IN ('john@test.com', 'jane@test.com');
-- ATTENDU : is_admin = 0 pour les deux

-- TEST 6.3 — Passer un user normal en admin
SELECT '-- TEST 6.3: Promouvoir John en admin' AS test;
UPDATE users SET is_admin = TRUE WHERE id = '11111111-1111-1111-1111-111111111111';
SELECT email, is_admin FROM users WHERE id = '11111111-1111-1111-1111-111111111111';
-- ATTENDU : is_admin = 1

-- TEST 6.4 — Retirer les droits admin
SELECT '-- TEST 6.4: Retirer droits admin de John' AS test;
UPDATE users SET is_admin = FALSE WHERE id = '11111111-1111-1111-1111-111111111111';
SELECT email, is_admin FROM users WHERE id = '11111111-1111-1111-1111-111111111111';
-- ATTENDU : is_admin = 0

-- ============================================================
-- SECTION 7 — SUPPRESSION DANS LE BON ORDRE
-- ============================================================

SELECT '========================================' AS separator;
SELECT 'SECTION 7 — SUPPRESSION ORDONNEE' AS section;
SELECT '========================================' AS separator;

-- TEST 7.1 — Supprimer reviews d'abord
SELECT '-- TEST 7.1: Supprimer toutes les reviews' AS test;
DELETE FROM reviews;
SELECT COUNT(*) AS nb_reviews FROM reviews;
-- ATTENDU : 0

-- TEST 7.2 — Supprimer place_amenity
SELECT '-- TEST 7.2: Supprimer place_amenity' AS test;
DELETE FROM place_amenity;
SELECT COUNT(*) AS nb_pa FROM place_amenity;
-- ATTENDU : 0

-- TEST 7.3 — Supprimer les places
SELECT '-- TEST 7.3: Supprimer toutes les places' AS test;
DELETE FROM places;
SELECT COUNT(*) AS nb_places FROM places;
-- ATTENDU : 0

-- TEST 7.4 — Supprimer les users de test
SELECT '-- TEST 7.4: Supprimer users de test' AS test;
DELETE FROM users WHERE id != '36c9050e-ddd3-4c3b-9731-9f487208bbc1';
SELECT COUNT(*) AS nb_users FROM users;
-- ATTENDU : 1 (admin seulement)

-- ============================================================
-- VERIFICATION FINALE
-- ============================================================

SELECT '========================================' AS separator;
SELECT 'VERIFICATION FINALE' AS separator;
SELECT '========================================' AS separator;

SELECT '-- FINAL: Seul admin reste' AS test;
SELECT id, email, is_admin FROM users;
-- ATTENDU : 1 ligne (admin)

SELECT '-- FINAL: 3 amenities initiales intactes' AS test;
SELECT id, name FROM amenities ORDER BY name;
-- ATTENDU : 3 lignes

SELECT '-- FINAL: 0 places' AS test;
SELECT COUNT(*) AS nb_places FROM places;

SELECT '-- FINAL: 0 reviews' AS test;
SELECT COUNT(*) AS nb_reviews FROM reviews;
