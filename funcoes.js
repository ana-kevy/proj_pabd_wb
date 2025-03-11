export async function testarConexao() {
    try {
        const response = await fetch('http://127.0.0.1:8000/test');
        const data = await response.json();
        console.log('Resposta da API:', data);
    } catch (error) {
        console.error('Erro ao testar conexão:', error);
    }
}


export async function cadastrarUsuario(usuario) {
    try {
        const response = await fetch('http://127.0.0.1:8000/cadastrar_usuario', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify(usuario),
        });
        const data = await response.json();
        console.log('Resposta da API:', data);
        return data;
    } catch (error) {
        console.error('Erro ao cadastrar usuário:', error);
    }
}


export async function login(email, senha) {
    try {
        // Monta a URL com os parâmetros de email e senha
        // encodeURIComponent serve para codificar caracteres especiais para evitar erros
        const url = `http://127.0.0.1:8000/usuario_existente?email=${encodeURIComponent(email)}&senha=${encodeURIComponent(senha)}`;

        const response = await fetch(url, {
            method: 'GET', // Usar GET para enviar dados na URL
            headers: {
                'Content-Type': 'application/json', // Indica que a resposta é JSON
            },
        });

        const data = await response.json(); // Converte a resposta para JSON
        console.log('Resposta da API:', data); // Ver no console para teste

        // Verifica se a resposta contém user_id
        if (data.user_id !== undefined) {
            return {data: data, user_id: data.user_id };// Retorna o objeto com data e user_id
        } else {
            throw new Error("Resposta da API não contém user_id");
        }
    } catch (error) {
        console.error('Erro ao verificar usuário:', error);
        throw error; // Lança o erro para ser capturado no catch do verificar_login
    }
}


export async function criarPlano(plano) {
    try {
        const response = await fetch('http://127.0.0.1:8000/plano', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify(plano),
        });
        const data = await response.json();
        console.log('Resposta da API:', data);
        return data.plano_id; // Retorna o plano_id gerado
    } catch (error) {
        console.error('Erro ao criar plano:', error);
    }
}


export async function inserirDetalhesEnterro(detalhes) {
    try {
        const response = await fetch('http://127.0.0.1:8000/detalhes_enterro', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify(detalhes),
        });
        const data = await response.json();
        console.log('Resposta da API:', data);
        return data;
    } catch (error) {
        console.error('Erro ao inserir detalhes de enterro:', error);
    }
}


export async function inserirDetalhesCremacao(detalhes) {
    try {
        const response = await fetch('http://127.0.0.1:8000/detalhes_cremacao', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify(detalhes),
        });
        const data = await response.json();
        console.log('Resposta da API:', data);
        return data;
    } catch (error) {
        console.error('Erro ao inserir detalhes de cremação:', error);
    }
}


export async function atualizarSenha(usuario) {
    try {
        const response = await fetch('http://127.0.0.1:8000/atualiza_user', {
            method: 'PUT',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify(usuario),
        });
        const data = await response.json();
        console.log('Resposta da API:', data);
        return data;
    } catch (error) {
        console.error('Erro ao atualizar senha:', error);
    }
}


export async function excluirUsuario(user_id) {
    try {
        const response = await fetch(`http://127.0.0.1:8000/delete_usuarios?user_id=${user_id}`, {
            method: 'DELETE',
            headers: {'Content-Type': 'application/json'},
        });
        const data = await response.json();
        console.log('Resposta da API:', data);
        return data;
    } catch (error) {
        console.error('Erro ao excluir usuário:', error);
    }
}

