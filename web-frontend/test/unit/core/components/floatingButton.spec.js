import { shallowMount } from '@vue/test-utils'
import FloatingButton from '@baserow/modules/core/components/FloatingButton'

describe('FloatingButton.vue', () => {
  it('renders the button with the correct class when type prop is provided', () => {
    const type = 'secondary'
    const wrapper = shallowMount(FloatingButton, {
      propsData: { type },
    })
    expect(wrapper.classes()).toContain(`floating-button--${type}`)
  })

  it('renders the button with the correct icon', () => {
    const icon = 'plus'
    const wrapper = shallowMount(FloatingButton, {
      propsData: { icon },
    })
    expect(wrapper.find('.floating-button__icon').classes()).toContain(
      `iconoir-${icon}`
    )
  })

  it('disables the button when disabled prop is true', () => {
    const wrapper = shallowMount(FloatingButton, {
      propsData: { disabled: true },
    })
    expect(wrapper.classes()).toContain('disabled')
  })

  it('activates the button when active prop is true', () => {
    const wrapper = shallowMount(FloatingButton, {
      propsData: { active: true },
    })
    expect(wrapper.classes()).toContain('active')
  })

  it('renders the button with the correct position when position prop is provided', () => {
    const position = 'fixed'
    const wrapper = shallowMount(FloatingButton, {
      propsData: { position },
    })
    expect(wrapper.classes()).toContain(`floating-button--${position}`)
  })

  it('emits the click event when clicked', () => {
    const wrapper = shallowMount(FloatingButton)
    wrapper.vm.$emit('click')
    expect(wrapper.emitted().click).toBeTruthy()
  })
})
