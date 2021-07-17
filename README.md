# colcon-clean

[![GitHub Workflow Status](https://github.com/ruffsl/colcon-clean/actions/workflows/test.yml/badge.svg)](https://github.com/ruffsl/colcon-clean/actions/workflows/test.yml)
[![Codecov](https://codecov.io/gh/ruffsl/colcon-clean/branch/master/graph/badge.svg)](https://codecov.io/gh/ruffsl/colcon-clean)

An extension for [colcon-core](https://github.com/colcon/colcon-core) to clean package workspaces. Enables cleaning of various colcon paths, such as build or install folders, for either the entire workspace or for selected perpackge with advanced path globing options. In conjunction with [colcon-package-selection](https://github.com/colcon/colcon-package-selection), this extension can help maintin a higenic builds when leveraging persistent workpsaces for caching by allowing users to finely remove stale artifacts while preserving what can be cached for during software development. For example, when pulling various changes into a local workspace to review pull requests, this extension can be used to wipe only build and install paths for modified or effected packages, ensuring subsqent build are not cross contaminated from previous jobs.

The extension works by generating lockfiles that incorporate the respective state of package source files, either directly via hashing source directories or indirectly via detected revision control. Upon successful task completion for a package job, as when evoking colcon verbs like build, test, etc, these lockfiles are updated for the evoked verb, thereby delineating the provenance of the job’s results. For package selection, these lockfiles are then used to assess whether a verb’s cached outcome for a package remains relevant or valid.


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

Clean build and install paths for entire workspace:
```
colcon clean workspace \
    --base-select \
        build \
        install
```


## Subverbs

### `workspace` - Clean paths for workspace

The `workspace` subverb 
...

- `--build-base`
  - The base path for all build directories (default: build)
- `--ignore-dependencies`
  - Ignore dependencies when capturing caches (default: false)

### `packages` - Clean paths for packages

The `packages` subverb 
...
Package Selection

- `--build-base`
  - The base path for all build directories (default: build)
- `--ignore-dependencies`
  - Ignore dependencies when capturing caches (default: false)


## Clean subverb arguments

- `-y`, `--yes`
  - Automatic yes to prompts

### Base handler arguments

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

This extension makes use of a number of colcon-core extension points for registering verbs, subverbs with colcon CLI. This extension also provides it's own extension points for additional support for further cleaning strategies.

### `BaseHandlerExtensionPoint`

This extension point determines 
...
. Default base handler extensions provided include:

- `build`
  - Do not propagate lockfile, as `lock` subverb handles this explicitly
- `install`
  - Do not propagate lockfile, using `cache` lockfile as a reference
- `log`
  - Propagate lockfile, using `cache` lockfile as a reference
- `test_result`
  - Propagate lockfile, using `build` lockfile as a reference
