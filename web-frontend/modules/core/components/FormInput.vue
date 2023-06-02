<template>
  <FormElement
    :error="hasError"
    class="control"
    :class="{
      'control--horizontal': horizontal,
    }"
  >
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
          'form-input': true,
          'form-input--error': hasError,
          'form-input--monospace': monospace,
          'form-input--icon-left': iconLeft,
          'form-input--icon-right': iconLeft,
          'form-input--loading': loading,
          'form-input--disabled': disabled,
        }"
      >
        <i
          v-if="iconLeft"
          class="form-input__icon form-input__icon-left"
          :class="[`iconoir-${iconLeft}`]"
        />
        <input
          :id="id"
          ref="base_url"
          class="form-input__input"
          :value="fromValue(value)"
          :disabled="disabled"
          :type="type"
          :placeholder="placeholder"
          @blur="$emit('blur', $event)"
          @input="$emit('input', toValue($event.target.value))"
        />

        <i
          v-if="iconRight"
          class="form-input__icon form-input__icon-right"
          :class="[`iconoir-${iconRight}`]"
        />
      </div>
    </div>
    <div class="control__messages">
      <p v-if="helperText" class="control__helper-text">
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
  name: 'FormInput',
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
    type: {
      type: String,
      required: false,
      default: 'text',
    },
    disabled: {
      type: Boolean,
      required: false,
      default: false,
    },
    monospace: {
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
    iconLeft: {
      type: String,
      required: false,
      default: null,
    },
    iconRight: {
      type: String,
      required: false,
      default: null,
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
    hasIcon() {
      return Boolean(this.iconLeft || this.iconRight)
    },
  },
}
</script>
