# API RESTful - MedPass

## Base URL
```
http://localhost:8000/api/
```

## Endpoints Disponíveis

### 📋 Especialidades

#### Listar todas as especialidades
```http
GET /api/especialidades/
```

#### Listar especialidades ativas
```http
GET /api/especialidades/ativas/
```

#### Criar especialidade
```http
POST /api/especialidades/
Content-Type: application/json

{
    "nome": "Cardiologia",
    "descricao": "Especialidade médica focada no coração",
    "ativo": true
}
```

#### Obter especialidade específica
```http
GET /api/especialidades/{id}/
```

#### Atualizar especialidade
```http
PUT /api/especialidades/{id}/
Content-Type: application/json

{
    "nome": "Cardiologia",
    "descricao": "Especialidade atualizada",
    "ativo": true
}
```

#### Deletar especialidade
```http
DELETE /api/especialidades/{id}/
```

---

### 👨‍⚕️ Profissionais

#### Listar todos os profissionais
```http
GET /api/profissionais/
```

#### Listar profissionais ativos
```http
GET /api/profissionais/ativos/
```

#### Listar profissionais por especialidade
```http
GET /api/profissionais/por_especialidade/?especialidade_id={id}
```

#### Criar profissional
```http
POST /api/profissionais/
Content-Type: application/json

{
    "nome": "Dr. João Silva",
    "crm": "12345-SP",
    "especialidade": 1,
    "telefone": "(11) 98765-4321",
    "email": "joao.silva@medpass.com",
    "ativo": true
}
```

#### Obter profissional específico
```http
GET /api/profissionais/{id}/
```

#### Atualizar profissional
```http
PUT /api/profissionais/{id}/
Content-Type: application/json

{
    "nome": "Dr. João Silva",
    "crm": "12345-SP",
    "especialidade": 1,
    "telefone": "(11) 98765-4321",
    "email": "joao.silva@medpass.com",
    "ativo": true
}
```

#### Deletar profissional
```http
DELETE /api/profissionais/{id}/
```

---

### 🎫 Senhas

#### Listar todas as senhas
```http
GET /api/senhas/
```

#### Gerar nova senha
```http
POST /api/senhas/
Content-Type: application/json

{
    "especialidade": 1,
    "tipo": "normal"  // ou "prioritario"
}
```

**Resposta:**
```json
{
    "id": 1,
    "numero": "CAR-N-001",
    "especialidade": 1,
    "especialidade_nome": "Cardiologia",
    "tipo": "normal",
    "tipo_display": "Normal",
    "status": "aguardando",
    "status_display": "Aguardando",
    "guiche": null,
    "criado_em": "2025-11-16T14:30:00Z",
    "chamado_em": null,
    "atendido_em": null,
    "finalizado_em": null,
    "atualizado_em": "2025-11-16T14:30:00Z"
}
```

#### Senhas aguardando
```http
GET /api/senhas/aguardando/
```

#### Senhas sendo chamadas
```http
GET /api/senhas/chamando/
```

#### Senhas em atendimento
```http
GET /api/senhas/em_atendimento/
```

#### Senhas finalizadas
```http
GET /api/senhas/finalizadas/
```

#### Senhas de hoje
```http
GET /api/senhas/hoje/
```

#### Próxima senha (prioritárias primeiro)
```http
GET /api/senhas/proxima/
```

#### Estatísticas
```http
GET /api/senhas/estatisticas/
```

**Resposta:**
```json
{
    "total_hoje": 25,
    "aguardando": 5,
    "chamando": 1,
    "em_atendimento": 3,
    "finalizadas_hoje": 16,
    "data": "2025-11-16"
}
```

#### Dados para o painel
```http
GET /api/senhas/painel/
```

**Resposta:**
```json
{
    "senha_chamando": {
        "id": 5,
        "numero": "CAR-N-005",
        "especialidade_nome": "Cardiologia",
        "guiche": 3,
        "status": "chamando"
    },
    "ultimas_chamadas": [...],
    "senhas_aguardando": [...],
    "estatisticas": {
        "total_hoje": 25,
        "total_atendidas": 16,
        "total_aguardando": 5,
        "total_em_atendimento": 3
    }
}
```

#### Chamar senha
```http
POST /api/senhas/{id}/chamar/
Content-Type: application/json

{
    "guiche": 3
}
```

#### Iniciar atendimento
```http
POST /api/senhas/{id}/iniciar_atendimento/
```

#### Finalizar atendimento
```http
POST /api/senhas/{id}/finalizar/
```

#### Cancelar senha
```http
POST /api/senhas/{id}/cancelar/
```

---

## Status das Senhas

- `aguardando`: Senha gerada, aguardando ser chamada
- `chamando`: Senha sendo chamada no painel
- `atendimento`: Paciente em atendimento
- `finalizado`: Atendimento concluído ou senha cancelada

## Tipos de Senha

- `normal`: Senha normal
- `prioritario`: Senha prioritária (idosos, gestantes, etc.)

## Códigos de Status HTTP

- `200 OK`: Requisição bem-sucedida
- `201 Created`: Recurso criado com sucesso
- `400 Bad Request`: Dados inválidos
- `404 Not Found`: Recurso não encontrado
- `500 Internal Server Error`: Erro no servidor

## Exemplos de Uso

### Python (requests)
```python
import requests

# Gerar uma nova senha
response = requests.post(
    'http://localhost:8000/api/senhas/',
    json={
        'especialidade': 1,
        'tipo': 'normal'
    }
)
senha = response.json()
print(f"Senha gerada: {senha['numero']}")

# Chamar a senha
response = requests.post(
    f'http://localhost:8000/api/senhas/{senha["id"]}/chamar/',
    json={'guiche': 3}
)
```

### JavaScript (fetch)
```javascript
// Gerar uma nova senha
fetch('http://localhost:8000/api/senhas/', {
    method: 'POST',
    headers: {
        'Content-Type': 'application/json',
    },
    body: JSON.stringify({
        especialidade: 1,
        tipo: 'normal'
    })
})
.then(response => response.json())
.then(data => {
    console.log('Senha gerada:', data.numero);
});

// Obter dados do painel
fetch('http://localhost:8000/api/senhas/painel/')
    .then(response => response.json())
    .then(data => {
        console.log('Senha chamando:', data.senha_chamando);
        console.log('Estatísticas:', data.estatisticas);
    });
```

### cURL
```bash
# Gerar senha
curl -X POST http://localhost:8000/api/senhas/ \
  -H "Content-Type: application/json" \
  -d '{"especialidade": 1, "tipo": "normal"}'

# Chamar senha
curl -X POST http://localhost:8000/api/senhas/1/chamar/ \
  -H "Content-Type: application/json" \
  -d '{"guiche": 3}'

# Ver estatísticas
curl http://localhost:8000/api/senhas/estatisticas/
```

## Interface Navegável

Você pode acessar a interface navegável da API em:
```
http://localhost:8000/api/
```

Esta interface permite testar todos os endpoints diretamente no navegador.
