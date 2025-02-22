from fastapi import FastAPI
from routes import organizacao, vaga, voluntario, inscricao

app = FastAPI()


app.include_router(organizacao.router)
app.include_router(vaga.router)
app.include_router(voluntario.router)
app.include_router(inscricao.router)