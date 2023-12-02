from oscal_pydantic.core import properties, datatypes


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
