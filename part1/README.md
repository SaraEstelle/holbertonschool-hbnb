# HBnB Evolution – Part 1: Technical Documentation

## Project Overview

HBnB Evolution is a simplified AirBnB-like application designed to demonstrate best practices in software architecture and object-oriented design.

The purpose of Part 1 of this project is to create comprehensive technical documentation that defines the architecture, core business logic, and interactions within the system. This documentation serves as a blueprint for the implementation phases that follow.

---

## Objectives

The main objectives of this part are:

- Understand and apply a layered architecture
- Design the core business entities of the application
- Represent system interactions using UML diagrams
- Provide clear documentation to guide future development

---

## Application Architecture

The HBnB Evolution application follows a **three-layered architecture**, ensuring a clear separation of concerns:

### 1. Presentation Layer
- Handles user interactions
- Exposes APIs and services
- Does not contain business logic

### 2. Business Logic Layer
- Contains the core business rules
- Defines the main domain models:
  - User
  - Place
  - Review
  - Amenity

### 3. Persistence Layer
- Manages data storage and retrieval
- Interacts directly with the database

---

## Facade Pattern

To simplify communication between layers, the application uses the **Facade design pattern**.

The Facade provides a unified interface between the Presentation Layer and the Business Logic Layer, hiding internal complexity and reducing coupling between components.

---

## UML Diagrams

This part of the project includes the following UML diagrams:

### High-Level Package Diagram
- Illustrates the three-layer architecture
- Shows communication between layers via the Facade pattern

### Class Diagram (Business Logic Layer)
- Represents the core entities and their relationships
- Includes attributes, methods, and associations

### Sequence Diagrams
- Demonstrate interactions between layers for key API calls:
  - User registration
  - Place creation
  - Review submission
  - Fetching a list of places

---

## Project Structure
part1/
├── README.md
├── high_level_package_diagram.md
├── class_diagram.md
├── sequence_diagrams/
│ ├── user_registration.md
│ ├── place_creation.md
│ ├── review_submission.md
│ └── list_places.md

---

## Tools and Resources

- UML notation
- Mermaid.js for diagrams
- draw.io (optional)
- Object-Oriented Programming principles

---

## Expected Outcome

By the end of this part, the project provides a clear and structured technical documentation that:

- Describes the system architecture
- Defines the business logic
- Explains interactions between components
- Prepares the ground for implementation in future parts

---

## Author
REBATI SARA
PLANCHON VALENTIN
ROSSI DAMIEN

HBnB Evolution Project – Part 1
Holberton School - Thonon
