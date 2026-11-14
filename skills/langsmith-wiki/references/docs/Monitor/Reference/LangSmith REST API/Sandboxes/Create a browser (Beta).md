# Create a browser (Beta)

> Beta: create a browser sandbox, which runs one persistent Chrome that other sandboxes attach to. Logins made in it persist across restarts. It keeps its memory when it stops. A stopped browser is deleted after the sandbox default, along with its logins, unless delete_after_stop_seconds sets another delay or 0 to keep it.



## OpenAPI

````yaml /langsmith/langsmith-platform-openapi.json post /api/v2/sandboxes/browsers
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
  /api/v2/sandboxes/browsers:
    post:
      tags:
        - sandboxes
      summary: Create a browser (Beta)
      description: >-
        Beta: create a browser sandbox, which runs one persistent Chrome that
        other sandboxes attach to. Logins made in it persist across restarts. It
        keeps its memory when it stops. A stopped browser is deleted after the
        sandbox default, along with its logins, unless delete_after_stop_seconds
        sets another delay or 0 to keep it.
      parameters: []
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/sandboxes.CreateBrowserPayload'
      responses:
        '201':
          description: Created
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/sandboxes.BrowserResponse'
        '409':
          description: Name already exists
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/sandboxes.ErrorResponse'
        '422':
          description: Validation error
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/sandboxes.ErrorResponse'
        '429':
          description: Quota exceeded
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/sandboxes.ErrorResponse'
        '501':
          description: The browser beta is not enabled
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/sandboxes.ErrorResponse'
      security:
        - API Key: []
        - Tenant ID: []
        - Bearer Auth: []
components:
  schemas:
    sandboxes.CreateBrowserPayload:
      type: object
      properties:
        delete_after_stop_seconds:
          description: >-
            DeleteAfterStopSeconds deletes the browser this long after it stops.

            Defaults to the sandbox default; 0 keeps a stopped browser until it
            is

            deleted.
          type: integer
          minimum: 0
        hidpi:
          description: >-
            HiDPI renders pages at twice the resolution, so the live view is
            sharp on

            HiDPI screens, at four times the pixels for the browser to render
            and

            stream. Off by default, and fixed once the browser is created.
          type: boolean
        idle_ttl_seconds:
          description: >-
            IdleTTLSeconds stops the browser after this long without use. A
            stopped

            browser resumes with its memory on the next connection. Defaults to
            the

            sandbox default; 0 disables the idle stop.
          type: integer
          minimum: 0
        mem_bytes:
          type: integer
        name:
          description: |-
            Name of the browser sandbox. Generated when omitted, as "browser-"
            followed by the browser's ID.
          type: string
        proxy_config:
          description: |-
            ProxyConfig applies a sandbox's proxy rules to the pages the browser
            loads: header injection, access control, and relay rules.
          allOf:
            - $ref: '#/components/schemas/sandboxes.ProxyConfig'
        vcpus:
          description: >-
            VCPUs and MemBytes size the browser sandbox, as for any sandbox.
            With

            neither set, a browser gets 2 vCPUs and 8 GiB.
          type: integer
    sandboxes.BrowserResponse:
      type: object
      properties:
        attachments:
          description: Attachments are listed only while the browser is running.
          type: array
          items:
            $ref: '#/components/schemas/sandboxes.BrowserAttachment'
        hidpi:
          description: |-
            HiDPI reports whether pages render at twice the resolution. It is
            reported only while the browser is running.
          type: boolean
        id:
          type: string
        name:
          type: string
        status:
          type: string
    sandboxes.ErrorResponse:
      type: object
      properties:
        detail:
          type: object
          properties:
            error:
              type: string
            error_id:
              type: string
            message:
              type: string
    sandboxes.ProxyConfig:
      type: object
      properties:
        access_control:
          $ref: '#/components/schemas/sandboxes.AccessControl'
        callbacks:
          type: array
          items:
            $ref: '#/components/schemas/sandboxes.Callback'
        description:
          description: >-
            Description says what this configuration as a whole lets the sandbox
            reach, complementing the per-rule descriptions. At most 1024
            characters.
          type: string
          maxLength: 1024
        no_proxy:
          items:
            type: string
          type: array
        rules:
          type: array
          items:
            $ref: '#/components/schemas/sandboxes.ProxyRule'
    sandboxes.BrowserAttachment:
      type: object
      properties:
        act_url:
          type: string
        api_cdp_url:
          description: >-
            APICDPURL is the same Chrome DevTools endpoint through the LangSmith
            API,

            for clients outside any sandbox. It takes any API credential:
            headers as

            for any API call (X-Api-Key, or Authorization: Bearer with an OAuth

            access token, plus X-Tenant-Id where needed), or, for clients that
            take

            only a URL, api_key, token and tenant_id query parameters.
          type: string
        cdp_url:
          description: >-
            CDPURL is the Chrome DevTools endpoint the attached sandbox connects
            to,

            for example with Playwright's connect_over_cdp. It works only from
            inside

            that sandbox.
          type: string
        clients:
          description: >-
            Clients are the sandboxes currently connected to this window, with
            "api"

            for each client connected through api_cdp_url. An unrestricted
            window's

            connections are not listed.
          type: array
          items:
            type: string
        controller:
          description: >-
            Controller is "agent" while the attached sandbox drives the window
            and

            "user" while a person has taken it over.
          type: string
          enum:
            - agent
            - user
        created_at:
          type: string
        height:
          type: integer
        id:
          type: string
        links_expire_at:
          type: string
          format: date-time
        localhost_alias:
          description: >-
            LocalhostAlias is the sandbox's localhost as the browser sees it:
            open

            http://<localhost_alias>:<port> in a window to reach a server
            listening

            on that port in the sandbox, whether bound to localhost or to all

            interfaces (any port but 80 and 443). While this is the only sandbox

            sharing its localhost, http://localhost:<port> works too. Pages on
            other

            sites can navigate to a plain-HTTP server there but cannot fetch
            from it.

            Set only for windows attached with share_localhost.
          type: string
        name:
          type: string
        reason:
          description: Reason is why the agent asked a person to take over, when it did.
          type: string
        sandbox:
          description: Sandbox is the attached sandbox; empty for a window a person opened.
          type: string
        tabs:
          type: array
          items:
            $ref: '#/components/schemas/sandboxes.BrowserTab'
        unrestricted:
          description: >-
            Unrestricted windows give their sandbox the whole browser over CDP,
            with

            nothing filtered: every window and tab, every site's cookies, and

            commands that close or crash the browser. Taking over such a window
            does

            not pause its sandbox, and the LSBrowserControl domain is not
            available.
          type: boolean
        view_url:
          description: >-
            ViewURL and ActURL open the window on the sandbox service domain
            with no

            LangSmith login, for an agent to send to a person: ViewURL to watch
            it,

            ActURL also to use it while its controller is "user". Anyone holding
            a

            link can open the window until LinksExpireAt. Each response mints
            new

            ones; they are returned only to those who may use the browser.
          type: string
        width:
          description: >-
            Width and Height are the window's page size in CSS pixels, when it
            was

            given one; a window without one keeps Chrome's default of 1280x800.
          type: integer
    sandboxes.AccessControl:
      type: object
      properties:
        allow_list:
          items:
            type: string
          type: array
        deny_list:
          items:
            type: string
          type: array
    sandboxes.Callback:
      type: object
      required:
        - match_hosts
        - ttl_seconds
        - url
      properties:
        full_request:
          type: boolean
        match_hosts:
          type: array
          minItems: 1
          items:
            type: string
        request_headers:
          type: array
          items:
            $ref: '#/components/schemas/sandboxes.ProxyHeader'
        ttl_seconds:
          type: integer
          maximum: 3600
          minimum: 60
        url:
          type: string
    sandboxes.ProxyRule:
      type: object
      required:
        - name
      properties:
        aws:
          $ref: '#/components/schemas/sandboxes.ProxyAWSConfig'
        azure:
          $ref: '#/components/schemas/sandboxes.ProxyAzureConfig'
        description:
          description: >-
            Description says what this rule lets the sandbox reach, so an agent
            driving the sandbox can be told its capabilities. At most 1024
            characters.
          type: string
          maxLength: 1024
        enabled:
          type: boolean
        env_vars:
          description: >-
            EnvVars are plaintext env vars set for every command in the sandbox
            while this rule is enabled. Use them for tools that refuse to run
            unless a credential env var is present (e.g. gh needs GH_TOKEN) even
            though this rule injects the real credential on the wire — set a
            dummy value here so the command starts. Explicit per-sandbox
            env_vars win over these, and provider-managed (AWS/GCP) vars win
            over both.
          type: object
          additionalProperties:
            type: string
        gcp:
          $ref: '#/components/schemas/sandboxes.ProxyGCPConfig'
        headers:
          type: array
          items:
            $ref: '#/components/schemas/sandboxes.ProxyHeader'
        match_headers:
          description: >-
            MatchHeaders restricts a header injection or rewrite rule to
            requests carrying every listed header, each written "name: value"
            with a lowercase name and an exact value. Pair with headers of the
            same name to swap a placeholder the sandbox sends (e.g.
            "authorization: Bearer account-b") for a real credential, so one
            host can serve several accounts. Rules are evaluated in order and
            the first match wins.
          type: array
          items:
            type: string
        match_hosts:
          description: >-
            MatchHosts lists the hosts a header injection, rewrite, or relay
            rule

            covers. AWS and GCP rules match their provider's hosts built in;
            there

            MatchHosts optionally narrows them to the listed hosts (e.g.

            "sts.amazonaws.com", "bigquery.googleapis.com"), and when empty the
            rule

            covers every host the provider can authenticate. A host no rule
            covers is

            passed through without TLS interception. Azure rules do not accept
            it. A

            relay rule may also list IP addresses and CIDR blocks (10.0.0.0/8),
            which

            match connections the sandbox makes to an IP address rather than a
            name.
          type: array
          items:
            type: string
        match_paths:
          description: >-
            MatchPaths restricts a header injection or rewrite rule to requests
            whose path matches one of the patterns, so one host can use a
            different credential per route. The path excludes the query string.
            A pattern is an exact path (`/v1/runs`); a prefix, written as the
            prefix followed by a slash and `*` or `**`, which matches any path
            starting with that prefix (the prefix `/v1` also matches `/v10`); a
            suffix, written as `*`, a slash, and then the ending, which matches
            any path that ends with that text (the ending `runs` also matches
            `/v1/xruns`); or `*` alone for every path. A wildcard in the middle
            of a path is not supported. An empty list matches every path. Rules
            are evaluated in order and the first match wins. Rejected on aws,
            gcp, azure, and relay rules.
          type: array
          items:
            type: string
        name:
          type: string
        relay_id:
          description: >-
            RelayID is the ID of the LangSmith relay (a connection of kind
            relay) that carries connections to match_hosts when type is relay.
            Those connections leave from the relay's connector, and its network
            and IP, instead of the sandbox host. Access control still applies
            first, the first enabled matching relay rule wins, and a matched
            host never falls back to a direct connection.
          type: string
          format: uuid
        rewrite:
          $ref: '#/components/schemas/sandboxapi.ProxyRewriteConfig'
        type:
          type: string
    sandboxes.BrowserTab:
      type: object
      properties:
        id:
          type: string
        title:
          type: string
        url:
          type: string
    sandboxes.ProxyHeader:
      type: object
      required:
        - name
        - type
      properties:
        is_set:
          type: boolean
        name:
          type: string
        type:
          enum:
            - plaintext
            - opaque
            - workspace_secret
          allOf:
            - $ref: '#/components/schemas/sandboxes.HeaderType'
        value:
          type: string
    sandboxes.ProxyAWSConfig:
      type: object
      oneOf:
        - $ref: '#/components/schemas/sandboxes.ProxyAWSRoleConfig'
        - $ref: '#/components/schemas/sandboxes.ProxyAWSStaticConfig'
    sandboxes.ProxyAzureConfig:
      type: object
      oneOf:
        - $ref: '#/components/schemas/sandboxes.ProxyAzureWorkloadIdentityConfig'
        - $ref: '#/components/schemas/sandboxes.ProxyAzureAccountKeyConfig'
        - $ref: '#/components/schemas/sandboxes.ProxyAzureSASConfig'
    sandboxes.ProxyGCPConfig:
      type: object
      oneOf:
        - $ref: '#/components/schemas/sandboxes.ProxyGCPWorkloadIdentityConfig'
        - $ref: '#/components/schemas/sandboxes.ProxyGCPServiceAccountConfig'
    sandboxapi.ProxyRewriteConfig:
      type: object
      required:
        - port
      properties:
        credentials:
          description: >-
            Credentials is what happens to credential headers the sandbox sent,
            such as Authorization and Cookie: "strip" (the default) removes
            them, "redact" keeps each with its value replaced by "redacted"
            (after an auth scheme such as "Bearer "), and "keep" forwards them
            unchanged.
          type: string
          enum:
            - strip
            - redact
            - keep
        host:
          description: >-
            Host is an HTTPS destination. Exactly one of host and sandbox is
            set.
          type: string
        port:
          type: integer
          maximum: 65535
          minimum: 1
        sandbox:
          description: >-
            Sandbox is the name or ID of a sandbox to send requests to, over
            plain HTTP. A sandbox link from this sandbox to that sandbox's port
            must exist. Exactly one of host and sandbox is set.
          type: string
    sandboxes.HeaderType:
      type: string
      enum:
        - plaintext
        - opaque
        - workspace_secret
      x-enum-varnames:
        - HeaderTypePlaintext
        - HeaderTypeOpaque
        - HeaderTypeWorkspaceSecret
    sandboxes.ProxyAWSRoleConfig:
      type: object
      properties:
        role_arn:
          description: >-
            IAM role to assume with AssumeRoleWithWebIdentity, using a
            short-lived OIDC token LangSmith signs for this workspace. The
            role's trust policy must trust LangSmith's issuer for the token
            subject. Credentials renew automatically, and access follows the
            role's effective AWS permissions. Mutually exclusive with static
            keys, and cannot be changed after creation.
          type: string
          minLength: 1
        subject_scope:
          description: >-
            SubjectScope picks the token subject the role trusts: "workspace"
            (the default) or "tag:<tag value id>", which must be one of the
            sandbox's tag_value_ids. Only valid with role_arn.
          type: string
          pattern: >-
            ^(workspace|tag:[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12})$
        session_tags:
          description: >-
            SessionTags are AWS session tags on the role session, for role
            policies that scope access with ${aws:PrincipalTag/<key>}. The
            role's trust policy must allow sts:TagSession. At most 50; keys are
            1-128 and values 1-256 letters, numbers, spaces or _.:=+-@ (keys may
            also contain /); keys starting with aws: or langsmith: are reserved.
            Only valid with role_arn, and cannot be changed after creation.
          type: object
          additionalProperties:
            type: string
          maxProperties: 50
      required:
        - role_arn
      not:
        anyOf:
          - required:
              - access_key_id
          - required:
              - secret_access_key
    sandboxes.ProxyAWSStaticConfig:
      type: object
      properties:
        access_key_id:
          $ref: '#/components/schemas/sandboxes.ProxySecretValue'
        role_arn:
          description: >-
            IAM role to assume with AssumeRoleWithWebIdentity, using a
            short-lived OIDC token LangSmith signs for this workspace. The
            role's trust policy must trust LangSmith's issuer for the token
            subject. Credentials renew automatically, and access follows the
            role's effective AWS permissions. Mutually exclusive with static
            keys, and cannot be changed after creation.
          type: string
          enum:
            - ''
        secret_access_key:
          $ref: '#/components/schemas/sandboxes.ProxySecretValue'
      required:
        - access_key_id
        - secret_access_key
      not:
        anyOf:
          - required:
              - subject_scope
            properties:
              subject_scope:
                minLength: 1
          - required:
              - session_tags
            properties:
              session_tags:
                minProperties: 1
    sandboxes.ProxyAzureWorkloadIdentityConfig:
      type: object
      properties:
        tenant_id:
          description: >-
            TenantID is the Entra tenant (directory) ID, a GUID. Setting it
            selects workload identity: LangSmith signs an OIDC token for this
            workspace and exchanges it at Entra ID for access tokens of
            client_id, so no secret is stored. Cannot be changed after creation.
          type: string
          minLength: 1
          pattern: >-
            ^[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}$
        client_id:
          description: >-
            ClientID is the application (client) ID, a GUID, of the app
            registration or user-assigned managed identity whose federated
            identity credential trusts LangSmith's issuer. Required with
            tenant_id.
          type: string
          minLength: 1
          pattern: >-
            ^[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}$
        subject_scope:
          description: >-
            SubjectScope picks the token subject the federated credential
            trusts: "workspace" (the default) or "tag:<tag value id>", which
            must be one of the sandbox's tag_value_ids. Only valid with
            tenant_id.
          type: string
          pattern: >-
            ^(workspace|tag:[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12})$
        resources:
          description: >-
            Resources narrows the Entra resources access tokens are obtained
            for, from https://storage.azure.com, https://vault.azure.net,
            https://management.azure.com and
            https://cognitiveservices.azure.com. Defaults to all of them. Only
            valid with tenant_id.
          type: array
          items:
            type: string
            enum:
              - https://storage.azure.com
              - https://vault.azure.net
              - https://management.azure.com
              - https://cognitiveservices.azure.com
          uniqueItems: true
      required:
        - tenant_id
        - client_id
      not:
        anyOf:
          - required:
              - account_key
          - required:
              - sas_token
          - required:
              - storage_account
    sandboxes.ProxyAzureAccountKeyConfig:
      type: object
      properties:
        storage_account:
          minLength: 3
          description: >-
            StorageAccount is the storage account static credentials
            authenticate to: requests to its blob, dfs, queue, table and file
            endpoints. Requires exactly one of account_key (requests are signed
            with SharedKey) or sas_token (appended to each request).
          type: string
          maxLength: 24
          pattern: ^[a-z0-9]+$
        account_key:
          $ref: '#/components/schemas/sandboxes.ProxySecretValue'
      required:
        - storage_account
        - account_key
      not:
        anyOf:
          - required:
              - sas_token
          - required:
              - tenant_id
            properties:
              tenant_id:
                minLength: 1
          - required:
              - client_id
            properties:
              client_id:
                minLength: 1
          - required:
              - subject_scope
            properties:
              subject_scope:
                minLength: 1
          - required:
              - resources
            properties:
              resources:
                minItems: 1
    sandboxes.ProxyAzureSASConfig:
      type: object
      properties:
        storage_account:
          minLength: 3
          description: >-
            StorageAccount is the storage account static credentials
            authenticate to: requests to its blob, dfs, queue, table and file
            endpoints. Requires exactly one of account_key (requests are signed
            with SharedKey) or sas_token (appended to each request).
          type: string
          maxLength: 24
          pattern: ^[a-z0-9]+$
        sas_token:
          $ref: '#/components/schemas/sandboxes.ProxySecretValue'
      required:
        - storage_account
        - sas_token
      not:
        anyOf:
          - required:
              - account_key
          - required:
              - tenant_id
            properties:
              tenant_id:
                minLength: 1
          - required:
              - client_id
            properties:
              client_id:
                minLength: 1
          - required:
              - subject_scope
            properties:
              subject_scope:
                minLength: 1
          - required:
              - resources
            properties:
              resources:
                minItems: 1
    sandboxes.ProxyGCPWorkloadIdentityConfig:
      type: object
      properties:
        workload_identity_provider:
          description: >-
            WorkloadIdentityProvider federates an OIDC token LangSmith signs for
            this workspace through Workload Identity Federation instead of a
            service account key. Use the full resource name:
            //iam.googleapis.com/projects/<number>/locations/global/workloadIdentityPools/<pool>/providers/<provider>.
            Cannot be changed after creation.
          type: string
          minLength: 1
        service_account_email:
          description: >-
            ServiceAccountEmail is the service account to impersonate with the
            federated token. Omit it to use the federated principal directly.
          type: string
        subject_scope:
          description: >-
            SubjectScope picks the token subject the provider trusts:
            "workspace" (the default) or "tag:<tag value id>", which must be one
            of the sandbox's tag_value_ids. Only valid with
            workload_identity_provider.
          type: string
          pattern: >-
            ^(workspace|tag:[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12})$
        scopes:
          description: >-
            Scopes are the OAuth scopes requested for the access token. Omit
            them to use https://www.googleapis.com/auth/cloud-platform.
          type: array
          items:
            type: string
      required:
        - workload_identity_provider
      not:
        required:
          - service_account_json
    sandboxes.ProxyGCPServiceAccountConfig:
      type: object
      properties:
        service_account_json:
          $ref: '#/components/schemas/sandboxes.ProxySecretValue'
        scopes:
          description: >-
            Scopes are the OAuth scopes requested for the access token. Omit
            them to use https://www.googleapis.com/auth/cloud-platform.
          type: array
          items:
            type: string
      required:
        - service_account_json
      not:
        anyOf:
          - required:
              - workload_identity_provider
            properties:
              workload_identity_provider:
                minLength: 1
          - required:
              - service_account_email
            properties:
              service_account_email:
                minLength: 1
          - required:
              - subject_scope
            properties:
              subject_scope:
                minLength: 1
    sandboxes.ProxySecretValue:
      type: object
      required:
        - type
      properties:
        is_set:
          type: boolean
        type:
          enum:
            - plaintext
            - opaque
            - workspace_secret
          allOf:
            - $ref: '#/components/schemas/sandboxes.HeaderType'
        value:
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
