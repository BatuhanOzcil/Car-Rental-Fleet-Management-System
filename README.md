# Car Rental Fleet Management System

A Python-based Object-Oriented application designed to simulate real-world logistics and fleet management software. 

This project implements core backend principles including state management, file-based data persistence, and robust business logic for a car rental service.

## Features
* **Core Business Logic:** Complete transaction lifecycle including adding vehicles to the fleet, renting them out, and returning them. The system automatically calculates total costs based on daily rates and rental duration.
* **State Management & Persistence:** Saves and loads fleet and rental history to a local text file (`fleet_data.txt`) to maintain data across sessions.
* **Custom Exception Handling:** Robust error management using custom Python exceptions such as `VehicleUnavailableError`, `InvalidDurationError`, and `VehicleNotFoundError` to prevent invalid transactions.
* **Data Analysis & Reporting:** Generates revenue reports summarizing total income and calculates the most popular rented vehicle category.
* **Interactive CLI:** A user-friendly console interface to navigate through the fleet management system seamlessly.

## Tech Stack
* **Language:** Python

## How to Run
Ensure you have Python installed on your system. Run the script via terminal:

```bash
python main.py
