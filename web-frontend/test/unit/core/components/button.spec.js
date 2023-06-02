import { shallowMount } from '@vue/test-utils'
import Button from '@baserow/modules/core/components/Button'

describe('Button.vue', () => {
  it('renders button text in slot', () => {
    const text = 'Click me'
    const wrapper = shallowMount(Button, {
      slots: {
        default: text,
      },
    })
    expect(wrapper.find('span').text()).toMatch(text)
  })

  it('sets href attribute when passed', () => {
    const href = 'https://example.com'
    const wrapper = shallowMount(Button, {
      propsData: { href },
    })
    expect(wrapper.attributes('href')).toMatch(href)
  })

  it('sets target attribute when passed', () => {
    const target = '_blank'
    const wrapper = shallowMount(Button, {
      propsData: { tag: 'a', target: '_blank' },
    })
    expect(wrapper.attributes('target')).toMatch(target)
  })

  it('emits click event when clicked', () => {
    const wrapper = shallowMount(Button)
    wrapper.vm.$emit('click')
    expect(wrapper.emitted().click).toBeTruthy()
  })

  it('disables button when disabled prop is true', () => {
    const wrapper = shallowMount(Button, {
      propsData: { disabled: true },
    })
    expect(wrapper.attributes('disabled')).toBeTruthy()
  })

  it('renders the correct button type', () => {
    const wrapper = shallowMount(Button, {
      propsData: { type: 'danger' },
    })
    expect(wrapper.classes()).toContain('button--danger')
  })

  it('renders the correct button icon', () => {
    const wrapper = shallowMount(Button, {
      propsData: { icon: 'gitlab-full' },
    })
    expect(wrapper.find('i').classes()).toContain('iconoir-gitlab-full')
  })

  it('shows the loading spinner when loading prop is true', () => {
    const wrapper = shallowMount(Button, {
      propsData: { loading: true },
    })
    expect(wrapper.find('.button--loading').exists()).toBe(true)
  })

  it('adds the active class when active prop is true', () => {
    const wrapper = shallowMount(Button, {
      propsData: { active: true },
    })
    expect(wrapper.classes()).toContain('active')
  })
})
