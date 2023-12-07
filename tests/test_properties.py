from oscal_pydantic.core import datatypes
from oscal_pydantic.properties import base_property, oscal_properties


class TestProperties:
    def test_base_property(self):
        assert isinstance(
            base_property.BaseProperty(
                name="property",
                ns=datatypes.OscalUri("http://www.credentive.com"),
                value="value",
            ),
            base_property.BaseProperty,
        )

    def test_base_property_implicit_ns(self):
        assert isinstance(
            base_property.BaseProperty(
                name="property",
                value="value",
            ),
            base_property.BaseProperty,
        )

    def test_oscal_marking_property(self):
        assert isinstance(
            oscal_properties.OscalMarkingProperty(
                ns=datatypes.OscalUri("http://csrc.nist.gov/ns/oscal"),
                name="marking",
                value="value",
            ),
            oscal_properties.OscalMarkingProperty,
        )

    # Generic method to test all possible values of a property
    def test_property(self):
        pass
