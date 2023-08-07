from src.oscal_pydantic.core import datatypes, properties

ns = datatypes.Uri("http://csrc.nist.gov/ns/oscal")
name = datatypes.Token("marking")
value = datatypes.String("test")

test_prop = properties.OscalProperty(ns=ns, name=name, value=value)

name = datatypes.Token("type")
value = datatypes.String("data-center")
loc_class = datatypes.Token("primary")

test_loc = properties.LocationProperty(
    ns=ns, name=name, value=value, prop_class=loc_class
)
