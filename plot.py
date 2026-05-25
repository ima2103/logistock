# generate_graphs.py
import matplotlib.pyplot as plt
import numpy as np
import matplotlib

# Style professionnel
matplotlib.rcParams['font.size'] = 12
matplotlib.rcParams['axes.titlesize'] = 14
matplotlib.rcParams['axes.labelsize'] = 12
plt.style.use('seaborn-v0_8-whitegrid')


def generate_convergence_curve():
    """Courbe de convergence MCTS"""
    simulations = np.array([100, 500, 1000, 2000, 5000, 10000])
    couts = np.array([35.2, 28.7, 26.3, 25.1, 24.9, 24.9])

    plt.figure(figsize=(10, 6))
    plt.plot(simulations, couts, 'b-o', linewidth=2.5, markersize=8,
             markerfacecolor='white', markeredgewidth=2)

    # Zone de convergence
    plt.axvspan(2000, 10000, alpha=0.1, color='green', label='Zone de convergence')
    plt.axhline(y=24.9, color='red', linestyle='--', linewidth=2,
                alpha=0.7, label='Optimum (24.9)')

    plt.xlabel('Nombre de simulations MCTS', fontweight='bold')
    plt.ylabel('Espérance de coût', fontweight='bold')
    plt.title('Convergence de l\'algorithme MCTS', fontsize=16, fontweight='bold')
    plt.grid(True, alpha=0.3)
    plt.legend(loc='upper right')
    plt.tight_layout()
    plt.savefig('convergence_mcts.png', dpi=300, bbox_inches='tight')
    plt.close()
    print("✓ Courbe de convergence générée")


def generate_benchmark_charts():
    """Graphiques de benchmark"""
    methodes = ['MCTS\n(logiStock)', 'Recuit\nsimulé', 'Algo.\ngénétique', 'Heuristique\ngloutonne']
    couts = [25.14, 26.72, 26.05, 29.85]
    temps = [3.2, 12.7, 8.9, 0.1]
    colors = ['#2ecc71', '#e74c3c', '#3498db', '#f39c12']

    # Graphique des coûts
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))

    bars1 = ax1.bar(methodes, couts, color=colors, edgecolor='black', linewidth=1.5)
    ax1.set_ylabel('Espérance de coût', fontweight='bold')
    ax1.set_title('Qualité des solutions', fontsize=14, fontweight='bold')
    ax1.grid(axis='y', alpha=0.3)

    # Annotations sur les barres
    for bar in bars1:
        height = bar.get_height()
        ax1.text(bar.get_x() + bar.get_width() / 2., height + 0.1,
                 f'{height:.2f}', ha='center', va='bottom', fontweight='bold')

    # Graphique des temps (log)
    bars2 = ax2.bar(methodes, temps, color=colors, edgecolor='black', linewidth=1.5)
    ax2.set_ylabel('Temps de calcul (s)', fontweight='bold')
    ax2.set_title('Temps de calcul (échelle log)', fontsize=14, fontweight='bold')
    ax2.set_yscale('log')
    ax2.grid(axis='y', alpha=0.3)

    # Annotations
    for bar in bars2:
        height = bar.get_height()
        ax2.text(bar.get_x() + bar.get_width() / 2., height * 1.1,
                 f'{height:.1f}s', ha='center', va='bottom', fontweight='bold')

    plt.tight_layout()
    plt.savefig('benchmark_comparison.png', dpi=300, bbox_inches='tight')
    plt.close()
    print("✓ Graphiques de benchmark générés")


def generate_learning_curve():
    """Courbe d'apprentissage avec persistance"""
    sessions = np.array([1, 2, 3, 4, 5])
    temps = np.array([4.1, 3.4, 2.9, 2.3, 1.8])
    couts = np.array([25.14, 24.87, 24.65, 24.52, 24.48])

    fig, ax1 = plt.subplots(figsize=(10, 6))

    # Courbe des coûts
    line1 = ax1.plot(sessions, couts, 'g-s', linewidth=2.5, markersize=10,
                     markerfacecolor='white', markeredgewidth=2, label='Coût moyen')
    ax1.set_xlabel('Session d\'optimisation', fontweight='bold')
    ax1.set_ylabel('Espérance de coût', color='green', fontweight='bold')
    ax1.tick_params(axis='y', labelcolor='green')
    ax1.set_xticks(sessions)
    ax1.grid(True, alpha=0.3)

    # Courbe des temps
    ax2 = ax1.twinx()
    line2 = ax2.plot(sessions, temps, 'b-o', linewidth=2.5, markersize=10,
                     markerfacecolor='white', markeredgewidth=2, label='Temps de calcul')
    ax2.set_ylabel('Temps (secondes)', color='blue', fontweight='bold')
    ax2.tick_params(axis='y', labelcolor='blue')

    # Annotations
    for i, (t, c) in enumerate(zip(temps, couts)):
        ax1.annotate(f'{c:.2f}', (sessions[i], couts[i]),
                     textcoords="offset points", xytext=(0, 10), ha='center')
        ax2.annotate(f'{t:.1f}s', (sessions[i], temps[i]),
                     textcoords="offset points", xytext=(0, -15), ha='center', color='blue')

    plt.title('Impact de la persistance MCTS sur l\'apprentissage',
              fontsize=16, fontweight='bold')
    plt.tight_layout()
    plt.savefig('learning_curve.png', dpi=300, bbox_inches='tight')
    plt.close()
    print("✓ Courbe d'apprentissage générée")


def generate_sensitivity_analysis():
    """Analyse de sensibilité"""
    c_values = np.array([0.5, 1.0, 1.5, 2.0, 2.5, 3.0, 3.5, 4.0])
    couts = np.array([26.8, 25.9, 25.3, 25.14, 25.2, 25.4, 25.7, 26.1])

    plt.figure(figsize=(10, 6))
    plt.plot(c_values, couts, 'm-^', linewidth=2.5, markersize=10,
             markerfacecolor='white', markeredgewidth=2)

    # Zone optimale
    plt.axvspan(1.8, 2.2, alpha=0.2, color='green', label='Zone optimale')
    plt.axvline(x=2.0, color='red', linestyle='--', linewidth=2,
                label='Valeur par défaut (c=2.0)')

    plt.xlabel('Constante d\'exploration (c)', fontweight='bold')
    plt.ylabel('Coût moyen', fontweight='bold')
    plt.title('Sensibilité au paramètre d\'exploration MCTS',
              fontsize=16, fontweight='bold')
    plt.grid(True, alpha=0.3)
    plt.legend()

    # Annotations
    for c, cout in zip(c_values, couts):
        plt.annotate(f'{cout:.2f}', (c, cout),
                     textcoords="offset points", xytext=(0, 10), ha='center')

    plt.tight_layout()
    plt.savefig('sensitivity_analysis.png', dpi=300, bbox_inches='tight')
    plt.close()
    print("✓ Analyse de sensibilité générée")


def main():
    print("Génération des graphiques pour le mémoire...")
    generate_convergence_curve()
    generate_benchmark_charts()
    generate_learning_curve()
    generate_sensitivity_analysis()
    print("\n✅ Tous les graphiques ont été générés dans le dossier courant")
    print("📁 Fichiers créés :")
    print("   - convergence_mcts.png")
    print("   - benchmark_comparison.png")
    print("   - learning_curve.png")
    print("   - sensitivity_analysis.png")


if __name__ == "__main__":
    main()