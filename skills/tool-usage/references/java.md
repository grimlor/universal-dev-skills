# Java Tool Usage Reference

Java-specific details for applying `tool-usage`.

## Recommended VS Code Extensions

| Extension | ID | Purpose |
|---|---|---|
| Extension Pack for Java | `vscjava.vscode-java-pack` | Language support, debugging, project management, test runner |
| Checkstyle for Java | `shengchen.vscode-checkstyle` | Inline Checkstyle diagnostics from project config |
| Gradle for Java | `vscjava.vscode-gradle` | Gradle task browser and execution |
| SpotBugs | (via Gradle task) | No dedicated extension; run `./gradlew spotbugsMain` |

The Extension Pack for Java bundles Red Hat's Java language support
(`redhat.java`), the Maven/Gradle project manager, the debugger, and the
test runner. It provides IntelliSense, go-to-definition, inline diagnostics,
and refactoring support — equivalent to what Pylance does for Python or the
TS language service does for TypeScript.

### Test runner integration

The Java Test Runner (bundled in the Extension Pack) discovers JUnit 5 tests
and shows inline pass/fail indicators. Use the `runTests` tool when available;
otherwise use `./gradlew test` in the terminal.

## Recommended Settings

```jsonc
{
  // Use project's Java version (from toolchain block in build.gradle.kts)
  "java.configuration.updateBuildConfiguration": "automatic",

  // Enable annotation processing (Lombok, MapStruct, etc.)
  "java.compile.nullAnalysis.mode": "automatic",

  // Checkstyle config path
  "java.checkstyle.configuration": "config/checkstyle/checkstyle.xml",

  // Format on save using the Google Java Format style
  "java.format.settings.url": "https://raw.githubusercontent.com/google/styleguide/gh-pages/eclipse-java-google-style.xml",
  "editor.formatOnSave": true,
  "[java]": {
    "editor.defaultFormatter": "redhat.java"
  },

  // Organize imports on save
  "editor.codeActionsOnSave": {
    "source.organizeImports": "explicit"
  }
}
```

**Why `updateBuildConfiguration: automatic`:** Re-imports the project
whenever `build.gradle.kts` or `pom.xml` changes, keeping the editor's
classpath in sync with the build system.

## Diagnostics vs. Build Output

Java diagnostics appear in the Problems panel from two sources:

- **Java language server** (red hat) — real-time compiler errors and
  warnings as you type. These match `javac` output.
- **Checkstyle extension** — style violations from the checkstyle config.

After completing edits, run the full quality gate in the terminal as final
verification — the Problems panel may buffer changes or miss SpotBugs
findings entirely.

```bash
./gradlew check
```

## Java Snippet Execution

For quick Java snippets, use JShell (Java 9+):

```bash
echo 'System.out.println("hello");' | jshell -
```

For multi-line snippets, write to a `.jsh` file and execute:

```bash
jshell .copilot/scripts/snippet.jsh
```

For scripts that need project dependencies, prefer writing a small test or
main method and running via Gradle:

```bash
./gradlew run
```

For scripts longer than 10 lines, follow the standard script-file fallback
from the core `tool-usage` skill: write to `.copilot/scripts/`, then execute.

## Gradle Task Execution

Always use the Gradle wrapper rather than running `gradle` directly:

```bash
# ✅ Uses the wrapper — reproducible
./gradlew test

# ❌ Global install — version may differ
gradle test
```

The Gradle extension provides a task browser in the sidebar, but terminal
execution via `./gradlew` is preferred for consistency between agent and CI.
