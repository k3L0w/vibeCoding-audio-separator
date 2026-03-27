# AGENTS.md

## Objetivo
Este repositório é uma plataforma web de separação musical em 6 stems para o mercado brasileiro.

## Como os agentes devem trabalhar
1. Ler o contexto antes de propor mudanças.
2. Apresentar plano curto antes de editar muitos arquivos.
3. Fazer mudanças pequenas e incrementais.
4. Explicar riscos em billing, auth, storage e processamento.
5. Nunca remover arquivos sem avisar.
6. Nunca alterar esquema do banco sem migration.

## Áreas críticas
- billing
- autenticação
- storage privado
- worker de processamento
- limites por plano
- webhooks

## Regras obrigatórias
- Toda mudança em billing precisa de teste.
- Toda rota privada precisa validar user_id.
- Toda alteração em upload/download precisa manter controle de acesso.
- Todo job do worker deve registrar status, tempo e erro.