# Flow Graph Algorithm Runner

This project implements algorithms to solve the Single-Source Unsplittable Flow Problem (SSUFP). Algorithms include Brute Force, Genetic Algorithm, Simulated Annealing, and Variable Neighborhood Search (VNS). You can generate graphs, run algorithms, and analyze results.

## Usage

### Arguments
- `--action`: Choose between "generate", "run", or "analyze".
- `--algorithms`: Comma-separated list of algorithms to run: `"brute-force", "genetic", "simulated-annealing", "vns"`.
- `--examples`: Directory containing graph instances to run algorithms on.
- `--reports`: Directory to store or analyze result reports.

### Available Commands
1. **Generate Graphs**:
   ```bash
   python main.py --action generate
   ```
   Generates randomly small, medium, and large graph instances and stores them in the resources/generated folder.

2. **Run Algorithms**:
   ```bash
   python main.py --action run --algorithms "genetic,simulated-annealing" --examples ./resources/generated
   ```
   Runs the specified algorithms on all graph instances in the examples folder and stores the results in reports.

2. **Analyze Results**:
   ```bash
   python main.py --action analyze --reports ./path/to/reports
   ```
   Analyzes the results in the reports folder, comparing performance across different algorithms and parameter configurations.

## Algorithms

- **Brute Force**: Exhaustively explores all possible flow paths.
- **Genetic Algorithm**: Uses selection, crossover, and mutation to evolve solutions.
- **Simulated Annealing**: Accepts worse solutions with decreasing probability to avoid local optima.
- **VNS**: Systematically changes neighborhoods to escape local optima.

## Results

Results for each algorithm run per instance are stored in a `reports.csv` file inside instance folder, which includes algorithm parameters, runtime, feasibility, objective result, and performance metrics.
