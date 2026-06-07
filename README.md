<h1 align="center">
Alassane WADE — Tree C# Script
</h1>

<h2 align="center">
"⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣽⣿⣿⣿⡇⣿⣿⣿⣿⣿⣿⣷⣶⣥⣴⣿"
</h2>

A Python script that parses a C# solution file (`.sln`) and generates three text files visualizing project dependencies, frameworks, and tree structure.

---

## Prerequisites

- **Python 3.10 or higher** (required for type hint syntax used in the code)
- **Windows only** — paths are parsed using Windows backslash separators (`\`)
- The `.sln` file and all referenced `.csproj` / `.vcxproj` files must be accessible from the machine running the script

---

## Installation

Clone the repository in the path of your choice:

```bash
git clone https://github.com/alassane8/TreeCSharp.git
cd TreeCSharp/code
```

---

## Project Structure

```
code/
├── main.py          # Entry point — orchestrates the full parsing pipeline
├── project.py       # Project class definition
├── open_path.py     # Parses .csproj files for missed references
├── tree.py          # Recursive tree display function
└── writers.py       # Generates the three output .txt files
```

---

## Usage

Run the script from the `code/` folder:

```bash
python main.py
```

When prompted, enter the **absolute path** to your `.sln` file:

```
Enter path to .sln file:
C:\Users\you\Projects\MyApp\MyApp.sln
```

The three output files will be created in the same folder as `main.py`.

---

## Output Files

### `All_Projects.txt`
Lists all projects that have at least one dependency or are depended on by another project. For each project:
- Name and GUID
- Framework version
- Path to `.csproj` or `.vcxproj`
- Child projects (projects that depend on it)
- Mother projects (projects it depends on)

### `Independent_Projects.txt`
Lists all projects with no dependencies and no dependents. For each project:
- Name and GUID
- Framework version
- Path

### `Tree.txt`
A hierarchical view of dependency relationships between projects. Example:

```
MyApp.Core: net6.0
		------- MyApp.Services: net6.0
		        ------- MyApp.API: net6.0
MyApp.Shared: net6.0
```

---

## Common Issues

| Error | Likely cause |
|---|---|
| `FileNotFoundError` | The path entered is incorrect, or a `.csproj` referenced in the `.sln` has been moved or deleted |
| `PermissionError` | The script does not have read access to the file — try running as administrator |
| `Could not retrieve framework` | The `.csproj` file does not contain a `<TargetFramework>` tag (older project formats) |
| Empty output files | The `.sln` has no inter-project dependencies — all projects may appear in `Independent_Projects.txt` |
