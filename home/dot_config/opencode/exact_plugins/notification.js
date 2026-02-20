export const NotificationPlugin = async ({ project, client, $, directory, worktree }) => {
  return {
    event: async ({ event }) => {
      if (
        event.type === "session.idle" ||
        event.type === "permission.asked"
      ) {
        await $`osascript -e 'display notification "OpenCode needs your attention" with title "OpenCode"'`
      }
    },
  }
}
