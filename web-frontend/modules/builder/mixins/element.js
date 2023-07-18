import DataLedger from '@baserow/modules/core/dataLedger'
import { resolveFormula } from '@baserow/formula'

export default {
  props: {
    element: {
      type: Object,
      required: true,
    },
    page: {
      type: Object,
      required: true,
    },
    builder: {
      type: Object,
      required: true,
    },
    mode: {
      // editing = being editing by the page editor
      // preview = previewing the application
      // public = publicly published application
      type: String,
      required: false,
      default: '',
    },
  },
  computed: {
    isEditable() {
      return this.mode === 'editing'
    },
  },
  methods: {
    getDataLedger() {
      const { builder, page, element, $registry } = this
      return DataLedger($registry.getAll('builderDataProvider'), {
        builder,
        page,
        element,
      })
    },

    resolveFormula(formula) {
      return resolveFormula(formula, this.getDataLedger())
    },
  },
}
