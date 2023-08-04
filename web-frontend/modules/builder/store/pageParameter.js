const state = {
  // The parameter values
}

const mutations = {
  SET_PARAMETER(state, { page, name, value }) {
    page.parameters = { ...page.parameters, [name]: value }
  },
}

const actions = {
  setParameter({ commit }, { page, name, value }) {
    commit('SET_PARAMETER', { page, name, value })
  },
}

const getters = {
  getParameters: (state) => (page) => {
    return page.parameters
  },
}

export default {
  namespaced: true,
  state,
  getters,
  actions,
  mutations,
}
