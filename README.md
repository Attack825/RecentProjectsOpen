# Flow.Launcher.Plugin.RecentProjectsOpen

A Flow Launcher plugin for quickly reopening recent projects in IDEs and editors such as VSCode, IntelliJ IDEA, PyCharm, and Typora.

## Installation

Install from the plugin store (or download a release from GitHub).

> **Requirements**
>
> - Flow Launcher 2.1.3 or newer (Windows only).
> - A **Python 3.9 – 3.13** interpreter configured in Flow Launcher
>   (Flow Settings → Python Path).
>
> The release package bundles every runtime dependency under `lib/` as pure
> Python, so nothing has to be installed with `pip` inside the plugin folder.
> Since 1.4.0 fuzzy matching uses the standard library, so the old
> "install Levenshtein" workaround is no longer needed.

## Supported programs

- [x] visual studio code
- [x] pycharm
- [x] clion
- [x] goland
- [x] intellij idea
- [x] android studio
- [x] cursor
- [x] sumatra pdf
- [x] trae
- [x] vscode ssh
- [x] typora

You can access different programs using the following acronyms:

```json
{
    "vsc": "VSCODE",
    "py": "PYCHARM",
    "cl": "CLION",
    "go": "GOLAND",
    "idea": "INTELLIJ_IDEA",
    "as": "ANDROID_STUDIO",
    "cur": "CURSOR",
    "pdf": "SUMATRA",
    "trae": "TRAE",
    "vscs": "VSCODE_SSH",
    "ty": "TYPORA"
}
```

## Configuration

All configurations can be done in the Settings Panel. Change the configurations as needed and they will be applied immediately.

### Program Path

- Configure program paths in the following format:

  ```plaintext
  APP_DOWNLOAD=C:/path/to/app.exe
  APP_STORAGE=C:/path/to/storage/file
  ```

- Each program needs both DOWNLOAD and STORAGE entries, where `APP` is the
  registration name from [Supported programs](#supported-programs)
  (e.g. `VSCODE`, `INTELLIJ_IDEA`, `TYPORA`)
- Example configuration (excerpt — add the apps you actually use):

  ```plaintext
  VSCODE_DOWNLOAD=D:/VSCode/bin/code
  VSCODE_STORAGE=C:/Users/YourUsername/AppData/Roaming/Code/User/globalStorage/storage.json
  ANDROID_STUDIO_DOWNLOAD=D:/Android Studio/bin/studio64.exe
  ANDROID_STUDIO_STORAGE=C:/Users/YourUsername/AppData/Roaming/Google/AndroidStudio2024.1/options/recentProjects.xml
  INTELLIJ_IDEA_DOWNLOAD=D:/IntelliJ IDEA 2024.3/bin/idea64.exe
  INTELLIJ_IDEA_STORAGE=C:/Users/YourUsername/AppData/Roaming/JetBrains/IntelliJIdea2024.3/options/recentProjects.xml
  GOLAND_DOWNLOAD=D:/goland/GoLand 2023.2/bin/goland64.exe
  GOLAND_STORAGE=C:/Users/YourUsername/AppData/Roaming/JetBrains/GoLand2023.2/options/recentProjects.xml
  CLION_DOWNLOAD=D:/Clion/CLion 2024.1.4/bin/clion64.exe
  CLION_STORAGE=C:/Users/YourUsername/AppData/Roaming/JetBrains/CLion2024.1/options/recentProjects.xml
  CURSOR_DOWNLOAD=C:/Users/YourUsername/AppData/Local/Programs/cursor/Cursor.exe
  CURSOR_STORAGE=C:/Users/YourUsername/AppData/Roaming/Cursor/globalStorage/storage.json
  TYPORA_DOWNLOAD=D:/Typora/Typora.exe
  TYPORA_STORAGE=C:/Users/YourUsername/AppData/Roaming/Typora/history.data
  ```

### Suggestions List

- You can customize the program suggestions list displayed when no input is provided.
- Configure program suggestions list in the following format:

  ```plaintext
  VSCODE
  PYCHARM
  INTELLIJ_IDEA
  # ... other programs
  ```

- Keep empty to display the default program suggestions list — the plugin will suggest the programs that are configured in the [Program Path](#program-path).

### Plugin Trigger Keyword

- Make sure to update this configuration when you change the trigger keyword of this plugin.
- It affects the usage of [Suggestions List](#suggestions-list).

### Custom Acronyms Map

- Configure custom acronyms for your programs in the following format:

  ```plaintext
  VSCODE=vs
  PYCHARM=pc
  # ... other acronyms map
  ```

- This allows you to use custom acronyms when the [default acronyms](#supported-programs) do not match your preferences.

### Tips

- **Verify Paths**: Ensure that the paths you enter are correct and that the files or executables exist at those locations
- **Permissions**: Make sure that Flow Launcher has the necessary permissions to access the specified directories and files
- **Path Format**: Use forward slashes (`/`) or double backslashes (`\\`) in Windows paths

## Usage

To open a project named "MyProject" in Visual Studio Code, you would use:

`r`

![Suggestions list shown when typing r](image/README/1752128883045.png)

`r vsc`

![Configured applications after typing r vsc](image/README/1733284352742.png)

`r vsc My`

![Filtered projects after typing r vsc My](image/README/1733284374591.png)

`r vsc 空`

![Pinyin search after typing r vsc 空](image/README/1733284760505.png)

`context menu`

![Context menu with copy path and open in explorer](image/README/1742873448581.png)

## Features

- [x] fuzzy search (prefix / substring / similarity, stdlib only)
- [x] support pinyin
- [x] prevent configurations from disappearing after updates
- [x] open in file explorer and copy absolute path

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for development setup, how to add a new
application, and the checks that run in CI.
