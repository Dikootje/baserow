import { mount } from '@vue/test-utils'
import Tab from '@baserow/modules/core/components/Tab'

describe('Tab', () => {
  it('renders the title and content when active', () => {
    const title = 'Tab 1'
    const content = 'Tab 1 content'

    const wrapper = mount(Tab, {
      slots: {
        default: content,
      },
      data() {
        return {
          isActive: true,
        }
      },
      propsData: {
        title,
      },
    })

    expect(wrapper.text()).toBe(content)
  })
})
