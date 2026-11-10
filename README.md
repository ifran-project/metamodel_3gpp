# 3GPP-based 5G/6G Metamodel

<p align="center">
  <a href="(https://pypi.python.org/pypi/metamodel_3gpp">
    <img src="https://img.shields.io/pypi/v/metamodel_3gpp.svg" alt="Latest PyPi version" />
  </a>
  <a href="https://github.com/ifran-project/metamodel_3gpp/blob/main/LICENSE">
    <img src="https://img.shields.io/badge/License-BSD--3--Clause--Clear-blue.svg" alt="BSD 3-Clause Clear license" />
  </a>
  <a href="https://www.codefactor.io/repository/github/ifran-project/metamodel_3gpp">
    <img src="https://www.codefactor.io/repository/github/ifran-project/metamodel_3gpp/badge" alt="CodeFactor" />
  </a>
  <a href="https://github.com/ifran-project/metamodel_3gpp/releases">
    <img src="https://img.shields.io/github/v/release/ifran-project/metamodel_3gpp?color=orange" alt="Latest release" />
  </a>
  <a href="https://github.com/ifran-project/metamodel_3gpp/pulls">
    <img src="https://img.shields.io/badge/PRs-Welcome-brightgreen" alt="Pull requests welcome" />
  </a>
</p>

`metamodel_3gpp` is a [Pydantic](https://pydantic.dev/docs/validation/dev/get-started/)-based, implementation-agnostic model of 5G/6G mobile networks built around [3GPP](https://www.3gpp.org/) concepts.

It describes network topology, services, and deployment configuration independently of any implementation, orchestrator, or vendor. This shared representation supports experiments, testbeds, simulations, and reproducible deployments across different environments.

## Key concepts

The metamodel separates the **logical description of a network** from the details of how a particular implementation deploys it. It provides typed, validation-friendly models that are easy to serialize and extend.

The main models are:

| Model | Description |
| --- | --- |
| `MetaModel` | Aggregates the complete network description |
| `Core` | 5G/6G core network functions and their configuration |
| `RAN` | Radio access network components |
| `RIC` | RAN Intelligent Controller topology |
| `RU` | Radio unit configuration |
| `Slice` | Network slices and their DNNs |
| `UE` | UE subscriptions and sessions |

## Installation

Install the package from [PyPI](https://pypi.org):

```bash
pip install metamodel_3gpp
```

Or install the latest source from [GitHub](https://github.com/ifran-project/metamodel_3gpp):

```bash
git clone https://github.com/ifran-project/metamodel_3gpp.git
cd metamodel_3gpp
pip install -e .
```

## Quick start

Create a network using the default topology:

```python
from metamodel_3gpp import MetaModel

network = MetaModel()

# Export as JSON-compatible data or YAML
print(network.model_dump(mode="json"))
print(network.to_yaml())
```

The default topology includes:

- A 5G core with `amf`, `ausf`, `bsf`, `nssf`, `nrf`, `pcf`, `smf`, `upf`, `udm`, and `udr`
- One RAN gNB
- One simulated radio unit (`sim_ru`)
- One UE (`sim_ue`)
- One network slice (`internet`)
- One RIC instance (`ric`)

## Custom networks

Build a network from a YAML configuration with `MetaModel.from_yaml()`:

```python
from metamodel_3gpp import MetaModel

network = MetaModel.from_yaml_file("network.yaml")

print(network.to_yaml(exclude_defaults=False))
```

A network configuration is organized around these top-level sections:

```yaml
core:
  components: {}  # Core network functions

ran:
  components: {}  # RAN components, such as gNBs

ric:
  components: {}  # RIC components

rus: {}            # Radio units
ues: {}            # UE profiles and subscriptions
slices: {}         # Network slices and DNNs
```

Add component-specific configuration under the relevant section. All the models provide helpers for loading YAML or JSON from text or files.

## Contributing

Contributions are welcome. To add or improve network concepts, extend the metamodel with additional typed fields or model classes and submit a pull request.

## License

Distributed under the **BSD 3-Clause Clear** license. See [LICENSE](LICENSE) for details.
