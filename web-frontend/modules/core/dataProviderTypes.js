import { Registerable } from '@baserow/modules/core/registry'

/**
 * A data provider gets data from the application context and populate the context for
 * the formula resolver.
 */
export class DataProviderType extends Registerable {
  get name() {
    throw new Error('`name` must be set on the dataProviderType.')
  }

  /**
   * Should be true if the data provider needs backend context during its
   * initialisation phase.
   */
  get needBackendContext() {
    return false
  }

  /**
   * Initialize the data needed by the data provider if necessary. Used during the
   * page init phase to collect all the data for the first display.
   */
  async init(RuntimeFormulaContext) {}

  /**
   * Should return the context needed to be send to the backend for each dataProvider
   * to be able to solve the formulas on the backend.
   * @returns An object if the dataProvider wants to send something to the backend.
   */
  getBackendContext(RuntimeFormulaContext) {
    return null
  }

  /**
   * Returns the actual data.
   * @param {object} RuntimeFormulaContext the data ledger instance.
   * @param {Array<str>} path the path of the data we want to get
   */
  getDataChunk(RuntimeFormulaContext, path) {
    throw new Error('.getDataChunk() must be set on the dataProviderType.')
  }

  getOrder() {
    return 0
  }
}
