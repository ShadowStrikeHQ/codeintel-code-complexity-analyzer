# codeintel-Code-Complexity-Analyzer
Calculates cyclomatic complexity and other code complexity metrics for Python code. Uses the `ast` module to parse the code and calculate complexity scores based on control flow. Reports on functions or classes exceeding defined complexity thresholds. Can use `radon` library for complexity calculation. - Focused on Tools for static code analysis, vulnerability scanning, and code quality assurance

## Install
`git clone https://github.com/ShadowStrikeHQ/codeintel-code-complexity-analyzer`

## Usage
`./codeintel-code-complexity-analyzer [params]`

## Parameters
- `-h`: Show help message and exit
- `--threshold`: Complexity threshold for reporting functions/classes. Defaults to 10.
- `--report-raw`: No description provided
- `--include-imports`: Include import statements in the code complexity calculation.

## License
Copyright (c) ShadowStrikeHQ
