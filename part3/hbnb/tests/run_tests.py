#!/usr/bin/env python3
"""
HBnB — Script de tests automatises
Organises par type : CRUD, Relations, RBAC
Usage : python3 tests/run_tests.py
"""

import sqlite3
import os
import sys

# ============================================================
# Configuration
# ============================================================

DB_PATH = "instance/development.db"
ADMIN_ID = "36c9050e-ddd3-4c3b-9731-9f487208bbc1"
ADMIN_EMAIL = "admin@hbnb.io"
BCRYPT_HASH = "$2b$12$Z24N6SlkS8E6YEjB5weWseNPC8oPALbIfEIjM/AanPP9JuheGsZFq"

WIFI_ID = "7c9fdf4d-99be-4b1c-8c2e-5aea5db0d0eb"
POOL_ID = "ae5ae8a5-0203-451b-9cb8-6086e5b2f41e"
AIRCO_ID = "97bc1cc5-3dcd-439e-894f-e9986dedd012"

JOHN_ID = "11111111-1111-1111-1111-111111111111"
JANE_ID = "22222222-2222-2222-2222-222222222222"
PLACE_ID = "bbbb0001-0000-0000-0000-000000000000"
REVIEW1_ID = "cccc0001-0000-0000-0000-000000000000"
REVIEW2_ID = "cccc0002-0000-0000-0000-000000000000"

# ============================================================
# Utilitaires
# ============================================================

passed = 0
failed = 0
total = 0


def test(name, condition, expected=""):
    """Affiche le resultat d'un test."""
    global passed, failed, total
    total += 1
    if condition:
        passed += 1
        print(f"  [OK]   {name}")
    else:
        failed += 1
        print(f"  [FAIL] {name}")
        if expected:
            print(f"         Attendu : {expected}")


def expect_error(conn, sql):
    """Retourne True si la requete SQL leve une erreur."""
    try:
        conn.execute(sql)
        conn.commit()
        return False
    except (sqlite3.IntegrityError, sqlite3.OperationalError):
        return True


def get_one(conn, sql, params=()):
    """Retourne une seule ligne."""
    row = conn.execute(sql, params).fetchone()
    return row


def get_all(conn, sql, params=()):
    """Retourne toutes les lignes."""
    return conn.execute(sql, params).fetchall()


def get_count(conn, sql, params=()):
    """Retourne un entier."""
    row = conn.execute(sql, params).fetchone()
    return row[0] if row else 0


def section(title):
    print(f"\n{'=' * 60}")
    print(f"  {title}")
    print(f"{'=' * 60}")


# ============================================================
# Setup
# ============================================================

def setup(conn):
    """Nettoie et prepare la DB pour les tests."""
    conn.execute("PRAGMA foreign_keys = ON")
    conn.execute("DELETE FROM place_amenity")
    conn.execute("DELETE FROM reviews")
    conn.execute("DELETE FROM places")
    conn.execute(f"DELETE FROM users WHERE id != '{ADMIN_ID}'")
    conn.commit()


def teardown(conn):
    """Remet la DB dans l'etat initial."""
    conn.execute("DELETE FROM place_amenity")
    conn.execute("DELETE FROM reviews")
    conn.execute("DELETE FROM places")
    conn.execute(f"DELETE FROM users WHERE id != '{ADMIN_ID}'")
    conn.commit()


# ============================================================
# SECTION 0 — Donnees initiales
# ============================================================

def test_initial_data(conn):
    section("SECTION 0 — DONNEES INITIALES")

    admin = get_one(conn, "SELECT id, email, is_admin FROM users WHERE email = ?", (ADMIN_EMAIL,))
    test("0.1 — Admin existe avec is_admin = TRUE",
         admin and admin[2] == 1)

    test("0.2 — Admin a l'ID fixe impose par la task",
         admin and admin[0] == ADMIN_ID)

    count = get_count(conn, "SELECT COUNT(*) FROM amenities")
    test("0.3 — 3 amenities initiales presentes",
         count == 3, f"3, obtenu {count}")

    wifi = get_one(conn, "SELECT id FROM amenities WHERE id = ?", (WIFI_ID,))
    test("0.4 — WiFi present avec bon UUID", wifi is not None)

    pool = get_one(conn, "SELECT id FROM amenities WHERE id = ?", (POOL_ID,))
    test("0.5 — Swimming Pool present avec bon UUID", pool is not None)

    airco = get_one(conn, "SELECT id FROM amenities WHERE id = ?", (AIRCO_ID,))
    test("0.6 — Air Conditioning present avec bon UUID", airco is not None)


# ============================================================
# SECTION 1 — CRUD : USERS
# ============================================================

def test_crud_users(conn):
    section("SECTION 1 — CRUD : USERS")

    print("\n  -- CREATE --")

    conn.execute(f"""
        INSERT INTO users (id, first_name, last_name, email, password, is_admin, created_at, updated_at)
        VALUES ('{JOHN_ID}', 'John', 'Doe', 'john@test.com', '{BCRYPT_HASH}', FALSE,
                CURRENT_TIMESTAMP, CURRENT_TIMESTAMP)
    """)
    conn.commit()
    row = get_one(conn, f"SELECT id FROM users WHERE id = '{JOHN_ID}'")
    test("1.1 — Creer un utilisateur valide (John)", row is not None)

    conn.execute(f"""
        INSERT INTO users (id, first_name, last_name, email, password, is_admin, created_at, updated_at)
        VALUES ('{JANE_ID}', 'Jane', 'Smith', 'jane@test.com', '{BCRYPT_HASH}', FALSE,
                CURRENT_TIMESTAMP, CURRENT_TIMESTAMP)
    """)
    conn.commit()
    row = get_one(conn, f"SELECT id FROM users WHERE id = '{JANE_ID}'")
    test("1.2 — Creer un deuxieme utilisateur valide (Jane)", row is not None)

    test("1.3 — Rejeter email duplique",
         expect_error(conn, f"""
             INSERT INTO users (id, first_name, last_name, email, password, is_admin, created_at, updated_at)
             VALUES ('dup-user-id', 'Dup', 'User', 'john@test.com', '{BCRYPT_HASH}', FALSE,
                     CURRENT_TIMESTAMP, CURRENT_TIMESTAMP)
         """))

    password = get_one(conn, "SELECT password FROM users WHERE email = 'john@test.com'")
    test("1.4 — Mot de passe stocke en hash bcrypt ($2b$)",
         password and password[0].startswith("$2b$"))

    print("\n  -- READ --")

    count = get_count(conn, "SELECT COUNT(*) FROM users")
    test("1.5 — Lire tous les utilisateurs (3 attendus)", count == 3, f"3, obtenu {count}")

    row = get_one(conn, f"SELECT first_name FROM users WHERE id = '{JOHN_ID}'")
    test("1.6 — Lire un utilisateur par ID", row and row[0] == "John")

    print("\n  -- UPDATE --")

    conn.execute(f"UPDATE users SET first_name = 'Johnny' WHERE id = '{JOHN_ID}'")
    conn.commit()
    row = get_one(conn, f"SELECT first_name FROM users WHERE id = '{JOHN_ID}'")
    test("1.7 — Modifier prenom John -> Johnny", row and row[0] == "Johnny")

    conn.execute(f"UPDATE users SET email = 'johnny@test.com' WHERE id = '{JOHN_ID}'")
    conn.commit()
    row = get_one(conn, f"SELECT email FROM users WHERE id = '{JOHN_ID}'")
    test("1.8 — Modifier email valide", row and row[0] == "johnny@test.com")

    test("1.9 — Rejeter email duplique sur UPDATE",
         expect_error(conn, f"UPDATE users SET email = 'jane@test.com' WHERE id = '{JOHN_ID}'"))

    print("\n  -- DELETE --")

    conn.execute(f"DELETE FROM users WHERE id = '{JANE_ID}'")
    conn.commit()
    row = get_one(conn, f"SELECT id FROM users WHERE id = '{JANE_ID}'")
    test("1.10 — Supprimer user sans places -> succes", row is None)

    # Reinstaller Jane
    conn.execute(f"""
        INSERT INTO users (id, first_name, last_name, email, password, is_admin, created_at, updated_at)
        VALUES ('{JANE_ID}', 'Jane', 'Smith', 'jane@test.com', '{BCRYPT_HASH}', FALSE,
                CURRENT_TIMESTAMP, CURRENT_TIMESTAMP)
    """)
    conn.commit()


# ============================================================
# SECTION 2 — CRUD : AMENITIES
# ============================================================

def test_crud_amenities(conn):
    section("SECTION 2 — CRUD : AMENITIES")

    print("\n  -- CREATE --")

    PARKING_ID = "aaaa0001-0000-0000-0000-000000000000"
    conn.execute(f"""
        INSERT INTO amenities (id, name, created_at, updated_at)
        VALUES ('{PARKING_ID}', 'Parking', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP)
    """)
    conn.commit()
    row = get_one(conn, f"SELECT name FROM amenities WHERE id = '{PARKING_ID}'")
    test("2.1 — Creer une amenity valide (Parking)", row and row[0] == "Parking")

    test("2.2 — Rejeter nom duplique",
         expect_error(conn, f"""
             INSERT INTO amenities (id, name, created_at, updated_at)
             VALUES ('aaaa0002-0000-0000-0000-000000000000', 'Parking',
                     CURRENT_TIMESTAMP, CURRENT_TIMESTAMP)
         """))

    test("2.3 — Rejeter nom NULL",
         expect_error(conn, f"""
             INSERT INTO amenities (id, name, created_at, updated_at)
             VALUES ('aaaa0003-0000-0000-0000-000000000000', NULL,
                     CURRENT_TIMESTAMP, CURRENT_TIMESTAMP)
         """))

    print("\n  -- READ --")

    count = get_count(conn, "SELECT COUNT(*) FROM amenities")
    test("2.4 — Lire toutes les amenities (4 attendus)", count == 4, f"4, obtenu {count}")

    print("\n  -- UPDATE --")

    conn.execute(f"UPDATE amenities SET name = 'Parking prive' WHERE id = '{PARKING_ID}'")
    conn.commit()
    row = get_one(conn, f"SELECT name FROM amenities WHERE id = '{PARKING_ID}'")
    test("2.5 — Modifier nom Parking -> Parking prive",
         row and row[0] == "Parking prive")

    print("\n  -- DELETE --")

    conn.execute(f"DELETE FROM amenities WHERE id = '{PARKING_ID}'")
    conn.commit()
    row = get_one(conn, f"SELECT id FROM amenities WHERE id = '{PARKING_ID}'")
    test("2.6 — Supprimer amenity non liee -> succes", row is None)


# ============================================================
# SECTION 3 — CRUD : PLACES
# ============================================================

def test_crud_places(conn):
    section("SECTION 3 — CRUD : PLACES")

    print("\n  -- CREATE --")

    conn.execute(f"""
        INSERT INTO places (id, title, description, price, latitude, longitude, owner_id, created_at, updated_at)
        VALUES ('{PLACE_ID}', 'Test Place', 'Nice place', 99.99, 48.8566, 2.3522,
                '{JOHN_ID}', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP)
    """)
    conn.commit()
    row = get_one(conn, f"SELECT title FROM places WHERE id = '{PLACE_ID}'")
    test("3.1 — Creer une place valide", row and row[0] == "Test Place")

    test("3.2 — Rejeter owner_id inexistant",
         expect_error(conn, f"""
             INSERT INTO places (id, title, description, price, latitude, longitude, owner_id, created_at, updated_at)
             VALUES ('bbbb0002-0000-0000-0000-000000000000', 'Ghost', 'No owner',
                     50.0, 48.0, 2.0, 'ffffffff-ffff-ffff-ffff-ffffffffffff',
                     CURRENT_TIMESTAMP, CURRENT_TIMESTAMP)
         """))

    test("3.3 — Rejeter prix negatif",
         expect_error(conn, f"""
             INSERT INTO places (id, title, description, price, latitude, longitude, owner_id, created_at, updated_at)
             VALUES ('bbbb0003-0000-0000-0000-000000000000', 'Bad', 'Neg price',
                     -10.0, 48.0, 2.0, '{JOHN_ID}', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP)
         """))

    test("3.4 — Rejeter latitude hors limites",
         expect_error(conn, f"""
             INSERT INTO places (id, title, description, price, latitude, longitude, owner_id, created_at, updated_at)
             VALUES ('bbbb0004-0000-0000-0000-000000000000', 'Bad', 'Bad lat',
                     50.0, 999.0, 2.0, '{JOHN_ID}', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP)
         """))

    test("3.5 — Rejeter longitude hors limites",
         expect_error(conn, f"""
             INSERT INTO places (id, title, description, price, latitude, longitude, owner_id, created_at, updated_at)
             VALUES ('bbbb0005-0000-0000-0000-000000000000', 'Bad', 'Bad lng',
                     50.0, 48.0, 999.0, '{JOHN_ID}', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP)
         """))

    print("\n  -- READ --")

    rows = get_all(conn, """
        SELECT p.title, u.first_name FROM places p JOIN users u ON p.owner_id = u.id
    """)
    test("3.6 — Lire place avec son owner via JOIN",
         len(rows) == 1 and rows[0][0] == "Test Place")

    rows = get_all(conn, f"SELECT id FROM places WHERE owner_id = '{JOHN_ID}'")
    test("3.7 — Lire les places d'un user specifique", len(rows) == 1)

    print("\n  -- UPDATE --")

    conn.execute(f"UPDATE places SET price = 149.99 WHERE id = '{PLACE_ID}'")
    conn.commit()
    row = get_one(conn, f"SELECT price FROM places WHERE id = '{PLACE_ID}'")
    test("3.8 — Modifier prix 99.99 -> 149.99", row and abs(row[0] - 149.99) < 0.01)

    test("3.9 — Rejeter prix 0 sur UPDATE",
         expect_error(conn, f"UPDATE places SET price = 0 WHERE id = '{PLACE_ID}'"))

    print("\n  -- DELETE --")

    # Creer une review pour bloquer la suppression
    conn.execute(f"""
        INSERT INTO reviews (id, text, rating, user_id, place_id, created_at, updated_at)
        VALUES ('{REVIEW1_ID}', 'Test', 4, '{JANE_ID}', '{PLACE_ID}',
                CURRENT_TIMESTAMP, CURRENT_TIMESTAMP)
    """)
    conn.commit()

    test("3.10 — Rejeter suppression place avec reviews",
         expect_error(conn, f"DELETE FROM places WHERE id = '{PLACE_ID}'"))


# ============================================================
# SECTION 4 — CRUD : REVIEWS
# ============================================================

def test_crud_reviews(conn):
    section("SECTION 4 — CRUD : REVIEWS")

    print("\n  -- CREATE --")

    # Review 1 deja inseree dans test_crud_places
    row = get_one(conn, f"SELECT rating FROM reviews WHERE id = '{REVIEW1_ID}'")
    test("4.1 — Review existante (Jane sur Test Place)", row and row[0] == 4)

    conn.execute(f"""
        INSERT INTO reviews (id, text, rating, user_id, place_id, created_at, updated_at)
        VALUES ('{REVIEW2_ID}', 'Very nice!', 5, '{ADMIN_ID}', '{PLACE_ID}',
                CURRENT_TIMESTAMP, CURRENT_TIMESTAMP)
    """)
    conn.commit()
    row = get_one(conn, f"SELECT rating FROM reviews WHERE id = '{REVIEW2_ID}'")
    test("4.2 — Creer deuxieme review valide (Admin)", row and row[0] == 5)

    test("4.3 — Rejeter doublon user/place",
         expect_error(conn, f"""
             INSERT INTO reviews (id, text, rating, user_id, place_id, created_at, updated_at)
             VALUES ('cccc0003-0000-0000-0000-000000000000', 'Dup', 3,
                     '{JANE_ID}', '{PLACE_ID}', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP)
         """))

    test("4.4 — Rejeter rating > 5",
         expect_error(conn, f"""
             INSERT INTO reviews (id, text, rating, user_id, place_id, created_at, updated_at)
             VALUES ('cccc0004-0000-0000-0000-000000000000', 'Bad', 10,
                     '{JANE_ID}', '{PLACE_ID}', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP)
         """))

    test("4.5 — Rejeter user_id inexistant",
         expect_error(conn, f"""
             INSERT INTO reviews (id, text, rating, user_id, place_id, created_at, updated_at)
             VALUES ('cccc0005-0000-0000-0000-000000000000', 'Ghost', 3,
                     'ffffffff-ffff-ffff-ffff-ffffffffffff', '{PLACE_ID}',
                     CURRENT_TIMESTAMP, CURRENT_TIMESTAMP)
         """))

    test("4.6 — Rejeter place_id inexistant",
         expect_error(conn, f"""
             INSERT INTO reviews (id, text, rating, user_id, place_id, created_at, updated_at)
             VALUES ('cccc0006-0000-0000-0000-000000000000', 'Ghost', 3,
                     '{JANE_ID}', 'ffffffff-ffff-ffff-ffff-ffffffffffff',
                     CURRENT_TIMESTAMP, CURRENT_TIMESTAMP)
         """))

    print("\n  -- READ --")

    rows = get_all(conn, f"""
        SELECT r.text, u.first_name, p.title FROM reviews r
        JOIN users u ON r.user_id = u.id
        JOIN places p ON r.place_id = p.id
    """)
    test("4.7 — Lire toutes les reviews avec auteur et lieu",
         len(rows) == 2)

    rows = get_all(conn, f"SELECT id FROM reviews WHERE place_id = '{PLACE_ID}'")
    test("4.8 — Lire les reviews d'une place specifique (2 attendus)",
         len(rows) == 2)

    print("\n  -- UPDATE --")

    conn.execute(f"UPDATE reviews SET text = 'Updated!', rating = 3 WHERE id = '{REVIEW1_ID}'")
    conn.commit()
    row = get_one(conn, f"SELECT text, rating FROM reviews WHERE id = '{REVIEW1_ID}'")
    test("4.9 — Modifier texte et rating d'une review",
         row and row[0] == "Updated!" and row[1] == 3)

    test("4.10 — Rejeter rating 0 sur UPDATE",
         expect_error(conn, f"UPDATE reviews SET rating = 0 WHERE id = '{REVIEW1_ID}'"))

    print("\n  -- DELETE --")

    conn.execute(f"DELETE FROM reviews WHERE id = '{REVIEW1_ID}'")
    conn.commit()
    row = get_one(conn, f"SELECT id FROM reviews WHERE id = '{REVIEW1_ID}'")
    test("4.11 — Supprimer une review -> succes", row is None)


# ============================================================
# SECTION 5 — RELATIONS
# ============================================================

def test_relations(conn):
    section("SECTION 5 — RELATIONS")

    # Lier amenities a la place
    conn.execute(f"INSERT INTO place_amenity (place_id, amenity_id) VALUES ('{PLACE_ID}', '{WIFI_ID}')")
    conn.execute(f"INSERT INTO place_amenity (place_id, amenity_id) VALUES ('{PLACE_ID}', '{POOL_ID}')")
    conn.commit()

    count = get_count(conn, f"SELECT COUNT(*) FROM place_amenity WHERE place_id = '{PLACE_ID}'")
    test("5.1 — Lier 2 amenities a une place", count == 2)

    test("5.2 — Rejeter doublon place_amenity",
         expect_error(conn, f"INSERT INTO place_amenity VALUES ('{PLACE_ID}', '{WIFI_ID}')"))

    test("5.3 — Rejeter place_id inexistant dans place_amenity",
         expect_error(conn, f"""
             INSERT INTO place_amenity (place_id, amenity_id)
             VALUES ('ffffffff-ffff-ffff-ffff-ffffffffffff', '{WIFI_ID}')
         """))

    test("5.4 — Rejeter amenity_id inexistant dans place_amenity",
         expect_error(conn, f"""
             INSERT INTO place_amenity (place_id, amenity_id)
             VALUES ('{PLACE_ID}', 'ffffffff-ffff-ffff-ffff-ffffffffffff')
         """))

    test("5.5 — Rejeter suppression amenity liee",
         expect_error(conn, f"DELETE FROM amenities WHERE id = '{WIFI_ID}'"))

    test("5.6 — Rejeter suppression user avec places",
         expect_error(conn, f"DELETE FROM users WHERE id = '{JOHN_ID}'"))

    rows = get_all(conn, f"""
        SELECT p.title, u.first_name, a.name FROM places p
        JOIN users u ON p.owner_id = u.id
        JOIN place_amenity pa ON p.id = pa.place_id
        JOIN amenities a ON pa.amenity_id = a.id
        WHERE p.id = '{PLACE_ID}'
    """)
    test("5.7 — JOIN complet Place + Owner + Amenities (2 lignes)",
         len(rows) == 2)

    orphans = get_count(conn, """
        SELECT COUNT(*) FROM places p
        LEFT JOIN users u ON p.owner_id = u.id WHERE u.id IS NULL
    """)
    test("5.8 — Aucune place orpheline", orphans == 0)

    orphans = get_count(conn, """
        SELECT COUNT(*) FROM reviews r
        LEFT JOIN users u ON r.user_id = u.id WHERE u.id IS NULL
    """)
    test("5.9 — Aucune review sans auteur", orphans == 0)

    orphans = get_count(conn, """
        SELECT COUNT(*) FROM reviews r
        LEFT JOIN places p ON r.place_id = p.id WHERE p.id IS NULL
    """)
    test("5.10 — Aucune review sans place", orphans == 0)


# ============================================================
# SECTION 6 — RBAC
# ============================================================

def test_rbac(conn):
    section("SECTION 6 — RBAC (Role Based Access Control)")

    row = get_one(conn, f"SELECT is_admin FROM users WHERE id = '{ADMIN_ID}'")
    test("6.1 — Admin a is_admin = 1", row and row[0] == 1)

    row = get_one(conn, f"SELECT is_admin FROM users WHERE id = '{JOHN_ID}'")
    test("6.2 — User normal a is_admin = 0", row and row[0] == 0)

    conn.execute(f"UPDATE users SET is_admin = TRUE WHERE id = '{JOHN_ID}'")
    conn.commit()
    row = get_one(conn, f"SELECT is_admin FROM users WHERE id = '{JOHN_ID}'")
    test("6.3 — Promouvoir user normal en admin -> succes", row and row[0] == 1)

    conn.execute(f"UPDATE users SET is_admin = FALSE WHERE id = '{JOHN_ID}'")
    conn.commit()
    row = get_one(conn, f"SELECT is_admin FROM users WHERE id = '{JOHN_ID}'")
    test("6.4 — Retirer droits admin -> succes", row and row[0] == 0)

    admins = get_count(conn, "SELECT COUNT(*) FROM users WHERE is_admin = TRUE")
    test("6.5 — Un seul admin actif", admins == 1)


# ============================================================
# SECTION 7 — SUPPRESSION ORDONNEE
# ============================================================

def test_ordered_delete(conn):
    section("SECTION 7 — SUPPRESSION ORDONNEE")

    conn.execute("DELETE FROM place_amenity")
    conn.commit()
    count = get_count(conn, "SELECT COUNT(*) FROM place_amenity")
    test("7.1 — Supprimer place_amenity d'abord", count == 0)

    conn.execute("DELETE FROM reviews")
    conn.commit()
    count = get_count(conn, "SELECT COUNT(*) FROM reviews")
    test("7.2 — Supprimer toutes les reviews", count == 0)

    conn.execute("DELETE FROM places")
    conn.commit()
    count = get_count(conn, "SELECT COUNT(*) FROM places")
    test("7.3 — Supprimer toutes les places", count == 0)

    conn.execute(f"DELETE FROM users WHERE id != '{ADMIN_ID}'")
    conn.commit()
    count = get_count(conn, "SELECT COUNT(*) FROM users")
    test("7.4 — Supprimer users de test (garde admin)", count == 1)


# ============================================================
# VERIFICATION FINALE
# ============================================================

def test_final_state(conn):
    section("VERIFICATION FINALE")

    row = get_one(conn, f"SELECT email, is_admin FROM users WHERE id = '{ADMIN_ID}'")
    test("F.1 — Seul admin reste dans users",
         row and row[0] == ADMIN_EMAIL and row[1] == 1)

    count = get_count(conn, "SELECT COUNT(*) FROM users")
    test("F.2 — 1 seul user (admin)", count == 1, f"1, obtenu {count}")

    count = get_count(conn, "SELECT COUNT(*) FROM amenities")
    test("F.3 — 3 amenities initiales intactes", count == 3, f"3, obtenu {count}")

    count = get_count(conn, "SELECT COUNT(*) FROM places")
    test("F.4 — 0 places restantes", count == 0, f"0, obtenu {count}")

    count = get_count(conn, "SELECT COUNT(*) FROM reviews")
    test("F.5 — 0 reviews restantes", count == 0, f"0, obtenu {count}")

    count = get_count(conn, "SELECT COUNT(*) FROM place_amenity")
    test("F.6 — 0 place_amenity restantes", count == 0, f"0, obtenu {count}")


# ============================================================
# MAIN
# ============================================================

def main():
    if not os.path.exists(DB_PATH):
        print(f"[ERREUR] Base de donnees introuvable : {DB_PATH}")
        print("Lancez d'abord : flask shell -> from app import db -> db.create_all()")
        sys.exit(1)

    print("\n" + "=" * 60)
    print("   HBNB — TESTS AUTOMATISES")
    print("=" * 60)

    conn = sqlite3.connect(DB_PATH)
    conn.execute("PRAGMA foreign_keys = ON")

    try:
        setup(conn)

        test_initial_data(conn)
        test_crud_users(conn)
        test_crud_amenities(conn)
        test_crud_places(conn)
        test_crud_reviews(conn)
        test_relations(conn)
        test_rbac(conn)
        test_ordered_delete(conn)
        test_final_state(conn)

    finally:
        teardown(conn)
        conn.close()

    print("\n" + "=" * 60)
    print(f"  RESULTATS : {passed}/{total} tests passes")
    if failed == 0:
        print("  TOUS LES TESTS SONT PASSES !")
    else:
        print(f"  {failed} ECHEC(S) — voir les [FAIL] ci-dessus")
    print("=" * 60 + "\n")

    sys.exit(0 if failed == 0 else 1)


if __name__ == "__main__":
    main()
