# Expert-System

## Overview
This project is an **Expert System** for Propositional Calculus. It implements a **backward-chaining inference engine** that processes propositional logic. The system parses a set of rules and facts from an input file and determines the truth value (`True`, `False`, or `Undetermined`) of specific query facts.

## Features

### Mandatory Features
* **Backward-Chaining Engine**: Uses recursive search to infer truth values.
* **Logic Operators**: Supports `+` (AND), `|` (OR), `^` (XOR), and `!` (NOT).
* **Complex Rules**:
    * Parentheses for grouping expressions: `(A + B)`.
    * Complex Conclusions: `A => B + C` (A implies both B and C).
    * Multiple rules concluding the same fact.
* **Precedence Handling**: Strictly adheres to operator priority: `()` > `!` > `+` > `|` > `^` > `=>`.
* **Error Handling**: Detects syntax errors, contradictions.

### Bonus Features
* **Biconditional Rules**: Supports `<=>` (If-and-only-if) logic.
* **Disjunctive Conclusions**: Handles `OR` and `XOR` in conclusions (e.g., `A => B | C`).
* **Reasoning Visualization**: Displays the step-by-step logic used to derive an answer.
* **Interactive Mode**: Allows users to modify facts dynamically without restarting.
* a

## Installation & Usage

### Prerequisites
* Python 3.x

### Running the Program
```
python3 expert_system.py input/<file_name>
```
To add initial facts dynamically while the programm is running (e.g. adding A):
```
=A
```
To remove initial facts dynamically while the programm is running (e.g. removing A):
```
-A
```
To quit:
```
exit
```
