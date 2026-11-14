# Update data plane settings

> Update specific settings for a data plane owned by the caller's organization.



## OpenAPI

````yaml /langsmith/langsmith-platform-openapi.json patch /orgs/current/data-planes/{id}
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
  /orgs/current/data-planes/{id}:
    patch:
      tags:
        - data_planes
      summary: Update data plane settings
      description: >-
        Update specific settings for a data plane owned by the caller's
        organization.
      parameters:
        - description: Data plane ID
          name: id
          in: path
          required: true
          schema:
            type: string
            format: uuid
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/data_planes.UpdateDataPlaneRequest'
      responses:
        '200':
          description: Updated data plane
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/data_planes.PublicDataPlane'
        '400':
          description: Invalid request
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/shared.ProblemDetails'
        '403':
          description: BYOC not enabled or insufficient permissions
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/shared.ProblemDetails'
        '409':
          description: Data plane is not ready or its status does not allow updates
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
    data_planes.UpdateDataPlaneRequest:
      type: object
      properties:
        firewall:
          $ref: '#/components/schemas/data_planes.UpdateDataPlaneFirewallSettings'
        fleet_oidc:
          $ref: '#/components/schemas/data_planes.UpdateDataPlaneFleetOIDCSettings'
        maintenance_window:
          description: >-
            MaintenanceWindow is a weekly UTC window: two hours on AWS and GCP,
            or four hours on Azure.
          type: string
        ttl:
          $ref: '#/components/schemas/data_planes.UpdateDataPlaneTTLSettings'
    data_planes.PublicDataPlane:
      type: object
      properties:
        api_url:
          type: string
        created_at:
          type: string
        firewall:
          $ref: '#/components/schemas/data_planes.DataPlaneFirewallSettings'
        fleet_oidc:
          $ref: '#/components/schemas/data_planes.DataPlaneFleetOIDCSettings'
        id:
          type: string
        maintenance_window:
          type: string
        name:
          type: string
        provisioning_settings:
          $ref: '#/components/schemas/data_planes.DataPlaneProvisioningSettings'
        region:
          type: string
        status:
          $ref: '#/components/schemas/data_planes.Status'
        status_updated_at:
          type: string
        ttl:
          $ref: '#/components/schemas/data_planes.DataPlaneTTLSettings'
        workspaces:
          type: array
          items:
            $ref: '#/components/schemas/data_planes.PublicDataPlaneWorkspace'
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
    data_planes.UpdateDataPlaneFirewallSettings:
      type: object
      properties:
        allow_http:
          type: boolean
        allowed_cidrs:
          type: object
          additionalProperties:
            items:
              type: integer
            type: array
        allowed_domains:
          items:
            type: string
          type: array
    data_planes.UpdateDataPlaneFleetOIDCSettings:
      type: object
      properties:
        audience:
          type: string
        email_claim:
          type: string
        groups_claim:
          type: string
        is_enabled:
          type: boolean
        issuer_url:
          type: string
        provider:
          type: string
        subject_claim:
          type: string
        tenant_claim:
          type: string
        tenant_mappings:
          type: object
          additionalProperties:
            type: string
    data_planes.UpdateDataPlaneTTLSettings:
      type: object
      properties:
        enabled:
          type: boolean
        long_days:
          type: integer
        short_days:
          type: integer
    data_planes.DataPlaneFirewallSettings:
      type: object
      required:
        - allow_http
        - allowed_cidrs
        - allowed_domains
      properties:
        allow_http:
          type: boolean
        allowed_cidrs:
          type: object
          additionalProperties:
            items:
              type: integer
            type: array
        allowed_domains:
          items:
            type: string
          type: array
    data_planes.DataPlaneFleetOIDCSettings:
      type: object
      required:
        - audience
        - email_claim
        - groups_claim
        - is_enabled
        - issuer_url
        - provider
        - subject_claim
        - tenant_claim
        - tenant_mappings
      properties:
        audience:
          type: string
        email_claim:
          type: string
        groups_claim:
          type: string
        is_enabled:
          type: boolean
        issuer_url:
          type: string
        provider:
          type: string
        subject_claim:
          type: string
        tenant_claim:
          type: string
        tenant_mappings:
          type: object
          additionalProperties:
            type: string
    data_planes.DataPlaneProvisioningSettings:
      type: object
      properties:
        additional_tags:
          type: object
          additionalProperties:
            type: string
        azure_entra_tenant_id:
          description: EntraTenantID is the Microsoft Entra tenant of the resource group.
          type: string
        byoiam:
          $ref: '#/components/schemas/data_planes.DataPlaneBYOIAMSettings'
        byovpc:
          $ref: '#/components/schemas/data_planes.DataPlaneBYOVPCSettings'
        cloud:
          $ref: '#/components/schemas/data_planes.DataPlaneCloud'
        gcp_project_id:
          description: ProjectID is the customer project that hosts the data plane.
          type: string
        is_eks_api_privatelink_disabled:
          type: boolean
        is_gcp_byoiam_enabled:
          description: >-
            IsGCPBYOIAMEnabled is true when the customer created the data plane

            service accounts. It has its own name because AWS has the byoiam
            object.
          type: boolean
        is_public_load_balancer:
          type: boolean
        provisioner_service_account:
          description: |-
            ProvisionerServiceAccount is the customer service account that the
            control plane impersonates.
          type: string
        resource_group_id:
          type: string
        role_arn:
          type: string
        trace_storage:
          description: >-
            TraceStorage is the run and trace store. It is SMITHDB when SmithDB
            is

            enabled and serves queries, and CLICKHOUSE otherwise, including for
            data

            planes created before this setting existed.
          allOf:
            - $ref: '#/components/schemas/data_planes.DataPlaneTraceStorage'
        vpc_cidr:
          description: >-
            VPCCIDR is the effective AWS VPC, Azure VNet, or GCP VPC network
            CIDR, including for customer-managed VPCs.
          type: string
    data_planes.Status:
      type: string
      enum:
        - requested
        - provisioning
        - provisioning_failed
        - active
        - updating
        - inactive
        - deprovisioning
        - deleted
        - revoked
      x-enum-varnames:
        - DataPlaneStatusRequested
        - DataPlaneStatusProvisioning
        - DataPlaneStatusProvisioningFailed
        - DataPlaneStatusActive
        - DataPlaneStatusUpdating
        - DataPlaneStatusInactive
        - DataPlaneStatusDeprovisioning
        - DataPlaneStatusDeleted
        - DataPlaneStatusRevoked
    data_planes.DataPlaneTTLSettings:
      type: object
      required:
        - enabled
        - long_days
        - short_days
      properties:
        enabled:
          type: boolean
        long_days:
          type: integer
        short_days:
          type: integer
    data_planes.PublicDataPlaneWorkspace:
      type: object
      properties:
        id:
          type: string
        name:
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
    data_planes.DataPlaneBYOIAMSettings:
      type: object
      properties:
        is_enabled:
          description: True when the customer created the data plane IAM resources.
          type: boolean
    data_planes.DataPlaneBYOVPCSettings:
      type: object
      properties:
        private_app_subnet_ids:
          items:
            type: string
          type: array
        private_db_subnet_ids:
          items:
            type: string
          type: array
        public_subnet_ids:
          items:
            type: string
          type: array
        vpc_id:
          type: string
    data_planes.DataPlaneCloud:
      type: string
      enum:
        - AWS
        - AZURE
        - GCP
      x-enum-varnames:
        - DataPlaneCloudAWS
        - DataPlaneCloudAzure
        - DataPlaneCloudGCP
    data_planes.DataPlaneTraceStorage:
      type: string
      enum:
        - CLICKHOUSE
        - SMITHDB
      x-enum-varnames:
        - DataPlaneTraceStorageClickHouse
        - DataPlaneTraceStorageSmithDB
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
