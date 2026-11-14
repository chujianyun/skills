# Computer use

> Run code, manage files, and call authenticated APIs from a persistent virtual computer attached to your Fleet agent.

Computer use gives your Fleet agent access to an isolated virtual computer. The agent can write and execute code, manage files, install packages, and call authenticated external APIs without exposing credentials to the language model.

> [!NOTE]
>
> Computer use is available on the [Plus and Enterprise plans](https://www.langchain.com/pricing).

## Computer modes

Choose how the virtual computer is shared across an agent's conversation threads:

| Mode | Description |
| - | - |
| **Shared computer** | All threads share a single computer. The filesystem, installed packages, and running processes persist across threads. Choose this mode when you want files, dependencies, or environment setup to accumulate across conversations. Shared computers are not deleted automatically. |
| **Computer per thread** | Each thread gets its own isolated computer that starts fresh and is archived when it goes idle. Choose this mode for software-engineering agents and other workloads that run many parallel, write-heavy tasks, or for any case where threads should not see each other's state. |

## Configure computer use

> [!WARNING]
>
> The computer mode is set when the agent is created and cannot be changed afterward. To switch modes, create a new agent.

**1. Open the Create agent dialog**

In the [Fleet](https://smith.langchain.com/agents?utm_source=docs&utm_medium=cta&utm_campaign=langsmith-signup&utm_content=langsmith-fleet-computer-use) left navigation, under **My Agents**, click  and select either **Create with AI** or **Blank agent**. Enter a name for your agent.

**2. Enable computer use**

Under **Should your agent use a computer?**, select **Yes**, then choose **Shared computer** or **Computer per thread**. If you select **No** (the default), the agent is created with no computer access.

**3. Set the base snapshot (optional)**

Expand **Advanced** to choose a **Snapshot** for new computers.

**4. Create the agent**

Click **Create Agent**.

## Access profiles

Use access profiles to let your agent call authenticated external APIs without putting credentials in the prompt or exposing them to the language model. Outbound HTTP requests to matching hosts are routed through a proxy that injects the configured headers before forwarding.

A profile contains one or more **Custom rules**. Each rule specifies:

* **Match Hosts**: The target hostnames the rule applies to. Use `*` as a wildcard (for example, `*.example.com` matches `api.example.com`).
* **Source Type and Provider**: The credential source. Choose **Connection** for user-delegated OAuth, or **Workspace Secret** for static API keys.
* **Inject Headers**: The HTTP headers the proxy adds to matched requests. Use template values such as `{access_token}` to reference the credential (for example, `Authorization: Bearer {access_token}`).

A profile also has a **Network scope** that controls outbound traffic for the agent's computer. The default is **None (all traffic allowed)**.

### Add an access profile

**1. Create the access profile**

Go to the [Fleet Integrations tab](https://smith.langchain.com/agents/tools) and navigate to the **Computer** section. Click **+ Create profile** and follow the prompts to configure the host patterns and credentials.

**2. Attach the profile to an agent**

In the agent editor, click the **Computer** node. Click **+ Add** next to **Access profiles** and select the profile you created.

**3. Save changes**

Click **Save changes**.

## Computer lifecycle

Each agent has two lifecycle settings that control how long a computer stays active and how long it is kept after it stops. [Configure both in the settings popover](#configure-lifecycle-and-snapshot).

* **Idle timeout**: When the computer has not received any commands for this duration, it pauses and the disk is archived. The agent can resume the same computer later without losing data. Default: **15 minutes**.
* **Stopped computer cleanup**: After a computer has been stopped for this duration, it is permanently deleted along with all disk data. Default: **14 days**.

> [!NOTE]
>
> **Stopped computer cleanup** applies only to **Computer per thread** mode. Shared computers are not deleted automatically.

## Choose a base snapshot

A snapshot is the disk image used to boot the computer. When no snapshot is selected, Fleet uses the platform default, `system/default:latest`. The current default starts from `ubuntu:26.04` and includes Python 3, Node.js 24, Go, Git, Docker, a browser, and document-processing libraries. For the full tool list and the other system snapshots, see [Understand system snapshots](../../../Deploy/Sandboxes/Sandbox%20snapshots.md#understand-system-snapshots).

To change the snapshot for an existing agent, set **Snapshot** in the settings popover, as described in [Configure lifecycle and snapshot](#configure-lifecycle-and-snapshot). To build or capture your own snapshot, see [Sandbox snapshots](../../../Deploy/Sandboxes/Sandbox%20snapshots.md), and include the components listed in [Prepare a custom image for Fleet](#prepare-a-custom-image-for-fleet).

> [!NOTE]
>
> Snapshot changes apply only to new computers for the agent. The single shared computer in **Shared computer** mode keeps its original snapshot for its lifetime.

## Configure lifecycle and snapshot

The snapshot, idle timeout, and stopped computer cleanup for an agent are all set in the **Computer lifecycle** section of the settings popover.

**1. Open the settings popover**

In [Fleet](https://smith.langchain.com/agents?utm_source=docs&utm_medium=cta&utm_campaign=langsmith-signup&utm_content=langsmith-fleet-computer-use), open the agent and click the  settings icon in the agent editor.

**2. Set the lifecycle fields**

Scroll to the **Computer lifecycle** section. Set the **Snapshot**, **Idle timeout**, and, for **Computer per thread** mode, **Stopped computer cleanup**.

**3. Save changes**

Click **Save changes**.

## Prepare a custom image for Fleet

A custom snapshot replaces the default filesystem; it does not inherit the default tools. Include the dependencies for the Fleet capabilities your agents use, even when starting from a minimal Linux image.

| Capability | Components |
| - | - |
| Command execution | Bash at `/bin/bash`. Fleet runs every command with it, so commands fail without it. |
| Run setup and file tools | Commands must run as `root` or as a user that can create directories under `/`. Python 3, `tar`, `grep`, and core utilities such as `mkdir`, `rm`, and `ln`. |
| [Access profiles](#access-profiles) | A system CA bundle at `/etc/ssl/certs/ca-certificates.crt`. At boot, the sandbox appends the proxy's CA to this file and points common CA-bundle environment variables at it. Debian, Ubuntu, Alpine, and Wolfi use this path. RHEL-family images keep their bundle elsewhere, so provide one at this path or HTTPS requests from the sandbox can fail certificate verification. |
| PowerPoint files (`fleet-pptx`) | Python 3 and `python-pptx`. |
| Word files (`fleet-docx`) | Python 3 and `python-docx`. |
| Excel files (`fleet-xlsx`) | Python 3, `openpyxl`, `defusedxml`, and `lxml`. The skill requires `openpyxl.xml.DEFUSEDXML` to be `True` before opening files. |
| Legacy document conversion (`fleet-document-converter`) | Node.js 20 or later and the `anydoc` executable from `@firecrawl/anydoc`, including its platform-specific native package. |

If `python-pptx` or `python-docx` is missing, the skill installs the pinned version into a virtual environment under `/tmp`, which requires Python's `venv` module and access to PyPI. If `anydoc` is missing, the converter runs it with `npx`, which requires npm and access to the npm registry. The Excel skill has no install fallback. Preinstall every component in images that run without package registry access.

To see the versions the default image includes in your release, start a sandbox from `system/default:latest` and run:

```bash
python3 -m pip list 2>/dev/null | grep -iE '^(python-docx|python-pptx|openpyxl|defusedxml|lxml|pillow|xlsxwriter) '
anydoc --version
```

Run the same commands in a sandbox started from your custom snapshot to confirm it is ready for Fleet. Also check that the document libraries import and the hardened XML parser is active:

```bash
python3 -c "import docx, pptx, openpyxl.xml; assert openpyxl.xml.DEFUSEDXML"
```

Your image does not need to use Ubuntu or include every development tool from the default image. If you use another distribution, provide compatible packages and their native dependencies.

`system/default:latest` is a snapshot reference, not a container image URI for a Dockerfile `FROM` instruction. Build your own container image, then [create a snapshot from it](../../../Deploy/Sandboxes/Sandbox%20snapshots.md#build-a-snapshot-from-a-container-image). To audit the default or a named system snapshot, follow [Inspect the default snapshot filesystem in self-hosted deployments](../../../Deploy/Sandboxes/Sandbox%20snapshots.md#inspect-the-default-snapshot-filesystem-in-self-hosted-deployments) using your deployed `sandbox-host` image.
