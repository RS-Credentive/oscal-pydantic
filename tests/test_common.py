from oscal_pydantic.core import datatypes, common, properties


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
                    properties.OscalLocationProperty(
                        name=datatypes.OscalToken("type"),
                        value=datatypes.OscalString("data-center"),
                        prop_class=datatypes.OscalToken("primary"),
                    )
                ],
            ),
            common.Location,
        )
