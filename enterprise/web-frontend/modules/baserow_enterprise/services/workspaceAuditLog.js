import baseService from '@baserow/modules/core/crudTable/baseService'
import jobService from '@baserow/modules/core/services/job'

export default (client, workspaceId) => {
  return Object.assign(
    baseService(client, `/workspaces/${workspaceId}/audit-log/`),
    {
      fetchUsers(page, search) {
        const usersUrl = `/workspaces/${workspaceId}/audit-log/users/`
        const userPaginatedService = baseService(client, usersUrl)
        return userPaginatedService.fetch(usersUrl, page, search, [], [])
      },
      fetchActionTypes(page, search) {
        const actionTypesUrl = `/workspaces/${workspaceId}/audit-log/action-types/`
        const actionTypePaginatedService = baseService(client, actionTypesUrl)
        return actionTypePaginatedService.fetch(
          actionTypesUrl,
          page,
          search,
          [],
          []
        )
      },
      startExportCsvJob(data) {
        return client.post(`/workspaces/${workspaceId}/audit-log/export/`, data)
      },
      getExportJobInfo(jobId) {
        return jobService(client).get(jobId)
      },
      async getLastExportJobs(maxCount = 3) {
        const { data } = await jobService(client).fetchAll({
          states: ['!failed'],
        })
        const jobs = data.jobs || []
        return jobs
          .filter((job) => job.type === 'audit_log_export')
          .slice(0, maxCount)
      },
    }
  )
}
