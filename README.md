# 🏥 MedPass

**MedPass** é um sistema web de **gerenciamento e automação de senhas** desenvolvido para **UPAs** e **Policlínicas de Mato Grosso**.  
A proposta é oferecer uma forma simples e eficiente de organizar o atendimento, reduzindo filas e garantindo um fluxo automatizado de senhas médicas e especialidades.

---

## 📋 Sumário
- [Sobre o Projeto](#-sobre-o-projeto)
- [Tecnologias Utilizadas](#-tecnologias-utilizadas)
- [Arquitetura do Projeto](#-arquitetura-do-projeto)
- [Instalação e Configuração](#-instalação-e-configuração)
- [Como Executar o Projeto](#-como-executar-o-projeto)
- [Funcionalidades](#-funcionalidades)
- [Estrutura de Pastas](#-estrutura-de-pastas)
- [Contribuindo](#-contribuindo)
- [Roadmap](#-roadmap)
- [Licença](#-licença)

---

## 💡 Sobre o Projeto

O **MedPass** nasceu da necessidade de modernizar o atendimento em unidades de saúde pública, permitindo:
- Geração automatizada de senhas por especialidade;
- Controle centralizado de médicos e especialidades;
- Exibição em tempo real das senhas sendo chamadas;
- Redução de filas e otimização do tempo de espera.

Atualmente, o sistema encontra-se na **fase inicial**, mas **já é funcional** — servindo como um protótipo sólido para expansão futura.

---

## 🛠️ Tecnologias Utilizadas

| Categoria | Tecnologias |
|------------|--------------|
| **Back-end** | [Django 5+](https://www.djangoproject.com/) |
| **Front-end** | HTML5, [Tailwind CSS](https://tailwindcss.com/), [Feather Icons](https://feathericons.com/) |
| **Banco de Dados** | SQLite (para desenvolvimento) |
| **Linguagem** | Python 3.12+ |
| **Outros** | Templates do Django, Estrutura MVC (Model-View-Controller) |

---

## 🧩 Arquitetura do Projeto

O **MedPass** segue o padrão **Django MVC (Model-View-Template)**, organizando o código em módulos bem definidos:

- **Modelos (`models.py`)** → Estruturas de dados e tabelas do banco.
- **Views (`views.py`)** → Regras de negócio e controle das rotas.
- **Templates (`templates/`)** → Interfaces HTML estilizadas com Tailwind e Feather Icons.

---

## ⚙️ Instalação e Configuração

### 1️⃣ Clone o repositório
```bash
git clone https://github.com/seuusuario/medpass.git
cd medpass
