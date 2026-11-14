# Authenticate Vertex AI with GKE workload identity

> Configure keyless Vertex AI authentication for Playground, Chat, and Insights on self-hosted LangSmith running on GKE.

GKE Workload Identity Federation lets these self-hosted LangSmith services call Vertex AI without long-lived service account keys:

* Playground
* Chat (`polly` in Helm)
* Insights

Each workload uses its Kubernetes service account (KSA) to impersonate a Google service account (GSA) through Application Default Credentials (ADC).

> [!NOTE]
>
> Keyless authentication for Chat and Insights requires Helm chart version 0.17.0 or later and LangSmith application version 0.17.29 or later.

To configure keyless authentication:

1. **Enable GKE Workload Identity Federation.** Enable it on the cluster and the node pools that run LangSmith. See [Workload Identity Federation for GKE](https://cloud.google.com/kubernetes-engine/docs/how-to/workload-identity).

2. **Grant the GSA Vertex AI access.** Create or select a GSA for these model calls. Grant it only `roles/aiplatform.user` in the project that hosts the models:

   ```bash
   gcloud projects add-iam-policy-binding "<vertex-project-id>" \
     --member="serviceAccount:<gsa-name>@<gsa-project-id>.iam.gserviceaccount.com" \
     --role="roles/aiplatform.user"
   ```

3. **Allow each KSA to impersonate the GSA.** Grant each calling KSA `roles/iam.workloadIdentityUser` on the GSA. Replace the five KSA placeholders with the names rendered by your Helm release:

   ```bash
   for ksa in \
     "<playground-ksa>" \
     "<polly-api-ksa>" \
     "<polly-queue-ksa>" \
     "<insights-api-ksa>" \
     "<insights-queue-ksa>"; do
     gcloud iam service-accounts add-iam-policy-binding \
       "<gsa-name>@<gsa-project-id>.iam.gserviceaccount.com" \
       --role="roles/iam.workloadIdentityUser" \
       --member="serviceAccount:<cluster-project-id>.svc.id.goog[<namespace>/${ksa}]"
   done
   ```

   Bind only these specific KSA subjects. If the workloads use different namespaces, run the command separately with each KSA's namespace.

4. **Annotate every KSA.** Add the GSA annotation through your Helm values. The Chat and Insights API and queue identities are separate callers. Every API and queue identity needs an annotation and IAM binding:

   ```yaml Helm
   # Playground
   playground:
     deployment:
       extraEnv:
         - name: GOOGLE_CLOUD_PROJECT
           value: "<vertex-project-id>"
     serviceAccount:
       annotations:
         iam.gke.io/gcp-service-account: "<gsa-name>@<gsa-project-id>.iam.gserviceaccount.com"

   # Chat
   polly:
     apiServer:
       serviceAccount:
         annotations:
           iam.gke.io/gcp-service-account: "<gsa-name>@<gsa-project-id>.iam.gserviceaccount.com"
     queue:
       serviceAccount:
         annotations:
           iam.gke.io/gcp-service-account: "<gsa-name>@<gsa-project-id>.iam.gserviceaccount.com"

   # Insights
   engineInsightsAgent:
     apiServer:
       serviceAccount:
         annotations:
           iam.gke.io/gcp-service-account: "<gsa-name>@<gsa-project-id>.iam.gserviceaccount.com"
       deployment:
         extraEnv:
           - name: CLIO_VERTEX_AI_ADC_ENABLED
             value: "true"
           - name: GOOGLE_CLOUD_PROJECT
             value: "<vertex-project-id>"
     queue:
       serviceAccount:
         annotations:
           iam.gke.io/gcp-service-account: "<gsa-name>@<gsa-project-id>.iam.gserviceaccount.com"
       deployment:
         extraEnv:
           - name: CLIO_VERTEX_AI_ADC_ENABLED
             value: "true"
           - name: GOOGLE_CLOUD_PROJECT
             value: "<vertex-project-id>"
   ```

5. **Use ADC instead of explicit credentials.** In each Vertex AI or Gemini provider configuration, leave **Service Account JSON** empty. Keep `GOOGLE_VERTEX_AI_WEB_CREDENTIALS` and `GOOGLE_APPLICATION_CREDENTIALS` unset. LangSmith uses explicit JSON credentials instead of ADC when both are present.
