<div align="center">

# fastagent

fastagent: a tool making it easy to ship your agent to production

<h3>

[Documentation](https://fastagent.gitbook.io)

![GitHub Repo stars](https://img.shields.io/github/stars/bastienpo/fastagent?style=social)
![GitHub Actions Workflow Status](https://img.shields.io/github/actions/workflow/status/bastienpo/fastagent/ci.yml)


</h3>

</div>

---

> [!Warning]
> FastAgent is currently under **active development** and in alpha stage. It currently lacks SSL and CORS security features, as well as comprehensive testing needed for production deployment.

## Installation

You can install the project using pip: (Available on PyPI soon)

```bash
pip install git+https://github.com/bastienpo/fastagent.git
```

## How to use the project

First, create a simple LangChain application.

Let's create an app.py file with the simplest langchain runnable you can make, consisting of just a large language model.

```python
# pip install -qU langchain-mistralai and requires MISTRAL_API_KEY in to be set
from langchain_mistralai import ChatMistralAI

chain = ChatMistralAI(model="ministral-3b-latest")
```

Then, you need to initialize a fastagent configuration file (fastagent.toml) using the following command:

```bash
fastagent init
```
You will need to update the app field in the project section to match the path of your application in the form:

`<module_path>:<module_attribute>` in you case it would be `myapplication.app:chain`

If you decided to use a database in your configuration, you can use the `setup` command to create the tables and setup the database.

```bash
fastagent setup
```

When you are ready to develop or ship, you can start the production server:

```bash
fastagent dev # fastagent run
```

The difference between the `dev` and `run` command is that `dev` will reload the server on code changes and log to the console, while `run` will build a docker image and serve the application.

## Features

This is the current roadmap for the project:

- The project allows to setup a simple server for your agent. It only support langchain and postgresql to store your conversations and authentication data.
- It allows to setup a simple token based authentication and authorization.
- You can configure different middlewares CORS, Authorization and Rate limiting.

## What's next?

> [!Note]
> This project is still under active development and design is subject to change. I'm doing it only as a personal project because I was curious about how to ship an agent to production. Feel free to contribute or give feedback. I'm really open to any suggestion.

Near future:
- Add end-to-end testing of the project for langchain and langgraph.
- Add a permission system.
- Add stateless authentication.
- Add support for more databases (SQLite in particular).


Long term:
- Simplify the integration of monitoring and observability tools (Langfuse, Phoenix)
- Add support for Dspy and other frameworks.

## Resources

Some resources about the dependencies used for the project and thanks to the maintainers of the projects for their work.

- [FastAPI](https://fastapi.tiangolo.com/)
- [Granian](https://granian.dev/)
- [Langserve](https://github.com/Lightning-AI/LitServe)

The project is inspired by [LitServe](https://github.com/Lightning-AI/LitServe).
