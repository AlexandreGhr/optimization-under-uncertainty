import argparse
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle

# Probabilité que l'écart d change de delta, selon le style choisi
PROBAS = {
    "A": {+1: 0.45, 0: 0.00, -1: 0.55},   # agressif : pas de nul
    "D": {+1: 0.10, 0: 0.75, -1: 0.15},   # défensif : surtout des nuls
}


def recompense_finale(d):
    return (d > 0) - (d < 0)   # +1, 0 ou -1


def resoudre(N):
    u, politique = {}, {}

    # Cas de base : plus aucune partie à jouer
    for d in range(-N, N + 1):
        u[(0, d)] = recompense_finale(d)

    # On remonte : 1 partie restante, puis 2, etc.
    for n in range(1, N + 1):
        deja_jouees = N - n
        for d in range(-deja_jouees, deja_jouees + 1):
            valeurs = {
                a: sum(p * u[(n - 1, d + delta)] for delta, p in PROBAS[a].items())
                for a in PROBAS
            }
            meilleur = max(valeurs, key=valeurs.get)
            u[(n, d)] = valeurs[meilleur]
            politique[(n, d)] = meilleur
    return u, politique


def tracer_carte(N, u, politique, fichier=None):
    """Génère la grille des états : action optimale et valeur de chaque case."""
    couleurs = {"A": "#f5c26b", "D": "#9cc3ee",
                "gagne": "#a8d5a2", "nul": "#e0e0e0", "perd": "#f1a9a0"}
    fig, ax = plt.subplots(figsize=(9, 5.5))

    for n in range(N + 1):
        col = N - n                      # le temps va de gauche à droite
        deja_jouees = N - n
        for d in range(-deja_jouees, deja_jouees + 1):
            if n == 0:                   # match fini
                cle = "gagne" if d > 0 else "perd" if d < 0 else "nul"
                texte = f"{recompense_finale(d):+d}".replace("+0", "0")
            elif abs(d) > n:             # match déjà joué : l'action ne compte plus
                cle = "gagne" if d > 0 else "perd"
                texte = f"{recompense_finale(d):+d}"
            else:
                a = politique[(n, d)]
                cle = a
                texte = f"{a}\n{u[(n, d)]:.3f}"
            ax.add_patch(Rectangle((col + 0.05, d - 0.45), 0.9, 0.9,
                                   facecolor=couleurs[cle], edgecolor="gray"))
            ax.text(col + 0.5, d, texte, ha="center", va="center", fontsize=10)

    ax.set_xlim(0, N + 1)
    ax.set_ylim(-N - 0.6, N + 0.6)
    ax.set_xticks([c + 0.5 for c in range(N + 1)])
    ax.set_xticklabels([f"{N - c} partie(s)\nrestante(s)" if c < N else "match fini"
                        for c in range(N + 1)])
    ax.set_yticks(range(-N, N + 1))
    ax.set_ylabel("écart d (victoires - défaites de B)")
    ax.set_title("A = agressif (orange), D = défensif (bleu) : action optimale et valeur")
    for s in ("top", "right"):
        ax.spines[s].set_visible(False)

    fig.tight_layout()
    fichier = fichier or f"echecs_N{N}.png"
    fig.savefig(fichier, dpi=150)
    print(f"Image enregistrée : {fichier}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Match d'échecs (MDP)")
    parser.add_argument("--n", type=int, default=3, help="nombre de parties")
    args = parser.parse_args()

    u, pol = resoudre(args.n)
    for n in range(1, args.n + 1):
        print(f"--- {n} partie(s) restante(s) ---")
        j = args.n - n
        for d in range(-j, j + 1):
            print(f"d={d:+d} : choix {pol[(n, d)]}, valeur {u[(n, d)]:.4f}")
    tracer_carte(args.n, u, pol)