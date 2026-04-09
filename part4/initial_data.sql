-- =============================================================
-- HBnB — Données initiales complètes
-- =============================================================
-- Ce fichier remplace initial_data.sql + seed_demo.sql.
-- Toutes les insertions utilisent INSERT OR IGNORE :
--   → sûr à exécuter plusieurs fois sans écraser les données.
--
-- À exécuter APRÈS schema.sql :
--   sqlite3 instance/development.db < initial_data.sql
--
-- Comptes disponibles :
--   admin@hbnb.io  / admin1234  (admin)
--   sara@test.com  / pass1234   (propriétaire place001, place002, place007)
--   marc@test.com  / pass1234   (propriétaire place003, place004, place008)
--   lea@test.com   / pass1234   (propriétaire place005, place006, place009)
-- =============================================================

PRAGMA foreign_keys = ON;

-- =============================================================
-- 1. ADMINISTRATEUR
--    UUID fixe imposé par les tasks et les tests automatisés.
--    Mot de passe : admin1234
-- =============================================================

INSERT OR IGNORE INTO users (id, first_name, last_name, email, password, is_admin, created_at, updated_at)
VALUES (
    '36c9050e-ddd3-4c3b-9731-9f487208bbc1',
    'Admin', 'HBnB', 'admin@hbnb.io',
    '$2b$12$Uu5fTvVL036i9kQnGeAeNOlb5JAvFCFMDKuHfcycD/fpzVtjx7dty',
    TRUE, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP
);

-- =============================================================
-- 2. AMENITIES DE BASE
--    UUIDs fixes requis par les tests.
-- =============================================================

INSERT OR IGNORE INTO amenities (id, name, created_at, updated_at) VALUES
('7c9fdf4d-99be-4b1c-8c2e-5aea5db0d0eb', 'WiFi',             CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
('ae5ae8a5-0203-451b-9cb8-6086e5b2f41e', 'Swimming Pool',     CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
('97bc1cc5-3dcd-439e-894f-e9986dedd012', 'Air Conditioning',  CURRENT_TIMESTAMP, CURRENT_TIMESTAMP);

-- =============================================================
-- 3. UTILISATEURS DE DÉMO
--    Mot de passe commun : pass1234
--    Les hash bcrypt ci-dessous ont été générés via le backend
--    (flask_bcrypt) pour garantir la compatibilité.
-- =============================================================

INSERT OR IGNORE INTO users (id, first_name, last_name, email, password, is_admin, created_at, updated_at)
VALUES (
    'aaaa1111-0000-0000-0000-000000000001',
    'Sara', 'Dupont', 'sara@test.com',
    '$2b$12$SzfN8nVP8kP9EraJ4JT7SOgxITlJXSaKWN.0d8oBEPASBCJbY3yAW',
    FALSE, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP
);

INSERT OR IGNORE INTO users (id, first_name, last_name, email, password, is_admin, created_at, updated_at)
VALUES (
    'bbbb2222-0000-0000-0000-000000000002',
    'Marc', 'Bernard', 'marc@test.com',
    '$2b$12$I7LSxrCICg0YbYhu.8FjaeB5td8H4dn9J9k4qKqrR3YfkN6nIIX6W',
    FALSE, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP
);

INSERT OR IGNORE INTO users (id, first_name, last_name, email, password, is_admin, created_at, updated_at)
VALUES (
    'cccc3333-0000-0000-0000-000000000003',
    'Léa', 'Martin', 'lea@test.com',
    '$2b$12$yzIcFQytzWUyvJIZ6XQQDePTnAdIPkHLs1S/8SLTsRl9nvIBvjdpK',
    FALSE, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP
);

-- =============================================================
-- 4. PLACES DE DÉMO (9 places)
-- =============================================================

INSERT OR IGNORE INTO places (id, title, description, price, latitude, longitude, owner_id, created_at, updated_at)
VALUES (
    'place001-0000-0000-0000-000000000001',
    'Chalet vue sur le lac',
    'Magnifique chalet en bois avec vue panoramique sur le lac Léman. Terrasse privée, jacuzzi extérieur et accès direct à la plage.',
    180.00, 46.3667, 6.5000,
    'aaaa1111-0000-0000-0000-000000000001',
    CURRENT_TIMESTAMP, CURRENT_TIMESTAMP
);

INSERT OR IGNORE INTO places (id, title, description, price, latitude, longitude, owner_id, created_at, updated_at)
VALUES (
    'place002-0000-0000-0000-000000000002',
    'Studio moderne Genève centre',
    'Studio entièrement rénové au cœur de Genève. Idéal pour les voyageurs d''affaires ou les city-breaks. Accès direct aux transports.',
    95.00, 46.2044, 6.1432,
    'aaaa1111-0000-0000-0000-000000000001',
    CURRENT_TIMESTAMP, CURRENT_TIMESTAMP
);

INSERT OR IGNORE INTO places (id, title, description, price, latitude, longitude, owner_id, created_at, updated_at)
VALUES (
    'place003-0000-0000-0000-000000000003',
    'Appartement cosy Annecy',
    'Charmant appartement au bord du lac d''Annecy. Vue imprenable sur les montagnes, à 5 minutes du vieux centre historique.',
    120.00, 45.8992, 6.1294,
    'bbbb2222-0000-0000-0000-000000000002',
    CURRENT_TIMESTAMP, CURRENT_TIMESTAMP
);

INSERT OR IGNORE INTO places (id, title, description, price, latitude, longitude, owner_id, created_at, updated_at)
VALUES (
    'place004-0000-0000-0000-000000000004',
    'Maison de montagne Chamonix',
    'Grande maison familiale au pied du Mont-Blanc. Ski aux pieds en hiver, randonnées en été. Capacité 8 personnes.',
    350.00, 45.9237, 6.8694,
    'bbbb2222-0000-0000-0000-000000000002',
    CURRENT_TIMESTAMP, CURRENT_TIMESTAMP
);

INSERT OR IGNORE INTO places (id, title, description, price, latitude, longitude, owner_id, created_at, updated_at)
VALUES (
    'place005-0000-0000-0000-000000000005',
    'Loft industriel Lyon',
    'Loft atypique dans un ancien entrepôt transformé. Plafonds 4m, mobilier design, quartier branché de la Confluence.',
    85.00, 45.7640, 4.8357,
    'cccc3333-0000-0000-0000-000000000003',
    CURRENT_TIMESTAMP, CURRENT_TIMESTAMP
);

INSERT OR IGNORE INTO places (id, title, description, price, latitude, longitude, owner_id, created_at, updated_at)
VALUES (
    'place006-0000-0000-0000-000000000006',
    'Villa Provence avec piscine',
    'Villa provençale avec grand jardin et piscine. Entourée de lavandes, oliveraies et vignes. Calme absolu garanti.',
    220.00, 43.9352, 5.0764,
    'cccc3333-0000-0000-0000-000000000003',
    CURRENT_TIMESTAMP, CURRENT_TIMESTAMP
);

INSERT OR IGNORE INTO places (id, title, description, price, latitude, longitude, owner_id, created_at, updated_at)
VALUES (
    'place007-0000-0000-0000-000000000007',
    'Mini studio budget',
    'Petit studio simple mais propre, idéal pour backpackers et petits budgets.',
    8.00, 46.2100, 6.1500,
    'aaaa1111-0000-0000-0000-000000000001',
    CURRENT_TIMESTAMP, CURRENT_TIMESTAMP
);

INSERT OR IGNORE INTO places (id, title, description, price, latitude, longitude, owner_id, created_at, updated_at)
VALUES (
    'place008-0000-0000-0000-000000000008',
    'Chambre étudiante',
    'Chambre simple dans une colocation calme, proche des transports en commun.',
    25.00, 46.2050, 6.1400,
    'bbbb2222-0000-0000-0000-000000000002',
    CURRENT_TIMESTAMP, CURRENT_TIMESTAMP
);

INSERT OR IGNORE INTO places (id, title, description, price, latitude, longitude, owner_id, created_at, updated_at)
VALUES (
    'place009-0000-0000-0000-000000000009',
    'Studio compact',
    'Studio moderne mais très compact, parfait pour les courts séjours en ville.',
    45.00, 45.7600, 4.8350,
    'cccc3333-0000-0000-0000-000000000003',
    CURRENT_TIMESTAMP, CURRENT_TIMESTAMP
);

-- =============================================================
-- 5. LIENS PLACE ↔ AMENITY
-- =============================================================

-- Chalet : WiFi + Pool + AC
INSERT OR IGNORE INTO place_amenity VALUES ('place001-0000-0000-0000-000000000001', '7c9fdf4d-99be-4b1c-8c2e-5aea5db0d0eb');
INSERT OR IGNORE INTO place_amenity VALUES ('place001-0000-0000-0000-000000000001', 'ae5ae8a5-0203-451b-9cb8-6086e5b2f41e');
INSERT OR IGNORE INTO place_amenity VALUES ('place001-0000-0000-0000-000000000001', '97bc1cc5-3dcd-439e-894f-e9986dedd012');
-- Studio Genève : WiFi + AC
INSERT OR IGNORE INTO place_amenity VALUES ('place002-0000-0000-0000-000000000002', '7c9fdf4d-99be-4b1c-8c2e-5aea5db0d0eb');
INSERT OR IGNORE INTO place_amenity VALUES ('place002-0000-0000-0000-000000000002', '97bc1cc5-3dcd-439e-894f-e9986dedd012');
-- Appartement Annecy : WiFi
INSERT OR IGNORE INTO place_amenity VALUES ('place003-0000-0000-0000-000000000003', '7c9fdf4d-99be-4b1c-8c2e-5aea5db0d0eb');
-- Maison Chamonix : WiFi + AC
INSERT OR IGNORE INTO place_amenity VALUES ('place004-0000-0000-0000-000000000004', '7c9fdf4d-99be-4b1c-8c2e-5aea5db0d0eb');
INSERT OR IGNORE INTO place_amenity VALUES ('place004-0000-0000-0000-000000000004', '97bc1cc5-3dcd-439e-894f-e9986dedd012');
-- Loft Lyon : WiFi
INSERT OR IGNORE INTO place_amenity VALUES ('place005-0000-0000-0000-000000000005', '7c9fdf4d-99be-4b1c-8c2e-5aea5db0d0eb');
-- Villa Provence : Pool + AC
INSERT OR IGNORE INTO place_amenity VALUES ('place006-0000-0000-0000-000000000006', 'ae5ae8a5-0203-451b-9cb8-6086e5b2f41e');
INSERT OR IGNORE INTO place_amenity VALUES ('place006-0000-0000-0000-000000000006', '97bc1cc5-3dcd-439e-894f-e9986dedd012');

-- =============================================================
-- 6. REVIEWS DE DÉMO
-- =============================================================

INSERT OR IGNORE INTO reviews (id, text, rating, user_id, place_id, created_at, updated_at)
VALUES (
    'rev00001-0000-0000-0000-000000000001',
    'Endroit absolument magnifique ! La vue sur le lac au lever du soleil est inoubliable. Nous reviendrons sans hésiter.',
    5,
    'bbbb2222-0000-0000-0000-000000000002',
    'place001-0000-0000-0000-000000000001',
    CURRENT_TIMESTAMP, CURRENT_TIMESTAMP
);

INSERT OR IGNORE INTO reviews (id, text, rating, user_id, place_id, created_at, updated_at)
VALUES (
    'rev00002-0000-0000-0000-000000000002',
    'Très bon emplacement, studio propre et bien équipé. Le quartier est dynamique et sécurisé.',
    4,
    'cccc3333-0000-0000-0000-000000000003',
    'place002-0000-0000-0000-000000000002',
    CURRENT_TIMESTAMP, CURRENT_TIMESTAMP
);

INSERT OR IGNORE INTO reviews (id, text, rating, user_id, place_id, created_at, updated_at)
VALUES (
    'rev00003-0000-0000-0000-000000000003',
    'Un vrai coup de cœur ! Annecy est superbe et l''appartement correspond exactement aux photos.',
    5,
    'aaaa1111-0000-0000-0000-000000000001',
    'place003-0000-0000-0000-000000000003',
    CURRENT_TIMESTAMP, CURRENT_TIMESTAMP
);
