import { StoreItemLookupError } from '@baserow/modules/core/errors'
import { BuilderApplicationType } from '@baserow/modules/builder/applicationTypes'
import PageService from '@baserow/modules/builder/services/page'
import { generateHash } from '@baserow/modules/core/utils/hashing'

export function populatePage(page) {
  return {
    ...page,
    _: {
      selected: false,
    },
  }
}

const state = {
  // Holds the value of which page is currently selected
  selected: {},
  deviceTypeSelected: null,
  // A job object that tracks the progress of a page duplication currently running
  duplicateJob: null,
}

const mutations = {
  ADD_ITEM(state, { builder, page }) {
    populatePage(page)
    builder.pages.push(page)
  },
  UPDATE_ITEM(state, { page, values }) {
    Object.assign(page, page, values)
  },
  DELETE_ITEM(state, { builder, id }) {
    const index = builder.pages.findIndex((item) => item.id === id)
    builder.pages.splice(index, 1)
  },
  SET_SELECTED(state, { builder, page }) {
    Object.values(builder.pages).forEach((item) => {
      item._.selected = false
    })
    page._.selected = true
    state.selected = page
  },
  UNSELECT(state) {
    if (state.selected) {
      state.selected._.selected = false
    }
    state.selected = {}
  },
  SET_DUPLICATE_JOB(state, job) {
    state.duplicateJob = job
  },
  ORDER_PAGES(state, { builder, order, isHashed = false }) {
    builder.pages.forEach((page) => {
      const pageId = isHashed ? generateHash(page.id) : page.id
      const index = order.findIndex((value) => value === pageId)
      page.order = index === -1 ? 0 : index + 1
    })
  },
  SET_DEVICE_TYPE_SELECTED(state, deviceType) {
    state.deviceTypeSelected = deviceType
  },
}

const actions = {
  forceUpdate({ commit }, { page, values }) {
    commit('UPDATE_ITEM', { page, values })
  },
  forceCreate({ commit }, { builder, page }) {
    commit('ADD_ITEM', { builder, page })
  },
  async selectById({ commit, dispatch }, { builderId, pageId }) {
    const builder = await dispatch('application/selectById', builderId, {
      root: true,
    })
    const type = BuilderApplicationType.getType()

    // Check if the just selected application is a builder
    if (builder.type !== type) {
      throw new StoreItemLookupError(
        `The application doesn't have the required ${type} type.`
      )
    }

    // Check if the provided page id is found in the just selected builder.
    const index = builder.pages.findIndex((item) => item.id === pageId)
    if (index === -1) {
      throw new StoreItemLookupError(
        'The page is not found in the selected application.'
      )
    }
    const page = builder.pages[index]

    commit('SET_SELECTED', { builder, page })

    // Unselect previously selected element
    dispatch(
      'element/select',
      {
        element: null,
      },
      { root: true }
    )

    return { builder, page }
  },
  unselect({ commit }) {
    commit('UNSELECT')
  },
  forceDelete({ commit }, { builder, page }) {
    if (page._.selected) {
      // Redirect back to the dashboard because the page doesn't exist anymore.
      this.$router.push({ name: 'dashboard' })
    }

    commit('DELETE_ITEM', { builder, id: page.id })
  },
  async create({ commit, dispatch }, { builder, name, path, pathParams }) {
    const { data: page } = await PageService(this.$client).create(
      builder.id,
      name,
      path,
      pathParams
    )

    commit('ADD_ITEM', { builder, page })

    await dispatch('selectById', { builderId: builder.id, pageId: page.id })

    return page
  },
  async update({ dispatch }, { builder, page, values }) {
    const { data } = await PageService(this.$client).update(page.id, values)

    const update = Object.keys(values).reduce((result, key) => {
      result[key] = data[key]
      return result
    }, {})

    await dispatch('forceUpdate', { builder, page, values: update })
  },
  async delete({ dispatch }, { builder, page }) {
    await PageService(this.$client).delete(page.id)

    await dispatch('forceDelete', { builder, page })
  },
  async order(
    { commit, getters },
    { builder, order, oldOrder, isHashed = false }
  ) {
    commit('ORDER_PAGES', { builder, order, isHashed })

    try {
      await PageService(this.$client).order(builder.id, order)
    } catch (error) {
      commit('ORDER_PAGES', { builder, order: oldOrder, isHashed })
      throw error
    }
  },
  setDeviceTypeSelected({ commit }, deviceType) {
    commit('SET_DEVICE_TYPE_SELECTED', deviceType)
  },
  async duplicate({ commit, dispatch }, { page }) {
    const { data: job } = await PageService(this.$client).duplicate(page.id)

    await dispatch('job/create', job, { root: true })

    commit('SET_DUPLICATE_JOB', job)
  },
}

const getters = {
  getSelected(state) {
    return state.selected
  },
  getDeviceTypeSelected(state) {
    return state.deviceTypeSelected
  },
  getDuplicateJob(state) {
    return state.duplicateJob
  },
}

export default {
  namespaced: true,
  state,
  getters,
  actions,
  mutations,
}
