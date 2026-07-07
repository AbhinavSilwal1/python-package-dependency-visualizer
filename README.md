# Python Package Dependency Visualizer

Command-line dependency analysis tool built with Python, AST parsing, NetworkX, and Graphviz to analyze Python project structures, visualize dependencies, and generate detailed reports.

## 🚀 Features
- Scan Python projects and analyze import dependencies
- AST-based Python import extraction
- Internal project dependency detection
- Dependency graph generation
- Circular dependency detection
- Orphan module detection
- Leaf module detection
- Dependency ranking:
  - Most imported modules
  - Most dependent modules
- Dependency graph exports:
  - DOT
  - PNG
  - SVG
- Internal-only dependency filtering
- JSON dependency reports
- HTML dependency reports
- Custom CLI application using Typer
- Configurable tool metadata:
  - Tool name
  - Version information
  - Report timestamps

## 🧠 Purpose
This project is built to strengthen understanding of software architecture analysis, dependency management, and command-line application development.

It focuses on:
- Abstract Syntax Tree (AST) parsing
- Graph algorithms
- Dependency analysis
- CLI application design
- Report generation

## 🛠 Technologies Used
- Python
- Typer
- NetworkX
- Graphviz
- AST
- HTML
- JSON

## 📦 How To Run
Clone the repository:
```bash
git clone https://github.com/AbhinavSilwal1/python-package-dependency-visualizer.git
cd python-package-dependency-visualizer
```

Create and activate virtual environment:
```bash
python -m venv .venv
source .venv/bin/activate
```

Install dependencies:
```bash
pip install -r requirements.txt
```

Install DepViz as a command-line tool:
```bash
pip install .
```

Verify installation:
```bash
depviz --help
```

## 📌 Current Commands

### ❓ Help
Open the help module of the tool.
```bash
depviz --help
```

<br>

### 🔢 Version
Show the version of the tool.
```bash
depviz version
```

<br>

### 🔍 Scan Project
Analyze Python files and display dependency information.

Scan current directory:
```bash
depviz scan
```

Scan a specific project:
```bash
depviz scan path/to/project
```

<br>

### 📊 Export Dependency Graph
Export dependency graphs in different formats.

#### DOT Export
Default DOT export:
```bash
depviz export path/to/project filename.dot
```

DOT export to a specific location:
```bash
depviz export path/to/project path/to/location/filename.dot
```

#### PNG Export
Default PNG export:
```bash
depviz export path/to/project filename.png
```

PNG export to a specific location:
```bash
depviz export path/to/project path/to/location/filename.png
```

#### SVG Export
Default SVG export:
```bash
depviz export path/to/project filename.svg
```

SVG export to a specific location:
```bash
depviz export path/to/project path/to/location/filename.svg
```

#### Internal Dependency Export
Default Internal Dependency export:
```bash
depviz export path/to/project filename.dot --internal-only
```
```bash
depviz export path/to/project filename.png --internal-only
```
```bash
depviz export path/to/project filename.svg --internal-only
```

Internal Dependency export to a specific location:
```bash
depviz export path/to/project path/to/location/filename.dot --internal-only
```
```bash
depviz export path/to/project path/to/location/filename.png --internal-only
```
```bash
depviz export path/to/project path/to/location/filename.svg --internal-only
```

<br>

### 📄 Generate JSON Report
Generate machine-readable dependency analysis reports.

Default JSON report:
```bash
depviz report-json path/to/project filename.json
```

Export JSON report to a specific location:
```bash
depviz report-json path/to/project path/to/location/filename.json
```

<br>

### 🌐 Generate HTML Report
Generate browser-based dependency analysis reports.

Default HTML report:
```bash
depviz report-html path/to/project filename.html
```

Export HTML report to a specific location:
```bash
depviz report-html path/to/project path/to/location/filename.html
```