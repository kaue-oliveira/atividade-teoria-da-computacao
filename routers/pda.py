from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Dict, Any
import uuid
from automata.pda.npda import NPDA

from fastapi.responses import StreamingResponse

router = APIRouter()
pda_db = {}

class PDACreateRequest(BaseModel):
    states: List[str]
    input_symbols: List[str]
    stack_symbols: List[str]
    transitions: Dict[str, Dict[str, Dict[str, List[List[Any]]]]]
    initial_state: str
    initial_stack_symbol: str
    final_states: List[str]

@router.post("/create")
async def create_pda(request: PDACreateRequest):
    pda_id = str(uuid.uuid4())
    try:
        npda = NPDA(
            states=set(request.states),
            input_symbols=set(request.input_symbols),
            stack_symbols=set(request.stack_symbols),
            transitions=request.transitions,
            initial_state=request.initial_state,
            initial_stack_symbol=request.initial_stack_symbol,
            final_states=set(request.final_states)
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    
    pda_db[pda_id] = npda
    return {"id": pda_id}

@router.get("/{pda_id}")
async def get_pda(pda_id: str):
    pda = pda_db.get(pda_id)
    if not pda:
        raise HTTPException(status_code=404, detail="PDA not found")
    
    return {
        "states": list(pda.states),
        "input_symbols": list(pda.input_symbols),
        "stack_symbols": list(pda.stack_symbols),
        "transitions": pda.transitions,
        "initial_state": pda.initial_state,
        "initial_stack_symbol": pda.initial_stack_symbol,
        "final_states": list(pda.final_states)
    }

@router.post("/{pda_id}/accept")
async def test_acceptance(pda_id: str, string: str):
    pda = pda_db.get(pda_id)
    if not pda:
        raise HTTPException(status_code=404, detail="PDA not found")
    
    try:
        accepted = pda.accepts_input(string)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    
    return {"accepted": accepted}

from graphviz import Digraph

@router.get("/{pda_id}/visualize")
async def visualize_pda(pda_id: str):
    pda = pda_db.get(pda_id)
    if pda is None:
        raise HTTPException(status_code=404, detail="PDA not found")
    
    try:
        dot = Digraph()
        dot.attr(rankdir='LR')
        
        # Add states
        for state in pda.states:
            if state in pda.final_states:
                dot.node(state, state, shape='doublecircle')
            else:
                dot.node(state, state, shape='circle')
        
        # Add transitions
        for from_state, input_dict in pda.transitions.items():
            for input_symbol, stack_dict in input_dict.items():
                for stack_top, transitions in stack_dict.items():
                    for transition in transitions:
                        to_state, stack_push = transition
                        label = f"{input_symbol},{stack_top}/{stack_push}"
                        dot.edge(from_state, to_state, label=label)
        
        # Mark initial state
        dot.node('', '', shape='none')
        dot.edge('', pda.initial_state)
        
        # Render to PNG
        buf = BytesIO()
        buf.write(dot.pipe(format='png'))
        buf.seek(0)
        return StreamingResponse(buf, media_type="image/png")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
        raise HTTPException(status_code=500, detail=str(e))

from io import BytesIO
