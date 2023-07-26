import { Registerable } from '@baserow/modules/core/registry'

export class IntegrationType extends Registerable {
  get name() {
    throw new Error('Must be set on the type.')
  }

  /**
   * The image associated to this integration.
   */
  get image() {
    throw new Error('Must be set on the type.')
  }

  /**
   * Return a summary describing the integration in one sentence.
   *
   * @param {object} integration The integration we want the summary for.
   * @param {object} workspace The workspace we want the summary for.
   * @returns A string description.
   */
  getSummary(integration, workspace) {
    return this.name
  }

  /**
   * The form to edit this integration.
   */
  get formComponent() {
    return null
  }

  /**
   * An optional warning to display when creating or editing this integration.
   @param {object} integration: The integration we may warn the user about.
   @param {object} workspace The workspace record, in case it's needed.
   @returns An optional warning.
   */
  getWarning(integration, workspace) {
    return ''
  }

  /**
   * Default values on integration creation.
   *
   * @returns an object with the default values.
   */
  getDefaultValues() {
    return {}
  }

  getOrder() {
    return 0
  }

  /**
   * Retrieves the authorized user profile.
   * @param {object} integration The integration we pluck out the auth user from.
   * @param {object} workspace The workspace the auth user belongs to.
   */
  getAuthorizedUser(integration, workspace) {
    return workspace.users.find(
      (user) => user.id === integration.authorized_user
    )
  }
}
