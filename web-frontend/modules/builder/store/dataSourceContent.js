import _ from 'lodash'

const state = {
  // The data source loaded content.
  dataSourceContents: {},
}

const mutations = {
  SET_CONTENT(state, { dataSource, value }) {
    if (!state.dataSourceContents[dataSource.id]) {
      // Here we need to change the reference of the dataSourceContents object to
      // trigger computed values that use it in some situation (before the key exists
      // for instance)
      state.dataSourceContents = {
        ...state.dataSourceContents,
        [dataSource.id]: value,
      }
    } else if (!_.isEqual(state.dataSourceContents[dataSource.id], value)) {
      state.dataSourceContents[dataSource.id] = value
    }
  },
}

const actions = {
  setDataSourceContent({ commit }, { dataSource, value }) {
    commit('SET_CONTENT', { dataSource, value })
  },
}

const getters = {
  getDataSourceContents: (state) => {
    return state.dataSourceContents
  },
}

export default {
  namespaced: true,
  state,
  getters,
  actions,
  mutations,
}
