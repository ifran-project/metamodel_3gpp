# 5G Meta-model

A declarative Python model for describing 5G and 6G experiment infrastructures.

The model is built with [Pydantic](https://docs.pydantic.dev/) and is intended to be consumed by deployment tools and management units.

The main idea behind is to keep the description separate from the deployment state, making experiments easier to combine, share, and reproduce across different implementations and testbeds.
