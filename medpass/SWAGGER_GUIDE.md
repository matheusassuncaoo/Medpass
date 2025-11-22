# 🎨 Documentação Swagger/OpenAPI - MedPass

## ✅ Implementado com Sucesso!

A documentação interativa da API foi configurada usando **drf-spectacular**, a melhor solução para Django REST Framework.

## 📚 Acesse a Documentação

### 🔷 Swagger UI (Recomendado)
Interface interativa e moderna para testar a API:
```
http://localhost:8000/api/docs/
```

### 🔶 ReDoc
Documentação alternativa, estilo documentação de referência:
```
http://localhost:8000/api/redoc/
```

### 📄 Schema OpenAPI (JSON)
Schema bruto em formato OpenAPI 3.0:
```
http://localhost:8000/api/schema/
```

## 🎯 O que foi implementado

### ✅ Configuração
- ✅ `drf-spectacular` instalado
- ✅ Configurações adicionadas ao `settings.py`
- ✅ Rotas configuradas no `urls.py`
- ✅ Decoradores `@extend_schema` nos ViewSets

### ✅ Documentação Automática
- ✅ Todos os endpoints documentados
- ✅ Descrições detalhadas de cada operação
- ✅ Exemplos de requisições
- ✅ Parâmetros explicados
- ✅ Tipos de resposta definidos
- ✅ Tags organizadas por módulo

### ✅ Recursos do Swagger UI

#### Testar Endpoints
- Botão "Try it out" em cada endpoint
- Executar requisições direto do navegador
- Ver respostas em tempo real

#### Exemplos de Código
- cURL
- Python (requests)
- JavaScript (fetch)
- E mais...

#### Schemas
- Ver estrutura completa dos modelos
- Campos obrigatórios e opcionais
- Tipos de dados
- Validações

## 📖 Tags Organizadas

A documentação está organizada em 3 grupos principais:

### 🏥 Especialidades
- Listar todas
- Criar nova
- Atualizar
- Deletar
- Listar apenas ativas

### 👨‍⚕️ Profissionais
- Listar todos
- Criar novo
- Atualizar
- Deletar
- Listar apenas ativos
- Filtrar por especialidade

### 🎫 Senhas
- Gerar nova senha
- Listar por status
- Chamar senha
- Iniciar atendimento
- Finalizar atendimento
- Cancelar senha
- Próxima senha
- Estatísticas
- Dados do painel

## 🎮 Como Usar o Swagger UI

### 1. Abra o Swagger UI
```
http://localhost:8000/api/docs/
```

### 2. Escolha um Endpoint
Clique em qualquer endpoint para expandir

### 3. Clique em "Try it out"
Habilita o modo de teste

### 4. Preencha os Parâmetros
- Query params
- Path params
- Request body

### 5. Execute
Clique em "Execute" para fazer a requisição

### 6. Veja a Resposta
- Status code
- Response body
- Headers
- cURL command

## 🔥 Exemplo: Gerar Senha via Swagger

1. Acesse: http://localhost:8000/api/docs/
2. Procure por **Senhas** → **POST /api/senhas/**
3. Clique em **"Try it out"**
4. No campo Request body, coloque:
```json
{
  "especialidade": 1,
  "tipo": "normal"
}
```
5. Clique em **"Execute"**
6. Veja a senha gerada na resposta!

## 📊 Vantagens do Swagger

### ✅ Para Desenvolvedores
- Teste endpoints sem Postman
- Documentação sempre atualizada
- Exemplos de código automáticos
- Validação de schemas

### ✅ Para Equipe
- Documentação visual e interativa
- Fácil entendimento da API
- Não precisa ler código
- Exemplos prontos para usar

### ✅ Para Integração
- Schema OpenAPI padrão da indústria
- Compatível com ferramentas como:
  - Postman (importar schema)
  - Insomnia
  - Geradores de código
  - Validadores automáticos

## 🎨 Personalização

A documentação foi configurada com:

```python
SPECTACULAR_SETTINGS = {
    'TITLE': 'MedPass API',
    'DESCRIPTION': 'API RESTful para sistema de gerenciamento de senhas médicas',
    'VERSION': '1.0.0',
    'CONTACT': {
        'name': 'MedPass',
        'email': 'contato@medpass.com',
    },
    'LICENSE': {
        'name': 'MIT License',
    },
    'TAGS': [
        {'name': 'Especialidades', 'description': 'Gerenciamento de especialidades médicas'},
        {'name': 'Profissionais', 'description': 'Gerenciamento de profissionais de saúde'},
        {'name': 'Senhas', 'description': 'Sistema de senhas e atendimento'},
    ],
}
```

## 🚀 Próximos Passos

Para produção, considere:

1. **Autenticação**
   - Adicionar JWT/OAuth2 ao Swagger
   - Botão "Authorize" funcional

2. **Exemplos Reais**
   - Adicionar mais exemplos de requests
   - Casos de uso específicos

3. **Versionamento**
   - Documentar múltiplas versões da API
   - v1, v2, etc.

4. **Exportação**
   - Gerar PDF da documentação
   - Exportar para outros formatos

## 📝 Comandos Úteis

### Gerar Schema em Arquivo
```bash
python manage.py spectacular --file schema.yml
```

### Validar Schema
```bash
python manage.py spectacular --validate
```

---

**🎉 Swagger configurado com sucesso!**

Acesse agora: http://localhost:8000/api/docs/
