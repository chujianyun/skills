# List access policies

> Lists all access policies for the organization.



## OpenAPI

````yaml /langsmith/langsmith-platform-openapi.json get /api/v1/platform/orgs/current/access-policies
openapi: 3.1.0
info:
  title: LangSmith
  description: >+
    The LangSmith API is used to programmatically create and manage LangSmith
    resources.


    ## Host

    https://api.smith.langchain.com


    ## Authentication

    To authenticate with the LangSmith API, set the `X-Api-Key` header

    to a valid [LangSmith API
    key](https://docs.langchain.com/langsmith/create-account-api-key#create-an-api-key).

  version: 0.1.0
servers:
  - url: /
security: []
tags:
  - name: run
    x-group: Tracing
  - name: runs
    x-group: Tracing
  - name: sessions
    x-group: Tracing
  - name: tracer-sessions
    x-group: Tracing
  - name: threads
    x-group: Threads
  - name: datasets
    x-group: Datasets
  - name: examples
    x-group: Datasets
  - name: evaluators
    x-group: Evaluation
  - name: experiment-view-overrides
    x-group: Evaluation
  - name: experiments
    x-group: Evaluation
  - name: annotation-queues
    x-group: Feedback & Annotation
  - name: annotation_queues
    x-group: Feedback & Annotation
  - name: feedback
    x-group: Feedback & Annotation
  - name: feedback-configs
    x-group: Feedback & Annotation
  - name: alert_rules
    x-group: Monitoring
  - name: bulk-exports
    x-group: Monitoring
  - name: charts
    x-group: Monitoring
  - name: commits
    x-group: Prompts & Playground
  - name: directories
    x-group: Prompts & Playground
  - name: hub_environments
    x-group: Prompts & Playground
  - name: playground-settings
    x-group: Prompts & Playground
  - name: prompt-webhooks
    x-group: Prompts & Playground
  - name: prompts
    x-group: Prompts & Playground
  - name: tag-transitions
    x-group: Prompts & Playground
  - name: comments
    x-group: Prompt Hub
  - name: likes
    x-group: Prompt Hub
  - name: optimization-jobs
    x-group: Prompt Hub
  - name: ownerships
    x-group: Prompt Hub
  - name: repos
    x-group: Prompt Hub
  - name: settings
    x-group: Prompt Hub
  - name: tags
    x-group: Prompt Hub
  - name: integrations
    x-group: Integrations & Tools
  - name: mcp
    x-group: Integrations & Tools
  - name: mcp_vendors
    x-group: Integrations & Tools
  - name: oauth
    x-group: Integrations & Tools
  - name: tools
    x-group: Integrations & Tools
  - name: gateway-policies
    x-group: LLM Gateway
  - name: sandboxes
    x-group: Sandboxes
  - name: issues
    x-group: Issues
  - name: issues-agent
    x-group: Issues
  - name: Organizations
    x-group: Administration
  - name: SCIM Tokens
    x-group: Administration
  - name: TTL Settings
    x-group: Administration
  - name: access_policies
    x-group: Administration
  - name: api-key
    x-group: Administration
  - name: audit-logs
    x-group: Administration
  - name: auth
    x-group: Administration
  - name: aws_marketplace
    x-group: Administration
  - name: data_planes
    x-group: Administration
  - name: me
    x-group: Administration
  - name: orgs
    x-group: Administration
  - name: service-accounts
    x-group: Administration
  - name: tenant
    x-group: Administration
  - name: ttl-settings
    x-group: Administration
  - name: usage-limits
    x-group: Administration
  - name: workspaces
    x-group: Administration
  - name: ace
    x-group: System
  - name: backfills
    x-group: System
  - name: features
    x-group: System
  - name: info
    x-group: System
  - name: model-price-map
    x-group: System
  - name: public
    x-group: System
  - name: agents
    x-hidden: true
  - name: fleet orgs
  - name: fleet secrets
  - name: fleet tenants
  - name: fleet threads
    x-hidden: true
  - name: fleet users
  - name: productfeedback
    x-hidden: true
  - name: teams
  - name: usage
paths:
  /api/v1/platform/orgs/current/access-policies:
    get:
      tags:
        - access_policies
      summary: List access policies
      description: Lists all access policies for the organization.
      parameters: []
      responses:
        '200':
          description: List of access policies
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/authz_internal.ListAccessPoliciesResponse'
        '403':
          description: Forbidden
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/shared.ProblemDetails'
        '500':
          description: Internal server error
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/shared.ProblemDetails'
        '503':
          description: Service unavailable
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/shared.ProblemDetails'
      security:
        - API Key: []
        - Organization ID: []
        - Bearer Auth: []
components:
  schemas:
    authz_internal.ListAccessPoliciesResponse:
      type: object
      properties:
        access_policies:
          type: array
          items:
            $ref: '#/components/schemas/authz_internal.AccessPolicy'
    shared.ProblemDetails:
      description: RFC 7807 problem details returned on V2 API errors.
      type: object
      properties:
        detail:
          type: string
        details:
          description: >-
            Details is a LangSmith extension carrying structured fields for
            ErrorClass.
          allOf:
            - $ref: '#/components/schemas/shared.ParseErrorDetails'
        error_class:
          description: |-
            ErrorClass is a LangSmith extension sub-categorizing a status code.
            Additional values require expanding this enum and adding a oneOf
            discriminator on Details to keep the class↔details contract typed.
          type: string
          enum:
            - PARSE_FAILURE
        instance:
          type: string
        remedy:
          description: Remedy is a LangSmith extension for user-recoverable errors.
          type: string
        status:
          type: integer
        title:
          type: string
        type:
          type: string
    authz_internal.AccessPolicy:
      type: object
      properties:
        condition_groups:
          type: array
          items:
            $ref: '#/components/schemas/authz_internal.ConditionGroup'
        created_at:
          type: string
        description:
          type: string
        effect:
          type: string
        id:
          type: string
        name:
          type: string
        role_ids:
          items:
            type: string
          type: array
        updated_at:
          type: string
    shared.ParseErrorDetails:
      description: Structured fields describing an adapter parse failure.
      type: object
      required:
        - adapter
        - item_type
      properties:
        adapter:
          type: string
        item_type:
          type: string
        run_id:
          type: string
    authz_internal.ConditionGroup:
      type: object
      properties:
        conditions:
          type: array
          items:
            $ref: '#/components/schemas/authz_internal.Condition'
        permission:
          $ref: '#/components/schemas/authz_internal.Permission'
        resource_type:
          type: string
    authz_internal.Condition:
      type: object
      properties:
        attribute_key:
          type: string
        attribute_name:
          $ref: '#/components/schemas/authz_internal.AbacAttributeName'
        attribute_value:
          type: string
        operator:
          $ref: '#/components/schemas/authz_internal.AbacOperator'
    authz_internal.Permission:
      type: string
      enum:
        - agent-auth-connections:create
        - agent-auth-connections:delete
        - agent-auth-connections:read
        - agent-auth-connections:revoke
        - agent-auth-connections:update
        - agent-auth-credentials:use
        - annotation-queues:create
        - annotation-queues:delete
        - annotation-queues:read
        - annotation-queues:update
        - bulk-exports:manage
        - bulk-exports:read
        - charts:create
        - charts:delete
        - charts:read
        - charts:update
        - custom-apps:create
        - custom-apps:delete
        - custom-apps:download
        - custom-apps:read
        - custom-apps:update
        - datasets:clone
        - datasets:create
        - datasets:delete
        - datasets:download
        - datasets:read
        - datasets:share
        - datasets:tag-on-create
        - datasets:update
        - deployments:cancel-runs
        - deployments:create
        - deployments:delete
        - deployments:read
        - deployments:update
        - experiments:run
        - feedback-configs:create
        - feedback-configs:delete
        - feedback-configs:manage-enforced
        - feedback-configs:update
        - feedback:create
        - feedback:delete
        - feedback:read
        - feedback:update
        - fleet-agents:create
        - fleet-agents:delete
        - fleet-agents:invoke
        - fleet-agents:read
        - fleet-agents:update
        - fleet-skills:create
        - fleet-skills:delete
        - fleet-skills:read
        - fleet-skills:update
        - fleet:read-admin-config
        - fleet:write-admin-config
        - functions:create
        - functions:delete
        - functions:update
        - gateway:invoke
        - issues:create
        - issues:delete
        - issues:read
        - issues:update
        - mcp-servers:create
        - mcp-servers:create-personal
        - mcp-servers:delete
        - mcp-servers:invoke
        - mcp-servers:read
        - mcp-servers:update
        - model-price-map:create
        - model-price-map:delete
        - model-price-map:read
        - model-price-map:update
        - organization:access-control:manage
        - organization:audit-logs:read
        - organization:authentication:manage
        - organization:billing:manage
        - organization:billing:read
        - organization:engine:manage
        - organization:engine:read
        - organization:gateway:manage
        - organization:infrastructure:manage
        - organization:infrastructure:read
        - organization:installation-operations:manage
        - organization:installation-operations:read
        - organization:installation-usage:manage
        - organization:integrations:manage
        - organization:integrations:read
        - organization:manage
        - organization:manage-model-configs
        - organization:manage-model-secrets
        - organization:members:manage
        - organization:pats:create
        - organization:pats:manage
        - organization:pats:read
        - organization:read
        - organization:read-metadata
        - organization:retention:manage
        - organization:security-policy:manage
        - organization:service-key:manage
        - organization:settings:manage
        - organization:usage-controls:manage
        - organization:workspaces:manage
        - projects:create
        - projects:decrease-trace-tier
        - projects:delete
        - projects:increase-trace-tier
        - projects:read
        - projects:tag-on-create
        - projects:update
        - prompts:create
        - prompts:delete
        - prompts:read
        - prompts:share
        - prompts:tag
        - prompts:tag-on-create
        - prompts:update
        - rules:configure-retention
        - rules:create
        - rules:delete
        - rules:read
        - rules:update
        - runs:create
        - runs:delete
        - runs:read
        - runs:read-inputs
        - runs:read-outputs
        - runs:read-stats
        - runs:share
        - sandboxes:create
        - sandboxes:delete
        - sandboxes:exec
        - sandboxes:read
        - sandboxes:tag-on-create
        - sandboxes:update
        - snapshots:create
        - snapshots:delete
        - snapshots:update
        - workspaces:access-control:assign-restricted
        - workspaces:credentials:manage
        - workspaces:credentials:read-metadata
        - workspaces:credentials:use
        - workspaces:delete
        - workspaces:fleet-feedback:read-all
        - workspaces:integrations:manage
        - workspaces:integrations:read
        - workspaces:manage
        - workspaces:manage-keys
        - workspaces:manage-members
        - workspaces:manage-model-configs
        - workspaces:manage-secrets
        - workspaces:read
        - workspaces:resource-tags:manage
        - workspaces:retention:manage
        - workspaces:sandbox-proxy-profiles:manage
        - workspaces:security-policy:manage
        - workspaces:settings:manage
        - workspaces:tracing-keys:create
        - workspaces:usage-controls:manage
      x-enum-varnames:
        - AgentAuthConnectionsCreate
        - AgentAuthConnectionsDelete
        - AgentAuthConnectionsRead
        - AgentAuthConnectionsRevoke
        - AgentAuthConnectionsUpdate
        - AgentAuthCredentialsUse
        - AnnotationQueuesCreate
        - AnnotationQueuesDelete
        - AnnotationQueuesRead
        - AnnotationQueuesUpdate
        - BulkExportsManage
        - BulkExportsRead
        - ChartsCreate
        - ChartsDelete
        - ChartsRead
        - ChartsUpdate
        - CustomAppsCreate
        - CustomAppsDelete
        - CustomAppsDownload
        - CustomAppsRead
        - CustomAppsUpdate
        - DatasetsClone
        - DatasetsCreate
        - DatasetsDelete
        - DatasetsDownload
        - DatasetsRead
        - DatasetsShare
        - DatasetsTagOnCreate
        - DatasetsUpdate
        - DeploymentsCancelRuns
        - DeploymentsCreate
        - DeploymentsDelete
        - DeploymentsRead
        - DeploymentsUpdate
        - ExperimentsRun
        - FeedbackConfigsCreate
        - FeedbackConfigsDelete
        - FeedbackConfigsManageEnforced
        - FeedbackConfigsUpdate
        - FeedbackCreate
        - FeedbackDelete
        - FeedbackRead
        - FeedbackUpdate
        - FleetAgentsCreate
        - FleetAgentsDelete
        - FleetAgentsInvoke
        - FleetAgentsRead
        - FleetAgentsUpdate
        - FleetSkillsCreate
        - FleetSkillsDelete
        - FleetSkillsRead
        - FleetSkillsUpdate
        - FleetReadAdminConfig
        - FleetWriteAdminConfig
        - FunctionsCreate
        - FunctionsDelete
        - FunctionsUpdate
        - GatewayInvoke
        - IssuesCreate
        - IssuesDelete
        - IssuesRead
        - IssuesUpdate
        - McpServersCreate
        - McpServersCreatePersonal
        - McpServersDelete
        - McpServersInvoke
        - McpServersRead
        - McpServersUpdate
        - ModelPriceMapCreate
        - ModelPriceMapDelete
        - ModelPriceMapRead
        - ModelPriceMapUpdate
        - OrganizationAccessControlManage
        - OrganizationAuditLogsRead
        - OrganizationAuthenticationManage
        - OrganizationBillingManage
        - OrganizationBillingRead
        - OrganizationEngineManage
        - OrganizationEngineRead
        - OrganizationGatewayManage
        - OrganizationInfrastructureManage
        - OrganizationInfrastructureRead
        - OrganizationInstallationOperationsManage
        - OrganizationInstallationOperationsRead
        - OrganizationInstallationUsageManage
        - OrganizationIntegrationsManage
        - OrganizationIntegrationsRead
        - OrganizationManage
        - OrganizationManageModelConfigs
        - OrganizationManageModelSecrets
        - OrganizationMembersManage
        - OrganizationPATsCreate
        - OrganizationPATsManage
        - OrganizationPATsRead
        - OrganizationRead
        - OrganizationReadMetadata
        - OrganizationRetentionManage
        - OrganizationSecurityPolicyManage
        - OrganizationServiceKeyManage
        - OrganizationSettingsManage
        - OrganizationUsageControlsManage
        - OrganizationWorkspacesManage
        - ProjectsCreate
        - ProjectsDecreaseTraceTier
        - ProjectsDelete
        - ProjectsIncreaseTraceTier
        - ProjectsRead
        - ProjectsTagOnCreate
        - ProjectsUpdate
        - PromptsCreate
        - PromptsDelete
        - PromptsRead
        - PromptsShare
        - PromptsTag
        - PromptsTagOnCreate
        - PromptsUpdate
        - RulesConfigureRetention
        - RulesCreate
        - RulesDelete
        - RulesRead
        - RulesUpdate
        - RunsCreate
        - RunsDelete
        - RunsRead
        - RunsReadInputs
        - RunsReadOutputs
        - RunsReadStats
        - RunsShare
        - SandboxesCreate
        - SandboxesDelete
        - SandboxesExec
        - SandboxesRead
        - SandboxesTagOnCreate
        - SandboxesUpdate
        - SnapshotsCreate
        - SnapshotsDelete
        - SnapshotsUpdate
        - WorkspacesAccessControlAssignRestricted
        - WorkspacesCredentialsManage
        - WorkspacesCredentialsReadMetadata
        - WorkspacesCredentialsUse
        - WorkspacesDelete
        - WorkspacesFleetFeedbackReadAll
        - WorkspacesIntegrationsManage
        - WorkspacesIntegrationsRead
        - WorkspacesManage
        - WorkspacesManageKeys
        - WorkspacesManageMembers
        - WorkspacesManageModelConfigs
        - WorkspacesManageSecrets
        - WorkspacesRead
        - WorkspacesResourceTagsManage
        - WorkspacesRetentionManage
        - WorkspacesSandboxProxyProfilesManage
        - WorkspacesSecurityPolicyManage
        - WorkspacesSettingsManage
        - WorkspacesTracingKeysCreate
        - WorkspacesUsageControlsManage
    authz_internal.AbacAttributeName:
      type: string
      enum:
        - resource_tag_key
        - root_run_metadata
      x-enum-varnames:
        - AbacAttributeNameResourceTagKey
        - AbacAttributeNameRootRunMetadata
    authz_internal.AbacOperator:
      type: string
      enum:
        - equals
        - not_equals
        - equals_ignore_case
        - not_equals_ignore_case
        - matches
        - not_matches
        - equals_if_exists
        - not_equals_if_exists
        - equals_ignore_case_if_exists
        - not_equals_ignore_case_if_exists
        - matches_if_exists
        - not_matches_if_exists
      x-enum-varnames:
        - AbacOperatorEquals
        - AbacOperatorNotEquals
        - AbacOperatorEqualsIgnoreCase
        - AbacOperatorNotEqualsIgnoreCase
        - AbacOperatorMatches
        - AbacOperatorNotMatches
        - AbacOperatorEqualsIfExists
        - AbacOperatorNotEqualsIfExists
        - AbacOperatorEqualsIgnoreCaseIfExists
        - AbacOperatorNotEqualsIgnoreCaseIfExists
        - AbacOperatorMatchesIfExists
        - AbacOperatorNotMatchesIfExists
  securitySchemes:
    API Key:
      type: apiKey
      in: header
      name: X-API-Key
    Organization ID:
      type: apiKey
      in: header
      name: X-Organization-Id
    Bearer Auth:
      type: http
      description: >-
        Bearer tokens are used to authenticate from the UI. Must also specify
        x-tenant-id or x-organization-id (for org scoped apis).
      scheme: bearer

````
