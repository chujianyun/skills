# Roll an issues agent webhook signing secret

> Replaces the signing secret for the given generic URL issues agent webhook. Slack
and Jira destinations do not have signing secrets. The new secret is returned once in this
response; future deliveries use it immediately. URL and header values are redacted;
only a safe URL display and header names are returned.



## OpenAPI

````yaml /langsmith/langsmith-platform-openapi.json post /api/v1/platform/sessions/{session_id}/issues-agent/webhooks/{id}/roll-secret
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
  /api/v1/platform/sessions/{session_id}/issues-agent/webhooks/{id}/roll-secret:
    post:
      tags:
        - issues-agent
      summary: Roll an issues agent webhook signing secret
      description: >-
        Replaces the signing secret for the given generic URL issues agent
        webhook. Slack

        and Jira destinations do not have signing secrets. The new secret is
        returned once in this

        response; future deliveries use it immediately. URL and header values
        are redacted;

        only a safe URL display and header names are returned.
      parameters:
        - description: Tracer session ID (UUID)
          name: session_id
          in: path
          required: true
          schema:
            type: string
        - description: Webhook ID (UUID)
          name: id
          in: path
          required: true
          schema:
            type: string
      responses:
        '200':
          description: OK
          content:
            application/json:
              schema:
                $ref: >-
                  #/components/schemas/tracer_session_issues_agent_webhooks.IssuesAgentWebhook
        '400':
          description: Bad Request
          content:
            application/json:
              schema:
                type: object
                additionalProperties:
                  type: string
        '401':
          description: Unauthorized
          content:
            application/json:
              schema:
                type: object
                additionalProperties:
                  type: string
        '403':
          description: Forbidden
          content:
            application/json:
              schema:
                type: object
                additionalProperties:
                  type: string
        '404':
          description: Not Found
          content:
            application/json:
              schema:
                type: object
                additionalProperties:
                  type: string
        '500':
          description: Internal Server Error
          content:
            application/json:
              schema:
                type: object
                additionalProperties:
                  type: string
      security:
        - API Key: []
        - Tenant ID: []
        - Bearer Auth: []
components:
  schemas:
    tracer_session_issues_agent_webhooks.IssuesAgentWebhook:
      type: object
      properties:
        created_at:
          type: string
        destination_type:
          type: string
          enum:
            - webhook
            - jira
            - slack
        event_types:
          items:
            type: string
          type: array
        has_jira_token:
          type: boolean
        has_signing_secret:
          type: boolean
        has_unreadable_credentials:
          description: >-
            HasUnreadableCredentials marks a row retained in the settings list
            whose

            encrypted credential envelope could not be opened. No
            credential-derived

            fields are populated for such a row; it must be deleted and
            recreated.
          type: boolean
        header_names:
          description: HeaderNames lists configured header names for write-only clients.
          type: array
          items:
            type: string
        headers:
          type: object
          additionalProperties:
            type: string
        id:
          type: string
        issue_statuses:
          items:
            type: string
          type: array
        organization_id:
          type: string
        session_id:
          type: string
        severity_threshold:
          $ref: '#/components/schemas/issues.Severity'
        signing_secret:
          description: >-
            SigningSecret is present only in successful create, URL-conversion
            update,

            and roll responses.
          type: string
        slack_channel_id:
          description: >-
            Keep empty Slack fields in the response. The frontend uses an
            explicit

            empty string to distinguish URL destinations from Slack
            destinations.
          type: string
        slack_handoff:
          description: >-
            SlackHandoff is nil when no coding-agent hand-off is set on this
            destination.
          anyOf:
            - allOf:
                - $ref: '#/components/schemas/webhooks.SlackHandoffResponse'
            - type: 'null'
        slack_team_id:
          type: string
        tenant_id:
          type: string
        updated_at:
          type: string
        url:
          description: >-
            URL and Headers are retained as always-empty fields so a client
            written

            against the pre-write-only contract still parses the response. Use

            URLDisplay and HeaderNames instead.
          type: string
        url_display:
          description: URLDisplay contains only the destination hostname.
          type: string
    issues.Severity:
      type: integer
      enum:
        - 0
        - 1
        - 2
        - 3
      x-enum-varnames:
        - SeverityUrgent
        - SeverityHigh
        - SeverityMed
        - SeverityLow
    webhooks.SlackHandoffResponse:
      type: object
      required:
        - bot_user_id
        - message
      properties:
        bot_user_id:
          type: string
        message:
          description: >-
            Message is the custom instruction after the mention; "" means the
            default

            text ("Investigate this issue and open a fix if needed.").
          type: string
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
