# Intelligent Agents for Two-Sided Two-Player Draw Dominoes (CSCI5511)

This project implements intelligent agents for a two-player, two-sided **Draw Dominoes (double-6)** game. The system includes a complete game engine and two AI agents: an **Expectiminimax agent** and a **Single Observer Information Set Monte Carlo Tree Search (SO-ISMCTS)** agent. The agents are evaluated through automated simulations and can also be played against by a human user.

---

## Authors
- **Justin Bueno**
- **Muhammad Shakil** 

---

## Project Overview

Draw Dominoes is a stochastic, partially observable game in which players alternate placing tiles that match the open ends of the board. If a player cannot make a legal move, they must draw from the boneyard until a move becomes possible or the boneyard is empty.

A round ends when a player empties their hand, earning points equal to the pip-sum of the opponent’s remaining tiles. The game continues across multiple rounds until one player reaches **200 points**.

This project explores two different AI approaches:
- **Expectiminimax**, which explicitly models chance and adversarial decision-making.
- **SO-ISMCTS**, which handles hidden information through determinization and Monte Carlo simulations.

All code was implemented from scratch.

---

## Game Rules Implemented

- **Domino Set:** Double-6 (28 unique tiles)
- **Initial Hand:** 7 tiles per player
- **Turn Order:** Determined by highest-priority tile:
  - Highest double first (6–6 → 0–0), then highest non-double (6–5 → 1–0)
- **Drawing Rules:**
  - If a player cannot move, they draw until a legal move is possible or the boneyard is empty.
- **Round End:**
  - A player empties their hand, or
  - Both players are blocked and the boneyard is empty
- **Scoring:**
  - Winner earns the pip-sum of the opponent’s remaining tiles
- **Game End:** First player to reach **200 points**

**Additional Rule:**  
If an initial hand contains **5 or more doubles**, both hands and the boneyard are reset.

---

## Agents

### Expectiminimax Agent
- Uses Minimax with **chance nodes**
- Employs a weighted evaluation function based on:
  - Tile difference
  - Mobility (number of legal moves)
  - Pip score
- Chance nodes estimate opponent tiles with a uniform probability model
- Branching is reduced by assuming a single opponent tile per chance node
- Min nodes are given full observation of the max node’s chosen move to compensate

### SO-ISMCTS Agent
- Based on **Single Observer Information Set Monte Carlo Tree Search**
- Handles hidden information via **determinization**
- Models the opponent as a random agent
- Uses Selection → Expansion → Simulation → Backpropagation
- Utility is computed from terminal game states using determinized states

---

## Software Requirements

- **Python 3.10 or higher**
- **numpy**


## How to Run

From the project root directory:

```bash
python main.py
```

You will be prompted with options to:
1. Run all evaluations
2. Run default evaluations
3. Run exploratory evaluations
4. Run agent comparison tests
5. Play as a human against an agent

---

## Playing as a Human

- Legal moves are displayed each turn
- Board placement options:
  - `0` → start of the board
  - `-1` → end of the board
- Invalid inputs are rejected

---

## Evaluations

Default evaluations run **100 games** to 200 points against a random player.

Evaluation parameters can be modified near the top of `main.py`.

---
