# Schedules

> Configure schedules to run your Fleet agents on a recurring basis.

Schedules run your agent on a recurring time-based schedule. Use schedules when your agent needs to do work proactively, not just in response to a message or event.

Common use cases include:

* **Daily briefings**: Summarize emails, calendar events, or Slack activity each morning.
* **Memory synthesis**: Periodically review and consolidate the agent's memory files to keep context clean and relevant.
* **Proactive outreach**: Draft weekly status updates, follow-up reminders, or recurring reports.
* **Data monitoring**: Check dashboards, metrics, or feeds on a set cadence and surface anything noteworthy.

> [!TIP]
>
> To start an agent based on an event (such as a Slack message or email), use [channels](Channels.md) instead.

## Add a schedule

To add a schedule:

1. In the **Schedules** section, click **+ Add**.

2. Select when the schedule should run.

   > [!NOTE]
   >
   > Schedules are in UTC. Convert your desired execution time to UTC when configuring the schedule.

3. (Optional) Add a **Prompt**. With a custom prompt, you can tell the agent what to do on each scheduled run. For example:

   * "Summarize my unread emails from the last 24 hours and post a digest to #team-updates in Slack."
   * "Review your memory files and consolidate any redundant or outdated entries."

4. Click **Create schedule**.

5. Click **Save changes**.
