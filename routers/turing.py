from fastapi import APIRouter, HTTPException
from graphviz import Digraph
from pydantic import BaseModel
from typing import List, Dict, Tuple
import uuid
from automata.tm.dtm import DTM as TuringMachine
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from io import BytesIO
from fastapi.responses import StreamingResponse

router = APIRouter()
turing_db = {}

class TuringCreateRequest(BaseModel):
    states: List[str]
    input_symbols: List[str]
    tape_symbols: List[str]
    transitions: Dict[str, Dict[str, Tuple[str, str, str]]]
    initial_state: str
    blank_symbol: str
    final_states: List[str]

@router.post("/create")
async def create_turing(request: TuringCreateRequest):
    turing_id = str(uuid.uuid4())
    try:
        tm = TuringMachine(
            states=set(request.states),
            input_symbols=set(request.input_symbols),
            tape_symbols=set(request.tape_symbols),
            transitions=request.transitions,
            initial_state=request.initial_state,
            blank_symbol=request.blank_symbol,
            final_states=set(request.final_states)
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    
    turing_db[turing_id] = tm
    return {"id": turing_id}

@router.get("/{turing_id}")
async def get_turing(turing_id: str):
    tm = turing_db.get(turing_id)
    if not tm:
        raise HTTPException(status_code=404, detail="Turing Machine not found")
    
    return {
        "states": list(tm.states),
        "input_symbols": list(tm.input_symbols),
        "tape_symbols": list(tm.tape_symbols),
        "transitions": tm.transitions,
        "initial_state": tm.initial_state,
        "blank_symbol": tm.blank_symbol,
        "final_states": list(tm.final_states)
    }

@router.post("/{turing_id}/accept")
async def test_acceptance(turing_id: str, string: str):
    tm = turing_db.get(turing_id)
    if not tm:
        raise HTTPException(status_code=404, detail="Turing Machine not found")
    
    try:
        accepted = tm.accepts_input(string)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    
    return {"accepted": accepted}


@router.get("/{tm_id}/visualize")
async def visualize_tm(tm_id: str):
    tm = turing_db.get(tm_id)
    if tm is None:
        raise HTTPException(status_code=404, detail="TM not found")
    
    try:
        dot = Digraph()
        dot.attr(rankdir='LR')
        
        # Add states
        for state in tm.states:
            if state in tm.final_states:
                dot.node(state, state, shape='doublecircle')
            else:
                dot.node(state, state, shape='circle')
        
        # Add transitions
        for from_state, transitions in tm.transitions.items():
            for symbol, (to_state, write_symbol, direction) in transitions.items():
                label = f"{symbol}/{write_symbol},{direction}"
                dot.edge(from_state, to_state, label=label)
        
        # Mark initial state
        dot.node('', '', shape='none')
        dot.edge('', tm.initial_state)
        
        # Render to PNG
        buf = BytesIO()
        buf.write(dot.pipe(format='png'))
        buf.seek(0)
        return StreamingResponse(buf, media_type="image/png")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
        raise HTTPException(status_code=500, detail=str(e))