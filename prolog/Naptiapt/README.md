# Naptiapt: Automatic Theorem Prover

      No automatic picture trasmicion , Is Automatic Theorem Prover ->Naptiapt

Naptiapt is a web-based automatic theorem prover that uses Prolog for logical reasoning. It provides an intuitive interface for defining axioms, rules, and facts, then attempts to prove theorems using logical inference.

![Naptiapt Screenshot](https://raw.githubusercontent.com/jero98772/Naptiapt/refs/heads/main/screenshot/screenshot.png)

## Features

- **Interactive Theorem Proving**: Define logical axioms, inference rules, and facts
- **Proof Visualization**: See step-by-step proof traces when theorems are proven
- **Prolog Backend**: Leverages Prolog's powerful logical inference engine
- **Predefined Examples**: Includes several built-in examples to demonstrate the system
- **Responsive UI**: Clean, intuitive interface for both beginners and experts

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/naptiapt.git
cd naptiapt
```

2. Create a virtual environment and install dependencies:
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

3. Install SWI-Prolog (required for pyswip):
```bash
sudo apt-get install swi-prolog
```

4. Run the application:
```bash
uvicorn main:app --reload
```

5. Open your browser and visit: http://localhost:8000

## Usage

1. **Define Axioms**: Enter logical axioms (one per line)
2. **Add Rules**: Create inference rules with premises and conclusions
3. **Specify Facts**: List known facts (one per line)
4. **Enter Theorem**: State the theorem you want to prove
5. **Submit**: Click "Prove Theorem" to see the result

The system will either:
- Provide a step-by-step proof trace
- Show an error if the theorem can't be proven
- Display any errors in the input

## Examples

Naptiapt comes with several built-in examples:

1. **Socrates Mortality**: 
   - Axioms: `human(socrates)`
   - Rules: `human(X) → mortal(X)`
   - Theorem: `mortal(socrates)`

2. **Basic Arithmetic**:
   - Axioms: `natural(zero)`, `add(zero, X, X)`
   - Rules: 
     - `natural(X) → natural(succ(X))`
     - `add(X, Y, Z) → add(succ(X), Y, succ(Z))`
   - Theorem: `natural(succ(zero))`

3. **Logical Reasoning**:
   - Axioms: `p`, `implies(p, q)`
   - Rules: `and(P, implies(P, Q)) → Q`
   - Theorem: `q`

## Project Structure

```
naptiapt/
├── main.py             # FastAPI backend and Prolog interface
├── static/             # Static assets (CSS, JS, images)
│   ├── script.js       # Frontend logic
│   └── styles.css      # Styling
├── templates/          # HTML templates
│   └── index.html      # Main UI
├── requirements.txt    # Python dependencies
└── README.md           # This file
```

## Dependencies

- Python 3.8+
- FastAPI
- Uvicorn
- pyswip
- SWI-Prolog

## License

This project is licensed under the GLPv3 License. See the [LICENSE](LICENSE) file for details.

## Contributing

Contributions are welcome! Please open an issue or submit a pull request for any improvements or bug fixes.

## Future Enhancements

- Show step by step the proces of proving a theorem
