# Modlist Scanner for Minecraft

A Python tool to scan Minecraft mod directories and generate a clean JSON list of mods with their IDs, names, and versions.

[![Python Version](https://img.shields.io/badge/Python-3.7%2B-blue)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## Features

- 🧩 Supports all major mod loaders: Forge, NeoForge, Fabric, and Quilt
- 🔍 Recursively scans directories for mod files
- 🧹 Cleans mod names and versions by removing special characters
- 💾 Outputs clean JSON with modid, name, and version
- 🛡️ Handles special characters and non-standard JAR files
- 📋 Detailed reporting of processed and skipped files

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yangyang8002/Modlist-for-Minecraft.git
cd Modlist-for-Minecraft
```

2. Ensure you have Python 3.6 or newer installed.

## Usage

### Basic Usage
Run the script and follow the prompts:
```bash
python mod_scanner.py
```

### Command Line Options
Run with a specific directory path:
```bash
python mod_scanner.py --directory "path/to/your/mods"
```

Silent mode (only errors and final result):
```bash
python mod_scanner.py --quiet
```

Specify output file:
```bash
python mod_scanner.py --output custom_mods.json
```

### Example Output
The script will generate a `mods.json` file with the following structure:
```json
[
  {
    "modid": "jei",
    "name": "Just Enough Items",
    "version": "11.2.0.256"
  },
  {
    "modid": "lazydfu",
    "name": "LazyDFU",
    "version": "0.1.3"
  }
]
```

## Supported File Types
The scanner will process files with these extensions:
- `.jar` (standard mod files)
- `.zip` (some mods use zip format)
- `.disabled` (disabled mods)

## How It Works
The scanner:
1. Recursively searches the specified directory
2. Opens each mod file as a ZIP archive
3. Looks for mod metadata files in this order:
   - `fabric.mod.json` (Fabric/Quilt mods)
   - `mods.toml` (Forge/NeoForge mods)
   - `mcmod.info` (older Forge mods)
4. If metadata is not found, extracts information from the filename
5. Cleans the data by removing special characters like `#mandatory` and `\`
6. Outputs the results to a JSON file

## Troubleshooting

### Known Problems
1.  Please batch-replace both the word “#mandatory” and the backslash “\” with nothing (i.e., delete them).

### Common Issues
1. **Permission errors**: Run the script as administrator/root if scanning protected directories
2. **Corrupted mod files**: Try re-downloading any mods that cause errors
3. **Special characters**: The script handles most special characters, but extremely malformed filenames might cause issues

### Reporting Problems
If you encounter any issues, please:
1. Run the script with the `--debug` flag
2. Note which mod file caused the problem
3. [Open an issue](https://github.com/yangyang8002/Modlist-for-Minecraft/issues) with this information

## Contributing
Contributions are welcome! Please follow these steps:
1. Fork the repository
2. Create a new branch for your feature
3. Commit your changes
4. Submit a pull request

## License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

**Note**: This tool is not affiliated with Minecraft, Mojang, or Microsoft. Minecraft is a trademark of Mojang Studios.
