# Create a snapshot

> Create a snapshot from a Docker image (async build). Names use lowercase registry-style components separated by slashes, up to 255 characters. The system/ namespace is read-only.



## OpenAPI

````yaml /langsmith/langsmith-platform-openapi.json post /api/v2/sandboxes/snapshots
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
  /api/v2/sandboxes/snapshots:
    post:
      tags:
        - sandboxes
      summary: Create a snapshot
      description: >-
        Create a snapshot from a Docker image (async build). Names use lowercase
        registry-style components separated by slashes, up to 255 characters.
        The system/ namespace is read-only.
      parameters: []
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/sandboxes.CreateSnapshotPayload'
      responses:
        '201':
          description: Created
          headers:
            Location:
              description: URL of the created snapshot
              schema:
                type: string
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/sandboxes.SnapshotResponse'
        '400':
          description: Bad Request
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/sandboxes.ErrorResponse'
        '403':
          description: Forbidden
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/sandboxes.ErrorResponse'
        '500':
          description: Internal Server Error
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
    sandboxes.CreateSnapshotPayload:
      type: object
      required:
        - docker_image
        - fs_capacity_bytes
        - name
      properties:
        description:
          description: >-
            Description says what this snapshot's image can do, so a caller can
            hand it to an agent as a capability summary. At most 1024
            characters.
          type: string
          maxLength: 1024
        docker_image:
          type: string
        fs_capacity_bytes:
          type: integer
        labels:
          description: >-
            Labels seed the snapshot's labels, overriding any label of the same
            key derived from the Docker image.
          allOf:
            - $ref: '#/components/schemas/sandboxes.Labels'
        name:
          type: string
        registry_id:
          type: string
        run_config:
          description: >-
            RunConfig overrides the runtime configuration taken from the Docker
            image.

            Every sandbox created from the snapshot runs as the image's USER, in
            its

            WORKDIR, with its ENV beneath the sandbox's own env_vars; user and

            work_dir given here replace the image's, and env_vars merge over it.
          allOf:
            - $ref: '#/components/schemas/sandboxapi.RunConfig'
        tag:
          description: mutable Docker-style tag; defaults to "latest"
          type: string
    sandboxes.SnapshotResponse:
      type: object
      properties:
        created_at:
          type: string
        created_by:
          type: string
        description:
          description: >-
            Description says what this snapshot's image can do, so a caller can
            hand it to an agent as a capability summary.
          type: string
        docker_image:
          type: string
        fs_capacity_bytes:
          type: integer
        fs_used_bytes:
          type: integer
        id:
          type: string
        image_digest:
          type: string
        included:
          description: >-
            The settings this snapshot carries, in include terms: sandboxes
            created from it start with each one their create request leaves
            unset. Env var values are never returned.
          type: array
          items:
            type: string
            enum:
              - mounts
              - proxy_config
              - env_vars
              - resources
              - lifecycle
              - labels
        labels:
          $ref: '#/components/schemas/sandboxes.Labels'
        memory_snapshot_size_bytes:
          description: >-
            MemorySnapshotSizeBytes is non-nil iff the snapshot was captured
            with

            VM memory state. A non-nil value is the canonical signal that this

            snapshot can warm-restore from memory; nil means rootfs only.
          type: integer
        mount_config:
          description: >-
            The mount_config sandboxes created from this snapshot start with
            when their create request has none, with secret values redacted.
            Present only on snapshots captured with include "mounts" or "all"
            from a sandbox that had mounts.
          allOf:
            - $ref: '#/components/schemas/sandboxes.SandboxMountConfig'
        name:
          type: string
        proxy_config:
          description: >-
            The proxy_config sandboxes created from this snapshot start with
            when their create request has none, with secret values redacted.
            Present only on snapshots captured with include "proxy_config" or
            "all".
          allOf:
            - $ref: '#/components/schemas/sandboxes.ProxyConfig'
        registry_id:
          type: string
        run_config:
          description: >-
            RunConfig is what sandboxes from this snapshot boot with. Absent on

            snapshots built before it was recorded, which run as root with their
            own env.
          allOf:
            - $ref: '#/components/schemas/sandboxapi.RunConfig'
        source_sandbox_id:
          type: string
        status:
          type: string
        status_message:
          type: string
        tags:
          description: >-
            Tags currently resolving to this snapshot, under Name. A snapshot
            with no

            tags is dangling — addressable only by id.
          type: array
          items:
            type: string
        updated_at:
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
    sandboxes.Labels:
      type: object
      additionalProperties:
        type: string
    sandboxapi.RunConfig:
      type: object
      properties:
        env_vars:
          type: object
          additionalProperties:
            type: string
        user:
          type: string
        work_dir:
          type: string
    sandboxes.SandboxMountConfig:
      type: object
      properties:
        auth:
          $ref: '#/components/schemas/sandboxes.SandboxMountAuthConfig'
        mounts:
          type: array
          items:
            $ref: '#/components/schemas/sandboxapi.MountSpec'
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
    sandboxes.SandboxMountAuthConfig:
      type: object
      properties:
        aws:
          $ref: '#/components/schemas/sandboxes.SandboxAWSMountAuthConfig'
        azure:
          $ref: '#/components/schemas/sandboxes.SandboxAzureMountAuthConfig'
        gcp:
          $ref: '#/components/schemas/sandboxes.SandboxGCPMountAuthConfig'
    sandboxapi.MountSpec:
      type: object
      required:
        - id
        - mount_path
        - type
      properties:
        azure_blob:
          $ref: '#/components/schemas/sandboxapi.AzureBlobMountSpec'
        cache:
          $ref: '#/components/schemas/sandboxapi.MountCacheSpec'
        contexthub:
          $ref: '#/components/schemas/sandboxapi.ContextHubMountSpec'
        encryption:
          $ref: '#/components/schemas/sandboxapi.MountEncryptionSpec'
        gcs:
          $ref: '#/components/schemas/sandboxapi.GCSMountSpec'
        git:
          $ref: '#/components/schemas/sandboxapi.GitMountSpec'
        id:
          type: string
          maxLength: 64
        mount_path:
          type: string
        read_only:
          type: boolean
        s3:
          $ref: '#/components/schemas/sandboxapi.S3MountSpec'
        type:
          enum:
            - s3
            - gcs
            - azure_blob
            - git
            - contexthub
          allOf:
            - $ref: '#/components/schemas/sandboxapi.MountKind'
      discriminator:
        mapping:
          s3: '#/components/schemas/sandboxapi.S3BucketMountSpec'
          gcs: '#/components/schemas/sandboxapi.GCSBucketMountSpec'
          git: '#/components/schemas/sandboxapi.GitRepoMountSpec'
          contexthub: '#/components/schemas/sandboxapi.ContextHubRepoMountSpec'
          azure_blob: '#/components/schemas/sandboxapi.AzureBlobContainerMountSpec'
        propertyName: type
      oneOf:
        - $ref: '#/components/schemas/sandboxapi.S3BucketMountSpec'
        - $ref: '#/components/schemas/sandboxapi.GCSBucketMountSpec'
        - $ref: '#/components/schemas/sandboxapi.GitRepoMountSpec'
        - $ref: '#/components/schemas/sandboxapi.ContextHubRepoMountSpec'
        - $ref: '#/components/schemas/sandboxapi.AzureBlobContainerMountSpec'
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
    sandboxes.SandboxAWSMountAuthConfig:
      type: object
      oneOf:
        - $ref: '#/components/schemas/sandboxes.SandboxAWSMountRoleAuthConfig'
        - $ref: '#/components/schemas/sandboxes.SandboxAWSMountStaticAuthConfig'
    sandboxes.SandboxAzureMountAuthConfig:
      type: object
      oneOf:
        - $ref: >-
            #/components/schemas/sandboxes.SandboxAzureMountWorkloadIdentityAuthConfig
        - $ref: '#/components/schemas/sandboxes.SandboxAzureMountAccountKeyAuthConfig'
        - $ref: '#/components/schemas/sandboxes.SandboxAzureMountSASAuthConfig'
    sandboxes.SandboxGCPMountAuthConfig:
      type: object
      oneOf:
        - $ref: >-
            #/components/schemas/sandboxes.SandboxGCPMountWorkloadIdentityAuthConfig
        - $ref: >-
            #/components/schemas/sandboxes.SandboxGCPMountServiceAccountAuthConfig
    sandboxapi.AzureBlobMountSpec:
      type: object
      required:
        - container
        - storage_account
      properties:
        container:
          type: string
        prefix:
          type: string
        storage_account:
          description: >-
            StorageAccount is the storage account name: 3 to 24 lowercase
            letters and digits.
          type: string
          maxLength: 24
          minLength: 3
          pattern: ^[a-z0-9]+$
    sandboxapi.MountCacheSpec:
      type: object
      properties:
        max_size_bytes:
          type: integer
          minimum: 0
        writeback_seconds:
          type: integer
          minimum: 0
    sandboxapi.ContextHubMountSpec:
      type: object
      required:
        - repo
      properties:
        initial_pull_only:
          description: >-
            InitialPullOnly syncs the repo once at startup instead of polling
            for

            updates for the sandbox's lifetime.
          type: boolean
        repo:
          description: |-
            Repo is the Context Hub repository to sync, as "owner/repo"
            (e.g. "-/my-agent", where "-" is the current workspace). The repo's
            latest commit tree is mirrored into the mount path.
          type: string
    sandboxapi.MountEncryptionSpec:
      type: object
      required:
        - kms_key
      properties:
        kms_key:
          description: >-
            KMSKey is the key to encrypt uploads with. S3 mounts take a KMS key
            ARN in the mount's region.
          type: string
    sandboxapi.GCSMountSpec:
      type: object
      required:
        - bucket
      properties:
        bucket:
          type: string
        prefix:
          type: string
    sandboxapi.GitMountSpec:
      type: object
      required:
        - remote_url
      properties:
        ref:
          $ref: '#/components/schemas/sandboxapi.GitMountRefSpec'
        refresh_interval_seconds:
          type: integer
          minimum: 1
        remote_url:
          type: string
    sandboxapi.S3MountSpec:
      type: object
      required:
        - bucket
        - region
      properties:
        bucket:
          type: string
        endpoint_url:
          type: string
        path_style:
          type: boolean
        prefix:
          type: string
        region:
          type: string
    sandboxapi.MountKind:
      type: string
      enum:
        - s3
        - gcs
        - azure_blob
        - git
        - contexthub
      x-enum-varnames:
        - MountKindS3
        - MountKindGCS
        - MountKindAzureBlob
        - MountKindGit
        - MountKindContextHub
    sandboxapi.S3BucketMountSpec:
      type: object
      required:
        - id
        - mount_path
        - type
        - s3
      properties:
        cache:
          $ref: '#/components/schemas/sandboxapi.MountCacheSpec'
        encryption:
          $ref: '#/components/schemas/sandboxapi.MountEncryptionSpec'
        id:
          type: string
          maxLength: 64
        mount_path:
          type: string
        read_only:
          type: boolean
        s3:
          $ref: '#/components/schemas/sandboxapi.S3MountSpec'
        type:
          enum:
            - s3
          allOf:
            - $ref: '#/components/schemas/sandboxapi.MountKind'
      not:
        anyOf:
          - required:
              - gcs
          - required:
              - git
          - required:
              - contexthub
          - required:
              - azure_blob
    sandboxapi.GCSBucketMountSpec:
      type: object
      required:
        - id
        - mount_path
        - type
        - gcs
      properties:
        cache:
          $ref: '#/components/schemas/sandboxapi.MountCacheSpec'
        gcs:
          $ref: '#/components/schemas/sandboxapi.GCSMountSpec'
        id:
          type: string
          maxLength: 64
        mount_path:
          type: string
        read_only:
          type: boolean
        type:
          enum:
            - gcs
          allOf:
            - $ref: '#/components/schemas/sandboxapi.MountKind'
      not:
        anyOf:
          - required:
              - s3
          - required:
              - git
          - required:
              - contexthub
          - required:
              - azure_blob
          - required:
              - encryption
    sandboxapi.GitRepoMountSpec:
      type: object
      required:
        - id
        - mount_path
        - type
        - git
      properties:
        git:
          $ref: '#/components/schemas/sandboxapi.GitMountSpec'
        id:
          type: string
          maxLength: 64
        mount_path:
          type: string
        read_only:
          type: boolean
        type:
          enum:
            - git
          allOf:
            - $ref: '#/components/schemas/sandboxapi.MountKind'
      not:
        anyOf:
          - required:
              - s3
          - required:
              - gcs
          - required:
              - contexthub
          - required:
              - azure_blob
          - required:
              - cache
          - required:
              - encryption
    sandboxapi.ContextHubRepoMountSpec:
      type: object
      required:
        - id
        - mount_path
        - type
        - contexthub
      properties:
        contexthub:
          $ref: '#/components/schemas/sandboxapi.ContextHubMountSpec'
        id:
          type: string
          maxLength: 64
        mount_path:
          type: string
        read_only:
          type: boolean
        type:
          enum:
            - contexthub
          allOf:
            - $ref: '#/components/schemas/sandboxapi.MountKind'
      not:
        anyOf:
          - required:
              - s3
          - required:
              - gcs
          - required:
              - git
          - required:
              - azure_blob
          - required:
              - cache
          - required:
              - encryption
    sandboxapi.AzureBlobContainerMountSpec:
      type: object
      required:
        - id
        - mount_path
        - type
        - azure_blob
      properties:
        azure_blob:
          $ref: '#/components/schemas/sandboxapi.AzureBlobMountSpec'
        cache:
          $ref: '#/components/schemas/sandboxapi.MountCacheSpec'
        id:
          type: string
          maxLength: 64
        mount_path:
          type: string
        read_only:
          type: boolean
        type:
          enum:
            - azure_blob
          allOf:
            - $ref: '#/components/schemas/sandboxapi.MountKind'
      not:
        anyOf:
          - required:
              - s3
          - required:
              - gcs
          - required:
              - git
          - required:
              - contexthub
          - required:
              - encryption
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
    sandboxes.SandboxAWSMountRoleAuthConfig:
      type: object
      properties:
        role_arn:
          description: >-
            IAM role to assume with AssumeRoleWithWebIdentity, using a
            short-lived OIDC token LangSmith signs for this workspace; the
            role's trust policy must trust LangSmith's issuer for the token
            subject. LangSmith scopes the credentials to the configured S3
            mounts. Mutually exclusive with static credentials, and cannot be
            changed after creation.
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
      required:
        - role_arn
      additionalProperties: false
    sandboxes.SandboxAWSMountStaticAuthConfig:
      type: object
      properties:
        access_key_id:
          $ref: '#/components/schemas/sandboxes.ProxySecretValue'
        role_arn:
          description: >-
            IAM role to assume with AssumeRoleWithWebIdentity, using a
            short-lived OIDC token LangSmith signs for this workspace; the
            role's trust policy must trust LangSmith's issuer for the token
            subject. LangSmith scopes the credentials to the configured S3
            mounts. Mutually exclusive with static credentials, and cannot be
            changed after creation.
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
    sandboxes.SandboxAzureMountWorkloadIdentityAuthConfig:
      type: object
      properties:
        tenant_id:
          description: >-
            TenantID is the Entra tenant (directory) ID, a GUID. Setting it
            selects workload identity: LangSmith signs an OIDC token for this
            workspace and exchanges it at Entra ID for storage access tokens of
            client_id. Cannot be changed after creation.
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
      required:
        - tenant_id
        - client_id
      not:
        anyOf:
          - required:
              - account_key
          - required:
              - sas_token
    sandboxes.SandboxAzureMountAccountKeyAuthConfig:
      type: object
      properties:
        account_key:
          $ref: '#/components/schemas/sandboxes.ProxySecretValue'
      required:
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
    sandboxes.SandboxAzureMountSASAuthConfig:
      type: object
      properties:
        sas_token:
          $ref: '#/components/schemas/sandboxes.ProxySecretValue'
      required:
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
    sandboxes.SandboxGCPMountWorkloadIdentityAuthConfig:
      type: object
      properties:
        workload_identity_provider:
          description: >-
            WorkloadIdentityProvider federates an OIDC token LangSmith signs for
            this workspace through Workload Identity Federation instead of a
            service account key:
            //iam.googleapis.com/projects/<number>/locations/global/workloadIdentityPools/<pool>/providers/<provider>.
            Mutually exclusive with service_account_json. Cannot be changed
            after creation.
          type: string
          minLength: 1
        service_account_email:
          description: >-
            ServiceAccountEmail is the service account to impersonate with the
            federated token. Omit it to use the federated principal directly.
            Only valid with workload_identity_provider.
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
      required:
        - workload_identity_provider
      not:
        required:
          - service_account_json
    sandboxes.SandboxGCPMountServiceAccountAuthConfig:
      type: object
      properties:
        service_account_json:
          $ref: '#/components/schemas/sandboxes.ProxySecretValue'
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
    sandboxapi.GitMountRefSpec:
      type: object
      required:
        - name
        - type
      properties:
        name:
          type: string
        type:
          type: string
          enum:
            - branch
            - tag
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
