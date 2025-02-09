# Automata API

A powerful FastAPI-based API for simulating and testing different types of automata: AFD (Deterministic Finite Automaton), PDA (Pushdown Automaton), and Turing Machines.

## Features

- Create and test AFDs, PDAs, and Turing Machines
- Visual representation of automata using GraphViz
- Input string acceptance testing
- Interactive web interface
- RESTful API endpoints
- Swagger and ReDoc documentation

## Setup and Installation

### Prerequisites

- Python 3.7+
- GraphViz installation
- Modern web browser

### Installation Steps

1. Clone the repository:

git clone <repository-url>
cd automata-api


2. Install dependencies:

pip install -r requirements.txt


3. Start the backend server:

uvicorn main:app --reload --host 0.0.0.0 --port 8000


4. Start the frontend server:

python -m http.server 3000


### Access Points

- Frontend Interface: http://localhost:3000
- Swagger Documentation: http://localhost:8000/docs
- ReDoc Documentation: http://localhost:8000/redoc

## API Usage Examples

### 1. AFD (Deterministic Finite Automaton)

Example: Create an AFD that accepts strings ending in "01"


{
    "states": ["q0", "q1", "q2"],
    "input_symbols": ["0", "1"],
    "transitions": {
        "q0": {
            "0": "q0",
            "1": "q1"
        },
        "q1": {
            "0": "q2",
            "1": "q1"
        },
        "q2": {
            "0": "q2",
            "1": "q2"
        }
    },
    "initial_state": "q0",
    "final_states": ["q2"]
}


### 2. PDA (Pushdown Automaton)

Example: Create a PDA that accepts a^n b^n


{
    "states": ["q0", "q1", "q2"],
    "input_symbols": ["a", "b"],
    "stack_symbols": ["A", "Z"],
    "transitions": {
        "q0": {
            "a": {
                "Z": [["q0", ["A", "Z"]]],
                "A": [["q0", ["A", "A"]]]
            },
            "b": {
                "A": [["q1", []]]
            }
        },
        "q1": {
            "b": {
                "A": [["q1", []]]
            },
            "": {
                "Z": [["q2", ["Z"]]]
            }
        }
    },
    "initial_state": "q0",
    "initial_stack_symbol": "Z",
    "final_states": ["q2"]
}


### 3. Turing Machine

Example: Create a TM that accepts a^n b^n c^n


{
    "states": ["q0", "q1", "q2", "q3", "qf"],
    "input_symbols": ["a", "b", "c"],
    "tape_symbols": ["a", "b", "c", "X", "Y", "Z", "_"],
    "transitions": {
        "q0": {
            "a": ["q1", "X", "R"],
            "Y": ["q3", "Y", "R"]
        },
        "q1": {
            "a": ["q1", "a", "R"],
            "b": ["q2", "Y", "R"],
            "Y": ["q1", "Y", "R"]
        },
        "q2": {
            "b": ["q2", "b", "R"],
            "c": ["q0", "Z", "L"],
            "Z": ["q2", "Z", "R"]
        },
        "q3": {
            "Y": ["q3", "Y", "R"],
            "Z": ["q3", "Z", "R"],
            "_": ["qf", "_", "R"]
        }
    },
    "initial_state": "q0",
    "blank_symbol": "_",
    "final_states": ["qf"]
}


## API Endpoints

### AFD Endpoints
- `POST /afd/create`: Create new AFD
- `GET /afd/{afd_id}`: Get AFD details
- `POST /afd/{afd_id}/accept`: Test string acceptance
- `GET /afd/{afd_id}/visualize`: Generate visual representation

### PDA Endpoints
- `POST /pda/create`: Create new PDA
- `GET /pda/{pda_id}`: Get PDA details
- `POST /pda/{pda_id}/accept`: Test string acceptance
- `GET /pda/{pda_id}/visualize`: Generate visual representation

### Turing Machine Endpoints
- `POST /tm/create`: Create new TM
- `GET /tm/{tm_id}`: Get TM details
- `POST /tm/{tm_id}/accept`: Test string acceptance
- `GET /tm/{tm_id}/visualize`: Generate visual representation

## Limitations and Specifications

### Input Constraints
- AFD: Binary alphabet (0,1)
- PDA: Limited to push and pop operations
- TM: Single tape implementation
- Single-character input symbols only


### Input Requirements
- Well-formed JSON according to professor specifications
- Standard state naming convention (q0, q1, etc.)
- Strict JSON format adherence required

###Thanks for using this project!
