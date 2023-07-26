from typing import TYPE_CHECKING, Any

from baserow.core.utils import to_path
from baserow.formula.types import FormulaContext

if TYPE_CHECKING:
    from baserow.core.formula.registries import DataProviderTypeRegistry


class RuntimeFormulaContext(FormulaContext):
    """
    The data ledger holds all the data useful for the formula resolution. It uses a
    Data provider registry to fulfill data queries. Each data provider is responsible
    for a slice of data.
    """

    def __init__(self, registry: "DataProviderTypeRegistry", **kwargs):
        """
        Loads the context for each data provider from the extra context given to the
        constructor.

        :param registry: The registry that registers the available data providers that
            can be used by this data ledger instance.
        :param kwargs: extra elements are given to the data providers to extract data.
        """

        self.registry = registry
        self.application_context = {**kwargs}

    def __getitem__(self, key: str) -> Any:
        """
        Mimics a simple get item interface but for complex dotted path. The first part
        of the path is the data provider to call to get the actual piece of data.

        For instance:
        - `data_source.My source.url` should return the `url` property of `My source`
            data source.
        - `page_parameter.id` should return the page parameter named `id`
        - `current_node.input.id` should return the `id` property of the input of the
            current node.

        :param key: the dotted path of the data.
        :return: the value for this path.
        """

        provider_name, *rest = to_path(key)
        data_provider_type = self.registry.get(provider_name)
        return data_provider_type.get_data_chunk(
            self,
            rest,
        )
