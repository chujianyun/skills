# Set up a build machine on a restricted network

> Configure pip, uv, Python, and the LangGraph CLI to pull every package, interpreter, and image from an internal registry, then build a Python or JavaScript Agent Server image with no public internet access.

A build machine on a restricted network has no route to pypi.org, npmjs.org, GitHub, or Docker Hub. Every package, tool, interpreter, and container image comes from an internal registry, such as Artifactory or Nexus. Configure each tool on that machine to use the internal registry, then build an [Agent Server](../../Agent%20Server/Capabilities/Agent%20Server.md) image with the [LangGraph CLI](../../Get%20started/Reference/LangGraph%20CLI.md).

pip, uv, uv's Python downloads, and the image build each read their own setting. Configuring one leaves the others pointed at the public internet. Work through the sections in order, then run the checks in [Verify the setup](#verify-the-setup). The LangGraph CLI is a Python package, so a JavaScript project needs the pip and uv setup too.

> [!TIP]
>
> This page covers the build machine. To run the image you build, see [Deploy with control plane](../Deploy%20with%20control%20plane.md) or [Self-host standalone servers](../Self-host%20standalone%20servers.md). For the egress a running deployment needs, see [Egress for billing and operational telemetry](../../../LangSmith%20setup/Self-hosted/Configure%20an%20instance/Egress%20for%20billing%20and%20operational%20telemetry.md).

## Prerequisites

Collect the following from your platform team before you start:

* **PyPI repository URL**: The internal index that proxies or hosts Python packages, written as `<PYPI_INDEX_URL>` on this page. For example, `https://pypi.example.internal/simple`.
* **Container registry**: The registry host, plus the port if it has one, written as `<DOCKER_REGISTRY>`. It must hold a mirror of the Agent Server base image. See [Additional images for Agent Server builds](../../../LangSmith%20setup/Self-hosted/Configure%20an%20instance/Mirror%20images%20for%20your%20LangSmith%20installation.md#additional-images-for-agent-server-builds).
* **npm registry URL (JavaScript only)**: The internal registry that proxies or hosts npm packages, written as `<NPM_REGISTRY_URL>`. For example, `https://npm.example.internal`. Leave off the trailing slash, because Corepack appends paths to it.
* **CA bundle**: The path to the PEM file for your internal certificate authority (CA), written as `<CA_BUNDLE_PATH>`. Internal registries usually serve certificates signed by your organization's own CA, which operating systems and tools do not trust by default.
* **Root access**: Whether you have `sudo` on the build machine. Without sudo, use the per-user file locations on this page. Ask the platform team to install OS packages and the CA.
* **Python versions**: Which versions the OS package repositories provide.

## Trust the internal CA

Every later step connects to the internal registry over HTTPS. Until the machine trusts the internal CA, those connections fail with certificate errors, so install the CA first:

1. Add `<CA_BUNDLE_PATH>` to the operating system trust store. The command depends on the OS. For example, on Debian and Ubuntu, copy the file to `/usr/local/share/ca-certificates/` with a `.crt` extension. Then run `sudo update-ca-certificates`.
2. On Linux, copy the CA to `/etc/docker/certs.d/<DOCKER_REGISTRY>/ca.crt` so Docker trusts the internal registry. For details, see Docker's [Verify repository client with certificates](https://docs.docker.com/engine/security/certificates/).

pip and uv each need their own CA setting, covered in [Configure pip](#configure-pip) and [Configure uv](#configure-uv).

## Configure pip

Set the index once in a pip configuration file. A long URL passed as `--index-url` on each command is easy to get wrong, and a missing space between two flags produces a misleading `404`.

Create `~/.config/pip/pip.conf`. To apply the setting to every user on the machine, create `/etc/pip.conf` instead:

```ini
[global]
index-url = <PYPI_INDEX_URL>
cert = <CA_BUNDLE_PATH>
```

* **`index-url`**: Replaces pypi.org as the package index.
* **`cert`**: The CA bundle pip uses to verify the index. Older pip releases do not read the OS trust store, so set it explicitly.

If the index uses plain HTTP, add `trusted-host = <host>` with the index host name. For the full list of file locations and keys, see pip's [Configuration](https://pip.pypa.io/en/stable/topics/configuration/) docs.

## Install uv from the internal index

Install uv as a Python package from the internal index. The uv install script (`curl ... | sh`) does not work on a restricted network, because it downloads the uv binary from `releases.astral.sh` or GitHub.

PyPI hosts uv as a wheel that contains the binary. On some distributions, `venv` ships as a separate OS package, such as `python3-venv` on Debian and Ubuntu.

Install uv into its own virtual environment so it does not touch the system Python. Then link the binaries onto your `PATH`:

```bash
python3 -m venv ~/.local/share/uv-bootstrap
~/.local/share/uv-bootstrap/bin/pip install uv
mkdir -p ~/.local/bin
ln -s ~/.local/share/uv-bootstrap/bin/uv ~/.local/bin/uv
ln -s ~/.local/share/uv-bootstrap/bin/uvx ~/.local/bin/uvx
```

The `pip install` reads the `pip.conf` from the previous section, so it resolves against `<PYPI_INDEX_URL>`.

`uv self update` works only for a uv installed by the install script. To upgrade this uv, run `~/.local/share/uv-bootstrap/bin/pip install --upgrade uv`.

## Configure uv

uv does not read `pip.conf` or `PIP_INDEX_URL`. Without its own setting, uv resolves against pypi.org.

Set the following once in your shell profile, such as `~/.bashrc`:

```bash
export UV_DEFAULT_INDEX="<PYPI_INDEX_URL>"
export UV_SYSTEM_CERTS=true
export UV_PYTHON_DOWNLOADS=never
```

* **`UV_DEFAULT_INDEX`**: Replaces pypi.org as the default index.
* **`UV_SYSTEM_CERTS`**: Loads certificates from the OS trust store, which holds the internal CA. By default, uv trusts only its bundled roots.
* **`UV_PYTHON_DOWNLOADS`**: Stops uv from downloading Python. [Provide the Python interpreter](#provide-the-python-interpreter) explains why.

> [!NOTE]
>
> `UV_SYSTEM_CERTS` requires uv 0.11.0 or later. Earlier versions use `UV_NATIVE_TLS=true`, which later versions still accept with a deprecation warning.

To trust only the internal CA, set `SSL_CERT_FILE=<CA_BUNDLE_PATH>` in place of `UV_SYSTEM_CERTS`. `SSL_CERT_FILE` replaces both uv's bundled roots and the OS trust store. For every setting, see uv's [environment variable reference](https://docs.astral.sh/uv/reference/environment/).

## Provide the Python interpreter

The Agent Server image ships its own Python. The build machine needs Python 3.10 or later only to run pip, uv, and the LangGraph CLI. Install it from the OS repositories, for example on RHEL-family distributions:

```bash
sudo dnf install python3.12
```

uv finds the interpreter on `PATH`. Keep `UV_PYTHON_DOWNLOADS=never`: without it, uv tries to download a missing interpreter from GitHub and retries with no clear error. If the OS repositories do not provide a supported version, see uv's [Installing Python](https://docs.astral.sh/uv/guides/install-python/) guide.

## Build the Agent Server image

The image build runs inside Docker, so the pip and uv settings and the OS trust store on the build machine do not apply to it. Set the base image, the package registry, and the internal CA in `langgraph.json` instead.

To prepare the build:

1. Install the LangGraph CLI. It resolves against `UV_DEFAULT_INDEX`:

   ```bash
   uv tool install langgraph-cli
   ```

2. Log in to the internal registry:

   ```bash
   docker login <DOCKER_REGISTRY>
   ```

3. Copy the CA bundle into the project directory, next to `langgraph.json`. The build can copy files only from the project directory:

   ```bash
   cp <CA_BUNDLE_PATH> internal-ca.pem
   ```

Then follow the steps for your project language.

### Build a Python project

> [!WARNING]
>
> Do not rely on `pip_config_file` alone. The CLI installs dependencies with `uv pip install` by default (`pip_installer` set to `auto`), and uv does not read the pip configuration file. The build then resolves against pypi.org and fails. Setting `pip_installer` to `pip` does not fix it either: the step that installs the server package still reads the default index. Set the `UV_DEFAULT_INDEX` build argument in `dockerfile_lines` instead.

To build the image:

1. Set `base_image` and `dockerfile_lines` in `langgraph.json`:

   ```json
   {
     "dependencies": ["."],
     "graphs": {
       "agent": "./agent.py:graph"
     },
     "python_version": "3.12",
     "base_image": "<DOCKER_REGISTRY>/langchain/langgraph-api",
     "dockerfile_lines": [
       "COPY internal-ca.pem /tmp/internal-ca.pem",
       "RUN cat /tmp/internal-ca.pem >> /etc/ssl/certs/ca-certificates.crt && rm /tmp/internal-ca.pem",
       "ARG SSL_CERT_FILE=/etc/ssl/certs/ca-certificates.crt",
       "ARG UV_DEFAULT_INDEX=<PYPI_INDEX_URL>"
     ]
   }
   ```

   * **`base_image`**: The mirrored Agent Server image, without a tag. The CLI appends a tag built from `python_version`, plus `api_version` or `image_distro` when you set them. With the configuration above, the build pulls `<DOCKER_REGISTRY>/langchain/langgraph-api:3.12`, so that tag must exist in the registry.
   * **`dockerfile_lines`**: Lines the CLI inserts after `FROM`. The `COPY` and `RUN` lines append the internal CA to the image's system CA bundle, which keeps the public roots. The two `ARG` lines apply to every install step in the build, including installs from a `uv.lock` file. `SSL_CERT_FILE` points uv at the system bundle, which uv otherwise ignores, and `UV_DEFAULT_INDEX` points uv at the internal index. `ARG` values are visible in `docker history`, so do not put credentials in `<PYPI_INDEX_URL>`.

   If the index uses a certificate from a public CA, leave out the `COPY`, `RUN`, and `SSL_CERT_FILE` lines.

2. Build the image:

   ```bash
   langgraph build -t my-agent
   ```

### Build a JavaScript project

The build installs packages with the package manager that matches the project's lockfile. Node.js does not read the system CA bundle, so the build trusts the internal CA through `NODE_EXTRA_CA_CERTS` instead.

To build the image:

1. Set `base_image` and `dockerfile_lines` in `langgraph.json`:

   ```json
   {
     "dependencies": ["."],
     "graphs": {
       "agent": "./src/agent.ts:graph"
     },
     "node_version": "20",
     "base_image": "<DOCKER_REGISTRY>/langchain/langgraphjs-api",
     "dockerfile_lines": [
       "COPY internal-ca.pem /etc/ssl/certs/internal-ca.pem",
       "ARG NODE_EXTRA_CA_CERTS=/etc/ssl/certs/internal-ca.pem",
       "ARG NPM_CONFIG_REGISTRY=<NPM_REGISTRY_URL>"
     ]
   }
   ```

   * **`base_image`**: The mirrored JavaScript Agent Server image, without a tag. With the configuration above, the build pulls `<DOCKER_REGISTRY>/langchain/langgraphjs-api:20`, so that tag must exist in the registry.
   * **`dockerfile_lines`**: The `COPY` line puts the internal CA in the image, and `NODE_EXTRA_CA_CERTS` adds it to the roots Node.js trusts. `NPM_CONFIG_REGISTRY` points npm and pnpm at the internal registry. `ARG` values are visible in `docker history`, so do not put credentials in `<NPM_REGISTRY_URL>`.

   If the registry uses a certificate from a public CA, leave out the `COPY` and `NODE_EXTRA_CA_CERTS` lines.

2. Add the settings for your package manager. The image runs pnpm and Yarn through Corepack, which downloads the package manager itself from the npm registry:

   * **npm** (`package-lock.json`, or no lockfile): No other settings. npm fetches from `NPM_CONFIG_REGISTRY` even when `package-lock.json` records public URLs.
   * **pnpm** (`pnpm-lock.yaml`): Add `"ARG COREPACK_NPM_REGISTRY=<NPM_REGISTRY_URL>"` to `dockerfile_lines`. Pin pnpm in `package.json`, for example `"packageManager": "pnpm@9.15.9"`.
   * **Yarn 1** (`yarn.lock`): Add the same `COREPACK_NPM_REGISTRY` line, and pin Yarn, for example `"packageManager": "yarn@1.22.22"`. Yarn 1 downloads from the URLs recorded in `yarn.lock`, so regenerate the lockfile against `<NPM_REGISTRY_URL>`.
   * **Yarn 2 or later** (`yarn.lock`): Replace the `NPM_CONFIG_REGISTRY` line with `"ARG YARN_NPM_REGISTRY_SERVER=<NPM_REGISTRY_URL>"`, add the `COREPACK_NPM_REGISTRY` line, and pin Yarn, for example `"packageManager": "yarn@4.9.2"`.

   The build copies the whole project directory into the image, including any `.npmrc` file. Do not store registry tokens in a project `.npmrc`.

3. Build the image:

   ```bash
   langgraph build -t my-agent
   ```

For every `langgraph.json` key, see the [LangGraph CLI configuration file](../../Get%20started/Reference/LangGraph%20CLI.md#configuration-file) reference.

## Verify the setup

Run these checks after setup and at the start of each working session. Each check confirms one section and shows the expected output.

### Check CA trust

```bash
curl -sS -o /dev/null -w '%{http_code}\n' <PYPI_INDEX_URL>/
```

```text
200
```

A certificate error here means the CA is not in the OS trust store.

### Check pip

```bash
python3 -m pip download --no-deps -d /tmp/pip-check idna
```

```text
Looking in indexes: <PYPI_INDEX_URL>
Collecting idna
...
Successfully downloaded idna
```

The first line must show `<PYPI_INDEX_URL>`. If it is missing, pip is using pypi.org.

### Check the uv installation

```bash
uv --version
```

```text
uv 0.13.0
```

The output shows the installed version. A `command not found` error means `~/.local/bin` is not on your `PATH`.

### Check the uv configuration

```bash
echo idna | uv pip compile - --emit-index-url
```

```text
# This file was autogenerated by uv via the following command:
#    uv pip compile - --emit-index-url
--index-url <PYPI_INDEX_URL>

idna==3.20
```

The `--index-url` line must show `<PYPI_INDEX_URL>`, and a resolved version confirms TLS works.

### Check the Python interpreter

```bash
uv python find 3.12
```

The output is the path to the interpreter, such as `/usr/bin/python3.12`. To confirm that a missing version fails immediately:

```bash
uv venv --python 3.99 /tmp/uv-check
```

```text
error: No interpreter found for Python 3.99 in managed installations or search path
```

### Check the image build

```bash
langgraph dockerfile Dockerfile
grep -E '^(FROM|COPY|RUN cat|ARG)' Dockerfile
```

For a Python project:

```text
FROM <DOCKER_REGISTRY>/langchain/langgraph-api:3.12
COPY internal-ca.pem /tmp/internal-ca.pem
RUN cat /tmp/internal-ca.pem >> /etc/ssl/certs/ca-certificates.crt && rm /tmp/internal-ca.pem
ARG SSL_CERT_FILE=/etc/ssl/certs/ca-certificates.crt
ARG UV_DEFAULT_INDEX=<PYPI_INDEX_URL>
```

For a JavaScript project that uses npm:

```text
FROM <DOCKER_REGISTRY>/langchain/langgraphjs-api:20
COPY internal-ca.pem /etc/ssl/certs/internal-ca.pem
ARG NODE_EXTRA_CA_CERTS=/etc/ssl/certs/internal-ca.pem
ARG NPM_CONFIG_REGISTRY=<NPM_REGISTRY_URL>
```

`FROM` must name the internal registry, and every line from `dockerfile_lines` must be present.

## Next steps

`langgraph build` leaves the image on the build machine. To run it:

* **[Push the image](../Deploy%20with%20control%20plane.md#step-3-push-to-container-registry)**: Push the image to a registry your cluster or host can pull from.
* **[Deploy with control plane](../Deploy%20with%20control%20plane.md#step-4-deploy-with-the-control-plane-ui)**: Create a deployment from the pushed image in the LangSmith UI.
* **[Self-host standalone servers](../Self-host%20standalone%20servers.md)**: Run the image without a control plane, on Kubernetes, Docker, or Docker Compose.
* **[Egress for billing and operational telemetry](../../../LangSmith%20setup/Self-hosted/Configure%20an%20instance/Egress%20for%20billing%20and%20operational%20telemetry.md)**: Allow the egress a running deployment needs, or ask about an offline (air-gapped) license.
* **[Custom TLS certificates](../../../LangSmith%20setup/Self-hosted/Platform%20auth%20%26%20access%20control/Configure%20custom%20TLS%20certificates.md)**: Mount the internal CA in your LangSmith installation.
