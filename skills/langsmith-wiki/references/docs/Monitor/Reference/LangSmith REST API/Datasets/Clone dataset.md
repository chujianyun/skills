# Clone dataset

> Copy examples from a source dataset into an existing target dataset.

Each copied example gets a new ID and keeps the inputs, outputs, metadata,
and source run ID of its source example. Attachments are copied when blob
storage is enabled. Copying the same examples twice adds them twice.
Requires the datasets:clone permission on both datasets. Returns the ID,
dataset ID, creation and modification times, and source run ID of each new
example. Without example IDs, a source or target that is not found can
return an empty list instead of an error.



## OpenAPI

````yaml /langsmith/langsmith-platform-openapi.json post /api/v1/datasets/clone
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
  /api/v1/datasets/clone:
    post:
      tags:
        - datasets
      summary: Clone dataset
      description: >-
        Copy examples from a source dataset into an existing target dataset.


        Each copied example gets a new ID and keeps the inputs, outputs,
        metadata,

        and source run ID of its source example. Attachments are copied when
        blob

        storage is enabled. Copying the same examples twice adds them twice.

        Requires the datasets:clone permission on both datasets. Returns the ID,

        dataset ID, creation and modification times, and source run ID of each
        new

        example. Without example IDs, a source or target that is not found can

        return an empty list instead of an error.
      operationId: clone_dataset_api_v1_datasets_clone_post
      requestBody:
        content:
          application/json:
            schema:
              $ref: >-
                #/components/schemas/Body_clone_dataset_api_v1_datasets_clone_post
        required: true
      responses:
        '200':
          description: Successful Response
          content:
            application/json:
              schema:
                items:
                  additionalProperties: true
                  type: object
                type: array
                title: Response Clone Dataset Api V1 Datasets Clone Post
        '404':
          description: >-
            Example IDs were given and nothing was copied, because none match or
            either dataset is not found.
          content:
            application/problem+json:
              schema:
                $ref: '#/components/schemas/ProblemDetails'
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
    Body_clone_dataset_api_v1_datasets_clone_post:
      properties:
        target_dataset_id:
          type: string
          format: uuid
          title: Target Dataset Id
          description: >-
            ID of the dataset in this workspace that receives the copied
            examples. Its current examples are kept.
        source_dataset_id:
          type: string
          format: uuid
          title: Source Dataset Id
          description: >-
            ID of the dataset in this workspace to copy examples from. It is not
            modified.
        as_of:
          anyOf:
            - anyOf:
                - type: string
                  format: date-time
                - type: string
              description: >-
                Only modifications made on or before this time are included. If
                None, the latest version of the dataset is used.
            - type: 'null'
          title: As Of
          description: >-
            Version of the source dataset to copy. A value that parses as an ISO
            8601 date or timestamp copies the examples as they were at that
            time; latest copies the current examples; any other value is a
            version tag. Defaults to latest.
        examples:
          items:
            type: string
            format: uuid
          type: array
          title: Examples
          description: >-
            IDs of source examples to copy. Defaults to every example in the
            source version. When IDs are given and nothing is copied, because
            none match or either dataset is not found, the request fails with
            404.
          default: []
        split:
          anyOf:
            - type: string
            - items:
                type: string
              type: array
            - type: 'null'
          title: Split
          description: >-
            Split name, or list of split names, assigned to every copied example
            in place of its source splits. Defaults to keeping the source
            splits.
        tag_value_ids:
          anyOf:
            - items:
                type: string
                format: uuid
              type: array
              maxItems: 100
            - type: 'null'
          title: Tag Value Ids
          description: >-
            List of resource tag value IDs to attach to the target dataset, up
            to 100. Requires the datasets:tag_on_create permission.
      type: object
      required:
        - target_dataset_id
        - source_dataset_id
      title: Body_clone_dataset_api_v1_datasets_clone_post
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
