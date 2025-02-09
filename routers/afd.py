from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Dict
import uuid
from automata.fa.dfa import DFA
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from io import BytesIO
from fastapi.responses import StreamingResponse
from automata.base import exceptions
import graphviz

router = APIRouter()
afd_db = {}

class AFDCreateRequest(BaseModel):
    states: List[str]
    input_symbols: List[str]
    transitions: Dict[str, Dict[str, str]]
    initial_state: str
    final_states: List[str]

@router.post("/create")
async def create_afd(request: AFDCreateRequest):
    afd_id = str(uuid.uuid4())
    try:
        dfa = DFA(
            states=set(request.states),
            input_symbols=set(request.input_symbols),
            transitions=request.transitions,
            initial_state=request.initial_state,
            final_states=set(request.final_states)
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    
    afd_db[afd_id] = dfa
    return {"id": afd_id}

@router.get("/{afd_id}")
async def get_afd(afd_id: str):
    dfa = afd_db.get(afd_id)
    if dfa is None:  # Changed from 'if not dfa'
        raise HTTPException(status_code=404, detail="AFD not found")
    
    return {
        "states": list(dfa.states),
        "input_symbols": list(dfa.input_symbols),
        "transitions": dfa.transitions,
        "initial_state": dfa.initial_state,
        "final_states": list(dfa.final_states)
    }

@router.post("/{afd_id}/accept")
async def test_acceptance(afd_id: str, string: str):
    dfa = afd_db.get(afd_id)
    if dfa is None:  # Changed from 'if not dfa:'
        raise HTTPException(status_code=404, detail="AFD not found")
    
    try:
        accepted = dfa.accepts_input(string)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    
    return {"accepted": accepted}
from graphviz import Digraph

@router.get("/{afd_id}/visualize")
async def visualize_afd(afd_id: str):
    dfa = afd_db.get(afd_id)
    if dfa is None:
        raise HTTPException(status_code=404, detail="AFD not found")
    
    try:
        dot = Digraph()
        dot.attr(rankdir='LR')
        
        # Add states
        for state in dfa.states:
            if state in dfa.final_states:
                dot.node(state, state, shape='doublecircle')
            else:
                dot.node(state, state, shape='circle')
        
        # Add transitions
        for from_state, transitions in dfa.transitions.items():
            for symbol, to_state in transitions.items():
                dot.edge(from_state, to_state, label=symbol)
        
        # Mark initial state
        dot.node('', '', shape='none')
        dot.edge('', dfa.initial_state)
        
        # Render to PNG
        buf = BytesIO()
        buf.write(dot.pipe(format='png'))
        buf.seek(0)
        return StreamingResponse(buf, media_type="image/png")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
