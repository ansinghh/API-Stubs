# API-Stubs

**API-Stubs** is the second part of the Smart Home API system, complementing the [`API_Smart_Home`](https://github.com/ansinghh/API_Smart_Home) backend. This repository provides stubbed versions of API endpoints used by the smart home system, allowing frontend developers to work independently of the live backend. It is especially useful during early‑stage development and testing.

---

## Features

- Mock/stub API responses for key endpoints  
- Enables frontend testing without backend dependency  
- Lightweight FastAPI‑based simulation server  
- Modular and easy to extend with additional routes  

---

## Technologies Used

- Python  
- FastAPI  
- Uvicorn  
- SQLite (optional or future use)  
- Pytest (for testing)  

---

## Getting Started

### Prerequisites

- Python 3.7 or higher  
- `pip` package manager  

### Installation

1. **Clone the repository**

   ```bash
   git clone https://github.com/ansinghh/API-Stubs.git
   cd API-Stubs
2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
3. **Run the application**
   ```bash
   uvicorn main:app --reload
4. **Test**
5. ```bash
   pytest
