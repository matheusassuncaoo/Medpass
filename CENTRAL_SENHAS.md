# Central de Senhas - MedPass

## ✅ Funcionalidades Implementadas

### 1. Modelo de Dados
- **Modelo Senha**: Criado com os seguintes campos:
  - Número da senha (N001, P001, U001)
  - Tipo (Normal, Preferencial, Urgência)
  - Especialidade
  - Status (Aguardando, Chamando, Atendendo, Concluído, Cancelado)
  - Profissional responsável
  - Guichê
  - Timestamps de criação, chamada, atendimento e conclusão

### 2. Rotas Implementadas
- `/central-senhas/` - Visualizar central de senhas
- `/gerar-senha/` - Gerar nova senha
- `/chamar-senha/<id>/` - Chamar senha para atendimento
- `/atualizar-status-senha/<id>/` - Atualizar status da senha

### 3. Interface Web
- **Coluna 1**: Gerar Senha
  - Seleção de especialidade
  - Escolha do tipo (Normal/Preferencial/Urgência)
  - Botão para gerar

- **Coluna 2**: Senhas Aguardando
  - Lista de senhas em espera
  - Botão para chamar cada senha
  - Informações: número, tipo, especialidade, horário

- **Coluna 3**: Em Atendimento
  - Senhas sendo chamadas
  - Senhas em atendimento
  - Botões para avançar status
  - Informações de guichê e profissional

### 4. Funcionalidades JavaScript
- Auto-refresh a cada 10 segundos
- Chamada de senha com seleção de guichê
- Atualização de status via AJAX
- Tratamento de erros

## 📋 Como Usar

### Gerar uma Senha
1. Acesse a Central de Senhas
2. Selecione a especialidade
3. Escolha o tipo de senha
4. Clique em "Gerar Senha"

### Chamar uma Senha
1. Na lista "Aguardando", clique em "Chamar"
2. Digite o número do guichê
3. A senha mudará para status "Chamando"

### Atender uma Senha
1. Na lista de senhas "Chamando", clique em "Iniciar Atendimento"
2. A senha mudará para status "Atendendo"

### Concluir um Atendimento
1. Na lista de senhas "Atendendo", clique em "Concluir"
2. A senha será marcada como concluída

## 🗃️ Banco de Dados

- ✅ Migração aplicada: `0002_senha`
- ✅ 4 especialidades cadastradas:
  - Cardiologia
  - Pediatria
  - Ortopedia
  - Clínica Geral

## 🔧 Configurações

### CSRF Token
- CSRF_TRUSTED_ORIGINS configurado para localhost
- Proteção CSRF ativa em todos os formulários

### Auto-refresh
- Página atualiza automaticamente a cada 10 segundos
- Mantém visualização atualizada sem intervenção manual

## 🚀 Para Iniciar o Servidor

```bash
cd /workspaces/Medpass/medpass
/workspaces/Medpass/.venv/bin/python manage.py runserver
```

Acesse: http://127.0.0.1:8000/central-senhas/
