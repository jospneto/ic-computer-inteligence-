# 🔧 Instalação e Troubleshooting - ExoRehab 3D

## 📥 Instalação

### Requisitos Mínimos

#### Hardware:
- **Processador**: Dual-core 2.0 GHz ou superior
- **RAM**: 4 GB mínimo (8 GB recomendado)
- **GPU**: Suporte a WebGL 2.0
- **Armazenamento**: 5 MB livres

#### Software:
- **Sistema Operacional**: 
  - Windows 10/11
  - macOS 10.14+
  - Linux (Ubuntu 20.04+)

- **Navegador** (um dos seguintes):
  - Google Chrome 90+ ✅ **Recomendado**
  - Mozilla Firefox 88+
  - Microsoft Edge 90+
  - Safari 14+ (macOS)

### Verificar Suporte a WebGL

1. Acesse: https://get.webgl.org/
2. Se ver um cubo rotativo, seu navegador suporta WebGL ✅
3. Se não funcionar, atualize seu navegador ou drivers de GPU

---

## 🚀 Instalação Passo a Passo

### Método 1: Download Direto (Mais Simples)

1. **Baixe os arquivos do projeto**
   ```
   projeto/
   ├── simulatorReabilty.html
   ├── README.md
   ├── GUIA_RAPIDO.md
   ├── ALGORITMO_A_STAR.md
   ├── APLICACOES_CLINICAS.md
   └── exemplo_trajetoria.csv
   ```

2. **Localize o arquivo principal**
   - Encontre `simulatorReabilty.html`

3. **Abra no navegador**
   - **Opção A**: Clique duplo no arquivo
   - **Opção B**: Arraste para o navegador aberto
   - **Opção C**: Clique direito → "Abrir com" → Navegador

4. **Pronto!** O simulador deve carregar automaticamente

---

### Método 2: Servidor Local (Recomendado para Desenvolvimento)

Se você planeja modificar o código:

#### Usando Python (Multiplataforma):

**Python 3.x:**
```bash
# Navegue até a pasta do projeto
cd caminho/para/projeto

# Inicie servidor HTTP
python -m http.server 8000

# Acesse no navegador:
# http://localhost:8000/simulatorReabilty.html
```

**Python 2.x:**
```bash
python -m SimpleHTTPServer 8000
```

#### Usando Node.js:

```bash
# Instale http-server globalmente
npm install -g http-server

# Navegue até a pasta
cd caminho/para/projeto

# Inicie servidor
http-server -p 8000

# Acesse: http://localhost:8000/simulatorReabilty.html
```

#### Usando PHP:

```bash
cd caminho/para/projeto
php -S localhost:8000

# Acesse: http://localhost:8000/simulatorReabilty.html
```

---

## ⚠️ Troubleshooting

### Problema 1: Tela Preta / Nada Aparece

**Sintomas:**
- Navegador abre, mas só mostra fundo preto
- Nenhum elemento 3D visível

**Soluções:**

#### Solução A: Verificar Console
1. Pressione `F12` (Chrome/Firefox/Edge)
2. Vá para aba "Console"
3. Procure por erros em vermelho

**Erros Comuns:**
```
Failed to load resource: net::ERR_INTERNET_DISCONNECTED
```
→ **Problema**: Sem internet (Three.js não carrega)
→ **Solução**: Conecte-se à internet ou use versão offline (veja abaixo)

```
Uncaught ReferenceError: THREE is not defined
```
→ **Problema**: Three.js não carregou
→ **Solução**: Recarregue a página (Ctrl+R ou Cmd+R)

#### Solução B: Verificar WebGL

1. Acesse: chrome://gpu (Chrome) ou about:support (Firefox)
2. Procure por "WebGL"
3. Deve estar **habilitado**

**Se WebGL estiver desabilitado:**
- Chrome: chrome://flags → Busque "WebGL" → Habilite
- Firefox: about:config → webgl.disabled → false

#### Solução C: Atualizar Drivers de GPU

**Windows:**
- NVIDIA: https://www.nvidia.com/drivers
- AMD: https://www.amd.com/support
- Intel: https://downloadcenter.intel.com

**macOS:**
- Atualize o sistema (System Update)

**Linux:**
```bash
# NVIDIA
sudo apt install nvidia-driver-xxx

# AMD
sudo apt install mesa-vulkan-drivers
```

---

### Problema 2: "Nenhum Caminho Encontrado (A*)"

**Sintomas:**
- Clica em "Simular" com A* selecionado
- Aparece alerta: "Nenhum caminho encontrado"

**Causas Possíveis:**

#### Causa 1: Obstáculo Bloqueando
O obstáculo está no meio do caminho planejado.

**Solução:**
```
1. Desmarque "Mostrar obstáculo"
2. OU ajuste os ângulos para evitar a região do obstáculo
3. OU use "Interpolação Linear"
```

#### Causa 2: Configuração Impossível
Os ângulos inicial e final são muito distantes com muitos obstáculos.

**Solução:**
```
1. Reduza a diferença entre ângulos inicial e final
2. Teste incrementalmente:
   - θ1: 20° → 50° (funciona?)
   - θ1: 20° → 80° (funciona?)
   - θ1: 20° → 100° (funciona?)
```

#### Causa 3: Limites Articulares
Tentando alcançar ângulos fora dos limites.

**Solução:**
```
Verifique:
- θ1: deve estar entre 0° e 180°
- θ2: deve estar entre -145° e 0°
```

---

### Problema 3: Simulação Muito Lenta / Travando

**Sintomas:**
- Movimento está engasgado
- FPS muito baixo
- Navegador congelando

**Soluções:**

#### Solução A: Reduzir Qualidade Visual

Edite `simulatorReabilty.html`, linha ~132:

```javascript
// ANTES:
renderer = new THREE.WebGLRenderer({antialias:true});

// DEPOIS:
renderer = new THREE.WebGLRenderer({antialias:false});
```

#### Solução B: Desabilitar Sombras

Linha ~134:

```javascript
// ANTES:
renderer.shadowMap.enabled = true;

// DEPOIS:
renderer.shadowMap.enabled = false;
```

#### Solução C: Reduzir Geometria

Linha ~188 (link1):

```javascript
// ANTES:
const geo1 = new THREE.CylinderGeometry(radius1, radius1, LINK1, 24);

// DEPOIS (menos polígonos):
const geo1 = new THREE.CylinderGeometry(radius1, radius1, LINK1, 12);
```

#### Solução D: Fechar Outras Abas
- Chrome/Edge/Firefox consomem muita RAM
- Feche abas desnecessárias

---

### Problema 4: Controles de Câmera Não Funcionam

**Sintomas:**
- Não consegue rotacionar a visualização 3D
- Mouse não responde

**Soluções:**

#### Solução A: Verificar se Está Arrastando na Área Correta
- ❌ Não arraste sobre os painéis de controle (esquerda/direita)
- ✅ Arraste na área 3D (fundo azul escuro, no centro)

#### Solução B: Verificar OrbitControls

Pressione F12 → Console:

```javascript
// Cole este comando:
controls
```

Se retornar `undefined`, OrbitControls não carregou.

**Solução**: Recarregue a página (Ctrl+R)

#### Solução C: Conflito de Extensões

Desabilite temporariamente extensões do navegador:
- Ad blockers
- Dark mode
- Gestores de mouse

---

### Problema 5: Exportação CSV Não Funciona

**Sintomas:**
- Clica em "Exportar CSV"
- Nada acontece ou erro

**Soluções:**

#### Solução A: Executar Simulação Primeiro
```
1. Configure ângulos
2. Clique em "Simular Movimento"
3. Aguarde completar
4. Agora clique em "Exportar CSV"
```

#### Solução B: Verificar Permissões de Download

**Chrome/Edge:**
- Settings → Privacy → Site Settings → Downloads
- Permitir downloads automáticos

**Firefox:**
- Options → General → Files and Applications
- Verificar ação padrão para CSV

#### Solução C: Popup Blocker

Se o download não inicia:
- Verifique se navegador bloqueou popup
- Procure ícone de "bloqueado" na barra de endereço
- Permita popups para este site

---

### Problema 6: Labels em Inglês / Texto Errado

**Sintomas:**
- Interface mostra texto em inglês
- Labels incorretas

**Solução:**

Verifique a tag `<html lang="...">` na linha 2:

```html
<!-- Deve estar: -->
<html lang="pt-BR">
```

Se ainda persistir, verifique configurações do navegador:
- Chrome: Settings → Languages → Português (Brasil)

---

### Problema 7: Versão Offline (Sem Internet)

**Problema:**
- Three.js é carregado de CDN (requer internet)
- Sem internet = não funciona

**Solução: Criar Versão Offline**

1. **Baixar Three.js:**
   - https://cdnjs.cloudflare.com/ajax/libs/three.js/r154/three.min.js
   - https://cdnjs.cloudflare.com/ajax/libs/three.js/r154/examples/js/controls/OrbitControls.min.js

2. **Salvar na mesma pasta do projeto:**
   ```
   projeto/
   ├── simulatorReabilty.html
   ├── three.min.js
   └── OrbitControls.min.js
   ```

3. **Editar simulatorReabilty.html (linhas 100-101):**

   ```html
   <!-- ANTES (online): -->
   <script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r154/three.min.js"></script>
   <script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r154/examples/js/controls/OrbitControls.min.js"></script>

   <!-- DEPOIS (offline): -->
   <script src="three.min.js"></script>
   <script src="OrbitControls.min.js"></script>
   ```

4. **Pronto!** Agora funciona sem internet ✅

---

## 🐛 Reportar Bugs

Se encontrou um problema não listado aqui:

### Informações a Coletar:

1. **Sistema:**
   - SO: Windows 10 / macOS 12 / Ubuntu 22.04
   - Navegador: Chrome 120 / Firefox 119 / etc.

2. **Console de Erros:**
   - Pressione F12
   - Copie mensagens em vermelho
   - Faça screenshot se necessário

3. **Passos para Reproduzir:**
   ```
   1. Abri o simulador
   2. Selecionei "Perna"
   3. Cliquei em "Simular"
   4. Erro apareceu
   ```

4. **Configuração Usada:**
   ```
   Tipo: Braço
   θ1 inicial: 20°
   θ2 inicial: -20°
   θ1 final: 100°
   θ2 final: -30°
   Algoritmo: A*
   ```

---

## 🔍 Diagnóstico Avançado

### Verificar Desempenho:

Pressione F12 → Console, cole:

```javascript
// FPS atual
let lastTime = performance.now();
function checkFPS() {
    const now = performance.now();
    const fps = 1000 / (now - lastTime);
    console.log('FPS:', fps.toFixed(1));
    lastTime = now;
    requestAnimationFrame(checkFPS);
}
checkFPS();
```

**Interpretação:**
- FPS > 50: ✅ Excelente
- FPS 30-50: ⚠️ Aceitável
- FPS < 30: 🚨 Problema de desempenho

---

### Verificar Memória:

Chrome: Shift+Esc (Task Manager do Chrome)

Procure por:
```
Tab: simulatorReabilty.html
Memory: XXX MB
```

**Interpretação:**
- < 100 MB: ✅ Normal
- 100-200 MB: ⚠️ OK
- > 200 MB: 🚨 Possível memory leak

**Solução**: Recarregue a página

---

### Testar WebGL Capabilities:

Console, cole:

```javascript
const canvas = renderer.domElement;
const gl = canvas.getContext('webgl2') || canvas.getContext('webgl');
console.log('WebGL Version:', gl ? (canvas.getContext('webgl2') ? '2.0' : '1.0') : 'NOT SUPPORTED');
console.log('Max Texture Size:', gl.getParameter(gl.MAX_TEXTURE_SIZE));
console.log('Max Vertex Attributes:', gl.getParameter(gl.MAX_VERTEX_ATTRIBS));
```

---

## 💾 Backup e Personalização

### Fazer Backup do Simulador:

```bash
# Windows (PowerShell)
Copy-Item -Path "projeto" -Destination "projeto_backup_$(Get-Date -Format 'yyyy-MM-dd')" -Recurse

# macOS / Linux
cp -r projeto projeto_backup_$(date +%Y-%m-%d)
```

### Personalizações Comuns:

#### Mudar Cores do Exoesqueleto:

Linha ~159 (braço) e ~163 (perna):

```javascript
// Braço (padrão: roxo #6366f1)
color: type === 'arm' ? 0x6366f1 : 0x10b981

// Exemplos:
0xff0000  // Vermelho
0x00ff00  // Verde
0x0000ff  // Azul
0xffaa00  // Laranja
```

#### Ajustar Tamanho do Exoesqueleto:

Linhas ~106-107:

```javascript
// Braço
LINK1 = 0.35;  // 35cm → ajuste aqui
LINK2 = 0.25;  // 25cm

// Perna (linha ~171-172)
LINK1 = 0.45;  // 45cm
LINK2 = 0.40;  // 40cm
```

#### Mudar Velocidade Padrão:

Linha ~70 (HTML):

```html
<input id="speed" type="range" min="10" max="200" step="5" value="35">
                                                              <!-- ^ mude aqui -->
```

---

## 📱 Suporte Mobile

**Aviso**: Este simulador foi otimizado para desktop.

### Funcionamento em Mobile:

| Recurso | Android | iOS |
|---------|---------|-----|
| Visualização 3D | ✅ | ✅ |
| Controles Touch | ⚠️ | ⚠️ |
| Exportar CSV | ❌ | ❌ |
| Desempenho | ⚠️ | ✅ |

### Dicas para Mobile:

1. **Use modo paisagem** (horizontal)
2. **Touch gestures:**
   - 1 dedo: Rotacionar
   - 2 dedos (pinch): Zoom
   - 2 dedos (pan): Mover
3. **Feche outros apps** (liberar RAM)

---

## 🔐 Segurança e Privacidade

### O Simulador É Seguro?

✅ **SIM!** Este é um simulador 100% local:

- ✅ Não envia dados para servidores
- ✅ Não requer login/cadastro
- ✅ Não usa cookies de rastreamento
- ✅ Código aberto (pode auditar)
- ✅ Funciona offline (após carregar)

### Dados Exportados:

- 📁 CSVs são salvos **localmente** no seu computador
- 🔒 Nenhum dado é enviado para nuvem
- 🗑️ Você controla quando deletar

---

## 🆘 Suporte Adicional

### Recursos de Aprendizado:

1. **Three.js Fundamentals**: https://threejs.org/manual/
2. **Algoritmo A***: https://en.wikipedia.org/wiki/A*_search_algorithm
3. **WebGL**: https://webglfundamentals.org/

### Comunidades:

- Stack Overflow (tag: three.js, webgl)
- Three.js Discourse: https://discourse.threejs.org/
- Reddit: r/threejs

---

## ✅ Checklist de Verificação

Antes de reportar um problema, verifique:

- [ ] Navegador atualizado (versão mais recente)
- [ ] WebGL habilitado e funcionando
- [ ] Internet conectada (primeira vez)
- [ ] Console sem erros (F12)
- [ ] Simulação executada antes de exportar
- [ ] Ângulos dentro dos limites válidos
- [ ] Outras abas fechadas (para desempenho)

---

**ExoRehab 3D** - Suporte Técnico 🔧🤖

_Se este guia resolveu seu problema, ótimo! Se não, documente os detalhes e procure suporte adicional._

