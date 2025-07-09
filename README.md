# Flow.Launcher.Plugin.RecentProjectsOpen

A plugin that enables quick access to recent projects across various IDEs like VSCode and PDF readers efficiency.

## Installation

Download from the store

## Supported applications

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

You can access different IDEs using the following format:

```python
{
    "vsc": "VSCODE",
    "py": "PYCHARM",
    "cl": "CLION",
    "go": "GOLAND",
    "idea": "INTELLIJ_IDEA",
    "as": "ANDROID_STUDIO",
    "cur":"CURSOR",
    "pdf":"SUMATRA_PDF",
    "trae":"TRAE",
    "vscs":"VSCODE_SSH",
    "ty": "TYPORA",
}
```

## Configuration

All configurations can be done in the Settings Panel. Change the configurations as needed and they will be applied immediately.

### Program Path

- Configure application paths in the following format:

   ```plaintext
   APP_DOWNLOAD=C:/path/to/app.exe
   APP_STORAGE=C:/path/to/storage/file
   ```

- Each application needs both DOWNLOAD and STORAGE entries
- Example configuration:

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

### Tips

- **Verify Paths**: Ensure that the paths you enter are correct and that the files or executables exist at those locations
- **Permissions**: Make sure that Flow Launcher has the necessary permissions to access the specified directories and files
- **Path Format**: Use forward slashes (`/`) or double backslashes (`\\`) in Windows paths

## Usage

To open a project named "MyProject" in Visual Studio Code, you would use:

r vsc

![1733284352742](image/README/1733284352742.png)

r vsc My

![1733284374591](image/README/1733284374591.png)

r vsc 空

![1733284760505](image/README/1733284760505.png)

context menu

![1742873448581](image/README/1742873448581.png)

## Feature

- [x] fuzzy search
- [x] support pinyin
- [x] prevent configurations from disappearing after updates
- [x] open in file explorer and copy absolute path

## Contribute

1. Create a new file in `src/application` directory (e.g., `myapp.py`)
2. Implement your application class by extending `BaseApplication` or `BaseJetBrains`
3. Register your application using the `@ApplicationRegistry.register` decorator
4. Use pre commit to check and format code
