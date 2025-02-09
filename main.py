from fastapi import FastAPI
from routers import afd, pda, turing
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="Automata API", version="1.0.0")

app.include_router(afd.router, prefix="/afd", tags=["AFD"])
app.include_router(pda.router, prefix="/pda", tags=["PDA"])
app.include_router(turing.router, prefix="/tm", tags=["Turing Machine"])

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

from automata.tm.dtm import DTM  # For deterministic Turing Machine

from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
