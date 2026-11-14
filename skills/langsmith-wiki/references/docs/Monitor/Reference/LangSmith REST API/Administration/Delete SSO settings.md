# Delete SSO settings

> Delete SSO provider settings for the current organization.



## OpenAPI

````yaml /langsmith/langsmith-platform-openapi.json delete /api/v1/orgs/current/sso-settings/{id}
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
  /api/v1/orgs/current/sso-settings/{id}:
    delete:
      tags:
        - orgs
      summary: Delete SSO settings
      description: Delete SSO provider settings for the current organization.
      operationId: delete_sso_settings_api_v1_orgs_current_sso_settings__id__delete
      parameters:
        - name: id
          in: path
          required: true
          schema:
            type: string
            format: uuid
            title: Id
      responses:
        '200':
          description: Successful Response
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/SSOProvider'
        '422':
          description: Validation Error
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/HTTPValidationError'
      security:
        - API Key: []
        - Organization ID: []
        - Bearer Auth: []
components:
  schemas:
    SSOProvider:
      properties:
        id:
          type: string
          format: uuid
          title: Id
        organization_id:
          type: string
          format: uuid
          title: Organization Id
        provider_id:
          type: string
          format: uuid
          title: Provider Id
        provider_type:
          $ref: '#/components/schemas/SSOProviderType'
          default: saml
          x-extensible-enum: true
        default_workspace_role_id:
          type: string
          format: uuid
          title: Default Workspace Role Id
        default_workspace_ids:
          items:
            type: string
            format: uuid
          type: array
          title: Default Workspace Ids
        metadata_url:
          anyOf:
            - type: string
            - type: 'null'
          title: Metadata Url
        metadata_xml:
          anyOf:
            - type: string
            - type: 'null'
          title: Metadata Xml
        oidc_issuer_url:
          anyOf:
            - type: string
            - type: 'null'
          title: Oidc Issuer Url
        oidc_client_id:
          anyOf:
            - type: string
            - type: 'null'
          title: Oidc Client Id
        oidc_scopes:
          items:
            type: string
          type: array
          title: Oidc Scopes
        oidc_claim_mapping:
          additionalProperties:
            type: string
          type: object
          title: Oidc Claim Mapping
        sso_groups_enabled:
          type: boolean
          title: Sso Groups Enabled
          default: false
        sso_groups_claim_field:
          type: string
          title: Sso Groups Claim Field
          default: groups
        sso_groups_required:
          type: boolean
          title: Sso Groups Required
          default: false
        sso_groups_role_sync_enabled:
          type: boolean
          title: Sso Groups Role Sync Enabled
          default: true
        attribute_mapping:
          anyOf:
            - $ref: '#/components/schemas/SupabaseAttributeMapping'
            - type: 'null'
        attribute_mapping_load_error:
          anyOf:
            - type: string
            - type: 'null'
          title: Attribute Mapping Load Error
      type: object
      required:
        - id
        - organization_id
        - provider_id
        - default_workspace_role_id
        - default_workspace_ids
      title: SSOProvider
    HTTPValidationError:
      properties:
        detail:
          items:
            type: string
          type: array
          title: Detail
      type: object
      title: HTTPValidationError
    SSOProviderType:
      type: string
      enum:
        - saml
        - oidc
      title: SSOProviderType
    SupabaseAttributeMapping:
      properties:
        keys:
          additionalProperties:
            $ref: '#/components/schemas/SupabaseAttributeMappingKey'
          type: object
          title: Keys
      type: object
      title: SupabaseAttributeMapping
      description: >-
        Supabase SAML provider attribute_mapping. Empty keys is a valid value

        (clears the mapping). Map key is the claim key written into
        identity_data;

        value points at the SAML assertion attribute name.
    SupabaseAttributeMappingKey:
      properties:
        name:
          type: string
          title: Name
        array:
          type: boolean
          title: Array
          default: false
      type: object
      required:
        - name
      title: SupabaseAttributeMappingKey
      description: Single entry in a Supabase SAML attribute_mapping.keys map.
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
