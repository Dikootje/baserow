<template>
  <Toast @close="close">
    <template #actions>
      <ButtonText size="small" :loading="loading" :icon="undo" @click="restore">
        {{
          $t('restoreToast.restore', {
            type: $t('trashType.' + toast.data.trash_item_type),
          })
        }}
      </ButtonText>
    </template>
  </Toast>
</template>

<script>
import Toast from '@baserow/modules/core/components/toasts/Toast'
import ButtonText from '@baserow/modules/core/components/ButtonText'
import TrashService from '@baserow/modules/core/services/trash'
import { notifyIf } from '@baserow/modules/core/utils/error'

export default {
  name: 'RestoreToast',
  components: {
    Toast,
    ButtonText,
  },
  props: {
    toast: {
      type: Object,
      required: true,
    },
  },
  data() {
    return {
      loading: false,
      pulsing: true,
    }
  },
  mounted() {
    setTimeout(() => {
      this.close()
    }, 5000)
  },
  methods: {
    close() {
      this.$store.dispatch('toast/remove', this.toast)
    },
    async restore() {
      this.loading = true
      try {
        await TrashService(this.$client).restore(this.toast.data)
      } catch (error) {
        notifyIf(error, 'trash')
      }
      this.close()
      this.loading = false
    },
  },
}
</script>
