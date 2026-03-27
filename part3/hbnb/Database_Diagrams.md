# HBnB — Diagramme Entité-Relation (ER)

Ce diagramme représente le schema complet de la base de données du projet HBnB,
généré avec Mermaid.js.

## Diagramme principal

```mermaid
erDiagram
    USER {
        char(36)    id          PK
        varchar(50) first_name
        varchar(50) last_name
        varchar(120) email      UK
        varchar(128) password
        boolean     is_admin
        datetime    created_at
        datetime    updated_at
    }

    PLACE {
        char(36)       id          PK
        varchar(255)   title
        text           description
        decimal(10_2)  price
        float          latitude
        float          longitude
        char(36)       owner_id    FK
        datetime       created_at
        datetime       updated_at
    }

    REVIEW {
        char(36)  id        PK
        text      text
        int       rating
        char(36)  user_id   FK
        char(36)  place_id  FK
        datetime  created_at
        datetime  updated_at
    }

    AMENITY {
        char(36)     id          PK
        varchar(255) name        UK
        datetime     created_at
        datetime     updated_at
    }

    PLACE_AMENITY {
        char(36) place_id    FK
        char(36) amenity_id  FK
    }

    USER ||--o{ PLACE        : "possede (owner_id)"
    USER ||--o{ REVIEW       : "ecrit (user_id)"
    PLACE ||--o{ REVIEW      : "recoit (place_id)"
    PLACE ||--o{ PLACE_AMENITY : "possede"
    AMENITY ||--o{ PLACE_AMENITY : "associee a"
```

---

## Description des relations

### User → Place (One-to-Many)
Un utilisateur peut posseder plusieurs logements.
Chaque logement appartient a un seul utilisateur (`owner_id`).

```
USER ||--o{ PLACE : "possede"
```

### User → Review (One-to-Many)
Un utilisateur peut ecrire plusieurs avis.
Chaque avis est ecrit par un seul utilisateur (`user_id`).

```
USER ||--o{ REVIEW : "ecrit"
```

### Place → Review (One-to-Many)
Un logement peut recevoir plusieurs avis.
Chaque avis concerne un seul logement (`place_id`).

```
PLACE ||--o{ REVIEW : "recoit"
```

### Place ↔ Amenity (Many-to-Many)
Un logement peut avoir plusieurs equipements.
Un equipement peut etre associe a plusieurs logements.
Cette relation est geree par la table de jonction `PLACE_AMENITY`.

```
PLACE ||--o{ PLACE_AMENITY : "possede"
AMENITY ||--o{ PLACE_AMENITY : "associee a"
```

---

## Contraintes importantes

| Table | Contrainte | Colonne |
|---|---|---|
| `users` | UNIQUE | `email` |
| `amenities` | UNIQUE | `name` |
| `reviews` | UNIQUE | `(user_id, place_id)` |
| `place_amenity` | PRIMARY KEY composite | `(place_id, amenity_id)` |
| `places` | CHECK | `price > 0` |
| `places` | CHECK | `latitude BETWEEN -90 AND 90` |
| `places` | CHECK | `longitude BETWEEN -180 AND 180` |
| `reviews` | CHECK | `rating BETWEEN 1 AND 5` |

---

## Diagramme etendu — avec Reservation (bonus)

La task demande d'imaginer une entite `Reservation` liee a `User` et `Place` :

```mermaid
erDiagram
    USER {
        char(36)     id          PK
        varchar(50)  first_name
        varchar(50)  last_name
        varchar(120) email       UK
        varchar(128) password
        boolean      is_admin
        datetime     created_at
        datetime     updated_at
    }

    PLACE {
        char(36)      id          PK
        varchar(255)  title
        text          description
        decimal(10_2) price
        float         latitude
        float         longitude
        char(36)      owner_id    FK
        datetime      created_at
        datetime      updated_at
    }

    REVIEW {
        char(36)  id        PK
        text      text
        int       rating
        char(36)  user_id   FK
        char(36)  place_id  FK
        datetime  created_at
        datetime  updated_at
    }

    AMENITY {
        char(36)     id          PK
        varchar(255) name        UK
        datetime     created_at
        datetime     updated_at
    }

    PLACE_AMENITY {
        char(36) place_id    FK
        char(36) amenity_id  FK
    }

    RESERVATION {
        char(36)      id          PK
        char(36)      user_id     FK
        char(36)      place_id    FK
        date          start_date
        date          end_date
        decimal(10_2) total_price
        varchar(20)   status
        datetime      created_at
        datetime      updated_at
    }

    USER ||--o{ PLACE        : "possede"
    USER ||--o{ REVIEW       : "ecrit"
    USER ||--o{ RESERVATION  : "fait"
    PLACE ||--o{ REVIEW      : "recoit"
    PLACE ||--o{ PLACE_AMENITY : "possede"
    PLACE ||--o{ RESERVATION : "est reservee"
    AMENITY ||--o{ PLACE_AMENITY : "associee a"
```

### Pourquoi Reservation ?
- Un `User` peut faire plusieurs reservations → `user_id` FK vers `users`
- Une `Place` peut etre reservee plusieurs fois → `place_id` FK vers `places`
- `status` peut etre : `pending`, `confirmed`, `cancelled`
- `total_price` = calculee automatiquement selon les dates et le prix par nuit
