# Create directory commit

> Creates a new directory commit for an agent or skill repository by applying file/link create, update, and delete operations. Linked directories default to the LATEST selector; use COMMIT to pin one commit. The legacy commit_id write field is deprecated and resolves as LATEST.



## OpenAPI

````yaml /langsmith/langsmith-platform-openapi.json post /api/v1/platform/hub/repos/{owner}/{repo}/directories/commits
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
  /api/v1/platform/hub/repos/{owner}/{repo}/directories/commits:
    post:
      tags:
        - directories
      summary: Create directory commit
      description: >-
        Creates a new directory commit for an agent or skill repository by
        applying file/link create, update, and delete operations. Linked
        directories default to the LATEST selector; use COMMIT to pin one
        commit. The legacy commit_id write field is deprecated and resolves as
        LATEST.
      parameters:
        - description: Repository owner handle or '-' for current tenant
          name: owner
          in: path
          required: true
          schema:
            type: string
        - description: Repository handle
          name: repo
          in: path
          required: true
          schema:
            type: string
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/directory.CreateDirectoryCommitRequest'
      responses:
        '200':
          description: OK
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/directory.CommitResponse'
        '400':
          description: Bad Request
          content:
            application/problem+json:
              schema:
                $ref: '#/components/schemas/directory.errorResponse'
        '401':
          description: Unauthorized
          content:
            application/problem+json:
              schema:
                $ref: '#/components/schemas/directory.errorResponse'
        '403':
          description: Forbidden
          content:
            application/problem+json:
              schema:
                $ref: '#/components/schemas/directory.errorResponse'
        '404':
          description: Not Found
          content:
            application/problem+json:
              schema:
                $ref: '#/components/schemas/directory.errorResponse'
        '409':
          description: Conflict
          content:
            application/problem+json:
              schema:
                $ref: '#/components/schemas/directory.errorResponse'
        '500':
          description: Internal Server Error
          content:
            application/problem+json:
              schema:
                $ref: '#/components/schemas/directory.errorResponse'
      security:
        - API Key: []
        - Tenant ID: []
        - Bearer Auth: []
components:
  schemas:
    directory.CreateDirectoryCommitRequest:
      type: object
      properties:
        files:
          additionalProperties:
            anyOf:
              - $ref: '#/components/schemas/directory.DirectoryEntryInput'
              - type: 'null'
          description: >-
            Paths to create, update, link, delete, or unlink. Use null to delete
            or unlink an existing path.
          type: object
        parent_commit:
          type: string
        skip_webhooks:
          description: SkipWebhooks suppresses Context Hub commit webhooks for this commit.
          type: boolean
      example:
        files:
          skills/current:
            type: skill
            repo_handle: shared-skill
            selector:
              type: LATEST
          agents/pinned:
            type: agent
            repo_handle: review-agent
            selector:
              type: COMMIT
              commit_id: 0198f3ab-7c2d-7def-8a91-23456789abcd
    directory.CommitResponse:
      type: object
      properties:
        commit:
          $ref: '#/components/schemas/directory.CommitInfo'
    directory.errorResponse:
      type: object
      required:
        - detail
        - status
        - title
        - type
      properties:
        code:
          type: string
        conflicting_path:
          type: string
        detail:
          type: string
        path:
          type: string
        rule:
          type: string
        status:
          type: integer
        title:
          type: string
        type:
          type: string
    directory.DirectoryEntryInput:
      discriminator:
        propertyName: type
        mapping:
          file: '#/components/schemas/directory.FileEntry'
          agent: '#/components/schemas/directory.AgentEntryInput'
          skill: '#/components/schemas/directory.SkillEntryInput'
      oneOf:
        - $ref: '#/components/schemas/directory.FileEntry'
        - $ref: '#/components/schemas/directory.AgentEntryInput'
        - $ref: '#/components/schemas/directory.SkillEntryInput'
    directory.CommitInfo:
      type: object
      properties:
        commit_hash:
          type: string
        created_at:
          type: string
        id:
          type: string
    directory.FileEntry:
      additionalProperties: false
      properties:
        type:
          enum:
            - file
          type: string
        content:
          type: string
      required:
        - type
        - content
      type: object
    directory.AgentEntryInput:
      additionalProperties: false
      not:
        required:
          - selector
          - commit_id
      properties:
        type:
          enum:
            - agent
          type: string
        repo_handle:
          type: string
        commit_id:
          deprecated: true
          description: >-
            Deprecated write input. It is accepted for compatibility but ignored
            for selection, so the link resolves as LATEST. Omit it for LATEST or
            replace it with selector {"type": "COMMIT", "commit_id": "<uuid>"}
            to pin a commit. commit_id and selector are mutually exclusive.
          format: uuid
          type: string
        selector:
          $ref: '#/components/schemas/directory.DirectorySelector'
          description: How to select the linked commit. Omit this field to use LATEST.
      required:
        - type
        - repo_handle
      type: object
    directory.SkillEntryInput:
      additionalProperties: false
      not:
        required:
          - selector
          - commit_id
      properties:
        type:
          enum:
            - skill
          type: string
        repo_handle:
          type: string
        commit_id:
          deprecated: true
          description: >-
            Deprecated write input. It is accepted for compatibility but ignored
            for selection, so the link resolves as LATEST. Omit it for LATEST or
            replace it with selector {"type": "COMMIT", "commit_id": "<uuid>"}
            to pin a commit. commit_id and selector are mutually exclusive.
          format: uuid
          type: string
        selector:
          $ref: '#/components/schemas/directory.DirectorySelector'
          description: How to select the linked commit. Omit this field to use LATEST.
      required:
        - type
        - repo_handle
      type: object
    directory.DirectorySelector:
      discriminator:
        propertyName: type
        mapping:
          LATEST: '#/components/schemas/directory.LatestSelector'
          COMMIT: '#/components/schemas/directory.CommitSelector'
      oneOf:
        - $ref: '#/components/schemas/directory.LatestSelector'
        - $ref: '#/components/schemas/directory.CommitSelector'
    directory.LatestSelector:
      additionalProperties: false
      properties:
        type:
          enum:
            - LATEST
          type: string
      required:
        - type
      type: object
    directory.CommitSelector:
      additionalProperties: false
      properties:
        type:
          enum:
            - COMMIT
          type: string
        commit_id:
          type: string
          format: uuid
      required:
        - type
        - commit_id
      type: object
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
