<<<<<<< HEAD
---
## Detailed Class Diagram – Business Logic Layer

The Business Logic layer contains the core entities of the HBnB application: User, Place, Review, and Amenity. These classes represent the main business concepts and enforce the application’s business rules.

Each entity includes a unique identifier (UUID) as well as creation and update timestamps to ensure traceability and auditability.

A User can own multiple Places and write multiple Reviews. A Place belongs to a single User, can have multiple Reviews, and can include multiple Amenities. Reviews are associated with both a User and a Place, representing feedback left by users on places they have visited.

The Amenity entity represents facilities that can be associated with multiple places, resulting in a many-to-many relationship.

This diagram provides a clear and structured representation of the core business logic and serves as a foundation for the implementation phase.
---
---
## Datailled class Diagram for business logic layer (version 1)
---

```mermaid

classDiagram

class User {
  UUID id
  string first_name
  string last_name
  string email
  string password
  bool is_admin
  datetime created_at
  datetime updated_at

  create()
  update()
  delete()
}

class Place {
  UUID id
  string title
  string description
  float price
  float latitude
  float longitude
  datetime created_at
  datetime updated_at

  create()
  update()
  delete()
}

class Review {
  UUID id
  int rating
  string comment
  datetime created_at
  datetime updated_at

  create()
  update()
  delete()
}

class Amenity {
  UUID id
  string name
  string description
  datetime created_at
  datetime updated_at

  create()
  update()
  delete()
}

=======
# Detailed Class Diagram – Business Logic Layer
## Introduction :

This document presents the detailed class diagram of the Business Logic Layer of the HBnB application.

The Business Logic Layer is responsible for managing the core domain entities and enforcing business rules independently from the presentation and persistence layers.

It defines:

* The main system entities

* Their attributes and methods

* The relationships between them

* Multiplicity rules

* Inheritance structures

The primary entities represented in this diagram are:

- User

- Admin (specialization of User)

- Place

- Review

- Amenity

The diagram follows standard UML conventions including visibility modifiers, associations, inheritance, and multiplicity.

## UML Class Diagram

````mermaid
classDiagram

%% =========================
%% USER
%% =========================
class User {
    -UUID id
    -string first_name
    -string last_name
    -string email
    -string password_hash
    -datetime created_at
    -datetime updated_at

    +register(first_name: string, last_name: string, email: string, password: string) void
    +update_profile(first_name: string, last_name: string, email: string) void
    +change_password(new_password: string) void
    +delete_account() void
}

%% =========================
%% ADMIN
%% =========================
class Admin {
    +manage_users() void
    +manage_places() void
    +manage_reviews() void
    +manage_amenities() void
}

User <|-- Admin

%% =========================
%% PLACE
%% =========================
class Place {
    -UUID id
    -string title
    -string description
    -float price
    -float latitude
    -float longitude
    -datetime created_at
    -datetime updated_at

    +create(title: string, description: string, price: float, latitude: float, longitude: float) void
    +update(title: string, description: string, price: float) void
    +delete() void
}

%% =========================
%% REVIEW
%% =========================
class Review {
    -UUID id
    -int rating
    -string comment
    -datetime created_at
    -datetime updated_at

    +create(rating: int, comment: string) void
    +update(rating: int, comment: string) void
    +delete() void
}

%% =========================
%% AMENITY
%% =========================
class Amenity {
    -UUID id
    -string name
    -string description
    -datetime created_at
    -datetime updated_at

    +create(name: string, description: string) void
    +update(name: string, description: string) void
    +delete() void
}

%% =========================
%% RELATIONSHIPS
%% =========================

>>>>>>> d4236ee3873b598a28b02929212898764f239ffe
User "1" --> "0..*" Place : owns
User "1" --> "0..*" Review : writes
Place "1" --> "0..*" Review : has
Place "0..*" -- "0..*" Amenity : includes
<<<<<<< HEAD

```
---
## Datailled class Diagram for business logic layer (version 2)
---
```mermaid
classDiagram

%% ===== BASE USER =====
class User {
  UUID id
  string first_name
  string last_name
  string email
  string password
  datetime created_at
  datetime updated_at

  register()
  update_profile()
  delete_account()
}

%% ===== ADMIN =====
class Admin {
  manage_users()
  manage_places()
  manage_reviews()
  manage_amenities()
}

%% ===== PLACE =====
class Place {
  UUID id
  string title
  string description
  float price
  float latitude
  float longitude
  datetime created_at
  datetime updated_at

  create()
  update()
  delete()
}

%% ===== REVIEW =====
class Review {
  UUID id
  int rating
  string comment
  datetime created_at
  datetime updated_at

  create()
  update()
  delete()
}

%% ===== AMENITY =====
class Amenity {
  UUID id
  string name
  string description
  datetime created_at
  datetime updated_at

  create()
  update()
  delete()
}

%% ===== RELATIONSHIPS =====

%% OWNER ROLE
User "1" --> "0..*" Place : owns (Owner)

%% VISITOR ROLE
User "1" --> "0..*" Review : writes (Visitor)
User <|-- Admin
%% PLACE RELATIONS
Place "1" --> "0..*" Review : has
Place "0..*" -- "0..*" Amenity : includes

```
---
### Explication of this version
---
## Detailed Class Diagram – Business Logic Layer (version 2)
---

The Business Logic layer is centered around the User entity, which represents all users of the HBnB application. Different roles are derived from the User entity based on behavior and permissions.

An Admin is a specialized type of User with elevated privileges, represented through inheritance. Admin users can manage users, places, reviews, and amenities across the system.

A User can act as an Owner if they own one or more Places. This role is represented through the association between User and Place. Owners are responsible for creating, updating, and deleting their own places.

A User can also act as a Visitor if they do not own places but interact with the platform by browsing places and writing reviews. This role is represented by the association between User and Review.

Places are owned by a single User and can have multiple Reviews. Amenities can be associated with multiple Places, resulting in a many-to-many relationship.

This design clearly separates responsibilities while keeping the model simple and extensible.

---
=======
````
## Entity Descriptions:

1️⃣ User :
--

Represents a platform user who can act both as:

Owner (owns Places)

Visitor (writes Reviews)

### Attributes :

id : UUID → Unique identifier (UUID4)

first_name : string → User’s first name

last_name : string → User’s last name

email : string → Unique login identifier

password_hash : string → Securely stored encrypted password

created_at : datetime → Account creation timestamp

updated_at : datetime → Last modification timestamp

### Methods :

register(...) → Creates a new user

update_profile(...) → Updates personal information

change_password(...) → Updates the password securely

delete_account() → Deletes or deactivates the account

2️⃣ Admin (Inheritance):
---

Admin is a specialization of User.

It inherits all attributes and methods from User and adds administrative privileges.

#### - Additional Methods :

* manage_users()

* manage_places()

* manage_reviews()

* manage_amenities()

This represents UML generalization (inheritance).

3️⃣ Place :
---

Represents a rental property listed on the platform.

#### - Attributes :

id : UUID

title : string

description : string

price : float

latitude : float

longitude : float

created_at : datetime

updated_at : datetime

#### - Methods :

Methods: CRUD operations (Create, Update, Delete)

create(...) → Creates a new place listing

update(...) → Updates place information

delete() → Removes the place from the system

4️⃣ Review :
---

Represents feedback left by a user for a place.

#### - Attributes :

id : UUID

rating : int → Numerical evaluation (e.g., 1–5)

comment : string → Written feedback

created_at : datetime

updated_at : datetime

#### - Methods :

Methods: CRUD operations (Create, Update, Delete)

create(...) → Creates a new review

update(...) → Updates rating or comment

delete() → Deletes the review

5️⃣ Amenity:
---

Represents a feature or service available in a place.

#### - Attributes

id : UUID

name : string

description : string

created_at : datetime

updated_at : datetime

#### - Methods

Methods: CRUD operations (Create, Update, Delete)

create(...) → Adds a new amenity

update(...) → Updates amenity information

delete() → Removes the amenity

## Relationships and Multiplicity
User — Place (Ownership):
---

#### Multiplicity:
1 User → 0..* Places

#### Meaning:

One User can own zero or multiple Places.

Each Place is owned by exactly one User.

#### Type: Association.

User — Review (Author) :
----

#### Multiplicity:
1 User → 0..* Reviews

#### Meaning:

One User can write zero or multiple Reviews.

Each Review is written by exactly one User.

#### Type: Association.

Place — Review :
----

#### Multiplicity:
1 Place → 0..* Reviews

#### Meaning:

One Place can have zero or multiple Reviews.

Each Review belongs to exactly one Place.

#### Type: Association.

Place — Amenity :
----

#### Multiplicity:
0..* ↔ 0..*

#### Meaning:

A Place can include multiple Amenities.

An Amenity can be associated with multiple Places.

#### Type: Many-to-many association.

UML Relationship Notation Explanation
----
#### Generalization (Inheritance)

Notation used:

User <|-- Admin

Solid line with a hollow triangle

Triangle points to the parent class

Represents inheritance

Meaning:
Admin is a specialized User and inherits its attributes and methods.

#### Association

Notation example:

User --> Place

Solid line

Multiplicity on both sides

Represents structural relationship

Multiplicity Symbols

1 → Exactly one

0..* → Zero or many

1..* → One or many

0..1 → Optional

Multiplicity defines business constraints between entities.

## Conclusion

This class diagram provides a structured representation of the Business Logic Layer of the HBnB application.

It respects object-oriented and UML principles by:

* Using encapsulation (private attributes, public methods)

* Clearly defining entity responsibilities

* Representing inheritance properly

* Specifying accurate multiplicities

* Including UUID identifiers and timestamps for traceability

* The model establishes a solid and scalable foundation for implementing the HBnB domain logic before moving to persistence or presentation layers.
>>>>>>> d4236ee3873b598a28b02929212898764f239ffe
