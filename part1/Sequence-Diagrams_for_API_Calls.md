# Sequence Diagrams – HBnB Application

## Overview

This document presents sequence diagrams illustrating how the different layers of the HBnB application interact to handle key API calls. These diagrams show the flow of information between the Presentation Layer, the Business Logic Layer, and the Persistence Layer.

---

## User Registration

This sequence diagram illustrates the process of creating a new user account. The request flows from the API to the Business Logic layer through the Facade, where validation and user creation are performed before persisting the data.

## Diagramme 1 : User Registration
```mermaid
sequenceDiagram
    actor User
    participant API
    participant Facade
    participant UserModel
    participant Repository

    User ->> API: POST /users (registration data)
    API ->> Facade: register_user(data)
    Facade ->> UserModel: create_user(data)
    UserModel ->> Repository: save(user)
    Repository -->> UserModel: user_saved
    UserModel -->> Facade: user_created
    Facade -->> API: success response
    API -->> User: 201 Created
```
---
## Place creation : owner
This diagram represents the creation of a place by an Owner. The system validates ownership and business rules before saving the place in the database.

```mermaid
sequenceDiagram
    actor Owner
    participant API
    participant Facade
    participant PlaceModel
    participant Repository

    Owner ->> API: POST /places
    API ->> Facade: create_place(data, owner_id)
    Facade ->> PlaceModel: validate_owner(owner_id)
    PlaceModel ->> PlaceModel: create_place(data)
    PlaceModel ->> Repository: save(place)
    Repository -->> PlaceModel: place_saved
    PlaceModel -->> Facade: place_created
    Facade -->> API: success response
    API -->> Owner: 201 Created
```
---
## Diagramme 3 : Review Submission (Visitor)

This diagram shows how a Visitor submits a review for a place. The review is validated and stored while respecting the layered architecture.


```mermaid
sequenceDiagram
    actor Visitor
    participant API
    participant Facade
    participant ReviewModel
    participant Repository

    Visitor ->> API: POST /reviews
    API ->> Facade: create_review(data)
    Facade ->> ReviewModel: validate_review(data)
    ReviewModel ->> Repository: save(review)
    Repository -->> ReviewModel: review_saved
    ReviewModel -->> Facade: review_created
    Facade -->> API: success response
    API -->> Visitor: 201 Created
````
---
## Diagramm : Fetching a List of Places

This diagram illustrates how users retrieve a list of places. The request is processed through the Business Logic layer before querying the database and returning the results.

```mermaid
sequenceDiagram
    actor User
    participant API
    participant Facade
    participant PlaceModel
    participant Repository

    User ->> API: GET /places (filters)
    API ->> Facade: get_places(filters)
    Facade ->> PlaceModel: fetch_places(filters)
    PlaceModel ->> Repository: query_places(filters)
    Repository -->> PlaceModel: places_list
    PlaceModel -->> Facade: places
    Facade -->> API: response
    API -->> User: 200 OK (places list)
```
---
