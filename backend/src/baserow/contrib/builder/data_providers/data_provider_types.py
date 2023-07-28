from typing import List, Union

from baserow.contrib.builder.data_sources.exceptions import (
    DataSourceImproperlyConfigured,
)
from baserow.core.formula.registries import DataProviderType
from baserow.core.formula.runtime_formula_context import RuntimeFormulaContext
from baserow.core.services.handler import ServiceHandler
from baserow.core.utils import get_nested_value_from_dict


class PageParameterDataProviderType(DataProviderType):
    """
    This data provider reads page parameter information from the data sent by the
    frontend during the dispatch. The data are then available for the formulas.
    """

    type = "page_parameter"

    def get_data_chunk(
        self, runtime_formula_context: RuntimeFormulaContext, path: List[str]
    ) -> Union[int, str]:
        """
        When a page parameter is read, returns the value previously saved from the
        request object.
        """

        if "request" not in runtime_formula_context.application_context:
            return None

        if len(path) != 1:
            return None

        first_part = path[0]

        return (
            runtime_formula_context.application_context["request"]
            .data.get("page_parameter", {})
            .get(first_part, None)
        )


class DataSourceDataProviderType(DataProviderType):
    """
    The data source provider can read data from registered page data sources.
    """

    type = "data_source"

    def get_data_source(self, runtime_formula_context, data_source_name):
        for data_source in runtime_formula_context.application_context["data_sources"]:
            if data_source.name == data_source_name:
                return data_source

        raise DataSourceImproperlyConfigured(
            f"Data source with name {data_source_name} doesn't exist"
        )

    def get_data_chunk(
        self, runtime_formula_context: RuntimeFormulaContext, path: List[str]
    ):
        """Load a data chunk from a datasource of the page in context."""

        data_source_name, *rest = path

        if "request" not in runtime_formula_context.application_context:
            return None

        data_source = self.get_data_source(runtime_formula_context, data_source_name)

        service_dispatch = ServiceHandler().dispatch_service(
            data_source.service, runtime_formula_context
        )

        return get_nested_value_from_dict(service_dispatch, rest)
