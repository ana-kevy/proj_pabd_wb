import asyncpg
from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware

#Isso aqui é para poder fazer o INSERT no post do login e sin-up
class cadastro(BaseModel):
    nome: str
    email:str
    senha: str
    sexo: str
    cep: str

class login(BaseModel):
    email: str
    senha: str

#Essa classe é para a tabela Planos (que associa usuário e ao número correspondente ao plano que ele escolheu)
#Lembrando que a tabela ritos não é preenchida pelo usuário, ela apenas lista os ritos disponíveis na funerária e o número deles
class plano(BaseModel):
    tipo_rito: int #varia entre 0 e 1
    user_id: int

#Aqui são as classes da tabela de enterro e cremação:
class DetalhesEnterro(BaseModel):
    plano_id: int
    cor_caixao: str
    material_caixao: str
    estilo_caixao: str
    tipo_lapide: str

class DetalhesCremacao(BaseModel):
    plano_id: int
    cor_das_cinzas: str
    material_pote: str
    cor_do_pote: str
    estilo_pote: str


app = FastAPI()

# Configuração do CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Permite todas as origens
    allow_credentials=True,
    allow_methods=["*"],  # Permite todos os métodos (GET, POST, etc.)
    allow_headers=["*"],  # Permite todos os cabeçalhos
)

#Aqui é a conexão sendo feita com o banco de dados da funerária (que está no PGADMIN)
async def get_db_connection():
    return await asyncpg.connect(
        user="postgres",
        password="sql",
        database="funeraria",
        host="localhost"
    )

@app.get("/test") #Verifica se a conexão do banco com o código foi feita ou não
async def test_connection():
    conn = await get_db_connection()
    await conn.close()
    return {"message": "conexão com o postgre bem sucedida!"}

@app.post("/cadastrar_usuario")
async def cadastrar_usuario(usuario: cadastro): #Essa parte "cadastro" se refere ao base model criado lá em cima
    conn = None
    try:
        conn = await get_db_connection()
        #Para verificar se o email já existe na tabela Cadastro:
        existing_user = await conn.fetchrow("SELECT email FROM cadastro WHERE email = $1", usuario.email)
        if existing_user:
            return {"mensagem": "Erro: Email já cadastrado."}
        
        # Inserir novo usuário e obter user_id gerado automaticamente
        user_id = await conn.fetchval(
            "INSERT INTO cadastro (nome, email, senha, sexo, cep) VALUES ($1, $2, $3, $4, $5) RETURNING user_id",
            usuario.nome, usuario.email, usuario.senha, usuario.sexo, usuario.cep
        )
        return {"mensagem": "Usuário cadastrado com sucesso!", "user_id": user_id}
    
    except Exception as e:
        #aqui é pra gente verificar se não vai dar nenhum erro na hora de testar viu
        #se der ruim, é pq deu MUITO ruim
        return {"mensagem": f"Um erro inesperado aconteceu ao cadastrar o usuário: {str(e)}"} 

    finally:
        if conn:
            await conn.close()

#Função para usuário JÁ cadastrados
@app.get("/usuario_existente")
async def get_usuario(email: str, senha: str):
    conn = None
    try:
        conn = await get_db_connection()

        # Validação de email e senha
        if not email or not senha:
            return {"mensagem": "Email e senha são obrigatórios"}

        # Consulta SQL para verificar se o usuário existe
        existing_user = await conn.fetchrow(
            "SELECT user_id FROM cadastro WHERE email = $1 AND senha = $2;", 
            email, senha
        )

        if existing_user:
            user_id = existing_user['user_id']  # Extrai o user_id do resultado
            return {"mensagem": "Usuário já cadastrado", "user_id": user_id}
        else:
            return {"mensagem": "Usuário não encontrado", "user_id": 0}  # Retorna user_id 0 se não encontrar
        
    except Exception as e:
        return {"mensagem": f"Um erro inesperado aconteceu :( --> {str(e)}"}
    
    finally:
        if conn:
            await conn.close()
    
#Criando um plano: add id_usuário e o rito que ele escolheu:
@app.post("/plano")
async def criar_plano(planinho: plano):
    conn = None
    try:
        conn = await get_db_connection()
        #Como o meu pg admin tá configurado pra auto-preencher o plano_id, talvez possa dar errado no seu computador
        #Se der errado coloque nesse conn.execute() o seguinte:
        #"INSERT INTO plano (plano_id, user_id, tipo_rito) VALUES ($1, $2)", planinho.plano_id, planinho.user_id, planinho.tipo_rito
        #Esse RETURNING plano_id; serve para retorna o plano_id de volta para o js, pois é autoincrementada pelo pgAdmin e preciso para pôr nos detalhes (ou funeral ou cremação)
        plano_id = await conn.fetchval("INSERT INTO plano (user_id, tipo_rito) VALUES ($1, $2) RETURNING plano_id;;", planinho.user_id, planinho.tipo_rito)
        return {"mensagem": "Plano funerário criado com sucesso!", "plano_id": plano_id}
    
    except Exception as e:
        return {"mensagem": f"Um erro inesperado aconteceu :( --> {str(e)}"}
    
    finally:
        if conn:
            await conn.close()

# Função ara inserir detalhes de enterro
@app.post("/detalhes_enterro")
async def inserir_detalhes_enterro(detalhes: DetalhesEnterro):
    conn = None
    try:
        conn = await get_db_connection()

        await conn.execute("INSERT INTO detalhes_enterro (plano_id, cor_caixao, material_caixao, estilo_caixao, tipo_lapide) VALUES ($1, $2, $3, $4, $5);", detalhes.plano_id, detalhes.cor_caixao, detalhes.material_caixao, detalhes.estilo_caixao, detalhes.tipo_lapide)
        return {"mensagem": "Detalhes de enterro cadastrados com sucesso!"}
    
    except Exception as e:
        return {"mensagem": f"Erro ao cadastrar detalhes de enterro: {str(e)}"}
    
    finally:
        if conn:
            await conn.close()

#Função para inserir detalhes de cremação
@app.post("/detalhes_cremacao")
async def inserir_detalhes_cremacao(detalhes: DetalhesCremacao):
    conn = None
    try:

        conn = await get_db_connection()

        await conn.execute("INSERT INTO detalhes_cremacao (plano_id, cor_das_cinzas, material_pote, cor_do_pote, estilo_pote) VALUES ($1, $2, $3, $4, $5);", detalhes.plano_id, detalhes.cor_das_cinzas, detalhes.material_pote, detalhes.cor_do_pote, detalhes.estilo_pote)
        return {"mensagem": "Detalhes de cremação cadastrados com sucesso!"}
    
    except Exception as e:
        return {"mensagem": f"Erro ao cadastrar detalhes de cremação: {str(e)}"}
    
    finally:
        if conn:
            await conn.close()

#Atualizando a tabela (UPDATE) caso o usuario decida que, de repente, quis mudar sua senha (pq? pq sim):
@app.put("/atualiza_user")
async def atualizar_usuario(usuario_atualiza: login):
    conn = None
    try:
        conn = await get_db_connection()

        existent_user1 = await conn.fetchrow("SELECT user_id FROM cadastro WHERE  email = $1;",  usuario_atualiza.email)

        if existent_user1:
            await conn.execute("UPDATE cadastro SET senha = $1 WHERE email = $2", usuario_atualiza.senha, usuario_atualiza.email)
            return {"mensagem": "Senha atualizado com sucesso!"}
        else: 
             return {'message' : 'Usuario não encontrado, assim não podemos atualizar sua senha!'}
        
    except Exception as e:
        return {"mensagem": f"Um erro inesperado aconteceu :( --> {str(e)}"}
    
    finally:
        if conn:
            await conn.close()

#Atender o requisito DELETE caso o usuário decida que odiou o site e quer excluir a conta dele e TODAS as informações veiculadas a ele:
@app.delete('/delete_usuarios')
async def delete_usuario(user_id: int):
    conn = None
    try:
        conn = await get_db_connection()

        existent_user = await conn.fetchrow("SELECT user_id FROM cadastro WHERE user_id = $1;",  user_id)

        if existent_user:
            await conn.execute('DELETE FROM detalhes_enterro WHERE plano_id IN (SELECT plano_id FROM plano WHERE user_id = $1);', user_id)
            await conn.execute('DELETE FROM detalhes_cremacao WHERE plano_id IN (SELECT plano_id FROM plano WHERE user_id = $1);', user_id)
            await conn.execute('DELETE FROM plano WHERE user_id = $1;', user_id)
            await conn.execute('DELETE FROM cadastro WHERE user_id = $1;', user_id)
            return {'message' : 'Usuario deletado e todas as suas informações foram removidas'}
        
        else:
            return {'message' : 'Usuario não encontrado para ser deletado'}
        
    except Exception as e:
        return {"mensagem": f"Um erro inesperado aconteceu :( --> {str(e)}"}
    
    finally:
        if conn:
            await conn.close()

