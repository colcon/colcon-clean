# colcon-clean

[![GitHub Workflow Status](https://github.com/ruffsl/colcon-clean/actions/workflows/test.yml/badge.svg)](https://github.com/ruffsl/colcon-clean/actions/workflows/test.yml)
[![Codecov](https://codecov.io/gh/ruffsl/colcon-clean/branch/master/graph/badge.svg)](https://codecov.io/gh/ruffsl/colcon-clean)

An extension for [colcon-core](https://github.com/colcon/colcon-core) to clean package workspaces. Enables cleaning of various colcon paths, such as build or install folders, for either the entire workspace or for selected packages with advanced path globing options. In conjunction with [colcon-package-selection](https://github.com/colcon/colcon-package-selection), this extension can help maintain hygienic build environments while leveraging persistent workspaces for caching by allowing users to finely remove stale artifacts, preserving what can be cached during software development. For example, when pulling various changes into a local workspace to review pull requests, this extension can be used to wipe only the build and install paths for affected packages, ensuring subsequent builds are not cross contaminated from previous jobs.

The extension works by providing a convenient wrapper around filesystem deletion, allowing users to specify at which base paths to be cleaned (`build`, `install`, `log`, `test_result`), at what level cleaning should take place (global workspace or per package), and if specified what exact files should (or should not) be removed.


## Quick start

Setup, build and test an example colcon workspace:
```
mkdir -p ~/ws/src && cd ~/ws
wget https://raw.githubusercontent.com/colcon/colcon.readthedocs.org/main/colcon.repos
vcs import src < colcon.repos
colcon build
colcon test
```

Clean build and install paths for select packages:
```
colcon clean packages \
    --base-select \
        build \
        install \
    --packages-select \
        colcon-cmake \
        colcon-package-information
```

Clean gcov count data files for entire workspace:
```
colcon clean workspace \
    --base-select \
        build \
    --clean-match \
      "*.gcda"
```


## Subverbs

### `workspace` - Clean paths for workspace

The `workspace` subverb provides a means to globally clean the top level base paths for the entire workspace.

### `packages` - Clean paths for packages

The `packages` subverb provides a means to locally clean the package level base paths using package selection.


## Clean subverb arguments

By default, this extension will provide an interactive confirmation prompt with a printout of files to be deleted. This dialogue can be automatically skipped; these deletion events can still be observed via the command's resulting colcon log file.

- `-y`, `--yes`
  - Automatic yes to prompts

### Base handler arguments

Additional arguments supported by all subverbs provide the option to select which base paths to clean, where they may be relocated:

- `--base-select`
  - Select base names to clean in workspace (default: [build, install, log, test_result])
- `--build-base`
  - The base path for all build directories (default: build)
- `--install-base`
  - The base path for all install directories (default: install)
- `--log-base`
  - The base path for all log directories (default: log)
- `--test-result-base`
  - The base path for all test_result directories (default: build)

### Clean filter arguments

Specify what files and directories to include. All files and directories (including symbolic links) are included by default. The --clean-match/--clean-ignore arguments allows for selection using glob/wildcard (".gitignore style") path matching. Paths relative to the root `directory` (i.e. excluding the name of the root directory itself) are matched against the provided patterns. For example, to only include Gcov Data files, use: `colcon clean workspace --clean-match "*.gcda"` or to exclude hidden files and directories use: `colcon clean workspace --clean-ignore ".*" ".*/"` which is short for `colcon clean workspace --clean-match "*" "!.*" "!.*/"`.

- `--clean-match`
  - One or several patterns for paths to include. NOTE: patterns with an asterisk must be in quotes ("*") or the asterisk preceded by an escape character (\*).
- `--clean-ignore`
  - One or several patterns for paths to exclude. NOTE: patterns with an asterisk must be in quotes ("*") or the asterisk preceded by an escape character (\*).
- `--clean-no-linked-dirs`
  - Do not include symbolic links to other directories.
- `--clean-no-linked-files`
  - Do not include symbolic links to files.


## Extension points

This extension makes use of a number of colcon-core extension points for registering verbs, subverbs with colcon CLI. This extension also provides it's own extension points to support additional cleaning strategies.

### `BaseHandlerExtensionPoint`

This extension point determines the types of base paths that may be selected for cleaning. Default base handler extensions provided include:

- `build`
  - Note: by default this extension does not follow symlinks
- `install`
  - Note: by default this extension does not follow symlinks
- `log`
  - Note: logs are stored by time, so package selection is not applicable
- `test_result`
  - Note: by default colcon uses `build` path to store test results
