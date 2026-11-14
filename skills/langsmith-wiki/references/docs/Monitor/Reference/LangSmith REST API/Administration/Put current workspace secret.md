# Put current workspace secret

> Create or update a workspace secret and the hosts it may be sent to.

Omit `value` to keep the current one; it is required to create a secret.
`configs` replaces the secret's hosts; omitted or empty restores the
built-in defaults for known provider keys. The value is never returned.



## OpenAPI

````yaml /langsmith/langsmith-platform-openapi.json put /api/v1/workspaces/current/secrets/{key}
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
  /api/v1/workspaces/current/secrets/{key}:
    put:
      tags:
        - workspaces
      summary: Put current workspace secret
      description: |-
        Create or update a workspace secret and the hosts it may be sent to.

        Omit `value` to keep the current one; it is required to create a secret.
        `configs` replaces the secret's hosts; omitted or empty restores the
        built-in defaults for known provider keys. The value is never returned.
      operationId: put_current_workspace_secret_api_v1_workspaces_current_secrets__key__put
      parameters:
        - name: key
          in: path
          required: true
          schema:
            type: string
            title: Key
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/WorkspaceSecretUpsert'
      responses:
        '200':
          description: Successful Response
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/WorkspaceSecret'
        '201':
          description: Secret created.
          headers:
            Location:
              description: URL of the created secret.
              schema:
                type: string
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/WorkspaceSecret'
        '400':
          content:
            application/problem+json:
              schema:
                $ref: '#/components/schemas/ProblemDetails'
          description: The value is missing for a new secret, or a host config is invalid.
        '422':
          description: Validation Error
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/HTTPValidationError'
      security:
        - API Key: []
        - Tenant ID: []
        - Bearer Auth: []
components:
  schemas:
    WorkspaceSecretUpsert:
      properties:
        value:
          anyOf:
            - type: string
              minLength: 1
            - type: 'null'
          title: Value
          description: >-
            Secret value. Required to create a secret; omit to keep the current
            value.
        configs:
          anyOf:
            - items:
                $ref: '#/components/schemas/SecretConfigInput'
              type: array
            - type: 'null'
          title: Configs
          description: >-
            Full replacement of the allowed hosts. Omitted or empty removes
            custom hosts so the built-in defaults, if any, apply.
      type: object
      title: WorkspaceSecretUpsert
    WorkspaceSecret:
      properties:
        key:
          type: string
          title: Key
        configs:
          items:
            $ref: '#/components/schemas/SecretConfig'
          type: array
          title: Configs
          description: >-
            Hosts the secret may be sent to, with built-in defaults applied.
            Listed secrets include it only when include_configs is true.
      type: object
      required:
        - key
      title: WorkspaceSecret
      description: >-
        A workspace secret's key and the hosts it may be sent to. Never the
        value.
    ProblemDetails:
      properties:
        type:
          type: string
          title: Type
        title:
          type: string
          title: Title
        status:
          type: integer
          title: Status
        detail:
          type: string
          title: Detail
      type: object
      required:
        - type
        - title
        - status
        - detail
      title: ProblemDetails
      description: Problem details describing an error response, as defined by RFC 7807.
    HTTPValidationError:
      properties:
        detail:
          items:
            type: string
          type: array
          title: Detail
      type: object
      title: HTTPValidationError
    SecretConfigInput:
      properties:
        host_pattern:
          type: string
          title: Host Pattern
          description: Exact host or a leading '*.' wildcard, e.g. 'api.openai.com'.
        header_name:
          anyOf:
            - type: string
            - type: 'null'
          title: Header Name
          description: HTTP header the secret is sent in. Null leaves it to the consumer.
        header_value_template:
          anyOf:
            - type: string
            - type: 'null'
          title: Header Value Template
          description: >-
            Header value with '{value}' replaced by the secret, e.g. 'Bearer
            {value}'. Null sends the raw secret.
      type: object
      required:
        - host_pattern
      title: SecretConfigInput
      description: A host a workspace secret may be sent to, and how it is sent.
    SecretConfig:
      properties:
        host_pattern:
          type: string
          title: Host Pattern
          description: Exact host or a leading '*.' wildcard, e.g. 'api.openai.com'.
        header_name:
          anyOf:
            - type: string
            - type: 'null'
          title: Header Name
          description: HTTP header the secret is sent in. Null leaves it to the consumer.
        header_value_template:
          anyOf:
            - type: string
            - type: 'null'
          title: Header Value Template
          description: >-
            Header value with '{value}' replaced by the secret, e.g. 'Bearer
            {value}'. Null sends the raw secret.
        id:
          anyOf:
            - type: string
              format: uuid
            - type: 'null'
          title: Id
          description: Omitted for a built-in default.
        source:
          $ref: '#/components/schemas/SecretConfigSource'
        created_at:
          anyOf:
            - type: string
              format: date-time
            - type: 'null'
          title: Created At
          description: Omitted for a built-in default.
        updated_at:
          anyOf:
            - type: string
              format: date-time
            - type: 'null'
          title: Updated At
          description: Omitted for a built-in default.
      type: object
      required:
        - host_pattern
        - source
      title: SecretConfig
    SecretConfigSource:
      type: string
      enum:
        - DEFAULT
        - CUSTOM
      title: SecretConfigSource
      description: Whether a secret config comes from the built-in catalog or an admin.
  securitySchemes:
    API Key:
      type: apiKey
      in: header
      name: X-API-Key
    Tenant ID:
      type: apiKey
      in: header
      name: X-Tenant-Id
    Bearer Auth:
      type: http
      description: >-
        Bearer tokens are used to authenticate from the UI. Must also specify
        x-tenant-id or x-organization-id (for org scoped apis).
      scheme: bearer

````
