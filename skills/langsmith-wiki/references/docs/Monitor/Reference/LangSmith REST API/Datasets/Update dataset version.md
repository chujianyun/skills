# Update dataset version

> Tag a dataset version.

Points the tag at the version given by as_of, creating the tag or moving it
if the dataset already has it. Other tags are unchanged. Requires permission
to update datasets. Returns the version's time and all of its tags. Returns
400 if the tag is latest, and 404 if the dataset or the as_of tag does not
exist.



## OpenAPI

````yaml /langsmith/langsmith-platform-openapi.json put /api/v1/datasets/{dataset_id}/tags
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
  /api/v1/datasets/{dataset_id}/tags:
    put:
      tags:
        - datasets
      summary: Update dataset version
      description: >-
        Tag a dataset version.


        Points the tag at the version given by as_of, creating the tag or moving
        it

        if the dataset already has it. Other tags are unchanged. Requires
        permission

        to update datasets. Returns the version's time and all of its tags.
        Returns

        400 if the tag is latest, and 404 if the dataset or the as_of tag does
        not

        exist.
      operationId: update_dataset_version_api_v1_datasets__dataset_id__tags_put
      parameters:
        - name: dataset_id
          in: path
          required: true
          schema:
            type: string
            format: uuid
            title: Dataset Id
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/PutDatasetVersionsSchema'
      responses:
        '200':
          description: Successful Response
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/DatasetVersion'
        '400':
          content:
            application/problem+json:
              schema:
                $ref: '#/components/schemas/ProblemDetails'
          description: The tag is latest, which is reserved.
        '404':
          content:
            application/problem+json:
              schema:
                $ref: '#/components/schemas/ProblemDetails'
          description: The dataset or the as_of tag does not exist.
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
    PutDatasetVersionsSchema:
      properties:
        as_of:
          anyOf:
            - type: string
              format: date-time
            - type: string
          title: As Of
          description: >-
            The version to tag: an ISO 8601 timestamp, or the name of an
            existing tag on this dataset (latest resolves to the most recent
            example change, and returns 404 for a dataset with no examples). A
            value that does not parse as a timestamp is treated as a tag name,
            and an unknown tag name returns 404. Timestamps are not checked
            against the dataset history: the tag covers every example change
            made on or before that time, so a future time keeps picking up new
            changes until it passes. Use the exact as_of of an existing version,
            since looking up a version by tag returns 404 when the tag's time
            does not match a version.
        tag:
          type: string
          title: Tag
          description: >-
            The tag to set. If the dataset already has this tag, it is moved to
            the new version. The tag latest is reserved and returns 400.
      type: object
      required:
        - as_of
        - tag
      title: PutDatasetVersionsSchema
    DatasetVersion:
      properties:
        tags:
          anyOf:
            - items:
                type: string
              type: array
            - type: 'null'
          title: Tags
        as_of:
          type: string
          format: date-time
          title: As Of
      type: object
      required:
        - as_of
      title: DatasetVersion
      description: Dataset version schema.
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
