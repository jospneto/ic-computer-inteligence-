import math
import heapq
import numpy as np
import matplotlib
matplotlib.use("TkAgg")
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from tkinter import *
from tkinter import ttk, messagebox
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.patches import Circle, Rectangle
import time

# ---------------------------------------------------------- 
# LIMITES FISIOLÓGICOS HUMANOS (baseado em estudos biomecânicos)
# ----------------------------------------------------------
PHYSIOLOGICAL_LIMITS = {
    'shoulder_flexion': (0, 180),      # Flexão do ombro
    'shoulder_extension': (-60, 0),     # Extensão do ombro
    'elbow_flexion': (0, 145),          # Flexão do cotovelo
    'knee_flexion': (0, 135),           # Flexão do joelho
    'hip_flexion': (-15, 125),          # Flexão do quadril
    'ankle_dorsiflexion': (-20, 30)     # Dorsiflexão do tornozelo
}

# Zonas de conforto (ângulos onde não há desconforto)
COMFORT_ZONES = {
    'shoulder': (10, 120),
    'elbow': (30, 130),
    'knee': (0, 120),
    'hip': (0, 100)
}

# ---------------------------------------------------------- 
# EXOSKELETON A* CLASS COM MELHORIAS
# ---------------------------------------------------------- 
class ExoAStar:
    def __init__(self, limb_type='arm', l1=0.35, l2=0.25):
        """
        limb_type: 'arm' (braço) ou 'leg' (perna)
        l1: comprimento do segmento proximal (parte superior do braço ou coxa)
        l2: comprimento do segmento distal (antebraço ou canela)
        """
        self.limb_type = limb_type
        self.l1 = l1
        self.l2 = l2
        
        # Definir limites baseados no tipo de membro
        if limb_type == 'arm':
            self.t1_range = PHYSIOLOGICAL_LIMITS['shoulder_flexion']
            self.t2_range = (-145, 0)  # Cotovelo (negativo para extensão)
            self.comfort_t1 = COMFORT_ZONES['shoulder']
            self.comfort_t2 = (-130, -30)
        else:  # leg
            self.t1_range = PHYSIOLOGICAL_LIMITS['hip_flexion']
            self.t2_range = (-135, 0)  # Joelho
            self.comfort_t1 = COMFORT_ZONES['hip']
            self.comfort_t2 = (-120, 0)
        
        # Discretização mais fina para movimentos suaves
        self.theta1_vals = np.linspace(self.t1_range[0], self.t1_range[1], 80)
        self.theta2_vals = np.linspace(self.t2_range[0], self.t2_range[1], 80)
        
        # Obstáculos (podem representar áreas de dor ou limitações)
        self.obstacles = []
        
        # Mapa de custo para áreas de desconforto/dor
        self.pain_map = {}
    
    def add_obstacle(self, center, radius):
        """Adiciona um obstáculo circular (área de dor/limitação)"""
        self.obstacles.append({'center': center, 'radius': radius})
    
    def add_pain_zone(self, t1_range, t2_range, cost_multiplier=5.0):
        """Adiciona uma zona de dor com custo aumentado"""
        for t1 in np.linspace(t1_range[0], t1_range[1], 10):
            for t2 in np.linspace(t2_range[0], t2_range[1], 10):
                i, j = self.angles_to_idx(np.deg2rad(t1), np.deg2rad(t2))
                self.pain_map[(i, j)] = cost_multiplier
    
    def idx_to_angles(self, i, j):
        """Converte índices para ângulos em radianos"""
        return np.deg2rad(self.theta1_vals[i]), np.deg2rad(self.theta2_vals[j])
    
    def angles_to_idx(self, t1, t2):
        """Converte ângulos em radianos para índices"""
        i = int(np.argmin(np.abs(np.rad2deg(t1) - self.theta1_vals)))
        j = int(np.argmin(np.abs(np.rad2deg(t2) - self.theta2_vals)))
        return i, j
    
    def fk(self, t1, t2):
        """
        Cinemática direta: calcula posição do end-effector e da junta intermediária
        Retorna: (posição_final, posição_junta_intermediária)
        """
        x1 = self.l1 * math.cos(t1)
        y1 = self.l1 * math.sin(t1)
        x2 = x1 + self.l2 * math.cos(t1 + t2)
        y2 = y1 + self.l2 * math.sin(t1 + t2)
        return (x2, y2), (x1, y1)
    
    def in_collision(self, t1, t2):
        """Verifica colisão com obstáculos"""
        (x, y), (x1, y1) = self.fk(t1, t2)
        
        for obs in self.obstacles:
            # Verifica colisão do end-effector
            if math.dist((x, y), obs['center']) <= obs['radius']:
                return True
            # Verifica colisão da junta intermediária
            if math.dist((x1, y1), obs['center']) <= obs['radius']:
                return True
        return False
    
    def is_in_comfort_zone(self, t1, t2):
        """Verifica se a configuração está na zona de conforto"""
        t1_deg = np.rad2deg(t1)
        t2_deg = np.rad2deg(t2)
        return (self.comfort_t1[0] <= t1_deg <= self.comfort_t1[1] and 
                self.comfort_t2[0] <= t2_deg <= self.comfort_t2[1])
    
    def heuristic(self, i, j, gi, gj):
        """Heurística: distância angular até o objetivo"""
        t1a, t2a = self.idx_to_angles(i, j)
        t1b, t2b = self.idx_to_angles(gi, gj)
        return abs(t1a - t1b) + abs(t2a - t2b)
    
    def cost_between(self, i1, j1, i2, j2):
        """
        Calcula custo de movimento entre duas configurações
        Considera: mudança angular, zonas de desconforto e mapa de dor
        """
        t1a, t2a = self.idx_to_angles(i1, j1)
        t1b, t2b = self.idx_to_angles(i2, j2)
        
        # Custo base (mudança angular)
        base_cost = abs(t1a - t1b) + abs(t2a - t2b)
        
        # Penalidade se sair da zona de conforto
        if not self.is_in_comfort_zone(t1b, t2b):
            base_cost *= 1.5
        
        # Adiciona custo de dor se existir
        pain_cost = self.pain_map.get((i2, j2), 0)
        
        return base_cost + pain_cost
    
    def neighbors(self, i, j):
        """Gera vizinhos válidos"""
        for di in (-1, 0, 1):
            for dj in (-1, 0, 1):
                if di == 0 and dj == 0:
                    continue
                ni = i + di
                nj = j + dj
                if 0 <= ni < len(self.theta1_vals) and 0 <= nj < len(self.theta2_vals):
                    yield ni, nj
    
    def astar(self, s_idx, g_idx):
        """Algoritmo A* para planejamento de trajetória"""
        si, sj = s_idx
        gi, gj = g_idx
        
        open_heap = [(0.0, si, sj)]
        gscore = {(si, sj): 0.0}
        came = {}
        visited = set()
        
        iterations = 0
        max_iterations = 10000
        
        while open_heap and iterations < max_iterations:
            iterations += 1
            f, i, j = heapq.heappop(open_heap)
            
            if (i, j) == (gi, gj):
                path = [(i, j)]
                while path[-1] in came:
                    path.append(came[path[-1]])
                path.reverse()
                return path
            
            if (i, j) in visited:
                continue
            
            visited.add((i, j))
            
            for ni, nj in self.neighbors(i, j):
                if (ni, nj) in visited:
                    continue
                
                t1, t2 = self.idx_to_angles(ni, nj)
                if self.in_collision(t1, t2):
                    continue
                
                new_g = gscore[(i, j)] + self.cost_between(i, j, ni, nj)
                
                if new_g < gscore.get((ni, nj), float("inf")):
                    gscore[(ni, nj)] = new_g
                    came[(ni, nj)] = (i, j)
                    heapq.heappush(open_heap, 
                                 (new_g + self.heuristic(ni, nj, gi, gj), ni, nj))
        
        return None
    
    def validate_angles(self, t1_deg, t2_deg):
        """Valida se os ângulos estão dentro dos limites fisiológicos"""
        if not (self.t1_range[0] <= t1_deg <= self.t1_range[1]):
            return False, f"Ângulo θ1 fora dos limites fisiológicos: {self.t1_range}"
        if not (self.t2_range[0] <= t2_deg <= self.t2_range[1]):
            return False, f"Ângulo θ2 fora dos limites fisiológicos: {self.t2_range}"
        return True, "OK"
    
    def draw_limb(self, ax, t1, t2, color='blue', alpha=1.0, linewidth=2):
        """Desenha o membro (braço ou perna) em uma configuração específica"""
        (x2, y2), (x1, y1) = self.fk(t1, t2)
        
        # Base (ombro ou quadril)
        ax.plot(0, 0, 'ko', markersize=10)
        
        # Segmento proximal
        ax.plot([0, x1], [0, y1], color=color, linewidth=linewidth, alpha=alpha)
        ax.plot(x1, y1, 'o', color=color, markersize=8, alpha=alpha)
        
        # Segmento distal
        ax.plot([x1, x2], [y1, y2], color=color, linewidth=linewidth, alpha=alpha)
        ax.plot(x2, y2, 'o', color=color, markersize=8, alpha=alpha)
        
        return (x2, y2)

# ---------------------------------------------------------- 
# TKINTER GUI COM ANIMAÇÃO
# ---------------------------------------------------------- 
def run_gui():
    root = Tk()
    root.title("Simulador de Exoesqueleto para Reabilitação - A* com Animação")
    root.geometry("900x700")
    
    # Frame de controles
    control_frame = Frame(root, padx=10, pady=10)
    control_frame.pack(side=TOP, fill=X)
    
    # Tipo de membro
    Label(control_frame, text="Tipo de Membro:", font=('Arial', 10, 'bold')).grid(row=0, column=0, sticky=W)
    limb_var = StringVar(value='arm')
    Radiobutton(control_frame, text="Braço", variable=limb_var, value='arm').grid(row=0, column=1)
    Radiobutton(control_frame, text="Perna", variable=limb_var, value='leg').grid(row=0, column=2)
    
    # Ângulos iniciais
    Label(control_frame, text="Ângulos Iniciais (graus):", font=('Arial', 10, 'bold')).grid(row=1, column=0, sticky=W, pady=5)
    Label(control_frame, text="θ1 (proximal):").grid(row=2, column=0, sticky=W)
    e_t1i = Entry(control_frame, width=10)
    e_t1i.insert(0, "20")
    e_t1i.grid(row=2, column=1)
    
    Label(control_frame, text="θ2 (distal):").grid(row=3, column=0, sticky=W)
    e_t2i = Entry(control_frame, width=10)
    e_t2i.insert(0, "-20")
    e_t2i.grid(row=3, column=1)
    
    # Ângulos finais
    Label(control_frame, text="Ângulos Finais (graus):", font=('Arial', 10, 'bold')).grid(row=4, column=0, sticky=W, pady=5)
    Label(control_frame, text="θ1 (proximal):").grid(row=5, column=0, sticky=W)
    e_t1f = Entry(control_frame, width=10)
    e_t1f.insert(0, "100")
    e_t1f.grid(row=5, column=1)
    
    Label(control_frame, text="θ2 (distal):").grid(row=6, column=0, sticky=W)
    e_t2f = Entry(control_frame, width=10)
    e_t2f.insert(0, "-80")
    e_t2f.grid(row=6, column=1)
    
    # Opções adicionais
    Label(control_frame, text="Opções:", font=('Arial', 10, 'bold')).grid(row=1, column=3, sticky=W, padx=20)
    add_obstacle_var = BooleanVar(value=True)
    Checkbutton(control_frame, text="Adicionar obstáculo (área de dor)", 
                variable=add_obstacle_var).grid(row=2, column=3, sticky=W, padx=20)
    
    add_pain_var = BooleanVar(value=False)
    Checkbutton(control_frame, text="Adicionar zona de desconforto", 
                variable=add_pain_var).grid(row=3, column=3, sticky=W, padx=20)
    
    Label(control_frame, text="Velocidade da animação:").grid(row=4, column=3, sticky=W, padx=20)
    speed_var = DoubleVar(value=50)
    speed_scale = Scale(control_frame, from_=10, to=200, orient=HORIZONTAL, 
                       variable=speed_var, length=150)
    speed_scale.grid(row=5, column=3, padx=20)
    
    # Status
    status_var = StringVar(value="Pronto para simular")
    status_label = Label(root, textvariable=status_var, relief=SUNKEN, anchor=W)
    status_label.pack(side=BOTTOM, fill=X)
    
    # Canvas matplotlib
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 5))
    canvas = FigureCanvasTkAgg(fig, master=root)
    canvas.get_tk_widget().pack(side=TOP, fill=BOTH, expand=True)
    
    # Variáveis globais para animação
    animation_data = {'anim': None, 'running': False}
    
    def animate_movement(sim, path, ax):
        """Cria animação suave do movimento"""
        angles = [sim.idx_to_angles(i, j) for (i, j) in path]
        
        def update(frame):
            ax.clear()
            
            # Desenha trajetória completa (transparente)
            for idx, (t1, t2) in enumerate(angles):
                alpha = 0.1 if idx != frame else 1.0
                color = 'lightblue' if idx != frame else 'blue'
                lw = 1 if idx != frame else 3
                sim.draw_limb(ax, t1, t2, color=color, alpha=alpha, linewidth=lw)
            
            # Desenha obstáculos
            for obs in sim.obstacles:
                circle = Circle(obs['center'], obs['radius'], 
                              fill=True, color='red', alpha=0.3)
                ax.add_patch(circle)
                ax.text(obs['center'][0], obs['center'][1], 
                       'Área de Dor', ha='center', fontsize=8)
            
            # Configuração do plot
            ax.set_aspect('equal')
            ax.set_xlim(-0.1, 0.7)
            ax.set_ylim(-0.3, 0.6)
            ax.grid(True, alpha=0.3)
            ax.set_xlabel('x (m)')
            ax.set_ylabel('y (m)')
            
            t1_deg = np.rad2deg(angles[frame][0])
            t2_deg = np.rad2deg(angles[frame][1])
            ax.set_title(f'Frame {frame+1}/{len(angles)}\n' + 
                        f'θ1={t1_deg:.1f}°, θ2={t2_deg:.1f}°')
            
            status_var.set(f"Animando... Frame {frame+1}/{len(angles)}")
        
        anim = FuncAnimation(fig, update, frames=len(angles), 
                           interval=speed_var.get(), repeat=True, blit=False)
        return anim
    
    def run_simulation():
        try:
            # Parar animação anterior se existir
            if animation_data['anim'] is not None:
                animation_data['anim'].event_source.stop()
            
            # Ler parâmetros
            limb_type = limb_var.get()
            t1i = float(e_t1i.get())
            t2i = float(e_t2i.get())
            t1f = float(e_t1f.get())
            t2f = float(e_t2f.get())
            
            # Criar simulador
            status_var.set("Inicializando simulador...")
            sim = ExoAStar(limb_type=limb_type, l1=0.35, l2=0.25)
            
            # Validar ângulos
            valid_start, msg_start = sim.validate_angles(t1i, t2i)
            valid_end, msg_end = sim.validate_angles(t1f, t2f)
            
            if not valid_start:
                messagebox.showerror("Erro", f"Ângulo inicial inválido: {msg_start}")
                return
            if not valid_end:
                messagebox.showerror("Erro", f"Ângulo final inválido: {msg_end}")
                return
            
            # Adicionar obstáculo se selecionado
            if add_obstacle_var.get():
                sim.add_obstacle((0.40, 0.15), 0.08)
            
            # Adicionar zona de dor se selecionado
            if add_pain_var.get():
                sim.add_pain_zone((50, 70), (-60, -40), cost_multiplier=10.0)
            
            # Planejar trajetória
            status_var.set("Planejando trajetória com A*...")
            root.update()
            
            t1s, t2s = np.radians(t1i), np.radians(t2i)
            t1g, t2g = np.radians(t1f), np.radians(t2f)
            s_idx = sim.angles_to_idx(t1s, t2s)
            g_idx = sim.angles_to_idx(t1g, t2g)
            
            path = sim.astar(s_idx, g_idx)
            
            if path is None:
                ax1.clear()
                ax2.clear()
                ax1.text(0.5, 0.5, "Nenhum caminho encontrado!\n" +
                        "Verifique obstáculos e limites.", 
                        ha='center', va='center', color='red', fontsize=12)
                canvas.draw()
                status_var.set("Erro: Nenhum caminho encontrado")
                messagebox.showwarning("Aviso", 
                    "Não foi possível encontrar um caminho seguro.\n" +
                    "Tente ajustar os ângulos ou remover obstáculos.")
                return
            
            # Plotar trajetória completa no ax2
            ax2.clear()
            angles = [sim.idx_to_angles(i, j) for (i, j) in path]
            ee_positions = [sim.fk(t1, t2)[0] for (t1, t2) in angles]
            xs = [p[0] for p in ee_positions]
            ys = [p[1] for p in ee_positions]
            
            ax2.plot(xs, ys, 'b-', linewidth=2, label='Trajetória')
            ax2.scatter(xs[0], ys[0], s=100, c='green', marker='o', 
                       label='Início', zorder=5)
            ax2.scatter(xs[-1], ys[-1], s=100, c='red', marker='s', 
                       label='Objetivo', zorder=5)
            
            # Desenhar obstáculos no ax2
            for obs in sim.obstacles:
                circle = Circle(obs['center'], obs['radius'], 
                              fill=True, color='red', alpha=0.3)
                ax2.add_patch(circle)
            
            ax2.set_aspect('equal')
            ax2.set_xlim(-0.1, 0.7)
            ax2.set_ylim(-0.3, 0.6)
            ax2.grid(True, alpha=0.3)
            ax2.set_xlabel('x (m)')
            ax2.set_ylabel('y (m)')
            ax2.set_title(f'Trajetória Planejada ({len(path)} passos)')
            ax2.legend()
            
            # Iniciar animação no ax1
            status_var.set("Iniciando animação...")
            animation_data['anim'] = animate_movement(sim, path, ax1)
            canvas.draw()
            
            status_var.set(f"Simulação concluída! {len(path)} passos planejados.")
            
        except ValueError as e:
            messagebox.showerror("Erro", f"Valores inválidos: {str(e)}")
            status_var.set("Erro nos valores de entrada")
        except Exception as e:
            messagebox.showerror("Erro", f"Erro inesperado: {str(e)}")
            status_var.set(f"Erro: {str(e)}")
    
    # Botões
    button_frame = Frame(root)
    button_frame.pack(side=TOP, pady=10)
    
    Button(button_frame, text="▶ Simular Movimento", command=run_simulation, 
           bg="#28a745", fg="white", font=('Arial', 11, 'bold'),
           padx=20, pady=5).pack(side=LEFT, padx=5)
    
    def stop_animation():
        if animation_data['anim'] is not None:
            animation_data['anim'].event_source.stop()
            status_var.set("Animação pausada")
    
    Button(button_frame, text="⏸ Pausar", command=stop_animation,
           bg="#ffc107", fg="black", font=('Arial', 11),
           padx=20, pady=5).pack(side=LEFT, padx=5)
    
    # Info
    info_text = f"""
    Limites Fisiológicos:
    Braço - Ombro: 0° a 180° | Cotovelo: -145° a 0°
    Perna - Quadril: -15° a 125° | Joelho: -135° a 0°
    """
    Label(root, text=info_text, justify=LEFT, font=('Courier', 8), 
          bg='#f0f0f0').pack(side=BOTTOM, fill=X)
    
    root.mainloop()

if __name__ == "__main__":
    run_gui()