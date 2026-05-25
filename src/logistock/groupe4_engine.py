import math
import random
from graphviz import Digraph

# =================================================================
# CLASSE WarehouseState : Logique de l'entrepôt
# =================================================================
class WarehouseState:
    def __init__(self, stack, inventory, mode="REMPLISSAGE", lambdas=None):
        self.stack = tuple(stack)
        self.inventory = inventory
        self.mode = mode
        self.lambdas = lambdas.copy() if lambdas is not None else {k: 1.0 for k in inventory}

    def get_legal_actions(self):
        if self.mode == "REMPLISSAGE":
            return sorted([k for k, v in self.inventory.items() if v > 0])
        else:
            return sorted(list(set([i for i in self.stack if i != 'X'])))

    def get_exit_probabilities(self):
        acts = sorted(list(set([i for i in self.stack if i != 'X'])))
        total = sum(self.lambdas.get(act, 0) for act in acts)
        if total <= 0:
            return {act: 0.0 for act in acts}
        return {act: self.lambdas.get(act, 0) / total for act in acts}

    def apply(self, action):
        new_stack = list(self.stack)
        new_inv = self.inventory.copy()
        if self.mode == "REMPLISSAGE":
            for i in range(len(new_stack)-1, -1, -1):
                if new_stack[i] == 'X':
                    new_stack[i] = action
                    break
            new_inv[action] -= 1
            next_mode = "SORTIE" if sum(new_inv.values()) == 0 else "REMPLISSAGE"
            return WarehouseState(new_stack, new_inv, next_mode, self.lambdas), 0
        else:
            idx = new_stack.index(action)
            above = sum(1 for i in new_stack[:idx] if i != 'X')
            cost = 2 * above + 1
            new_stack[idx] = 'X'
            current = [i for i in new_stack if i != 'X']
            new_stack = (['X'] * (len(self.stack) - len(current))) + current
            return WarehouseState(new_stack, new_inv, "SORTIE", self.lambdas), cost

# =================================================================
# CLASSE MCTSNode : Structure de l'arbre
# =================================================================
class MCTSNode:
    def __init__(self, state, parent=None, incoming_cost=0, action=""):
        self.state = state
        self.parent = parent
        self.action = action
        self.incoming_cost = incoming_cost
        self.children = {}
        self.visits = 0
        self.expected_cost = 0
        self.untried = state.get_legal_actions()

    def update_values(self):
        if not self.children: return
        if self.state.mode == "REMPLISSAGE":
            self.expected_cost = min(child.expected_cost for child in self.children.values())
        else:
            exit_probs = self.state.get_exit_probabilities()
            weights = [exit_probs.get(child.action, 0) for child in self.children.values()]
            total_weight = sum(weights)
            if total_weight == 0:
                self.expected_cost = sum(child.expected_cost for child in self.children.values()) / len(self.children)
            else:
                self.expected_cost = sum(weight * child.expected_cost for weight, child in zip(weights, self.children.values()))

# =================================================================
# FONCTION run_mcts : Calcul avec CONVERGENCE
# =================================================================
def run_mcts(inventory, min_iterations, epsilon, lambdas=None):
    size = sum(inventory.values())
    root = MCTSNode(WarehouseState(['X']*size, inventory, lambdas=lambdas))
    
    current_iter = 0
    prev_optimum_value = float('inf')
    converged = False

    print(f"\n--- Début de la recherche (Min: {min_iterations}, Epsilon: {epsilon}) ---")

    while not converged:
        node = root
        # 1. Sélection
        # Dans la boucle while de run_mcts :
        while not node.untried and node.children:
            if node.state.mode == "REMPLISSAGE":
                best_child = None
                best_lcb = float('inf') # On cherche le minimum

                for child in node.children.values():
                    if child.visits == 0:
                # Si un nœud n'a jamais été visité, sa priorité est maximale (coût -infini)
                        current_lcb = float('-inf')
                    else:
                # Formule LCB classique : Espérance - Terme d'exploration
                        exploration_term = 2 * math.sqrt(math.log(node.visits) / child.visits)
                        exploitation_term = child.expected_cost / child.visits
                        current_lcb = exploitation_term - exploration_term
            
                    if current_lcb < best_lcb:
                        best_lcb = current_lcb
                        best_child = child
        
                node = best_child
            else:
        # Mode SORTIE (probabilités pondérées)
                children = list(node.children.values())
                exit_probs = node.state.get_exit_probabilities()
                weights = [exit_probs.get(child.action, 0) for child in children]
                if sum(weights) == 0:
                    node = random.choice(children)
                else:
                    node = random.choices(children, weights=weights, k=1)[0]
        
        # 2. Expansion
        if node.untried:
            act = node.untried.pop()
            next_s, cost = node.state.apply(act)
            child = MCTSNode(next_s, node, cost, act)
            node.children[act] = child
            node = child
            
        # 3. Simulation
        sim_s = node.state
        cost_so_far = 0
        temp = node
        while temp:
            cost_so_far += temp.incoming_cost
            temp = temp.parent
            
        sim_total = cost_so_far
        while not (sim_s.mode == "SORTIE" and all(i == 'X' for i in sim_s.stack)):
            acts = sim_s.get_legal_actions()
            if not acts: break
            exit_probs = sim_s.get_exit_probabilities()
            weights = [exit_probs.get(act, 0) for act in acts]
            if sum(weights) == 0:
                act = random.choice(acts)
            else:
                act = random.choices(acts, weights=weights, k=1)[0]
            sim_s, c = sim_s.apply(act)
            sim_total += c
            
        # 4. Rétropropagation
        curr = node
        while curr:
            curr.visits += 1
            if not curr.children:
                curr.expected_cost = ((curr.expected_cost * (curr.visits - 1)) + sim_total) / curr.visits
            else:
                curr.update_values()
            curr = curr.parent
        
        current_iter += 1

        # --- TEST DE CONVERGENCE ---
        # On vérifie la convergence tous les 100 pas pour éviter de surcharger le calcul
        if current_iter >= min_iterations and current_iter % 100 == 0:
            # L'optimum actuel est la valeur de l'espérance à la racine
            current_optimum_value = root.expected_cost
            diff = abs(current_optimum_value - prev_optimum_value)
            
            if diff < epsilon:
                converged = True
                print(f"Convergence atteinte à l'itération {current_iter} (Delta: {diff:.6f} < {epsilon})")
            
            prev_optimum_value = current_optimum_value
            
            # Sécurité pour ne pas boucler à l'infini si ça ne converge pas
            if current_iter > 10000000: 
                print("Arrêt forcé : Limite de 10 000 000 itérations atteinte.")
                break

    return root, current_iter

# =================================================================
# FONCTION draw_tree : Visualisation
# =================================================================
def draw_tree(root, filename='mcts_convergence_2'):
    dot = Digraph(format='png')
    dot.attr('node', shape='record', style='filled', fontname='Arial', fontsize='9')
    q = [(root, "0")]
    dot.node("0", f"RACINE\\nE_total: {root.expected_cost:.2f}")
    cnt = 1
    while q:
        curr, name = q.pop(0)
        for act, child in curr.children.items():
            cid = str(cnt)
            color = "#E3F2FD" if child.state.mode == "REMPLISSAGE" else "#FFF9C4"
            label = f"{{ {child.action} | {child.state.stack} | E: {child.expected_cost:.2f} | V: {child.visits} }}"
            dot.node(cid, label, fillcolor=color)
            dot.edge(name, cid)
            q.append((child, cid))
            cnt += 1
            if cnt > 120: break
    dot.render(filename, cleanup=True)
    print(f"\n[Graphique] Image générée : {filename}.png")

# =================================================================
# BLOC PRINCIPAL
# =================================================================
if __name__ == "__main__":
    try:
        min_iters = int(input("Nombre minimum d'itérations ? : "))
        epsilon = float(input("Valeur de Epsilon (ex: 0.001) ? : "))
        
        nb_v = int(input("Nombre de variétés ? : "))
        mon_inv = {}
        mon_lambdas = {}
        for i in range(nb_v):
            nom = input(f"Nom variété {i+1} : ").upper()
            qte = int(input(f"Quantité {nom} : "))
            mon_inv[nom] = qte
            lam = float(input(f"Paramètre lambda pour {nom} : "))
            mon_lambdas[nom] = lam

        root_node, final_iters = run_mcts(mon_inv, min_iters, epsilon, mon_lambdas)
        
        # Extraction
        full_piles_dict = {}
        def find_full(n):
            if n.state.mode == "SORTIE" and n.parent and n.parent.state.mode == "REMPLISSAGE":
                if n.state.stack not in full_piles_dict:
                    full_piles_dict[n.state.stack] = n
            for c in n.children.values(): find_full(c)
        
        find_full(root_node)
        sorted_results = sorted(full_piles_dict.values(), key=lambda x: x.expected_cost)

        print("\n" + "="*85)
        print(f"RÉSULTATS APRÈS {final_iters} ITÉRATIONS")
        print("-" * 85)
        for i, n in enumerate(sorted_results[:10], 1):
            stack_str = " | ".join(n.state.stack)
            print(f"{i:<5} | ({stack_str}){' '*(33-len(stack_str))} | {n.expected_cost:<15.2f} | {n.visits}")
        print("="*85)

        draw_tree(root_node)
        
    except Exception as e:
        print(f"Erreur : {e}")