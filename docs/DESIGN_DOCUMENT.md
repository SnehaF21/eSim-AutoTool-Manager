
# DESIGN DOCUMENT
# eSim AutoTool Manager

## 1. Introduction

eSim AutoTool Manager is a Python-based command-line application designed to simplify the management of external Electronic Design Automation (EDA) tools used in the eSim workflow.

It provides a common interface to detect installed software, configure executable paths, check dependencies, manage supported installations and check for updates.

## 2. Objectives

- Detect installed EDA tools.
- Display software versions and executable paths.
- Simplify supported software installation.
- Check for available software updates.
- Configure custom executable paths.
- Verify system dependencies.
- Maintain activity logs.

## 3. Scope

The prototype manages two EDA tools:

1. Ngspice
2. KiCad

It supports Windows using winget and provides an APT-based implementation for supported Linux distributions.

The current Windows implementation has verified KiCad package-manager integration. Ngspice Windows installation and update integration remain future work.

## 4. System Architecture

The application follows a modular architecture.

### 4.1 Main Module

`main.py`

- Displays the main menu.
- Accepts user input.
- Calls the required modules.
- Controls application flow.

### 4.2 Tool Detector

`core/tool_detector.py`

- Maintains the tool catalogue.
- Detects installed software.
- Finds executable paths.
- Reads software versions.

### 4.3 Installer

`core/installer.py`

- Provides installation options.
- Checks whether a tool is already installed.
- Uses supported package managers.
- Requests user confirmation before installation.

### 4.4 Updater

`core/updater.py`

- Checks for available software updates.
- Displays update information.
- Executes supported update commands after confirmation through the application menu.

### 4.5 Configuration Manager

`core/config_manager.py`

- Loads configuration from JSON.
- Saves custom executable paths.
- Displays saved settings.

### 4.6 Dependency Checker

`core/dependency_checker.py`

- Checks Python version.
- Identifies the operating system.
- Checks package-manager availability.
- Checks EDA tool availability.

### 4.7 Logger

`core/logger.py`

- Records application activities.
- Stores logs in `logs/manager.log`.
- Helps identify errors and review operations.

## 5. Technologies Used

- Python 3.10+
- Windows 11
- Visual Studio Code
- Python standard library
- Windows Package Manager
- APT package manager
- JSON configuration files

## 6. Working Flow

1. User starts the application.
2. The main menu is displayed.
3. User selects an operation.
4. The main module calls the required core module.
5. The selected module performs its operation.
6. User confirmation is requested before supported installation or update actions.
7. Results are displayed.
8. Important activities are recorded in the log file.

## 7. Configuration Management

Configuration is stored in:

`config/settings.json`

Example:

```json
{
    "tool_paths": {
        "2": "C:\\Program Files\\KiCad\\10.0\\bin\\kicad-cli.exe"
    },
    "preferences": {
        "package_manager": "auto"
    }
}
```

This allows the application to use custom executable paths during tool detection.

## 8. Logging

The application stores logs in:

`logs/manager.log`

Example log entry:

```text
2026-11-17 | INFO | Checked updates for KiCad: No upgrade reported.
```

Logs help track application operations and troubleshooting information.

## 9. Security and Reliability

- Commands are passed as argument lists to subprocess.
- Installation requires explicit user confirmation.
- Update execution requires confirmation through the menu.
- Custom executable paths are stored in a configuration file.
- Already-installed tools are not unnecessarily reinstalled.

## 10. Testing

The application was tested on Windows 11 with Python 3.13.2.

KiCad 10.0.8 was detected successfully.

The following functions were tested:

- Tool detection
- Installation menu
- Already-installed software detection
- Update checking
- Configuration saving
- Dependency checking
- Configuration display
- Log generation

## 11. Limitations

- Ngspice automatic installation and update support on Windows are not configured.
- Linux support is limited to apt-based distributions and requires additional testing.
- Package-manager results depend on the available software sources.
- The project is a command-line prototype.

## 12. Future Enhancements

- Add verified Ngspice package integration.
- Support additional operating systems.
- Develop a graphical user interface.
- Add automated testing.
- Improve update detection.
- Integrate more deeply with eSim.

## 13. Conclusion

The eSim AutoTool Manager demonstrates a modular approach to managing EDA software using Python. It provides tool detection, configuration, dependency checking, update checking and logging through a simple command-line interface.
