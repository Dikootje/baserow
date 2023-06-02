<template>
  <div class="checkbox" :class="classNames" @click="toggle(checked)">
    <button class="checkbox__button">
      <svg
        v-if="checked && !indeterminate && !styleVariant"
        class="checkbox__tick"
        xmlns="http://www.w3.org/2000/svg"
        width="9"
        height="8"
        viewBox="0 0 9 8"
        fill="none"
      >
        <g clip-path="url(#clip0_1138_66)">
          <path
            d="M1.5179 4.4821L3.18211 6.18211L7.42475 2.15368"
            stroke="white"
            stroke-width="2"
            stroke-linecap="round"
            stroke-linejoin="round"
          />
        </g>
        <defs>
          <clipPath id="clip0_1138_66">
            <rect
              width="8"
              height="8"
              fill="white"
              transform="translate(0.5)"
            />
          </clipPath>
        </defs>
      </svg>

      <svg
        v-else-if="checked && indeterminate && !styleVariant"
        class="checkbox__tick-indeterminate"
        xmlns="http://www.w3.org/2000/svg"
        width="8"
        height="8"
        viewBox="0 0 8 8"
        fill="none"
      >
        <path
          d="M1.5 4L6.5 4"
          stroke="white"
          stroke-width="2"
          stroke-linecap="round"
          stroke-linejoin="round"
        />
      </svg>

      <svg
        v-else-if="checked && styleVariant"
        xmlns="http://www.w3.org/2000/svg"
        width="16"
        height="16"
        viewBox="0 0 16 16"
        fill="none"
      >
        <path
          d="M3.33337 8.66663L6.00004 11.3333L12.6667 4.66663"
          stroke="#0D9439"
          stroke-width="1.4"
          stroke-linecap="round"
          stroke-linejoin="round"
        />
      </svg>
    </button>

    <label class="checkbox__label">
      <slot></slot>
    </label>
  </div>
</template>

<script>
export default {
  name: 'Checkbox',
  props: {
    checked: {
      type: Boolean,
      required: false,
      default: false,
    },
    disabled: {
      type: Boolean,
      required: false,
      default: false,
    },
    error: {
      type: Boolean,
      required: false,
      default: false,
    },
    indeterminate: {
      type: Boolean,
      required: false,
      default: false,
    },
    styleVariant: {
      type: Boolean,
      required: false,
      default: false,
    },
  },
  computed: {
    classNames() {
      return {
        'checkbox--disabled': this.disabled,
        'checkbox--checked': this.checked,
        'checkbox--error': this.error,
        'checkbox--variant': this.styleVariant,
      }
    },
  },
  methods: {
    toggle(checked) {
      if (this.disabled) return

      this.$emit('input', !checked)
    },
  },
}
</script>
