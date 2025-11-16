# 🎯 API RESTful - MedPass

Transformamos o sistema MedPass em uma **API RESTful completa** usando Django REST Framework!

## 🚀 O que foi implementado

### ✅ Instalação e Configuração
- Django REST Framework instalado e configurado
- Serializers para todos os modelos (Especialidade, Profissional, Senha)
- ViewSets com operações CRUD completas
- Sistema de rotas automático com DefaultRouter

### 📡 Endpoints Disponíveis

#### **Especialidades** (`/api/especialidades/`)
- ✅ Listar todas
- ✅ Criar nova
- ✅ Atualizar
- ✅ Deletar
- ✅ Listar apenas ativas

#### **Profissionais** (`/api/profissionais/`)
- ✅ Listar todos
- ✅ Criar novo
- ✅ Atualizar
- ✅ Deletar
- ✅ Listar apenas ativos
- ✅ Filtrar por especialidade

#### **Senhas** (`/api/senhas/`)
- ✅ Listar todas
- ✅ Gerar nova senha (automático)
- ✅ Chamar senha (com guichê)
- ✅ Iniciar atendimento
- ✅ Finalizar atendimento
- ✅ Cancelar senha
- ✅ Listar por status (aguardando, chamando, atendimento, finalizadas)
- ✅ Senhas de hoje
- ✅ Próxima senha (prioritárias primeiro)
- ✅ Estatísticas completas
- ✅ Endpoint especial para painel

## 🎮 Como Usar

### 1. Acessar a Interface Navegável
```
http://localhost:8000/api/
```
A interface do Django REST Framework permite testar todos os endpoints diretamente no navegador!

### 2. Exemplo: Gerar uma Senha

**Request:**
```http
POST http://localhost:8000/api/senhas/
Content-Type: application/json

{
    "especialidade": 1,
    "tipo": "normal"
}
```

**Response:**
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
    "criado_em": "2025-11-16T14:30:00-04:00",
    "chamado_em": null,
    "atendido_em": null,
    "finalizado_em": null
}
```

### 3. Exemplo: Chamar Senha

**Request:**
```http
POST http://localhost:8000/api/senhas/1/chamar/
Content-Type: application/json

{
    "guiche": 3
}
```

### 4. Exemplo: Dados para o Painel

**Request:**
```http
GET http://localhost:8000/api/senhas/painel/
```

**Response:**
```json
{
    "senha_chamando": {
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

## 📚 Documentação Completa

Veja o arquivo `API_DOCUMENTATION.md` para documentação detalhada de todos os endpoints, exemplos em Python, JavaScript e cURL.

## 🔧 Recursos Especiais

### Geração Automática de Número de Senha
O sistema gera automaticamente números no formato:
```
SIGLA-TIPO-NÚMERO
Exemplo: CAR-N-001, CAR-P-002
```
- **SIGLA**: 3 primeiras letras da especialidade
- **TIPO**: P (Prioritário) ou N (Normal)
- **NÚMERO**: Contador sequencial do dia

### Priorização Automática
O endpoint `/api/senhas/proxima/` retorna automaticamente senhas prioritárias primeiro.

### Validações de Negócio
- ✅ Só pode chamar senha com status "aguardando"
- ✅ Só pode iniciar atendimento com status "chamando"
- ✅ Só pode finalizar com status "chamando" ou "atendimento"
- ✅ Não pode cancelar senha já finalizada

## 🎨 Interface Web + API

O sistema mantém:
- ✅ Todas as páginas web originais funcionando
- ✅ Nova API RESTful para integração
- ✅ Painel de senhas com atualização automática
- ✅ Sistema de fala (TTS) no painel

## 🌐 Integração com Frontend

Agora você pode criar:
- Apps mobile (React Native, Flutter)
- SPAs (React, Vue, Angular)
- Apps desktop (Electron)
- Integrações com outros sistemas

Tudo usando a API RESTful!

## 📊 Endpoints Mais Úteis

| Endpoint | Método | Descrição |
|----------|--------|-----------|
| `/api/senhas/` | POST | Gerar nova senha |
| `/api/senhas/{id}/chamar/` | POST | Chamar senha |
| `/api/senhas/painel/` | GET | Dados do painel |
| `/api/senhas/estatisticas/` | GET | Estatísticas |
| `/api/senhas/proxima/` | GET | Próxima senha |
| `/api/especialidades/ativas/` | GET | Especialidades ativas |

## 🚀 Próximos Passos

Para usar em produção, considere:
1. Adicionar autenticação (JWT, OAuth)
2. Implementar rate limiting
3. Adicionar cache (Redis)
4. Configurar CORS para apps externos
5. Documentação com Swagger/OpenAPI

---

**Desenvolvido com Django REST Framework** 🐍
