# 📚 ExoRehab 3D - Índice da Documentação

<div align="center">

**Documentação Completa v3.0**

Bem-vindo à documentação completa do **ExoRehab 3D**, um simulador de exoesqueleto para fisioterapia com planejamento de trajetória usando o algoritmo A*.

[🏠 Voltar ao README](../README.md)

</div>

---

## 🚀 Começando

### Para Usuários Finais (Fisioterapeutas, Estudantes)

1. **[GUIA_RAPIDO.md](GUIA_RAPIDO.md)** ⭐ COMECE AQUI
   - Início rápido em 3 passos
   - Controles da visualização 3D
   - Casos de uso comuns
   - Configurações recomendadas por tipo de reabilitação
   - **Tempo de leitura**: 10 minutos

2. **[README.md](README.md)**
   - Visão geral do projeto
   - Funcionalidades principais
   - Como usar o simulador
   - Tecnologias utilizadas
   - **Tempo de leitura**: 15 minutos

---

## 🏥 Aplicações Clínicas

3. **[APLICACOES_CLINICAS.md](APLICACOES_CLINICAS.md)**
   - Fundamentos da robótica na fisioterapia
   - Protocolos de tratamento detalhados:
     - Reabilitação pós-AVC
     - Recuperação de cirurgias (LCA, ombro)
     - Treinamento de marcha (lesão medular)
     - Parkinson
   - Estudos de caso reais
   - Métricas e avaliação de progresso
   - Contraindicações e precauções
   - **Tempo de leitura**: 25 minutos
   - **Para**: Fisioterapeutas, profissionais de saúde

---

## 🧠 Fundamentos Técnicos

4. **[ALGORITMO_A_STAR.md](ALGORITMO_A_STAR.md)**
   - Explicação detalhada do algoritmo A*
   - Espaço de configuração (C-Space)
   - Funções de custo e heurística
   - Detecção de colisão (cápsula vs esfera)
   - Suavização com Catmull-Rom splines
   - Análise de complexidade
   - Propriedades matemáticas (teoremas)
   - Comparação A* vs Interpolação Linear
   - **Tempo de leitura**: 30 minutos
   - **Para**: Programadores, pesquisadores, estudantes de IA

---

## 🔧 Suporte Técnico

5. **[INSTALACAO_TROUBLESHOOTING.md](INSTALACAO_TROUBLESHOOTING.md)**
   - Requisitos do sistema
   - Instalação passo a passo
   - Solução de problemas comuns:
     - Tela preta / WebGL
     - "Nenhum caminho encontrado"
     - Desempenho lento
     - Problemas de exportação
   - Versão offline (sem internet)
   - Diagnóstico avançado
   - Personalização e backup
   - **Tempo de leitura**: 20 minutos
   - **Para**: Todos os usuários, especialmente em caso de problemas

---

## 📊 Exemplos e Dados

6. **[exemplo_trajetoria.csv](exemplo_trajetoria.csv)**
   - Arquivo CSV de exemplo
   - Mostra formato de dados exportados
   - 50 frames de uma trajetória planejada
   - Inclui metadados e dados em graus/radianos
   - **Para**: Referência de formato de dados

---

## 🎯 Fluxo de Aprendizado Recomendado

### 📍 Nível Iniciante
**Objetivo**: Usar o simulador para planejamento de fisioterapia

```
1. README.md (visão geral)
   ↓
2. GUIA_RAPIDO.md (começar a usar)
   ↓
3. Abrir simulatorReabilty.html e testar
   ↓
4. APLICACOES_CLINICAS.md (protocolos)
   ↓
5. Consultar INSTALACAO_TROUBLESHOOTING.md se necessário
```

**Tempo total**: 1-2 horas

---

### 🧪 Nível Intermediário
**Objetivo**: Entender como funciona o planejamento de trajetória

```
1. README.md + GUIA_RAPIDO.md
   ↓
2. Usar o simulador (experimentar)
   ↓
3. ALGORITMO_A_STAR.md (seções introdutórias)
   ↓
4. APLICACOES_CLINICAS.md (casos de uso)
   ↓
5. Experimentar diferentes configurações
   ↓
6. Analisar arquivos CSV exportados
```

**Tempo total**: 3-4 horas

---

### 🔬 Nível Avançado
**Objetivo**: Dominar o sistema e possivelmente modificá-lo

```
1. Toda a documentação acima
   ↓
2. ALGORITMO_A_STAR.md (completo, incluindo matemática)
   ↓
3. Análise do código-fonte (simulatorReabilty.html)
   ↓
4. Experimentos com parâmetros
   ↓
5. Personalização (cores, dimensões, algoritmos)
   ↓
6. Desenvolvimento de extensões
```

**Tempo total**: 8-12 horas

---

## 📋 Checklist de Uso

### Primeira Vez Usando o Simulador:

- [ ] Leu o GUIA_RAPIDO.md
- [ ] Verificou requisitos do sistema
- [ ] Abriu simulatorReabilty.html no navegador
- [ ] Testou controles 3D (rotacionar, zoom)
- [ ] Executou uma simulação de exemplo
- [ ] Entendeu a diferença entre A* e Interpolação Linear

### Para Uso Clínico:

- [ ] Leu APLICACOES_CLINICAS.md
- [ ] Escolheu protocolo adequado para condição do paciente
- [ ] Definiu objetivos SMART
- [ ] Configurou parâmetros corretos (tipo, ângulos)
- [ ] Executou simulação e verificou resultado
- [ ] Exportou dados para documentação

### Para Pesquisa/Desenvolvimento:

- [ ] Leu ALGORITMO_A_STAR.md completamente
- [ ] Entendeu espaço de configuração
- [ ] Analisou funções de custo e heurística
- [ ] Compreendeu detecção de colisão
- [ ] Experimentou diferentes parâmetros
- [ ] Analisou dados exportados (CSV)
- [ ] Considerou extensões/melhorias possíveis

---

## 🗂️ Estrutura de Arquivos do Projeto

```
projeto/
│
├── simulatorReabilty.html          ← Arquivo principal (abrir no navegador)
│
├── README.md                        ← Visão geral do projeto
├── INDEX.md                         ← Este arquivo (índice)
├── GUIA_RAPIDO.md                   ← Início rápido
├── ALGORITMO_A_STAR.md              ← Documentação técnica do A*
├── APLICACOES_CLINICAS.md           ← Protocolos de fisioterapia
├── INSTALACAO_TROUBLESHOOTING.md   ← Suporte técnico
│
└── exemplo_trajetoria.csv          ← Exemplo de dados exportados
```

**Tamanho total**: ~5 MB (incluindo documentação)

---

## 🎓 Casos de Uso por Público

### 👨‍⚕️ Fisioterapeutas
**Documentos recomendados**:
1. GUIA_RAPIDO.md
2. APLICACOES_CLINICAS.md
3. README.md (opcional)

**Foco**: Protocolos de tratamento, casos clínicos, parâmetros recomendados

---

### 🎓 Estudantes de Fisioterapia
**Documentos recomendados**:
1. README.md
2. GUIA_RAPIDO.md
3. APLICACOES_CLINICAS.md
4. ALGORITMO_A_STAR.md (introdução)

**Foco**: Aprender sobre robótica em reabilitação, experimentar diferentes protocolos

---

### 💻 Programadores / Cientistas da Computação
**Documentos recomendados**:
1. README.md
2. ALGORITMO_A_STAR.md (completo)
3. INSTALACAO_TROUBLESHOOTING.md
4. Código-fonte (simulatorReabilty.html)

**Foco**: Implementação do A*, otimizações, extensões possíveis

---

### 🔬 Pesquisadores (Biomecânica, Robótica Médica)
**Documentos recomendados**:
1. Todos os arquivos
2. Especialmente: ALGORITMO_A_STAR.md e APLICACOES_CLINICAS.md

**Foco**: Validação de algoritmos, coleta de dados, desenvolvimento de novos protocolos

---

## 📖 Glossário de Termos

| Termo | Significado |
|-------|-------------|
| **A\*** | Algoritmo de busca de caminho que encontra trajetória ótima |
| **C-Space** | Espaço de configuração (todas as posições possíveis do robô) |
| **DOF** | Degrees of Freedom (graus de liberdade) - número de articulações |
| **Exoesqueleto** | Dispositivo robótico vestível que auxilia movimentos |
| **Heurística** | Função que estima custo restante (guia a busca do A*) |
| **Catmull-Rom** | Tipo de spline para suavizar trajetórias |
| **WebGL** | API JavaScript para gráficos 3D no navegador |
| **Three.js** | Biblioteca JavaScript para criar cenas 3D |
| **ROM** | Range of Motion (amplitude de movimento) |
| **θ (theta)** | Letra grega usada para representar ângulos |

---

## 📞 Referência Rápida

### Atalhos Úteis:

| Ação | Atalho |
|------|--------|
| Abrir console do navegador | F12 |
| Recarregar página | Ctrl+R (Cmd+R no Mac) |
| Recarregar ignorando cache | Ctrl+Shift+R |
| Tela cheia | F11 |
| Zoom in/out | Ctrl + / Ctrl - |

### Links Importantes:

- Three.js Documentation: https://threejs.org/docs/
- WebGL Test: https://get.webgl.org/
- Algoritmo A* (Wikipedia): https://en.wikipedia.org/wiki/A*_search_algorithm

---

## 🔄 Atualizações e Versão

**Versão Atual**: 1.0.0 (Novembro 2025)

### Histórico de Versões:

- **v1.0.0** (Nov 2025): Release inicial
  - Implementação do algoritmo A*
  - Suporte para braço e perna
  - Suavização com Catmull-Rom
  - Detecção de colisão
  - Exportação de dados CSV
  - Documentação completa

---

## 🎯 Próximos Passos

Após dominar esta documentação, você pode:

1. **Experimentar**: Testar diferentes configurações e protocolos
2. **Documentar**: Registrar resultados de suas simulações
3. **Contribuir**: Sugerir melhorias ou novos recursos
4. **Ensinar**: Compartilhar conhecimento com colegas
5. **Pesquisar**: Usar o simulador em estudos científicos

---

## 💡 Dicas de Navegação

- **Use Ctrl+F** (Cmd+F no Mac) para buscar termos específicos nos documentos
- **Abra múltiplos arquivos** em abas diferentes para referência cruzada
- **Imprima o GUIA_RAPIDO.md** para ter sempre à mão
- **Bookmark** este INDEX.md para acesso rápido

---

## 🙏 Agradecimentos

Este projeto foi desenvolvido como parte do estudo de **Inteligência Computacional** sobre **Robótica na Fisioterapia**.

Agradecimentos especiais a:
- Comunidade Three.js
- Pesquisadores em robótica de reabilitação
- Profissionais de fisioterapia que inspiraram este trabalho

---

## 📄 Licença

Este projeto é de código aberto e desenvolvido para fins educacionais e de pesquisa.

---

**ExoRehab 3D** - Documentação Completa 📚🤖💪

_Última atualização: Novembro 2025_
_Desenvolvido com dedicação para auxiliar na reabilitação e educação_

---

## 🚀 Comece Agora!

**👉 [Abra o GUIA_RAPIDO.md](GUIA_RAPIDO.md) para começar!**

ou

**👉 Abra `simulatorReabilty.html` diretamente no navegador e experimente!**

