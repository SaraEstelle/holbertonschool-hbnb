# HBnB Technical Documentation
## Introduction

This document provides a comprehensive technical overview of the HBnB application. It consolidates all architectural and design diagrams created in previous tasks into a single reference.

The purpose of this document is to guide the implementation phases, clarify system architecture, and provide detailed insight into the behavior and interactions of key components.

It includes:

* High-Level Package Diagram — overview of layered architecture

* Business Logic Layer Class Diagram — detailed entities, attributes, methods, and relationships

* API Sequence Diagrams — step-by-step flow for key API calls

## 1. High-Level Architecture
### Overview :

HBnB follows a layered architecture with three main layers:

- Presentation Layer — handles client interactions (REST API, Application Services)

- Business Logic Layer — manages core domain entities, business rules, and Facade interfaces

- Persistence Layer — handles data storage and retrieval via repositories

This structure improves maintainability, scalability, and testability while enforcing separation of concerns.

### Layer Responsibilities :
| Layer | Responsibilities | Components |
|-------|----------------|------------|
| Presentation | Handle HTTP requests, validate inputs, format responses | REST API, Application Services |
| Business Logic | Validate business rules, manage domain entities | Facade, Models (User, Place, Review, Amenity) |
| Persistence | Store, retrieve, update, delete data | Repository, Database |

The Facade provides a unified interface to the Business Logic Layer, reducing coupling between Presentation and domain models.

### Benefits:

Simplifies communication

Improves maintainability and scalability

Provides single entry point for business operations

## High-Level Package Diagram
````mermaid
flowchart TB

subgraph Presentation["Presentation Layer"]
    API["REST API"]
    Services["Application Services"]
end

Facade["Facade\n(Application Interface)"]

subgraph Business["Business Logic Layer"]
    User["User"]
    Place["Place"]
    Review["Review"]
    Amenity["Amenity"]
end

subgraph Persistence["Persistence Layer"]
    Repository["Repositories"]
    Database["Database"]
end

API --> Services
Services --> Facade

Facade --> User
Facade --> Place
Facade --> Review
Facade --> Amenity

User --> Repository
Place --> Repository
Review --> Repository
Amenity --> Repository

Repository --> Database
````
### Diagram Explanation:

Top-to-bottom flow: request moves downward, response moves upward

Arrows: indicate method calls, communication, and delegation

Facade: centralizes access to domain models

Repository: abstracts persistence layer to ensure loose coupling

## 2. Detailed Class Diagram – Business Logic Layer
### Introduction

The Business Logic Layer manages core entities and enforces rules. This diagram represents:

* Entities: User, Admin, Place, Review, Amenity

* Attributes and methods with visibility (private/protected/public)

* Relationships and multiplicity rules

* Inheritance (Admin extends User)

## UML Class Diagram
````mermaid
classDiagram

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

class Admin {
    +manage_users() void
    +manage_places() void
    +manage_reviews() void
    +manage_amenities() void
}

User <|-- Admin

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

User "1" --> "0..*" Place : owns
User "1" --> "0..*" Review : writes
Place "1" --> "0..*" Review : has
Place "0..*" -- "0..*" Amenity : includes
````

### Relationships Summary:

User → Place: 1-to-many, solid line, represents ownership

User → Review: 1-to-many, solid line, represents authorship

Place → Review: 1-to-many, solid line, represents feedback on a place

Place ↔ Amenity: many-to-many, dashed line, represents included amenities

## 3. API Sequence Diagrams
### Overview

Sequence diagrams illustrate how the layers interact for key API calls. They highlight:

* Input validation and business rule enforcement

* Step-by-step message flow between Presentation, Business Logic, and Persistence

* Success and error responses with HTTP status codes

### 3.1 User Registration (POST /users) :
### Description:
This diagram shows the full lifecycle of a user registration request. It illustrates how the API validates the request format, how the Business Logic Layer (Facade and UserModel) enforces business rules (e.g., unique email), and how the user is persisted to the database. Error scenarios such as invalid data or rule violations are also represented with appropriate HTTP status codes.

````mermaid
sequenceDiagram
    actor User
    participant API
    participant Facade
    participant UserModel
    participant Repository

    User ->> API: POST /users
    API ->> API: validate request format

    alt invalid data
        API -->> User: 400 Bad Request
    else valid
        API ->> Facade: register_user(data)
        Facade ->> UserModel: validate_business_rules(email uniqueness, format)

        alt rule violation
            Facade -->> API: validation error
            API -->> User: 422 Unprocessable Entity
        else ok
            UserModel ->> Repository: save(user)
            Repository -->> Facade: saved
            Facade -->> API: success
            API -->> User: 201 Created
        end
    end
````
### 3.2 Place Creation (POST /places) :
Description:
This diagram demonstrates how an Owner creates a new Place. It includes request validation, authorization checks, and business rule enforcement. It also shows the persistence step via the Repository and possible error responses such as 400, 403, or 422, depending on the type of violation.

````mermaid
sequenceDiagram
    actor Owner
    participant API
    participant Facade
    participant PlaceModel
    participant Repository

    Owner ->> API: POST /places
    API ->> API: validate request

    alt invalid
        API -->> Owner: 400 Bad Request
    else valid
        API ->> Facade: create_place(data, owner_id)
        Facade ->> PlaceModel: validate_owner + business rules

        alt violation
            API -->> Owner: 403/422 Error
        else ok
            PlaceModel ->> Repository: save(place)
            Repository -->> Facade: saved
            Facade -->> API: success
            API -->> Owner: 201 Created
        end
    end
````
### 3.3 Review Submission (POST /reviews) :
Description:
This diagram illustrates how a Visitor submits a review. It highlights API-level validation, business rule checks (rating limits, uniqueness, and place existence), and persistence. Different error codes (400, 422, 409) are returned depending on the type of failure, while a successful submission returns 201 Created.

````mermaid
sequenceDiagram
    actor Visitor
    participant API
    participant Facade
    participant ReviewModel
    participant Repository

    Visitor ->> API: POST /reviews
    API ->> API: validate request

    alt invalid
        API -->> Visitor: 400 Bad Request
    else valid
        API ->> Facade: create_review(data)
        Facade ->> ReviewModel: validate rules (rating, existence, uniqueness)

        alt violation
            API -->> Visitor: 422/409 Error
        else ok
            ReviewModel ->> Repository: save(review)
            Repository -->> Facade: saved
            Facade -->> API: success
            API -->> Visitor: 201 Created
        end
    end
`````

### 3.4 Fetching Places (GET /places) :
Description:
This diagram shows how users retrieve a list of Places. It demonstrates API-level query validation, interaction with the Facade and Repository layers, and successful retrieval or error handling (400 Bad Request) for invalid filters. It also emphasizes the distinction between read and write operations.

````mermaid
sequenceDiagram
    actor User
    participant API
    participant Facade
    participant PlaceModel
    participant Repository

    User ->> API: GET /places
    API ->> API: validate filters

    alt invalid filters
        API -->> User: 400 Bad Request
    else valid
        API ->> Facade: get_places(filters)
        Facade ->> Repository: query_places(filters)
        Repository -->> Facade: places
        Facade -->> API: response
        API -->> User: 200 OK
    end
````

## Conclusion

This comprehensive documentation consolidates the HBnB architecture and system behavior.

Key takeaways:

* Clear separation of layers ensures maintainable and scalable design

* Business Logic Layer enforces domain rules with structured entities and relationships

* Sequence diagrams clarify API call handling, validation, and persistence interactions

* UML conventions and Facade pattern support clean architecture principles

This document serves as a single source of truth for developers, ensuring consistency and clarity throughout implementation and future maintenance.
