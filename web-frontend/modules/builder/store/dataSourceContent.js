import _ from 'lodash'
import DataSourceService from '@baserow/modules/builder/services/dataSource'
import { clone } from '@baserow/modules/core/utils/object'

const state = {
  // The data source loaded content.
  contents: {},
}

const fetchContext = {}

const mutations = {
  SET_CONTENT(state, { dataSource, value }) {
    if (!state.contents[dataSource.id]) {
      // Here we need to change the reference of the dataSourceContents object to
      // trigger computed values that use it in some situation (before the key exists
      // for instance)
      state.contents = {
        ...state.contents,
        [dataSource.id]: value,
      }
    } else if (!_.isEqual(state.contents[dataSource.id], value)) {
      state.contents[dataSource.id] = value
    }
  },
  CLEAR_CONTENTS(state) {
    state.contents = {}
  },
}

const actions = {
  /**
   * Fetch the data from the server and add them to the store.
   * @param {object} dataSource the data source we want to dispatch
   * @param {object} data the query body
   */
  async fetchDataSourceContent({ commit }, { dataSource, data: queryData }) {
    try {
      const { data } = await DataSourceService(this.app.$client).dispatch(
        dataSource.id,
        queryData
      )
      if (!fetchContext[dataSource.id]) {
        fetchContext[dataSource.id] = {
          fetchTimeout: null,
          lastDataSource: null,
          lastQueryData: null,
        }
      }
      commit('SET_CONTENT', { dataSource, value: data })
    } catch (e) {
      commit('SET_CONTENT', { dataSource, value: null })
    } finally {
      fetchContext[dataSource.id].lastDataSource = clone(dataSource)
      fetchContext[dataSource.id].lastQueryData = clone(queryData)
    }
  },

  /**
   * Fetches the data from the server and add them to the store only when needed.
   * It's necessary when it's the first call (the store is empty) and when the
   * configuration or the body content has changed.
   * @param {object} dataSource the data source we want to dispatch
   * @param {object} data the query body
   */
  async smartFetchDataSourceContent(
    { dispatch },
    { dataSource, data: queryData }
  ) {
    let firstFetch = false
    if (!fetchContext[dataSource.id]) {
      fetchContext[dataSource.id] = {
        fetchTimeout: null,
        lastDataSource: null,
        lastQueryData: null,
      }
      firstFetch = true
    }

    const fetch = async () => {
      const { lastDataSource, lastQueryData } = fetchContext[dataSource.id]
      // We want to update the content only if the dataSource configuration or the query
      // parameters have changed.
      if (
        !_.isEqual(lastDataSource, dataSource) ||
        !_.isEqual(lastQueryData, queryData)
      ) {
        await dispatch('fetchDataSourceContent', {
          dataSource,
          data: queryData,
        })
      }
    }

    if (firstFetch) {
      // We execute the first call immediately to have the data ASAP
      await fetch()
    } else {
      // Then subsequent calls are debounced by 500ms
      clearTimeout(fetchContext[dataSource.id].fetchTimeout)
      fetchContext[dataSource.id].fetchTimeout = setTimeout(fetch, 500)
    }
  },

  clearDataSourceContents({ commit }) {
    commit('CLEAR_CONTENTS')
  },
}

const getters = {
  getDataSourceContents: (state) => {
    return state.contents
  },
}

export default {
  namespaced: true,
  state,
  getters,
  actions,
  mutations,
}
