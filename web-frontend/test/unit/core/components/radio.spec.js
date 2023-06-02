import { mount } from '@vue/test-utils'
import Radio from '@baserow/modules/core/components/Radio.vue'

describe('Radio', () => {
  it('renders the radio button correctly', () => {
    const wrapper = mount(Radio, {
      propsData: {
        id: 'option-1',
        value: 'option-1',
      },
      slots: {
        default: 'Option 1',
      },
    })

    expect(wrapper.find('input[type="radio"]').exists()).toBeTruthy()
    expect(wrapper.find('.radio__label').text()).toBe('Option 1')
  })

  it('emits input event when clicked', () => {
    const wrapper = mount(Radio, {
      propsData: {
        id: 'radio-1',
        name: 'radio-group',
        value: 'option-1',
      },
    })
    wrapper.vm.$emit('input', 'option-1')

    expect(wrapper.emitted().input).toBeTruthy()
    expect(wrapper.emitted().input[0]).toEqual(['option-1'])
  })

  it('disables the radio when disabled prop is true', () => {
    const wrapper = mount(Radio, {
      propsData: {
        id: 'radio-1',
        name: 'radio-group',
        value: 'option-1',
        disabled: true,
      },
    })

    expect(wrapper.find('input').attributes('disabled')).toBe('disabled')
  })

  it('shows loading indicator when loading prop is true', () => {
    const wrapper = mount(Radio, {
      propsData: {
        id: 'radio-1',
        name: 'radio-group',
        value: 'option-1',
        loading: true,
      },
    })

    expect(wrapper.find('.radio__loading').exists()).toBe(true)
  })
})
