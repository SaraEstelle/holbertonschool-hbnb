-- =============================================================
-- HBnB - Insertion des donnees initiales
-- =============================================================
-- A executer APRES schema.sql
-- =============================================================

-- Administrateur
-- ID fixe impose par la task
-- Mot de passe : admin1234 hache avec bcrypt
INSERT INTO users (id, first_name, last_name, email, password, is_admin, created_at, updated_at)
VALUES (
    '36c9050e-ddd3-4c3b-9731-9f487208bbc1',
    'Admin',
    'HBnB',
    'admin@hbnb.io',
    '$2b$12$Uu5fTvVL036i9kQnGeAeNOlb5JAvFCFMDKuHfcycD/fpzVtjx7dty',
    TRUE,
    CURRENT_TIMESTAMP,
    CURRENT_TIMESTAMP
);

-- Amenities de base
INSERT INTO amenities (id, name, created_at, updated_at) VALUES
('7c9fdf4d-99be-4b1c-8c2e-5aea5db0d0eb', 'WiFi', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
('ae5ae8a5-0203-451b-9cb8-6086e5b2f41e', 'Swimming Pool', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
('97bc1cc5-3dcd-439e-894f-e9986dedd012', 'Air Conditioning', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP);
