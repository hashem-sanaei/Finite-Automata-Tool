# Finite Automata Tool

This is a Python-based Finite Automata Tool that allows you to work with Deterministic Finite Automata (DFA) and Non-deterministic Finite Automata (NFA). You can create, manipulate, and visualize automata, as well as perform various operations on them. This tool provides an interactive command-line interface and includes a web-based visualization component.

## Features

- Create and manipulate DFA and NFA.
- Set the alphabet for the automaton.
- Add states and transitions to the automaton.
- Test strings to determine if they are accepted or rejected by the automaton.
- Convert NFA to DFA.
- Visualize automaton using a web-based graphical representation.

## Prerequisites

- Python 3.x
- The `vis-network` JavaScript library for visualization (included in the project).

## Getting Started

1. Clone the repository to your local machine:

   ```bash
   git clone <repository_url>
   ```

2. Ensure you have Python 3.x installed.

3. Open the project directory in your terminal.

4. Run the following command to start the Finite Automata Tool:

   ```bash
   python main.py
   ```

## Usage

1. Set the alphabet for the automaton.

2. Choose whether to create a DFA or an NFA.

3. Add states and transitions to the automaton.

4. Test strings to determine their acceptance.

5. Optionally, convert an NFA to a DFA.

6. Visualize the automaton using the web-based graphical representation.

7. You can also check if a DFA is valid (all transitions are defined for each state).

8. Exit the tool when done.

## Files

- `main.py`: Contains the Python code for the Finite Automata Tool.
- `plot.html`: Provides the web-based visualization component for automata.

## Visualizing Automata

Automata created or manipulated using this tool can be visualized by opening the `plot.html` file in a web browser after running the tool. The visualization updates automatically when you perform operations on the automaton.

## Example

![Automaton Visualization](example.png)

## Authors

- Hashem Sanaei (hashemsanaei8@gmail.com)

## Acknowledgments

- [vis-network](https://github.com/visjs/vis-network) for the JavaScript library used for automaton visualization.
- Any additional acknowledgments or credits.

