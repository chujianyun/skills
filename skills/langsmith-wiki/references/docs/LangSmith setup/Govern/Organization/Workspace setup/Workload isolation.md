# Workload isolation

LangSmith uses a hierarchical structure to organize your work: organizations, workspaces, agents or applications, and resources. This structure lets you balance collaboration with access control, allowing you to choose the right level of isolation for your organization's needs.

What the grouping level is called depends on which information architecture your workspace uses. The control at the top left tells you which one you are on:

* An agent-based workspace groups resources by [agent](../../../Overview/Agent-based%20workspaces/Agent%20Registry.md#agent), and each agent's traces divide across [environments](../../../Overview/Agent-based%20workspaces/Agent%20environments.md) drawn from a fixed set of four.
* A project-based workspace groups them by application instead, with no environment tier, so environments are approximated with separate tracing projects.

The models introduced below apply to both, and the differences are called out where they matter.

This page explains two common approaches to organizing workspaces based on your organization's isolation requirements:

* [Isolate by workspace](#isolate-by-workspace): One workspace per business unit (recommended for most customers)
* [Isolate by agent or application](#isolate-by-agent-or-application): Multiple business units per workspace

> [!TIP]
>
> For details on setting up organizations and workspaces, refer to [Set up hierarchy](Set%20up%20hierarchy.md).

## Control access with RBAC and ABAC

The LangSmith permission system builds on the [resource hierarchy](../Overview.md#resource-hierarchy):

* With [role-based access control (RBAC)](../../Users%20%26%20access%20control/Role-based%20access%20control.md), user permissions are scoped to one or more workspaces, enforcing isolation between workspaces.
* With more fine-grained [attribute-based access control](../../Users%20%26%20access%20control/Organization%20and%20workspace%20operations%20reference.md#access-policies) (ABAC), access can be further restricted or granted based on attributes such as tags, agents, or applications within a workspace. For example, ABAC enables restricting access to only development resources or only resources associated with a specific agent or application.

## Isolate by workspace

> [!WARNING]
>
> This is the default model and recommended choice for most customers.

In this model, each business unit in the organization gets its own workspace. The workspace is the isolation boundary: it governs which data and resources that business unit can access. Within a workspace, business units group the resources that support the same application by agent or by application, depending on the workspace.

In the diagram below, production and staging are an agent's environments in an agent-based workspace, and separate tracing projects in a project-based one.

```mermaid actions={false}
graph LR
    Org[Organization]

    WS1[Workspace: Business Unit A]
    WS2[Workspace: Business Unit B]

    AgentA[Agent or application]
    AgentB[Agent or application]

    ProdA[Production]
    StagingA[Staging]
    DatasetA[Dataset]

    ProdB[Production]
    StagingB[Staging]
    DatasetB[Dataset]

    Org --> WS1
    Org --> WS2

    WS1 --> AgentA
    WS2 --> AgentB

    AgentA --> ProdA
    AgentA --> StagingA
    AgentA --> DatasetA

    AgentB --> ProdB
    AgentB --> StagingB
    AgentB --> DatasetB

    classDef orgStyle fill:#B2DEFF,stroke:#006DDD,stroke-width:2px,color:#030710
    classDef wsStyle fill:#E5F4FF,stroke:#006DDD,stroke-width:2px,color:#030710
    classDef appStyle fill:#F6FFDB,stroke:#6E8900,stroke-width:2px,color:#2E3900
    classDef resourceStyle fill:#F2FAFF,stroke:#40668D,stroke-width:1px,color:#2F4B68

    class Org orgStyle
    class WS1,WS2 wsStyle
    class AgentA,AgentB appStyle
    class ProdA,StagingA,DatasetA,ProdB,StagingB,DatasetB resourceStyle
```

* **Pros:** A single workspace allows all resources belonging to a business unit to be shared within that business unit. This makes collaboration and iteration within a unit straightforward. It also simplifies promotion from development to production. For example, the same [prompt](../../../../Deploy/Prompt%20%26%20Context%20Hub/Prompt%20%26%20Context%20Hub.md#prompts) can be versioned and promoted to production using tags, without copying or duplication.
* **Cons:** Development, test, and production work coexists in one workspace, so workspace-scoped [RBAC](../../Users%20%26%20access%20control/Role-based%20access%20control.md) alone does not separate them. In an agent-based workspace, environments divide an agent's traces without any convention to maintain. In a project-based workspace, separation depends on a naming convention, such as paired projects `checkout-production` and `checkout-staging`. [ABAC](../../Users%20%26%20access%20control/Organization%20and%20workspace%20operations%20reference.md#access-policies) provides more granular permissions within a workspace by restricting access based on resource attributes, such as allowing a user to access only development resources.

## Isolate by agent or application

In this model, multiple business units share a single workspace within an organization. They use agents or applications, together with [ABAC](../../Users%20%26%20access%20control/Organization%20and%20workspace%20operations%20reference.md#access-policies), to separate resources and govern access. As a result, shared resources such as [prompts](../../../../Deploy/Prompt%20%26%20Context%20Hub/Prompt%20%26%20Context%20Hub.md#prompts) and [deployments](../../../../Deploy/Get%20started/LangSmith%20Agent%20Server.md) can be reused across business units. Access to sensitive resources like [traces](../../../../Monitor/Trace/Observability%20concepts.md#traces) and [datasets](../../../../Test/Get%20started/Evaluation%20concepts.md#datasets) is limited to the owning business unit.

```mermaid actions={false}
graph LR
    Org[Organization]

    WS[Shared Workspace]

    AgentA[Agent or application: Business Unit A]
    AgentB[Agent or application: Business Unit B]

    TracesA[Traces: Business Unit A]
    DatasetA[Dataset: Business Unit A]
    PromptA[Prompt: Shared]

    TracesB[Traces: Business Unit B]
    DatasetB[Dataset: Business Unit B]
    PromptB[Prompt: Shared]

    Org --> WS

    WS --> AgentA
    WS --> AgentB

    AgentA --> TracesA
    AgentA --> DatasetA
    AgentA --> PromptA

    AgentB --> TracesB
    AgentB --> DatasetB
    AgentB --> PromptB

    classDef orgStyle fill:#B2DEFF,stroke:#006DDD,stroke-width:2px,color:#030710
    classDef wsStyle fill:#E5F4FF,stroke:#006DDD,stroke-width:2px,color:#030710
    classDef appStyle fill:#F6FFDB,stroke:#6E8900,stroke-width:2px,color:#2E3900
    classDef restrictedStyle fill:#F8E8E6,stroke:#B27D75,stroke-width:1px,color:#634643
    classDef sharedStyle fill:#FDF3FF,stroke:#7E65AE,stroke-width:1px,color:#504B5F

    class Org orgStyle
    class WS wsStyle
    class AgentA,AgentB appStyle
    class TracesA,DatasetA,TracesB,DatasetB restrictedStyle
    class PromptA,PromptB sharedStyle
```

* **Pros:** Common resources such as prompts and deployments can be shared and reused across business units, increasing collaboration and reducing duplicated work. Unlike isolating by workspace, collaboration can span across multiple business units within the workspace.
* **Cons:** Isolation between business units is weaker than in multi-workspace models and depends on correct use of ABAC. Misconfigured tags or policies can expose sensitive [traces](../../../../Monitor/Trace/Observability%20concepts.md#traces) or [datasets](../../../../Test/Get%20started/Evaluation%20concepts.md#datasets) across business units. Managing permissions across multiple business units can add operational complexity.
