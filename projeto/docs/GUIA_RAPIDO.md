# 🚀 Guia Rápido - ExoRehab 3D

## Início Rápido (3 passos)

### 1️⃣ Abrir o Simulador
Abra o arquivo `simulatorReabilty.html` no seu navegador (Chrome, Firefox ou Edge recomendados).

### 2️⃣ Configurar a Simulação
- **Escolha o tipo**: Braço ou Perna
- **Defina os ângulos**: Posição inicial e final
- **Selecione o algoritmo**: A* (recomendado) ou Interpolação Linear

### 3️⃣ Executar
Clique em **"▶ Simular Movimento"** e observe a trajetória!

---

## 🎮 Controles da Visualização 3D

| Ação | Como Fazer |
|------|------------|
| **Rotacionar** | Clique e arraste com botão esquerdo |
| **Zoom** | Role o scroll do mouse |
| **Mover (Pan)** | Clique e arraste com botão direito |
| **Reset Câmera** | Clique no botão "🔄 Reset" |

---

## 🎯 Casos de Uso Comuns

### Reabilitação de Braço (Pós-AVC)

**Configuração Sugerida:**
```
Tipo: Braço
θ1 inicial: 20° (braço relaxado)
θ2 inicial: -30° (cotovelo flexionado)
θ1 final: 90° (braço elevado)
θ2 final: -10° (cotovelo quase estendido)
Algoritmo: A* (Otimizado)
Velocidade: 50ms
```

**Objetivo**: Treinar elevação do braço com extensão gradual do cotovelo

---

### Reabilitação de Marcha

**Configuração Sugerida:**
```
Tipo: Perna
θ1 inicial: 0° (perna em pé)
θ2 inicial: 0° (joelho reto)
θ1 final: 45° (elevação da coxa)
θ2 final: -90° (flexão do joelho)
Algoritmo: A* (Otimizado)
Velocidade: 40ms
```

**Objetivo**: Simular fase de balanço da marcha

---

### Exercício de Amplitude de Movimento

**Configuração Sugerida:**
```
Tipo: Braço
θ1 inicial: 10°
θ2 inicial: -5°
θ1 final: 160°
θ2 final: -140°
Algoritmo: Interpolação Linear
Velocidade: 30ms (movimento suave)
```

**Objetivo**: Alcançar máxima amplitude articular possível

---

## ⚙️ Entendendo os Ângulos

### Para Braço:
- **θ1 (Ombro)**: 
  - 0° = Braço apontando para frente
  - 90° = Braço elevado lateralmente
  - 180° = Braço apontando para trás

- **θ2 (Cotovelo)**: 
  - 0° = Cotovelo totalmente estendido
  - -90° = Cotovelo em ângulo reto
  - -145° = Cotovelo totalmente flexionado

### Para Perna:
- **θ1 (Quadril)**: 
  - 0° = Perna em pé (vertical)
  - 45° = Coxa elevada (fase de balanço)
  - 90° = Coxa horizontal

- **θ2 (Joelho)**: 
  - 0° = Joelho totalmente estendido
  - -60° = Flexão moderada
  - -145° = Joelho totalmente flexionado

---

## 🔬 Diferença entre os Algoritmos

### A* (Otimizado) ⭐
**Quando usar:**
- Quando há obstáculos visíveis
- Para trajetórias mais naturais e seguras
- Quando precisa de planejamento inteligente

**Características:**
- ✅ Desvia automaticamente de obstáculos
- ✅ Encontra o caminho mais eficiente
- ✅ Suavização com splines Catmull-Rom
- ⚠️ Pode levar alguns segundos para calcular

### Interpolação Linear
**Quando usar:**
- Quando não há obstáculos
- Para movimentos simples e diretos
- Quando precisa de execução rápida

**Características:**
- ✅ Muito rápido
- ✅ Movimento direto entre pontos
- ⚠️ Não desvia de obstáculos
- ⚠️ Pode não ser biomechanicamente natural

---

## 📊 Exportando Dados

1. Execute uma simulação completa
2. Clique em **"⤓ Exportar Trajetória (CSV)"**
3. O arquivo será salvo automaticamente com formato:
   - `exorehab_braco_YYYY-MM-DD-HH-MM-SS.csv`
   - `exorehab_perna_YYYY-MM-DD-HH-MM-SS.csv`

### Conteúdo do CSV:
- **Metadados**: Tipo, data, total de frames, algoritmo usado
- **Dados**: Frame, ângulos em graus e radianos

### Uso dos Dados Exportados:
- Análise em Excel/Sheets
- Importação em MATLAB/Python
- Documentação de sessões terapêuticas
- Pesquisa e desenvolvimento

---

## 🔧 Solução de Problemas

### "Nenhum caminho encontrado (A*)"
**Soluções:**
1. Desmarque "Mostrar obstáculo" (remove obstáculos)
2. Ajuste os ângulos inicial/final
3. Use "Interpolação Linear" como alternativa

### A simulação está muito rápida/lenta
**Solução:**
Ajuste o slider "Velocidade da Simulação":
- Valores baixos (10-30ms) = Rápido
- Valores médios (40-60ms) = Normal
- Valores altos (70-200ms) = Lento e detalhado

### O exoesqueleto desaparece ou fica estranho
**Solução:**
Clique em **"🔄 Reset"** para restaurar a visualização

### Não consigo mover a câmera
**Solução:**
Verifique se não está arrastando sobre os painéis de controle. Arraste na área 3D (fundo azul escuro).

---

## 💡 Dicas Profissionais

1. **Use o Obstáculo**: Simule limitações do ambiente (mesa, parede, etc.)
2. **Teste Diferentes Velocidades**: Encontre o timing ideal para cada tipo de exercício
3. **Combine Movimentos**: Execute várias simulações com diferentes configurações
4. **Documente Tudo**: Exporte os CSVs para acompanhar a evolução do planejamento
5. **Visualize em 3D**: Use os controles da câmera para ver de diferentes ângulos

---

## 📚 Para Saber Mais

Consulte o arquivo `README.md` para:
- Detalhes técnicos do algoritmo A*
- Arquitetura do sistema
- Referências acadêmicas
- Roadmap de desenvolvimento futuro

---

## 🆘 Suporte

Para dúvidas, bugs ou sugestões:
- Verifique o `README.md` completo
- Analise o código em `simulatorReabilty.html`
- Teste com o arquivo de exemplo `exemplo_trajetoria.csv`

---

**ExoRehab 3D** - Simulação de exoesqueletos para fisioterapia 🤖💪

_Desenvolvido com ❤️ para auxiliar na reabilitação e pesquisa em robótica médica_

