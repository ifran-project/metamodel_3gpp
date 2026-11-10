# 3GPP-based Metamodel

<p align="center">
<a href="https://github.com/ifran-project/metamodel_3gpp/releases"><img src="https://img.shields.io/github/v/release/metamodel_3gpp/metamodel_3gpp?color=orange" alt="Release"/></a>
<a href="https://github.com/ifran-project/metamodel_3gpp/blob/main/LICENSE"><img src="https://img.shields.io/badge/License-BSD--3--Clause--Clear-blue.svg" alt="License"/></a>
<a href="https://www.codefactor.io/repository/github/ifran-project/metamodel_3gpp"><img src="https://www.codefactor.io/repository/github/ifran-project/metamodel_3gpp/badge" alt="CodeFactor" /></a>
<a href="https://github.com/ifran-project/metamodel_3gpp/pulls"><img src="https://img.shields.io/badge/PRs-Welcome-brightgreen" alt="PRs Welcome"/></a>
<a href="https://www.bestpractices.dev/projects/9435"><img src="https://www.bestpractices.dev/projects/9435/badge"></a>
</p>

The `metamodel_3gpp` is a Python library built with [Pydantic](https://docs.pydantic.dev/).

It provides an abstract, implementation-agnostic description of a 5G/6G mobile network, based on [3GPP](https://www.3gpp.org) concepts: core, gNBs, UEs (SUPI, S-NSSAI, DNN), RUs, RIC and so on.

The main idea behind is to keep the mobile network description separated from the deployment state, making experiments easier to share and reproduce across different implementations and testbeds.
