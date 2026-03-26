---
name: java-code-standards
description: "Checkstyle, SpotBugs, and Java compiler configuration standards for Java projects. Use when setting up a new Java project, auditing an existing project's tooling config, or applying lint/type-checking fixes. Covers Maven and Gradle configuration, static analysis, JUnit 5, and pre-commit hooks."
---

# Java Code Standards

> **Forward-looking skill.** This skill was authored before any live Java projects
> exist in the workspace. Refine canonical configs and common fix patterns when
> real project usage begins.

## When This Skill Applies

Whenever:
- Setting up tooling in a new Java project
- Auditing or updating Maven (`pom.xml`) or Gradle (`build.gradle*`) configuration
- Running Checkstyle, SpotBugs, or the compiler to find and fix issues
- Adding or updating pre-commit hooks or CI quality gates
- Applying the standard build/test/lint tasks

---

## Scope — Personal vs. Team Projects

**This standard applies in full only to projects where you control the toolchain**
(personal projects, greenfield repos, repos where you are the sole or primary
author).

### How to determine if you control the toolchain

1. **GitHub owner is `grimlor`** → personal repo → full standard applies.
2. **Forked repo** (different owner, contributor commits from `grimlor`) → apply
   the higher bar of your personal standard and the upstream's standard to your
   contributions. Don't rewrite the upstream's existing configs — the upstream
   project's conventions (checkstyle rules, test framework, build system) are
   theirs to own.
3. **Repo lives under a work org path or an ADO workspace** → team repo → follow
   team conventions for shared config, but apply the higher bar of your personal
   standard and the team's standard to your own contributions. You may not be
   able to reduce existing tech debt, but don't add to it.
4. **`pom.xml` or `build.gradle` already has a different style/analysis setup** →
   someone else owns the config; don't replace it without team agreement.
5. **`CODEOWNERS` file exists or git log shows multiple authors** → shared
   codebase; don't commit toolchain changes unilaterally.

When in doubt, ask the user which category the repo falls into before applying the
full standard.

**Important:** Do not treat configs from forked projects as canonical examples of
this standard. Forked project configs reflect the original author's choices, not
necessarily yours.

At work or in open-source contributions, team repos may follow different
conventions — and that's expected. Key differences to watch for:

- **Build system:** teams may use Maven or Gradle (Groovy or Kotlin DSL). Match
  what's configured — don't switch build systems unilaterally.
- **Style checker:** teams may use Checkstyle, PMD, or Google Java Format. Adapt
  to what's in the project.
- **Test framework:** some teams use JUnit 4 or TestNG instead of JUnit 5. Don't
  migrate test frameworks without team agreement.
- **Static analysis:** teams may use SpotBugs, Error Prone, or SonarQube. Match
  the existing setup.

In team contexts, apply what you can personally (running spotbugs locally, using
strict compiler warnings in your IDE) without imposing changes on shared config
files. Your contributed code should still meet your personal quality bar even when
the team's bar is lower.

---

## Build System

**Prefer Gradle (Kotlin DSL) for all personal projects.** Use `build.gradle.kts`,
`settings.gradle.kts`, and the Gradle wrapper (`gradlew`).

For team/open-source projects, use whatever build system is present:

| File | Build system |
|---|---|
| `pom.xml` | Maven |
| `build.gradle` | Gradle (Groovy DSL) |
| `build.gradle.kts` | Gradle (Kotlin DSL) |

Always use the wrapper (`./gradlew` or `./mvnw`) rather than a globally installed
build tool — this ensures reproducible builds and eliminates version mismatch
between developers.

---

## Java Version

**Target Java 21 (LTS) for personal projects.** Adjust to the team's minimum
when contributing to shared codebases.

```kotlin
// build.gradle.kts
java {
    toolchain {
        languageVersion.set(JavaLanguageVersion.of(21))
    }
}
```

The toolchain block ensures the project builds with the declared Java version
regardless of what JDK is installed locally.

---

## Canonical `build.gradle.kts` Configuration

```kotlin
plugins {
    java
    checkstyle
    id("com.github.spotbugs") version "6.0+"
    id("com.diffplug.spotless") version "7.0+"
    jacoco
}

group = "com.example"
version = "0.1.0"

java {
    toolchain {
        languageVersion.set(JavaLanguageVersion.of(21))
    }
}

repositories {
    mavenCentral()
}

dependencies {
    // Test
    testImplementation(platform("org.junit:junit-bom:5.11+"))
    testImplementation("org.junit.jupiter:junit-jupiter")
    testImplementation("org.assertj:assertj-core:3.26+")
    testImplementation("org.mockito:mockito-core:5.14+")
    testImplementation("org.mockito:mockito-junit-jupiter:5.14+")

    // Static analysis annotations
    compileOnly("com.github.spotbugs:spotbugs-annotations:4.8+")
}

tasks.withType<JavaCompile> {
    options.compilerArgs.addAll(listOf(
        "-Xlint:all",       // enable all compiler warnings
        "-Werror",          // treat warnings as errors
        "-parameters",      // preserve parameter names for reflection
    ))
    options.encoding = "UTF-8"
}

// --- Testing ---
tasks.test {
    useJUnitPlatform()
    finalizedBy(tasks.jacocoTestReport)
}

tasks.jacocoTestReport {
    dependsOn(tasks.test)
    reports {
        xml.required.set(true)
        html.required.set(true)
    }
}

tasks.jacocoTestCoverageVerification {
    violationRules {
        rule {
            limit {
                minimum = "1.00".toBigDecimal()
            }
        }
    }
}

tasks.check {
    dependsOn(tasks.jacocoTestCoverageVerification)
}

// --- Checkstyle ---
checkstyle {
    toolVersion = "10.20+"
    configFile = file("config/checkstyle/checkstyle.xml")
    isIgnoreFailures = false
    maxWarnings = 0
}

// --- SpotBugs ---
spotbugs {
    effort.set(com.github.spotbugs.snom.Effort.MAX)
    reportLevel.set(com.github.spotbugs.snom.Confidence.LOW)
}

// --- Spotless (formatter) ---
spotless {
    java {
        googleJavaFormat("1.24.0")
        removeUnusedImports()
        trimTrailingWhitespace()
        endWithNewline()
    }
}
```

**Coverage threshold:** 100% line coverage for personal projects. This aligns
with the `bdd-testing` skill's principle that coverage equals complete
specification. For contributed or forked projects, match the upstream's threshold.

**Why `-Werror`:** Treating warnings as errors ensures no new warnings accumulate.
The same principle as `strict: true` in TypeScript or `typeCheckingMode: strict`
in Pyright — catch problems at compile time, not in production.

---

## Canonical Checkstyle Configuration

Create `config/checkstyle/checkstyle.xml` based on the Google Java Style Guide:

```xml
<?xml version="1.0"?>
<!DOCTYPE module PUBLIC
    "-//Checkstyle//DTD Checkstyle Configuration 1.3//EN"
    "https://checkstyle.org/dtds/configuration_1_3.dtd">
<module name="Checker">
    <module name="TreeWalker">
        <!-- Google style defaults -->
        <module name="GoogleStyle"/>

        <!-- Javadoc on all public APIs -->
        <module name="MissingJavadocMethod">
            <property name="scope" value="public"/>
            <property name="allowMissingPropertyJavadoc" value="true"/>
        </module>
        <module name="MissingJavadocType">
            <property name="scope" value="public"/>
        </module>
        <module name="JavadocMethod"/>
        <module name="JavadocType"/>

        <!-- Import order: static first, then regular, alphabetized -->
        <module name="CustomImportOrder">
            <property name="sortImportsInGroupAlphabetically" value="true"/>
            <property name="separateLineBetweenGroups" value="true"/>
            <property name="customImportOrderRules"
                      value="STATIC###THIRD_PARTY_PACKAGE"/>
        </module>

        <!-- No wildcard imports -->
        <module name="AvoidStarImport"/>

        <!-- Unused imports -->
        <module name="UnusedImports"/>
    </module>

    <!-- Line length -->
    <module name="LineLength">
        <property name="max" value="100"/>
        <property name="ignorePattern" value="^package.*|^import.*|a]href|href|http://|https://|ftp://"/>
    </module>

    <!-- No tabs -->
    <module name="FileTabCharacter"/>

    <!-- Newline at end of file -->
    <module name="NewlineAtEndOfFile"/>
</module>
```

**Adapt for team projects:** If the team uses a different style guide or
Checkstyle config, use theirs. Run Checkstyle locally with your own config only
if needed, but don't commit a different config than the team uses.

---

## Javadoc Documentation Standard

All public symbols must have Javadoc — classes, interfaces, methods, and
constructors. Checkstyle's `MissingJavadocMethod` and `MissingJavadocType`
modules enforce this.

### Javadoc format

```java
/**
 * Parse a duration string into milliseconds.
 *
 * @param input human-readable duration like "5m" or "2h30m"
 * @return the duration in milliseconds
 * @throws IllegalArgumentException if the input format is unrecognized
 */
public long parseDuration(String input) {
    // ...
}
```

### Common Javadoc patterns

**Class:**
```java
/**
 * Manages retry logic with exponential backoff.
 *
 * <p>Thread-safe. Each instance maintains its own retry counter.
 */
public class RetryPolicy {
    /**
     * Create a RetryPolicy with the given configuration.
     *
     * @param maxRetries maximum number of retry attempts
     * @param baseDelayMs base delay between retries in milliseconds
     */
    public RetryPolicy(int maxRetries, long baseDelayMs) {
        // ...
    }
}
```

**Interface:**
```java
/**
 * Storage adapter for persisting application state.
 *
 * <p>Implementations must be safe for concurrent access.
 */
public interface StorageAdapter {
    /**
     * Store a value by key, overwriting any previous value.
     *
     * @param key the storage key (must not be null)
     * @param value the value to store (must not be null)
     */
    void put(String key, String value);
}
```

**Tests do not require Javadoc** — the BDD-style `@DisplayName` and nested
`@Nested` class names serve as the specification.

---

## Canonical `package.json` Scripts (Gradle Tasks)

Gradle provides the standard lifecycle tasks:

| Task | Purpose |
|---|---|
| `./gradlew build` | Compile + test + analysis (full quality gate) |
| `./gradlew test` | Run tests only |
| `./gradlew check` | Run all verification tasks (test + coverage + checkstyle + spotbugs) |
| `./gradlew jacocoTestReport` | Generate coverage report |
| `./gradlew spotlessApply` | Auto-format source code |
| `./gradlew spotlessCheck` | Verify formatting without modifying files |
| `./gradlew checkstyleMain` | Run Checkstyle on main sources |
| `./gradlew spotbugsMain` | Run SpotBugs on main sources |

The `check` task is the full quality gate — equivalent to Python's `task check`
or TypeScript's `npm run check`.

### Maven equivalents

If the project uses Maven instead of Gradle:

| Maven command | Purpose |
|---|---|
| `./mvnw verify` | Full quality gate (compile + test + analysis) |
| `./mvnw test` | Run tests only |
| `./mvnw checkstyle:check` | Run Checkstyle |
| `./mvnw spotbugs:check` | Run SpotBugs |
| `./mvnw jacoco:report` | Generate coverage report |

---

## Pre-commit Hooks

For personal Java projects, use a pre-commit hook that runs formatting and
compilation checks.

### Using pre-commit framework

```yaml
# .pre-commit-config.yaml
repos:
  - repo: local
    hooks:
      - id: spotless
        name: spotless-format
        entry: ./gradlew spotlessApply
        language: system
        pass_filenames: false
      - id: compile-check
        name: compile-check
        entry: ./gradlew classes testClasses
        language: system
        pass_filenames: false
```

Running the full `check` task in a pre-commit hook is viable for small projects
but may be too slow for large codebases. At minimum, format and compile — reserve
the full gate (`./gradlew check`) for CI or a manual pre-push check.

### Using Gradle git hooks plugin

Alternatively, use a Gradle plugin to install git hooks automatically:

```kotlin
// build.gradle.kts
plugins {
    id("com.github.jakemarsden.git-hooks") version "0.0.2"
}

gitHooks {
    preCommit {
        from("./gradlew spotlessApply classes testClasses")
    }
}
```

---

## Suppression Policy

### `@SuppressWarnings`

- Always specify the exact warning being suppressed.
- Always include a comment explaining why.
- File-level or class-level `@SuppressWarnings` is never acceptable in source
  code.

```java
// ❌ Broad suppression, no reason
@SuppressWarnings("all")

// ❌ No reason
@SuppressWarnings("unchecked")

// ✅ Specific with reason
@SuppressWarnings("unchecked") // Generic type erasure at API boundary — SDK returns raw List
List<String> items = (List<String>) sdk.getItems();
```

### SpotBugs `@SuppressFBWarnings`

Same rules — narrow scope, specific bug pattern, always include a justification:

```java
@SuppressFBWarnings(
    value = "RCN_REDUNDANT_NULLCHECK_WOULD_HAVE_BEEN_A_NPE",
    justification = "False positive — try-with-resources generates redundant null check"
)
```

---

## Common Compiler Warning Fix Patterns

When enabling `-Xlint:all -Werror`, these patterns address the most common
warnings without reaching for `@SuppressWarnings`.

### Unchecked casts

```java
// ❌ Warning: unchecked cast
Map<String, Object> map = (Map<String, Object>) rawObject;

// ✅ Verify type at runtime
if (rawObject instanceof Map<?, ?> rawMap) {
    // Java 21 pattern matching
    @SuppressWarnings("unchecked") // verified via instanceof above
    Map<String, Object> map = (Map<String, Object>) rawMap;
}
```

### Raw types

```java
// ❌ Warning: raw type
List items = new ArrayList();

// ✅ Parameterized type
List<String> items = new ArrayList<>();
```

### Resource leak

```java
// ❌ Warning: resource leak
InputStream is = new FileInputStream("data.txt");
// ... no close

// ✅ Try-with-resources
try (InputStream is = new FileInputStream("data.txt")) {
    // ...
}
```

### Deprecated API usage

```java
// ❌ Warning: deprecated API
Date date = new Date(2024, 1, 1);

// ✅ Modern API
LocalDate date = LocalDate.of(2024, 1, 1);
```

### Null safety (with Optional)

```java
// ❌ Null return that callers must check
public String findName(int id) {
    return map.get(id); // may return null
}

// ✅ Explicit Optional signals absence
public Optional<String> findName(int id) {
    return Optional.ofNullable(map.get(id));
}
```

### Record types (Java 16+)

```java
// ❌ Boilerplate POJO
public class Config {
    private final String apiUrl;
    private final int timeout;
    // constructor, getters, equals, hashCode, toString...
}

// ✅ Record — immutable by default, no boilerplate
public record Config(String apiUrl, int timeout) {}
```

---

## Dev Dependencies

Standard dependencies for a new Java project (Gradle Kotlin DSL):

```kotlin
dependencies {
    // Test framework
    testImplementation(platform("org.junit:junit-bom:5.11+"))
    testImplementation("org.junit.jupiter:junit-jupiter")

    // Fluent assertions
    testImplementation("org.assertj:assertj-core:3.26+")

    // Mocking
    testImplementation("org.mockito:mockito-core:5.14+")
    testImplementation("org.mockito:mockito-junit-jupiter:5.14+")

    // Static analysis annotations
    compileOnly("com.github.spotbugs:spotbugs-annotations:4.8+")
}
```

---

## Workflow for Applying Standards to an Existing Project

**For personal projects:** apply the full standard below.
**For team projects:** see [Scope](#scope--personal-vs-team-projects) first — only
apply what the team has agreed to, or what doesn't affect shared config.

1. **Set up `build.gradle.kts`** — add Java toolchain, Checkstyle, SpotBugs,
   Spotless, and JaCoCo plugins per the canonical config.

2. **Create Checkstyle config** — place `config/checkstyle/checkstyle.xml` with
   the canonical Google-based config.

3. **Configure JUnit 5** — ensure `useJUnitPlatform()` in the test task and
   `junit-bom` platform dependency.

4. **Set compiler warnings** — add `-Xlint:all -Werror -parameters` to
   `JavaCompile` tasks.

5. **Run formatter:** `./gradlew spotlessApply`

6. **Run analysis with auto-fix where possible:** `./gradlew check`

7. **Fix remaining issues manually** — Checkstyle and SpotBugs reports include
   file + line. Common unfixable: missing Javadoc, unchecked casts at API
   boundaries.

8. **Verify clean:** `./gradlew check` should pass with no warnings.

9. **Set up pre-commit hooks** — configure pre-commit or Gradle git hooks plugin.

10. **Commit:** `chore(build): add Checkstyle, SpotBugs, and strict compiler warnings`
