import { mount } from '@vue/test-utils'
import SwitchInput from '@baserow/modules/core/components/SwitchInput.vue'

describe('SwitchInput', () => {
  it('emits an input event when clicked', async () => {
    const wrapper = mount(SwitchInput, {
      propsData: {
        checked: false,
      },
    })

    await wrapper.find('.switch').trigger('click')

    expect(wrapper.emitted('input')).toBeTruthy()
    expect(wrapper.emitted('input')[0]).toEqual([true])
  })

  it('does not emit an input event when clicked and disabled', async () => {
    const wrapper = mount(SwitchInput, {
      propsData: {
        checked: false,
        disabled: true,
      },
    })

    await wrapper.find('.switch').trigger('click')

    expect(wrapper.emitted('input')).toBeFalsy()
  })

  it('renders a small style when small prop is true', () => {
    const wrapper = mount(SwitchInput, {
      propsData: {
        small: true,
      },
    })

    expect(wrapper.find('.switch--small').exists()).toBe(true)
  })

  it('renders a disabled style when disabled prop is true', () => {
    const wrapper = mount(SwitchInput, {
      propsData: {
        disabled: true,
      },
    })

    expect(wrapper.find('.switch--disabled').exists()).toBe(true)
  })

  it('renders an active style when checked prop is true', () => {
    const wrapper = mount(SwitchInput, {
      propsData: {
        checked: true,
      },
    })

    expect(wrapper.find('.active').exists()).toBe(true)
  })
})
