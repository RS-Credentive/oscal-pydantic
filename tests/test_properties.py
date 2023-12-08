from oscal_pydantic.core import datatypes, properties


class TestProperties:
    def test_base_property(self):
        assert isinstance(
            properties.BaseProperty(
                name="property",
                ns=datatypes.OscalUri("http://www.credentive.com"),
                value="value",
            ),
            properties.BaseProperty,
        )

    def test_base_property_implicit_ns(self):
        assert isinstance(
            properties.BaseProperty(
                name="property",
                value="value",
            ),
            properties.BaseProperty,
        )

    def test_oscal_marking_property(self):
        assert isinstance(
            properties.OscalMarkingProperty(
                ns=datatypes.OscalUri("http://csrc.nist.gov/ns/oscal"),
                name="marking",
                value="value",
            ),
            properties.OscalMarkingProperty,
        )

    # Generic method to test all possible values of a property
    def test_property(self):
        pass

    def test_resource_property_published(self, get_random_date_string: str):
        assert isinstance(
            properties.OscalResourceProperty(
                ns=datatypes.OscalUri("http://csrc.nist.gov/ns/oscal"),
                name="published",
                value=get_random_date_string,
            ),
            properties.OscalResourceProperty,
        )
