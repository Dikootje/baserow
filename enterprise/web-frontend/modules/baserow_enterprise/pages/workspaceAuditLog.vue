<template>
  <div class="audit-log__table">
    <AuditLogExportModal
      ref="exportModal"
      :filters="filters"
      :service="service"
      :workspace-id="workspace.id"
    ></AuditLogExportModal>
    <CrudTable
      :columns="columns"
      :filters="filters"
      :default-column-sorts="[{ key: 'timestamp', direction: 'asc' }]"
      :service="service"
      :enable-search="false"
      row-id-key="id"
    >
      <template #title>
        {{
          $t('workspaceAuditLog.title', {
            workspaceName: workspace.name,
            workspaceId: workspace.id,
          })
        }}
      </template>
      <template #header-right-side>
        <button
          class="button button--large"
          @click.prevent="$refs.exportModal.show()"
        >
          {{ $t('workspaceAuditLog.exportToCsv') }}
        </button>
      </template>
      <template #header-filters>
        <div class="audit-log__filters audit-log__filters--workspace">
          <FilterWrapper :name="$t('workspaceAuditLog.filterUserTitle')">
            <PaginatedDropdown
              ref="userFilter"
              :value="filters.user_id"
              :fetch-page="fetchUsers"
              :empty-item-display-name="$t('workspaceAuditLog.allUsers')"
              :not-selected-text="$t('workspaceAuditLog.allUsers')"
              @input="filterUser"
            ></PaginatedDropdown>
          </FilterWrapper>
          <FilterWrapper :name="$t('workspaceAuditLog.filterActionTypeTitle')">
            <PaginatedDropdown
              ref="typeFilter"
              :value="filters.action_type"
              :fetch-page="fetchActionTypes"
              :empty-item-display-name="$t('workspaceAuditLog.allActionTypes')"
              :not-selected-text="$t('workspaceAuditLog.allActionTypes')"
              @input="filterActionType"
            ></PaginatedDropdown>
          </FilterWrapper>
          <FilterWrapper
            :name="$t('workspaceAuditLog.filterFromTimestampTitle')"
          >
            <DateFilter
              ref="fromTimestampFilter"
              :placeholder="$t('workspaceAuditLog.filterFromTimestamp')"
              :disable-dates="disableDates"
              @input="filterFromTimestamp"
            ></DateFilter>
          </FilterWrapper>
          <FilterWrapper :name="$t('workspaceAuditLog.filterToTimestampTitle')">
            <DateFilter
              ref="toTimestampFilter"
              :placeholder="$t('workspaceAuditLog.filterToTimestamp')"
              :disable-dates="disableDates"
              @input="filterToTimestamp"
            ></DateFilter>
          </FilterWrapper>
          <button
            class="audit-log__clear_filters_button button button--ghost"
            @click="clearFilters"
          >
            {{ $t('workspaceAuditLog.clearFilters') }}
          </button>
        </div>
      </template>
    </CrudTable>
  </div>
</template>

<script>
import _ from 'lodash'
import { mapGetters } from 'vuex'
import moment from '@baserow/modules/core/moment'
import CrudTable from '@baserow/modules/core/components/crudTable/CrudTable'
import PaginatedDropdown from '@baserow/modules/core/components/PaginatedDropdown'
import WorkspaceAuditLogService from '@baserow_enterprise/services/workspaceAuditLog'
import DateFilter from '@baserow_enterprise/components/crudTable/filters/DateFilter'
import FilterWrapper from '@baserow_enterprise/components/crudTable/filters/FilterWrapper'
import SimpleField from '@baserow/modules/core/components/crudTable/fields/SimpleField'
import LocalDateField from '@baserow/modules/core/components/crudTable/fields/LocalDateField'
import CrudTableColumn from '@baserow/modules/core/crudTable/crudTableColumn'
import LongTextField from '@baserow_enterprise/components/crudTable/fields/LongTextField'
import AuditLogExportModal from '@baserow_enterprise/components/admin/modals/AuditLogExportModal'
import EnterpriseFeatures from '@baserow_enterprise/features'

export default {
  name: 'WorkspaceAuditLog',
  components: {
    AuditLogExportModal,
    CrudTable,
    PaginatedDropdown,
    DateFilter,
    FilterWrapper,
  },
  layout: 'app',
  middleware: 'authenticated',
  asyncData({ store, error, route, app }) {
    if (!app.$hasFeature(EnterpriseFeatures.AUDIT_LOG)) {
      return error({
        statusCode: 401,
        message: 'Available in Enterprise version',
      })
    }

    const workspaceId = parseInt(route.params.workspaceId)
    const workspace = store.getters['workspace/get'](workspaceId)
    if (
      !app.$hasPermission(
        'workspace.list_audit_log_entries',
        workspace,
        workspaceId
      )
    ) {
      error({ statusCode: 404, message: 'Page not found' })
    }
    return { workspace }
  },
  data() {
    this.columns = [
      new CrudTableColumn(
        'user',
        () => this.$t('workspaceAuditLog.user'),
        SimpleField,
        true,
        false,
        false,
        {},
        '15'
      ),
      new CrudTableColumn(
        'type',
        () => this.$t('workspaceAuditLog.actionType'),
        SimpleField,
        true,
        false,
        false,
        {},
        '10'
      ),
      new CrudTableColumn(
        'description',
        () => this.$t('workspaceAuditLog.description'),
        LongTextField,
        false,
        false,
        false,
        {},
        '40'
      ),
      new CrudTableColumn(
        'timestamp',
        () => this.$t('workspaceAuditLog.timestamp'),
        LocalDateField,
        true,
        false,
        false,
        { dateTimeFormat: 'L LTS' },
        '10'
      ),
      new CrudTableColumn(
        'ip_address',
        () => this.$t('workspaceAuditLog.ip_address'),
        SimpleField,
        true,
        false,
        false,
        {},
        '10'
      ),
    ]

    const workspaceId = parseInt(this.$route.params.workspaceId)
    this.service = WorkspaceAuditLogService(this.$client, workspaceId)

    return {
      filters: {},
      dateTimeFormat: 'YYYY-MM-DDTHH:mm:ss.SSSZ',
    }
  },
  computed: {
    disableDates() {
      const minimumDate = moment('2023-01-01', 'YYYY-MM-DD')
      const maximumDate = moment().add(1, 'day').endOf('day')
      return {
        to: minimumDate.toDate(),
        from: maximumDate.toDate(),
      }
    },
    ...mapGetters({
      selectedWorkspaceId: 'workspace/selectedId',
    }),
  },
  watch: {
    selectedWorkspaceId(newValue, oldValue) {
      if (newValue !== oldValue) {
        this.$router.push({
          name: 'workspace-audit-log',
          params: { workspaceId: newValue },
        })
      }
    },
  },
  methods: {
    clearFilters() {
      for (const filterRef of [
        'userFilter',
        'typeFilter',
        'fromTimestampFilter',
        'toTimestampFilter',
      ]) {
        this.$refs[filterRef].clear()
      }
      this.filters = {}
    },
    setFilter(key, value) {
      if (value == null) {
        if (this.filters[key] !== undefined) {
          this.filters = _.pickBy(this.filters, (v, k) => {
            return key !== k
          })
        }
      } else {
        this.filters = { ...this.filters, [key]: value }
      }
    },
    filterUser(userId) {
      this.setFilter('user_id', userId)
    },
    fetchUsers(page, search) {
      return this.service.fetchUsers(page, search)
    },
    fetchActionTypes(page, search) {
      return this.service.fetchActionTypes(page, search)
    },
    filterActionType(actionTypeId) {
      this.setFilter('action_type', actionTypeId)
    },
    filterFromTimestamp(fromTimestamp) {
      if (fromTimestamp && moment(fromTimestamp).isValid()) {
        this.setFilter(
          'from_timestamp',
          moment(fromTimestamp).startOf('day').format(this.dateTimeFormat)
        )
      } else if (!fromTimestamp) {
        this.setFilter('from_timestamp', null)
      }
    },
    filterToTimestamp(toTimestamp) {
      if (toTimestamp && moment(toTimestamp).isValid()) {
        this.setFilter(
          'to_timestamp',
          moment(toTimestamp).endOf('day').format(this.dateTimeFormat)
        )
      } else if (!toTimestamp) {
        this.setFilter('to_timestamp', null)
      }
    },
  },
}
</script>
