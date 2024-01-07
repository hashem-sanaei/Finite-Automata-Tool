class DFA:
    def __init__(self):
        self.alphabet = set()
        self.states = set()
        self.transitions = {}
        self.start_state = None
        self.accept_states = set()

    def add_state(self, state):
        self.states.add(state)

    def add_transition(self, state_from, input_char, state_to):
        if state_from not in self.transitions:
            self.transitions[state_from] = {}
        self.transitions[state_from][input_char] = state_to

    def set_start_state(self, state):
        self.start_state = state

    def set_accept_states(self, states):
        self.accept_states = states

    def set_alphabet(self, alphabet):
        self.alphabet = alphabet

    def accepts(self, string):
        # Check if the string is accepted by the DFA
        current_state = self.start_state
        for char in string:
            if current_state not in self.transitions or char not in self.transitions[current_state]:
                return False
            current_state = self.transitions[current_state][char]
        return current_state in self.accept_states
    

class NFA:
    # Similar structure to DFA, but transitions allow for multiple next states
    def __init__(self):
        self.alphabet = set()
        self.states = set()
        self.transitions = {}
        self.start_state = None
        self.accept_states = set()

    def add_state(self, state):
        self.states.add(state)

    def add_transition(self, state_from, input_char, state_to):
        if state_from not in self.transitions:
            self.transitions[state_from] = {}
        if input_char not in self.transitions[state_from]:
            self.transitions[state_from][input_char] = set()
        self.transitions[state_from][input_char].add(state_to)

    def set_start_state(self, state):
        self.start_state = state

    def set_accept_states(self, states):
        self.accept_states = states

    def set_alphabet(self, alphabet):
        self.alphabet = alphabet

    def accepts(self, string):
        # Check if the string is accepted by the NFA
        current_states = set()
        current_states.add(self.start_state)
        for char in string:
            next_states = set()
            for state in current_states:
                if state not in self.transitions or char not in self.transitions[state]:
                    continue
                next_states = next_states.union(self.transitions[state][char])
            current_states = next_states
        return len(current_states.intersection(self.accept_states)) > 0
    

def convert_nfa_to_dfa(nfa):
    dfa = DFA()
    unmarked_states = []  # States in DFA that have not been processed yet
    dfa_start_state = frozenset([nfa.start_state])  # DFA start state is a set containing the NFA start state
    dfa.set_start_state(dfa_start_state)
    unmarked_states.append(dfa_start_state)
    dfa.add_state(dfa_start_state)

    while unmarked_states:
        current_dfa_state = unmarked_states.pop()
        
        # Check all input characters
        for input_char in set().union(*[set(transitions.keys()) for transitions in nfa.transitions.values()]):
            next_states = set()
            for nfa_state in current_dfa_state:
                if nfa_state in nfa.transitions and input_char in nfa.transitions[nfa_state]:
                    next_states.update(nfa.transitions[nfa_state][input_char])

            next_dfa_state = frozenset(next_states)
            if next_dfa_state not in dfa.states:
                dfa.add_state(next_dfa_state)
                unmarked_states.append(next_dfa_state)

            # Add transition in DFA
            dfa.add_transition(current_dfa_state, input_char, next_dfa_state)

    # Determine accept states in DFA
    for dfa_state in dfa.states:
        if any(state in nfa.accept_states for state in dfa_state):
            dfa.accept_states.add(dfa_state)

    return dfa

import json

def export_automaton_to_json(automaton):
    nodes = []
    for state in automaton.states:
        node = {'id': state, 'label': state}
        if state == automaton.start_state:
            node['label'] = 'Start State'
        if state in automaton.accept_states:
            node['label'] = 'Accept State'
        nodes.append(node)

    edges = []
    for state_from, transitions in automaton.transitions.items():
        for input_char, state_tos in transitions.items():
            if isinstance(state_tos, set): 
                for state_to in state_tos:
                    edges.append({'from': state_from, 'to': state_to, 'label': input_char})
            else:  
                edges.append({'from': state_from, 'to': transitions[input_char], 'label': input_char})

    automaton_data = {'nodes': nodes, 'edges': edges}
    with open('automaton_data.json', 'w') as file:
        json.dump(automaton_data, file)


import webbrowser
import os
import threading

def open_browser():
    def start_server():
        os.system('python -m http.server 5500')

    # Start server in a separate thread
    threading.Thread(target=start_server).start()

    url = 'http://127.0.0.1:5500/plot.html'
    webbrowser.open(url)




def add_multiple_transitions(automaton, state_from, input_char, states_to):
    for state_to in states_to:
        automaton.add_transition(state_from, input_char, state_to)


def user_interface():
    current_automaton = DFA()
    is_dfa = True
    step = 0
    with open('automaton_data.json', 'w') as file:
        json.dump({}, file)
    
    while True:
        if is_dfa and step > 0:
            print("\nCurrent automaton: DFA")
        else:
            print("\nCurrent automaton: NFA")

        print("\nFinite Automata Tool")
        if step == 0: print("0. Set alphabet")
        if step == 1: 
            print("1. Create DFA")
            print("2. Create NFA")
        if step == 2:
            print("3. Add states")
            print("4. Add transitions")
            print("5. Test strings")
            print("6. Convert NFA to DFA")
            print("7. Show")
            #print("8. check DFA is valid or not")
        print("9. Exit")

        choice = input("Enter your choice: ")

        if choice == '0' :
            alphabet = input("Enter alphabet (characters separated by spaces): ")
            if current_automaton is not None:
                current_automaton.set_alphabet(alphabet.split())
            else:
                print("current_automaton is not initialized")
            print("Alphabet set.")
            step = 1
        
        elif choice == '1':
            current_automaton = DFA()
            is_dfa = True
            print("DFA created.")
            step = 2
            

        elif choice == '2':
            current_automaton = NFA()
            is_dfa = False
            print("NFA created.")
            step = 2

        elif choice == '3':
            if current_automaton is None:
                print("Please create an automaton first.")
                continue
            state = input("Enter state name: ")
            current_automaton.add_state(state)
            print(len(current_automaton.states))
            if len(current_automaton.states) == 1:
                current_automaton.set_start_state(state)
            if input("Is this an accept state? (y/n): ") == 'y':
                current_automaton.set_accept_states([state])
            print(f"State {state} added.")

        elif choice == '4':
            if current_automaton is None:
                print("Please create an automaton first.")
                continue
            state_from = input("Enter source state: ")
            input_char = input("Enter input character: ")
            if is_dfa:
                state_to = input("Enter destination state: ")
                current_automaton.add_transition(state_from, input_char, state_to)
            else:
                states_to = input("Enter destination states (separated by space): ").split()
                add_multiple_transitions(current_automaton, state_from, input_char, states_to)
            print(f"Transition(s) added from state {state_from} on input {input_char}.")
        elif choice == '5':
            if current_automaton is None:
                print("Please create an automaton first.")
                continue
            test_string = input("Enter a string to test: ")
            if (is_dfa and current_automaton.accepts(test_string)) or \
               (not is_dfa and current_automaton.accepts(test_string)):
                print("String accepted.")
            else:
                print("String rejected.")

        elif choice == '6':
            if not is_dfa:
                if current_automaton is None:
                    print("Please create an NFA first.")
                    continue
                dfa = convert_nfa_to_dfa(current_automaton)
                current_automaton = dfa
                is_dfa = True
                print("NFA converted to DFA.")
            else:
                print("Current automaton is already a DFA.")

        elif choice == '7':
            if current_automaton is None:
                print("Please create an automaton first.")
                continue
            print("States: ", current_automaton.states)
            print("Transitions: ", current_automaton.transitions)
            print("Start state: ", current_automaton.start_state)
            print("Accept states: ", current_automaton.accept_states)
            export_automaton_to_json(current_automaton)
            open_browser()
            
        elif choice == '8':
            if current_automaton is None:
                print("Please create an automaton first.")
                continue
            if is_dfa:
                is_valid = all(len(current_automaton.transitions.get(state, {})) == len(current_automaton.alphabet) for state in current_automaton.states)
                print("DFA is valid." if is_valid else "DFA is not valid.")
            else:
                print("This option is only for DFA.")

        elif choice == '9':
            print("Exiting...")
            break

        else:
            print("Invalid choice. Please try again.")


def main():
    user_interface()

if __name__ == "__main__":
    main()