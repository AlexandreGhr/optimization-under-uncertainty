# MDP : exercices d'optimisation sous incertitude

Implémentations en Python d'exercices sur les processus de décision markoviens (MDP),
vus en cours d'optimisation sous incertitude (Master 2). Pour chaque problème :
la modélisation (états, actions, récompenses), la résolution par programmation
dynamique, et une visualisation du résultat.

## Exercices

| Dossier | Problème | Notion |
|---------|----------|--------|
| [01_match_echecs](01_match_echecs) | Choisir un style de jeu sur un match en 3 parties | Induction arrière, politique optimale adaptative |
| [02_roue_fortune](02_roue_fortune) | Garder ou relancer une roue (finie et infinie) | Arrêt optimal, seuils, point fixe |

D'autres exercices (patineur sur une grille, problème du stagiaire) seront ajoutés.

## Installation

```bash
git clone https://github.com/TON_PSEUDO/mdp-exercices.git
cd mdp-exercices
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Lancer un exercice

Chaque script se lance depuis son dossier et génère une image à côté de lui :

```bash
cd 01_match_echecs
python3 echecs.py

cd ../02_roue_fortune
python3 roue.py
```

## Idée commune

Tous ces problèmes se résolvent avec l'équation de Bellman :
on part de la fin et on remonte, en choisissant à chaque étape l'action qui maximise

récompense immédiate + espérance de la valeur de l'état suivant.

La stratégie optimale qui en sort est déterministe et ne dépend que de l'état courant.