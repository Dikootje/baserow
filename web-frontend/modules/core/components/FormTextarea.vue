<template>
  <FormElement :error="hasError" class="control">
    <label
      v-if="label"
      :for="id"
      class="control__label"
      :class="{ 'control__label--small': smallLabel }"
    >
      <span class="control__label-label">{{ label }} </span>
      <span v-if="!required" class="control__required">Optional</span>
    </label>
    <div class="control__elements">
      <div
        :class="{
          'form-textarea': true,
          'form-textarea--error': hasError,
          'form-textarea--disabled': disabled,
        }"
      >
        <textarea
          :id="id"
          ref="base_url"
          class="form-textarea__textarea"
          :value="fromValue(value)"
          :disabled="disabled"
          :placeholder="placeholder"
          @blur="$emit('blur', $event)"
          @input="$emit('input', toValue($event.target.value))"
        />
      </div>
    </div>
    <div class="control__messages">
      <p v-if="helperText">
        {{ helperText }}
      </p>
      <p v-if="hasError" class="error">
        {{ error }}
      </p>
    </div>
  </FormElement>
</template>

<script>
export default {
  name: 'FormTextarea',
  props: {
    id: {
      type: String,
      required: true,
    },
    error: {
      type: String,
      required: false,
      default: null,
    },
    label: {
      type: String,
      required: false,
      default: null,
    },
    placeholder: {
      type: String,
      required: false,
      default: null,
    },
    value: {
      required: true,
      validator: (value) => true,
    },
    toValue: {
      type: Function,
      required: false,
      default: (value) => value,
    },
    fromValue: {
      type: Function,
      required: false,
      default: (value) => value,
    },
    disabled: {
      type: Boolean,
      required: false,
      default: false,
    },
    smallLabel: {
      type: Boolean,
      required: false,
      default: false,
    },
    loading: {
      type: Boolean,
      required: false,
      default: false,
    },
    required: {
      type: Boolean,
      required: false,
      default: false,
    },
    helperText: {
      type: String,
      required: false,
      default: null,
    },
  },
  computed: {
    hasError() {
      return Boolean(this.error)
    },
  },
}
</script>
