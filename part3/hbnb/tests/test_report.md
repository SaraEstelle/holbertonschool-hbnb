# HBnB — Rapport de Tests
**Date :**
**Testeur :**
**Version :** Part 3

---

## Environnement de test

| Propriete | Valeur |
|---|---|
| DB | `instance/development.db` |
| Outil SQL | `sqlite3` |
| Version SQLite | `3.45.1` |
| URL API | `http://127.0.0.1:5000/api/v1/` |

---

## SECTION 1 — AUTH

| ID | Test | Attendu | Obtenu | Status |
|---|---|---|---|---|
| 1.1 | Login admin valide | `200` + token | | |
| 1.2 | Login mauvais mot de passe | `401` | | |
| 1.3 | Login email inexistant | `401` | | |
| 1.4 | Acces protege sans token | `401` | | |
| 1.5 | Acces protege avec token valide | `201` | | |

---

## SECTION 2 — CRUD : USERS

| ID | Test | Attendu | Obtenu | Status |
|---|---|---|---|---|
| 2.1 | Creer user valide (John) | `201` | | |
| 2.2 | Creer deuxieme user (Jane) | `201` | | |
| 2.3 | Email duplique | `422` | | |
| 2.4 | Lire tous les users | `200` (3 users) | | |
| 2.5 | Lire user par ID | `200` | | |
| 2.6 | Lire user inexistant | `404` | | |
| 2.7 | Modifier son propre profil | `200` | | |
| 2.8 | Modifier profil d'un autre | `403` | | |
| 2.9 | Modifier email via PUT /users | `400` | | |

---

## SECTION 3 — CRUD : AMENITIES

| ID | Test | Attendu | Obtenu | Status |
|---|---|---|---|---|
| 3.1 | Creer amenity valide (admin) | `201` | | |
| 3.2 | Creer amenity sans etre admin | `403` | | |
| 3.3 | Lire toutes les amenities | `200` | | |
| 3.4 | Lire amenity par ID | `200` | | |
| 3.5 | Lire amenity inexistante | `404` | | |
| 3.6 | Modifier amenity (admin) | `200` | | |
| 3.7 | Modifier amenity sans etre admin | `403` | | |

---

## SECTION 4 — CRUD : PLACES

| ID | Test | Attendu | Obtenu | Status |
|---|---|---|---|---|
| 4.1 | Creer place valide | `201` | | |
| 4.2 | Prix negatif | `400` | | |
| 4.3 | Latitude invalide | `400` | | |
| 4.4 | Lire toutes les places | `200` | | |
| 4.5 | Lire place par ID (owner + amenities) | `200` | | |
| 4.6 | Lire place inexistante | `404` | | |
| 4.7 | Modifier sa propre place | `200` | | |
| 4.8 | Modifier place d'un autre | `403` | | |

---

## SECTION 5 — CRUD : REVIEWS

| ID | Test | Attendu | Obtenu | Status |
|---|---|---|---|---|
| 5.1 | Creer review valide (Jane) | `201` | | |
| 5.2 | Review sur sa propre place | `400` | | |
| 5.3 | Doublon review | `400` | | |
| 5.4 | Rating invalide | `400` | | |
| 5.5 | Lire toutes les reviews | `200` | | |
| 5.6 | Lire review par ID | `200` | | |
| 5.7 | Lire reviews d'une place | `200` | | |
| 5.8 | Modifier sa propre review | `200` | | |
| 5.9 | Modifier review d'un autre | `403` | | |
| 5.10 | Supprimer sa propre review | `200` | | |
| 5.11 | Supprimer review inexistante | `404` | | |

---

## SECTION 6 — RBAC

| ID | Test | Attendu | Obtenu | Status |
|---|---|---|---|---|
| 6.1 | Admin cree un user | `201` | | |
| 6.2 | User normal cree un user | `403` | | |
| 6.3 | Admin modifie user d'un autre | `200` | | |
| 6.4 | Admin cree une amenity | `201` | | |
| 6.5 | User normal cree une amenity | `403` | | |
| 6.6 | Admin modifie place d'un autre | `200` | | |
| 6.7 | Admin supprime review d'un autre | `200` | | |
| 6.8 | Admin modifie une amenity | `200` | | |

---

## SECTION 7 — RELATIONS

| ID | Test | Attendu | Obtenu | Status |
|---|---|---|---|---|
| 7.1 | GET place retourne owner imbrique | `200` + owner | | |
| 7.2 | GET place retourne amenities | `200` + amenities | | |
| 7.3 | GET reviews retourne user_id/place_id | `200` + ids | | |
| 7.4 | Reviews place inexistante | `404` | | |

---

## SECTION 8 — TESTS SQL (run_tests.py)

```bash
python3 tests/run_tests.py
```

| Section | Tests | Passes | Echoues |
|---|---|---|---|
| 0 — Donnees initiales | 6 | | |
| 1 — CRUD Users | 10 | | |
| 2 — CRUD Amenities | 6 | | |
| 3 — CRUD Places | 10 | | |
| 4 — CRUD Reviews | 11 | | |
| 5 — Relations | 10 | | |
| 6 — RBAC | 5 | | |
| 7 — Suppression ordonnee | 4 | | |
| Final | 6 | | |
| **TOTAL** | **68** | | |

---

## Bugs identifies

| ID | Description | Fichier | Status |
|---|---|---|---|
| | | | |

---

## Conclusion

| Categorie | Resultat |
|---|---|
| Auth | |
| CRUD | |
| RBAC | |
| Relations | |
| Integrite DB | |
| **Bilan global** | |

---

