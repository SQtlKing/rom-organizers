# PS1 ROM Organizer

A Python utility for organizing PlayStation 1 ROMs into a consistent directory structure and generating `.m3u` playlists for emulator use.

This tool normalizes both single-disc and multi-disc games, correctly resolves `.cue` dependencies, and produces emulator-ready `.m3u` files as the primary entry point.

---

## Features

- Supports common PS1 formats:
  - `.chd`
  - `.cue` (including multi-track audio)
  - `.ccd`, `.toc` (entry-point handling)
- Handles single-disc and multi-disc games uniformly
- Generates `.m3u` playlists for **all games**
- Resolves `.cue` references relative to their original location
- Recursively scans subdirectories
- Requires no hardcoded paths or configuration files

---

## Resulting Directory Structure

After running the script, your ROM directory will look like this:

```text
roms/
├── Final Fantasy VII.m3u
├── Chrono Cross (USA).m3u
├── JoJo's Bizarre Adventure.m3u
└── multi/
    ├── Final Fantasy VII/
    │   ├── Final Fantasy VII (Disc 1).cue
    │   ├── Final Fantasy VII (Disc 1).bin
    │   ├── Final Fantasy VII (Disc 2).cue
    │   └── Final Fantasy VII (Disc 2).bin
    ├── Chrono Cross (USA)/
    │   └── Chrono Cross (USA).chd
    └── JoJo's Bizarre Adventure/
        └── JoJo's Bizarre Adventure.chd
```

Each `.m3u` file contains relative paths pointing into `multi/<Game>/`.

---

## Requirements

- Python 3.10 or newer
- No third-party dependencies

---

## Usage

Run the script with the ROM directory as an argument:

```text
python ps1_rom_organizer.py <roms_directory>
```

Example (Windows):

```text
python ps1_rom_organizer.py "C:\Users\Joshua Lucas\PS1\roms"
```

You can copy and paste the directory path directly from File Explorer.

---

## What the Script Does

1. Recursively scans the provided directory
2. Identifies PS1 disc entry files (`.chd`, `.cue`, etc.)
3. Normalizes game titles by removing `(Disc N)` suffixes
4. Groups files by game
5. Moves disc files into `multi/<Game>/`
6. Parses `.cue` files and moves referenced files (`.bin`, audio tracks)
7. Writes one `.m3u` file per game in the root directory

---

## Important Notes

- `.cue` files are not modified
- Referenced files are moved without guessing or global searching
- `.m3u` files reference `.cue` files, not `.bin` files
- Missing referenced files are reported as warnings

---

## Limitations and Future Work

- Disc order in `.m3u` files follows filesystem order
- `.ccd/.img/.sub` dependency resolution not yet implemented
- No dry-run mode (currently destructive by design)
- Logging is printed to stdout only

These limitations are intentional and can be addressed incrementally.

---

## Disclaimer

This tool **moves files**.

Use it on a backup or test directory first.
