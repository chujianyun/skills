# Set up composite online evaluators

[Online evaluations](../../../Test/Get%20started/Evaluation%20concepts.md#online-evaluations) provide real-time feedback on your production [traces](../../Trace/Observability%20concepts.md#traces). This is useful to continuously monitor the performance of your application: to identify issues, measure improvements, and ensure consistent quality over time.

[**Composite evaluators**](../../../Test/Evaluators/Evaluator%20types/UI/How%20to%20create%20a%20composite%20evaluator.md) are a way to combine multiple evaluator scores into a single [score](../../../Test/Get%20started/Evaluation%20concepts.md#evaluator-outputs). This is useful when you want to evaluate multiple aspects of your application and combine the results into a single result.

> [!NOTE]
>
> When an online evaluator runs on any run within a trace, the trace will be auto-upgraded to [extended data retention](../../Trace/Configuration%20%26%20troubleshooting/Usage%20and%20billing.md#data-retention-auto-upgrades). This ensures that traces meeting your evaluation criteria (typically those most valuable for analysis) are preserved for investigation.

## View online evaluators

Head to the **Tracing** tab and select a tracing project, or an agent environment. To view existing online evaluators for that project, click on the **Evaluators** tab.

## Configure composite online evaluators

You can create composite evaluators on a [tracing project](../../Trace/Observability%20concepts.md#tracing-projects) for [online evaluations](../../../Test/Get%20started/Evaluation%20concepts.md#online-evaluations). With composite evaluators in the UI, you can compute a weighted average or weighted sum of multiple evaluator scores, with configurable weights.

### 1. Navigate to the tracing project

To start configuring a composite evaluator, navigate to the **Tracing** page and select a tracing project, or an agent environment.

From the tracing project or agent environment view, navigate to the **Evaluators** tab. Click **+ Evaluator** to open the **Add Evaluator** panel. Click **Composite Score** under **Create from scratch**.

### 2. Configure the composite evaluator

1. Name your evaluator.
2. Select an aggregation method, either **Average** or **Sum**.
   * **Average**: ∑(weight\*score) / ∑(weight).
   * **Sum**: ∑(weight\*score).
3. Add the feedback keys you want to include in the composite score.
4. Add the weights for the feedback keys. By default, the weights are equal for each feedback key. Adjust the weights to increase or decrease the importance of specific feedback keys in the final score.
5. Click **Create** to save the evaluator.

> [!TIP]
>
> If you need to adjust the weights for the composite scores, they can be updated after the evaluator is created. The resulting scores will be updated for all runs that have the evaluator configured.

### 3. View composite evaluator results

Composite scores are attached to a run as **feedback**, similarly to feedback from a single evaluator.

**On a tracing project or agent environment**:

* Composite scores appear as feedback on runs.
* [Filter for runs](../../Debug/Viewing%20%26%20managing%20traces/Filter%20traces.md) with a composite score, or where the composite score meets a certain threshold.
* [Create a chart](../Monitoring%20%26%20alerting/Monitor%20projects%20with%20dashboards.md#custom-dashboards) to visualize trends in the composite score over time.

> [!NOTE]
>
> If any of the constituent evaluators are not configured on the run, the composite score will not be calculated for that run.
