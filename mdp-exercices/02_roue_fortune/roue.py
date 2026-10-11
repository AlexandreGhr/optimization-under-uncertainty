# roue.py
import argparse
import matplotlib.pyplot as plt


def esperances(K, faces=10, lam=1.0):
    """E[k] pour k = 1..K lancers restants (lam = facteur d'actualisation)."""
    valeurs = range(1, faces + 1)
    E = {1: sum(valeurs) / faces}                 # 1 lancer : on garde
    for k in range(2, K + 1):
        E[k] = sum(max(x, lam * E[k - 1]) for x in valeurs) / faces
    return E


def valeur_infinie(faces=10, lam=1.0, tol=1e-12):
    """Cas infini : point fixe de V = moyenne de max(x, lam * V)."""
    valeurs = range(1, faces + 1)
    V = sum(valeurs) / faces
    while True:
        V_suivant = sum(max(x, lam * V) for x in valeurs) / faces
        if abs(V_suivant - V) < tol:
            return V_suivant
        V = V_suivant


def tracer(K, faces=10, lam=1.0, fichier=None):
    """Génère l'image : seuil d'arrêt (gauche) et convergence de E (droite)."""
    K_courbe = max(K, 12)
    E = esperances(K_courbe, faces, lam)
    V = valeur_infinie(faces, lam)
    seuil = lam * E[K - 1] if K > 1 else 0

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(11, 4))

    # Gauche : pour chaque résultat x, on garde (bleu) ou on relance (gris)
    xs = list(range(1, faces + 1))
    couleurs = ["tab:blue" if x >= seuil else "lightgray" for x in xs]
    ax1.bar(xs, xs, color=couleurs)
    if K > 1:
        ax1.axhline(seuil, ls="--", color="black",
                    label=f"ce qu'on espère en relançant = {seuil:.2f}")
        ax1.legend(loc="upper left", fontsize=9)
    ax1.set_xticks(xs)
    ax1.set_xlabel("résultat x de la roue")
    ax1.set_ylabel("gain si on garde")
    ax1.set_title(f"{K} lancer(s) restant(s) : E = {E[K]:.4f}")

    # Droite : E[k] en fonction du nombre de lancers, et sa limite
    ax2.plot(list(E.keys()), list(E.values()), "o-")
    ax2.plot([K], [E[K]], "o", color="tab:red", markersize=10, label=f"k = {K}")
    ax2.axhline(V, ls="--", color="black", label=f"limite (infini) = {V:.3f}")
    ax2.set_xlabel("nombre de lancers restants")
    ax2.set_ylabel("espérance E")
    ax2.set_title(f"Convergence ({faces} faces, lambda = {lam})")
    ax2.legend(loc="lower right", fontsize=9)

    fig.tight_layout()
    fichier = fichier or f"roue_k{K}.png"
    fig.savefig(fichier, dpi=150)
    print(f"Image enregistrée : {fichier}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Roue de la fortune (MDP)")
    parser.add_argument("--k", type=int, default=2, help="lancers restants")
    parser.add_argument("--faces", type=int, default=10, help="nombre de faces")
    parser.add_argument("--lam", type=float, default=1.0, help="actualisation")
    args = parser.parse_args()

    E = esperances(args.k, args.faces, args.lam)
    for k, v in E.items():
        print(f"{k} lancer(s) restant(s) : {v:.4f}")
    print(f"Infini : {valeur_infinie(args.faces, args.lam):.4f}")
    tracer(args.k, args.faces, args.lam)