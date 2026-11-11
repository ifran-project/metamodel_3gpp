# Changelog

All notable changes to this project are documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [0.0.6] - 2026-11-11

### Changed
- Migrated the codebase to GitHub as `metamodel_3gpp`.

## [0.0.5] - 2026-11-02

### Changed
- **Breaking:** RU `type` is now restricted to `real` or `simulated`.

### Removed
- **Breaking:** Hardware-specific RU information (`model` and `capabilities` fields) from the metamodel.

## [0.0.4] - 2026-10-26

### Added
- `taiList` to the SMF configuration.
- Generated API reference documentation.

### Fixed
- Docstring formatting issues.

## [0.0.3] - 2026-10-03

### Fixed
- CU, DU, CU-UP and CU-CP IDs for FlexRIC compatibility.

## [0.0.2] - 2026-09-30

### Changed
- Froze Python dependency versions.

### Fixed
- RU is now unset for COTS UEs.
- E2 is now configured whenever a RIC is referenced.

## [0.0.1] - 2026-09-27

### Added
- Explicit CU-UP references in the DU configuration.

### Fixed
- K and OPC lengths (from 16 to 32).
- Typos.

[Unreleased]: https://github.com/ifran-project/metamodel_3gpp/compare/v0.0.6...HEAD
[0.0.6]: https://github.com/ifran-project/metamodel_3gpp/compare/v0.0.5...v0.0.6
[0.0.5]: https://github.com/ifran-project/metamodel_3gpp/compare/v0.0.4...v0.0.5
[0.0.4]: https://github.com/ifran-project/metamodel_3gpp/compare/v0.0.3...v0.0.4
[0.0.3]: https://github.com/ifran-project/metamodel_3gpp/compare/v0.0.2...v0.0.3
[0.0.2]: https://github.com/ifran-project/metamodel_3gpp/compare/v0.0.1...v0.0.2
[0.0.1]: https://github.com/ifran-project/metamodel_3gpp/releases/tag/v0.0.1
