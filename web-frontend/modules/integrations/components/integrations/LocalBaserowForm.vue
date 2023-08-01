<template>
  <div>
    <FormElement class="control">
      <label class="control__label">{{
        $t('localBaserowForm.chooseAuthorizedUserLabel')
      }}</label>
      <Dropdown
        v-model="values.authorized_user"
        class="local-baserow-form__authorized_user-dropdown"
        :placeholder="$t('localBaserowForm.chooseAuthorizedUserPlaceholder')"
      >
        <DropdownItem
          v-for="user in workspace_users"
          :key="user.id"
          :name="user.name"
          :value="user.id"
        >
          {{ user.name }}
          <Badge
            v-if="user.permissions !== 'ADMIN'"
            warning
            class="margin-left-1"
            >{{
              $t(
                `roles.${permissionSanitized(
                  user.permissions
                ).toLowerCase()}.name`
              )
            }}</Badge
          >
        </DropdownItem>
        <template #emptyState>{{
          $t('localBaserowForm.noValidUsers')
        }}</template>
      </Dropdown>
      <p v-if="values.authorized_user" class="margin-top-2">
        {{
          $t('localBaserowForm.authorizedUserConfirmation', {
            name: getAuthorizedUserDisplayName,
          })
        }}
      </p>
    </FormElement>
  </div>
</template>

<script>
import form from '@baserow/modules/core/mixins/form'

export default {
  mixins: [form],
  props: {
    application: {
      type: Object,
      required: true,
    },
    workspace: {
      type: Object,
      required: true,
    },
  },
  data() {
    return {
      workspace_users: [],
      values: {
        authorized_user: null,
      },
      allowedValues: ['authorized_user'],
    }
  },
  computed: {
    roles() {
      return this.workspace ? this.workspace._.roles : []
    },
    getAuthorizedUserDisplayName() {
      const authorizedUser = this.workspace_users.find(
        (user) => user.id === this.values.authorized_user
      )
      return authorizedUser ? authorizedUser.name : ''
    },
  },
  created() {
    this.workspace_users = this.workspace.users.filter(
      (user) => user.to_be_deleted === false
    )
  },
  methods: {
    permissionSanitized(uid) {
      const permission = this.roles.find((role) => role.uid === uid)
      return permission ? permission.uid : 'MEMBER'
    },
  },
}
</script>
