# Changelog

## [0.0.5]
- Removed hardware-specific RU information from the metamodel (`model` and `capabilities` fields).
- Restricted RU `type` to `real` or `simulated`.

## [0.0.4]
- Added `taiList` to the SMF configuration.
- Generated the API reference documentation.
- Fixed docstring formatting issues.

## [0.0.3]
- Fixed CU, DU, CU-UP, and CU-CP IDs for FlexRIC compatibility.

## [0.0.2]
- Froze Python dependencies.
- Ensured RU is unset for COTS UEs.
- Ensured E2 is configured when a RIC is referenced.

## [0.0.1]
- Fixed K and OPC lengths from 16 to 32.
- Added explicit CU-UP references in DU configuration.
- Fixed typos.
