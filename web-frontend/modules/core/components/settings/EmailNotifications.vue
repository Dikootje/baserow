<template>
  <div>
    <h2 class="box__title">{{ $t('emailNotifications.title') }}</h2>
    <form @submit.prevent="updateEmailNotificationFrequency">
      <FormElement
        :error="fieldHasErrors('email_notifications_frequency')"
        class="control"
      >
        <label class="control__label">
          {{ $t('emailNotifications.label') }}
        </label>
        <div class="control__description">
          {{ $t('emailNotifications.description') }}
        </div>
        <div class="control__elements">
          <Radio
            v-model="values.email_notifications_frequency"
            :value="EMAIL_NOTIFICATIONS_FREQUENCY_OPTIONS.INSTANT"
          >
            {{ $t('emailNotifications.instant') }}
          </Radio>
          <Radio
            v-model="values.email_notifications_frequency"
            :value="EMAIL_NOTIFICATIONS_FREQUENCY_OPTIONS.DAILY"
          >
            {{ $t('emailNotifications.daily') }}
          </Radio>
          <Radio
            v-model="values.email_notifications_frequency"
            :value="EMAIL_NOTIFICATIONS_FREQUENCY_OPTIONS.WEEKLY"
          >
            {{ $t('emailNotifications.weekly') }}
          </Radio>
          <Radio
            v-model="values.email_notifications_frequency"
            :value="EMAIL_NOTIFICATIONS_FREQUENCY_OPTIONS.NEVER"
          >
            {{ $t('emailNotifications.never') }}
          </Radio>
        </div>
      </FormElement>
      <div class="actions actions--right">
        <button
          :class="{ 'button--loading': loading, disabled: submitDisabled }"
          class="button button--large"
          :disabled="submitDisabled"
        >
          {{ $t('emailNotifications.submitButton') }}
        </button>
      </div>
    </form>
  </div>
</template>

<script>
import { mapGetters } from 'vuex'
import { required } from 'vuelidate/lib/validators'
import { EMAIL_NOTIFICATIONS_FREQUENCY_OPTIONS } from '@baserow/modules/core/enums'
import { notifyIf } from '@baserow/modules/core/utils/error'

import form from '@baserow/modules/core/mixins/form'

export default {
  name: 'EmailNotifications',
  mixins: [form],
  data() {
    return {
      loading: false,
      allowedValues: ['email_notifications_frequency'],
      values: {
        email_notifications_frequency:
          EMAIL_NOTIFICATIONS_FREQUENCY_OPTIONS.INSTANT,
      },
    }
  },
  computed: {
    submitDisabled() {
      return (
        this.loading ||
        this.values.email_notifications_frequency ===
          this.user.email_notifications_frequency
      )
    },
    EMAIL_NOTIFICATIONS_FREQUENCY_OPTIONS() {
      return EMAIL_NOTIFICATIONS_FREQUENCY_OPTIONS
    },
    ...mapGetters({
      user: 'auth/getUserObject',
    }),
  },
  mounted() {
    this.setInitialValue()
  },
  methods: {
    setInitialValue() {
      const emailNotificationFreq = this.user.email_notifications_frequency
      if (emailNotificationFreq) {
        this.values.email_notifications_frequency = emailNotificationFreq
      }
    },
    async updateEmailNotificationFrequency() {
      this.loading = true
      try {
        await this.$store.dispatch('auth/update', {
          first_name: this.user.first_name,
          email_notifications_frequency:
            this.values.email_notifications_frequency,
        })
      } catch (error) {
        notifyIf(error, 'settings.')
        this.setInitialValue()
      }
      this.loading = false
    },
  },
  validations: {
    values: {
      email_notifications_frequency: {
        required,
      },
    },
  },
}
</script>
