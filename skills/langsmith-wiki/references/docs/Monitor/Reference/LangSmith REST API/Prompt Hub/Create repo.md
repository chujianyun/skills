# Create repo

> Create a repo.



## OpenAPI

````yaml /langsmith/langsmith-platform-openapi.json post /api/v1/repos
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
  /api/v1/repos:
    post:
      tags:
        - repos
      summary: Create repo
      description: Create a repo.
      operationId: create_repo_api_v1_repos_post
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/CreateRepoRequest'
      responses:
        '200':
          description: Successful Response
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/CreateRepoResponse'
        '422':
          description: The request has an invalid path, query, header, or body parameter.
          content:
            application/problem+json:
              schema:
                allOf:
                  - $ref: '#/components/schemas/ProblemDetails'
                  - type: object
                    required:
                      - errors
                    properties:
                      errors:
                        type: array
                        items:
                          type: string
                        description: >-
                          One message per invalid parameter, prefixed with its
                          location.
      security:
        - API Key: []
        - Tenant ID: []
        - Bearer Auth: []
components:
  schemas:
    CreateRepoRequest:
      properties:
        tag_value_ids:
          anyOf:
            - items:
                type: string
                format: uuid
              type: array
              maxItems: 100
            - type: 'null'
          title: Tag Value Ids
        repo_handle:
          type: string
          title: Repo Handle
        description:
          anyOf:
            - type: string
            - type: 'null'
          title: Description
        readme:
          anyOf:
            - type: string
            - type: 'null'
          title: Readme
        is_public:
          type: boolean
          title: Is Public
        tags:
          anyOf:
            - items:
                type: string
              type: array
            - type: 'null'
          title: Tags
        repo_type:
          type: string
          enum:
            - prompt
            - file
            - agent
            - skill
          title: Repo Type
          default: prompt
        source:
          anyOf:
            - type: string
              enum:
                - internal
                - external
            - type: 'null'
          title: Source
        restricted_mode:
          anyOf:
            - type: boolean
            - type: 'null'
          title: Restricted Mode
      type: object
      required:
        - repo_handle
        - is_public
      title: CreateRepoRequest
      description: Fields to create a repo
    CreateRepoResponse:
      properties:
        repo:
          $ref: '#/components/schemas/RepoWithLookups'
      type: object
      required:
        - repo
      title: CreateRepoResponse
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
    RepoWithLookups:
      properties:
        repo_handle:
          type: string
          title: Repo Handle
        description:
          anyOf:
            - type: string
            - type: 'null'
          title: Description
        readme:
          anyOf:
            - type: string
            - type: 'null'
          title: Readme
        id:
          type: string
          format: uuid
          title: Id
        tenant_id:
          type: string
          format: uuid
          title: Tenant Id
        created_at:
          type: string
          format: date-time
          title: Created At
        updated_at:
          type: string
          format: date-time
          title: Updated At
        is_public:
          type: boolean
          title: Is Public
        is_archived:
          type: boolean
          title: Is Archived
        restricted_mode:
          type: boolean
          title: Restricted Mode
          default: false
        tags:
          items:
            type: string
          type: array
          title: Tags
        original_repo_id:
          anyOf:
            - type: string
              format: uuid
            - type: 'null'
          title: Original Repo Id
        upstream_repo_id:
          anyOf:
            - type: string
              format: uuid
            - type: 'null'
          title: Upstream Repo Id
        commit_tags:
          items:
            type: string
          type: array
          title: Commit Tags
          default: []
        repo_type:
          type: string
          enum:
            - prompt
            - file
            - agent
            - skill
          title: Repo Type
        source:
          anyOf:
            - type: string
              enum:
                - internal
                - external
            - type: 'null'
          title: Source
        owner:
          anyOf:
            - type: string
            - type: 'null'
          title: Owner
        full_name:
          type: string
          title: Full Name
        num_likes:
          type: integer
          title: Num Likes
        num_downloads:
          type: integer
          title: Num Downloads
        num_views:
          type: integer
          title: Num Views
        liked_by_auth_user:
          anyOf:
            - type: boolean
            - type: 'null'
          title: Liked By Auth User
        last_commit_hash:
          anyOf:
            - type: string
            - type: 'null'
          title: Last Commit Hash
        num_commits:
          type: integer
          title: Num Commits
        created_by:
          anyOf:
            - type: string
            - type: 'null'
          title: Created By
        original_repo_full_name:
          anyOf:
            - type: string
            - type: 'null'
          title: Original Repo Full Name
        upstream_repo_full_name:
          anyOf:
            - type: string
            - type: 'null'
          title: Upstream Repo Full Name
        latest_commit_manifest:
          anyOf:
            - $ref: '#/components/schemas/CommitManifestResponse'
            - type: 'null'
        owners:
          anyOf:
            - items:
                $ref: '#/components/schemas/RepoOwner'
              type: array
            - type: 'null'
          title: Owners
      type: object
      required:
        - repo_handle
        - id
        - tenant_id
        - created_at
        - updated_at
        - is_public
        - is_archived
        - tags
        - repo_type
        - owner
        - full_name
        - num_likes
        - num_downloads
        - num_views
        - num_commits
      title: RepoWithLookups
      description: All database fields for repos, plus helpful computed fields.
    CommitManifestResponse:
      properties:
        commit_hash:
          type: string
          title: Commit Hash
        manifest:
          additionalProperties: true
          type: object
          title: Manifest
        examples:
          anyOf:
            - items:
                $ref: '#/components/schemas/RepoExampleResponse'
              type: array
            - type: 'null'
          title: Examples
      type: object
      required:
        - commit_hash
        - manifest
      title: CommitManifestResponse
      description: Response model for get_commit_manifest.
    RepoOwner:
      properties:
        identity_id:
          anyOf:
            - type: string
              format: uuid
            - type: 'null'
          title: Identity Id
        ls_user_id:
          type: string
          format: uuid
          title: Ls User Id
        email:
          anyOf:
            - type: string
            - type: 'null'
          title: Email
        full_name:
          anyOf:
            - type: string
            - type: 'null'
          title: Full Name
        created_at:
          type: string
          format: date-time
          title: Created At
      type: object
      required:
        - identity_id
        - ls_user_id
        - email
        - full_name
        - created_at
      title: RepoOwner
      description: |-
        A repo owner with user details.

        Note: identity_id and email may be None when returned to users
        outside the repo's tenant (PII protection).
    RepoExampleResponse:
      properties:
        id:
          type: string
          format: uuid
          title: Id
        start_time:
          anyOf:
            - type: string
              format: date-time
            - type: 'null'
          title: Start Time
        inputs:
          anyOf:
            - additionalProperties: true
              type: object
            - type: 'null'
          title: Inputs
        outputs:
          anyOf:
            - additionalProperties: true
              type: object
            - type: 'null'
          title: Outputs
        session_id:
          type: string
          format: uuid
          title: Session Id
      type: object
      required:
        - id
        - session_id
      title: RepoExampleResponse
      description: Response model for example runs
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
