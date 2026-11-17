
# eSim AutoTool Manager

## 1. Project Overview

eSim AutoTool Manager is a Python command-line application developed to manage external Electronic Design Automation (EDA) tools used in an eSim workflow.

The application helps users detect installed tools, check dependencies, configure executable paths, check software updates and manage installation through supported package managers.

## 2. Features

1. **Tool Detection:** Detects Ngspice and KiCad and displays their installation status, version and executable path.
2. **Tool Installation:** Provides an installation menu and supports KiCad installation through Windows Package Manager (winget).
3. **Update Manager:** Checks available updates and provides an update option for supported packages.
4. **Configuration Manager:** Allows users to save custom executable paths.
5. **Dependency Checker:** Checks Python version, operating system, package manager and supported EDA tools.
6. **Logging:** Records important application activities in `logs/manager.log`.
7. **Configuration Display:** Displays saved configuration settings.

## 3. Technologies Used

- Python 3.10+
- Windows 11
- Visual Studio Code
- Python standard library
- Windows Package Manager (winget)
- APT package manager for supported Linux distributions
- JSON for configuration storage

## 4. System Requirements

- Windows 10/11 or supported Ubuntu/Debian Linux
- Python 3.10 or newer
- winget on Windows or apt on supported Linux distributions
- Internet connection for package installation and update checks

No third-party Python packages are required.

## 5. Installation and Execution

Open PowerShell and navigate to the project directory:

```powershell
cd "C:\Users\DELL\Downloads\eSim_AutoTool_Manager\eSim_AutoTool_Manager"
```

Check Python:

```powershell
python --version
```

Run the application:

```powershell
python main.py
```

## 6. Main Menu

The application provides these options:

1. View installed tools and versions
2. Install a tool
3. Check for updates / update a tool
4. Configure tool paths
5. Check dependencies
6. View saved configuration
0. Exit

## 7. Project Structure

```text
eSim_AutoTool_Manager/
|
|-- main.py
|-- requirements.txt
|
|-- core/
|   |-- __init__.py
|   |-- installer.py
|   |-- updater.py
|   |-- config_manager.py
|   |-- dependency_checker.py
|   |-- tool_detector.py
|   |-- logger.py
|
|-- config/
|   |-- settings.json
|
|-- logs/
|   |-- manager.log
|
|-- docs/
    |-- DESIGN_DOCUMENT.md
```

## 8. Testing

The following tests were performed on Windows 11:

| Test | Result |
|---|---|
| Python version detection | Passed |
| KiCad detection | Passed |
| KiCad version detection | Passed |
| Installation menu | Passed |
| Already-installed tool check | Passed |
| Update checking | Passed |
| Custom executable path saving | Passed |
| Dependency checking | Passed |
| Configuration display | Passed |
| Log file creation | Passed |

KiCad 10.0.8 was detected successfully.

## 9. Limitations

- Ngspice Windows automatic installation is not configured because a verified package ID is not available in the current implementation.
- Ngspice update checking is not configured on Windows.
- Linux package-manager support is intended for apt-based distributions and requires further platform testing.
- Update availability depends on package-manager results.
- The application is a prototype and is not an official eSim installer.

## 10. Future Scope

- Add verified Ngspice installation support.
- Add macOS and Homebrew support.
- Develop a graphical user interface.
- Improve version comparison and update reporting.
- Add automated testing.
- Integrate with eSim configuration files.

## 11. Conclusion

The eSim AutoTool Manager prototype demonstrates how Python can simplify EDA tool detection, configuration, dependency checking and update management through a command-line interface.
