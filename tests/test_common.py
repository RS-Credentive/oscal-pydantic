from oscal_pydantic.core import properties, datatypes, common


class TestCommon:
    def test_location(
        self,
        get_uuid: datatypes.OscalUUID,
        get_markupline: datatypes.OscalMarkupLine,
        get_address: common.Address,
    ):
        assert isinstance(
            common.Location(
                uuid=get_uuid,
                title=get_markupline,
                address=get_address,
                props=[
                    properties.LocationProperty(
                        name="type",
                        value="data-center",
                        prop_class="primary",
                    )
                ],
            ),
            common.Location,
        )
