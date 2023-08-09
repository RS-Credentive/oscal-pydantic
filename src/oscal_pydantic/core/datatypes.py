from __future__ import annotations

import re
import uuid
from datetime import date, datetime, timedelta, timezone
from typing import Any, Union, Optional

from pydantic import (
    Field,
    NonNegativeInt,
    PositiveInt,
    RootModel,
    ValidationError,
    EmailStr,
    AnyUrl,
    PrivateAttr,
)


class Boolean(RootModel[bool]):
    """
     A class used to represent an OSCAL Boolean:

     https://pages.nist.gov/OSCAL/reference/datatypes/#boolean

     A boolean value mapped in XML, JSON, and YAML as follows:
     | Value | XML               | JSON      | YAML      |
     |:---   |:---               |:---       |:---       |
     | true  | `true` or `1`     | `true`    | `true`    |
     | false | `false` or `0`    | `false`   | `false`   |

     Attributes:
         root: (bool, "0" or "1", or 0 or 1): A boolean value represented either as a bool, the str "0" or "1", or the int 0 or 1.

    Notes: Currently doesn't filter JSON "truthy" values.
    """

    # TODO: Pydantic will accept values from JSON that are invalid in oscal, including:
    # Allowed values: 'f', 'n', 'no', 'off',  't', 'y', 'on', 'yes'
    # How to fix?

    root: bool = Field(description="A boolean value")


class Decimal(RootModel[float]):
    """
    A class to represent an OSCAL Decimal

    https://pages.nist.gov/OSCAL/reference/datatypes/#decimal

    Attributes:
        root : float
            A real number expressed using decimal numerals.
    """

    root: float = Field(description="A real number expressed using decimal numerals.")


class Integer(RootModel[int]):
    """
    A class to represent an OSCAL Integer

    https://pages.nist.gov/OSCAL/reference/datatypes/#integer

    Attributes:
        root : int
            An integer value.
    """

    root: int = Field(description="An integer value.")


class NonNegativeInteger(RootModel[NonNegativeInt]):
    """
    A class to represent an OSCAL Non-negative Integer

    https://pages.nist.gov/OSCAL/reference/datatypes/#nonnegativeinteger

    Attributes:
        root: int
            An integer value that is equal to or greater than 0.
    """

    root: NonNegativeInt = Field(
        description="An integer value that is equal to or greater than 0."
    )


class PositiveInteger(RootModel[PositiveInt]):
    """
    A class to represent an OSCAL Positive Integer

    https://pages.nist.gov/OSCAL/reference/datatypes/#positiveinteger

    Attributes:
        root: int
            A positive integer value.
    """

    root: PositiveInt = Field(description="A positive integer value.")


class Base64Binary(RootModel[str]):
    """
    A class to represent an OSCAL Base64 Binary String

    https://pages.nist.gov/OSCAL/reference/datatypes/#base64binary

    Attributes:
        root: str
            A string representing arbitrary Base64-encoded binary data
    """

    root: str = Field(
        description="A string representing arbitrary Base64-encoded binary data.",
        pattern=r"^[0-9A-Fa-f]+$",
    )


class Date(RootModel[str]):
    """
    A class to represent an OSCAL Date String with optional Timezone(expressed as offset from UTC)

    https://pages.nist.gov/OSCAL/reference/datatypes/#date

    Attributes:
        root: A string which must conform to the following

        date: datetime.date
            A date

        timezone: datetime.timedelta
            A timedelta from UTC
    """

    # ISO 8601 pattern ^([1-9]\d{3}[\-.](0[13578]|1[02])[\-.](0[1-9]|[12][0-9]|3[01]) ([01]\d|2[0123]):([012345]\d):([012345]\d))|([1-9]\d{3}[\-.](0[469]|11)[\-.](0[1-9]|[12][0-9]|30) ([01]\d|2[0123]):([012345]\d):([012345]\d))|([1-9]\d{3}[\-.](02)[\-.](0[1-9]|1[0-9]|2[0-8]) ([01]\d|2[0123]):([012345]\d):([012345]\d))|(((([1-9]\d)(0[48]|[2468][048]|[13579][26])|(([2468][048]|[13579][26])00)))[\-.](02)[\-.]29 ([01]\d|2[0123]):([012345]\d):([012345]\d))$

    root: str = Field(
        description="A string representing a 24-hour period with optional time zone.",
        pattern="^(((2000|2400|2800|(19|2[0-9](0[48]|[2468][048]|[13579][26])))-02-29)|(((19|2[0-9])[0-9]{2})-02-(0[1-9]|1[0-9]|2[0-8]))|(((19|2[0-9])[0-9]{2})-(0[13578]|10|12)-(0[1-9]|[12][0-9]|3[01]))|(((19|2[0-9])[0-9]{2})-(0[469]|11)-(0[1-9]|[12][0-9]|30)))(Z|[+-][0-9]{2}:[0-9]{2})?$",
    )

    _date: date
    _timezone: timezone | None

    def model_post_init(self, __context: Any) -> None:
        patterns = re.match(
            "^([0-9]{4})-([0][1-9]|1[0-2])-([0][1-9]|[1-2][0-9]|[3][0-1])(Z|([+|-])([0-1][0-9]|2[0-3]):([0-5][0-9]))?$",
            self.root,
        )
        # This shouldn't happen because of the filter, but this shuts up pylint
        if patterns is not None:
            self._date = date(
                int(patterns.group(1)),  # year
                int(patterns.group(2)),  # month
                int(patterns.group(3)),  # day
            )

            if patterns.group(4) is None:
                self._timezone = None
            elif patterns.group(4) == "Z":
                self._timezone = timezone.utc
            else:
                if patterns.group(5) == "-":
                    self._timezone = timezone(
                        timedelta(
                            hours=-int(patterns.group(6)),
                            minutes=int(patterns.group(7)),
                        )
                    )
                elif patterns.group(5) == "+":
                    self._timezone = timezone(
                        timedelta(
                            hours=int(patterns.group(6)),
                            minutes=int(patterns.group(7)),
                        )
                    )
                else:
                    raise ValidationError("Invalid offset character - should be + or -")


class DateWithTimezone(RootModel[str]):
    """
    A class to represent an OSCAL Date String with mandatory Timezone(expressed as offset from UTC)

    https://pages.nist.gov/OSCAL/reference/datatypes/#date-with-timezone

    Attributes:
        root: A string which must conform to the following

        date: datetime.date
            A date

        timezone: datetime.timedelta
            A timedelta from UTC
    """

    # ISO 8601 pattern ^([1-9]\d{3}[\-.](0[13578]|1[02])[\-.](0[1-9]|[12][0-9]|3[01]) ([01]\d|2[0123]):([012345]\d):([012345]\d))|([1-9]\d{3}[\-.](0[469]|11)[\-.](0[1-9]|[12][0-9]|30) ([01]\d|2[0123]):([012345]\d):([012345]\d))|([1-9]\d{3}[\-.](02)[\-.](0[1-9]|1[0-9]|2[0-8]) ([01]\d|2[0123]):([012345]\d):([012345]\d))|(((([1-9]\d)(0[48]|[2468][048]|[13579][26])|(([2468][048]|[13579][26])00)))[\-.](02)[\-.]29 ([01]\d|2[0123]):([012345]\d):([012345]\d))$

    root: str = Field(
        description="A string representing a 24-hour period with optional time zone.",
        pattern="^(((2000|2400|2800|(19|2[0-9](0[48]|[2468][048]|[13579][26])))-02-29)|(((19|2[0-9])[0-9]{2})-02-(0[1-9]|1[0-9]|2[0-8]))|(((19|2[0-9])[0-9]{2})-(0[13578]|10|12)-(0[1-9]|[12][0-9]|3[01]))|(((19|2[0-9])[0-9]{2})-(0[469]|11)-(0[1-9]|[12][0-9]|30)))(Z|[+-][0-9]{2}:[0-9]{2})$",
    )

    _date: date
    _timezone: timezone | None

    def model_post_init(self, __context: Any) -> None:
        patterns = re.match(
            "^([0-9]{4})-([0][1-9]|1[0-2])-([0][1-9]|[1-2][0-9]|[3][0-1])(Z|([+|-])([0-1][0-9]|2[0-3]):([0-5][0-9]))$",
            self.root,
        )
        # This shouldn't happen because of the filter, but this shuts up pylint
        if patterns is not None:
            self._date = date(
                int(patterns.group(1)),  # year
                int(patterns.group(2)),  # month
                int(patterns.group(3)),  # day
            )

            if patterns.group(4) is None:
                raise ValidationError(
                    "Timezone is mandatory for this in date-with-timezone"
                )
            elif patterns.group(4) == "Z":
                self._timezone = timezone.utc
            else:
                if patterns.group(5) == "-":
                    self._timezone = timezone(
                        timedelta(
                            hours=-int(patterns.group(6)),
                            minutes=int(patterns.group(7)),
                        )
                    )
                elif patterns.group(5) == "+":
                    self._timezone = timezone(
                        timedelta(
                            hours=int(patterns.group(6)),
                            minutes=int(patterns.group(7)),
                        )
                    )
                else:
                    raise ValidationError("Invalid offset character - should be + or -")


class DateTime(RootModel[str]):
    """
    A class to represent an OSCAL DateTime String with optional Timezone(expressed as offset from UTC)

    https://pages.nist.gov/OSCAL/reference/datatypes/#date

    Attributes:
        root: A string which must conform to the following

        _datetime: datetime.datetime
            A date

        _timezone: datetime.timedelta
            A timedelta from UTC
    """

    root: str = Field(
        description="A string containing a date and time formatted according to 'date-time' as defined RFC3339. This type allows an optional time-offset (timezone). This use of timezone ensure that date/time information that is exchanged across timezones is unambiguous.",
        pattern=r"(((2000|2400|2800|(19|2[0-9](0[48]|[2468][048]|[13579][26])))-02-29)|(((19|2[0-9])[0-9]{2})-02-(0[1-9]|1[0-9]|2[0-8]))|(((19|2[0-9])[0-9]{2})-(0[13578]|10|12)-(0[1-9]|[12][0-9]|3[01]))|(((19|2[0-9])[0-9]{2})-(0[469]|11)-(0[1-9]|[12][0-9]|30)))T((2[0-3]|[01][0-9]):([0-5][0-9]):([0-5][0-9])(\.[0-9]+)?)(Z|[+-][0-9]{2}:[0-9]{2})?",
    )

    _datetime: datetime
    _timezone: timezone | None

    def model_post_init(self, __context: Any) -> None:
        patterns = re.match(
            r"^([0-9]{4})-([0][1-9]|1[0-2])-([0][1-9]|[1-2][0-9]|[3][0-1])T([0][1-9]|[1][0-2]):([0-5][0-9]):([0-5][0-9])(?:(?:\.)([0-9]+))?(Z|([+|-])([0-1][0-9]|2[0-3]):([0-5][0-9]))?$",
            self.root,
        )
        # This shouldn't happen because of the filter, but this shuts up pylint
        if patterns is not None:
            self._datetime = datetime(
                int(patterns.group(1)),  # year
                int(patterns.group(2)),  # month
                int(patterns.group(3)),  # day
                int(patterns.group(4)),  # hour
                int(patterns.group(5)),  # minute
                int(patterns.group(6)),  # second
            )
            if patterns.group(7) is not None:  # Add microseconds if we got them
                self._datetime += timedelta(microseconds=int(patterns.group(7)))

            if patterns.group(8) is None:
                # No timezone was passed in. Don't do anything
                pass
            elif patterns.group(8) == "Z":
                # Zulu was passed in  - set timezone to UTD
                self._timezone = timezone.utc
            else:
                # Confirm that the proper values were passed in
                if patterns.group(9) == "-":
                    self._timezone = timezone(
                        timedelta(
                            hours=-int(patterns.group(10)),
                            minutes=int(patterns.group(11)),
                        )
                    )
                elif patterns.group(9) == "+":
                    self._timezone = timezone(
                        timedelta(
                            hours=int(patterns.group(10)),
                            minutes=int(patterns.group(11)),
                        )
                    )
                else:
                    raise ValidationError("Invalid offset character - should be + or -")


class DateTimeWithTimezone(RootModel[str]):
    """
    A class to represent an OSCAL DateTime String with mandatory Timezone(expressed as offset from UTC)

    https://pages.nist.gov/OSCAL/reference/datatypes/#date

    Attributes:
        root: A string which must conform to the following

        _datetime: datetime.datetime
            A date

        _timezone: datetime.timedelta
            A timedelta from UTC
    """

    root: str = Field(
        description="A string containing a date and time formatted according to 'date-time' as defined RFC3339. This type requires a time-offset (timezone). This use of timezone ensure that date/time information that is exchanged across timezones is unambiguous.",
        pattern=r"(((2000|2400|2800|(19|2[0-9](0[48]|[2468][048]|[13579][26])))-02-29)|(((19|2[0-9])[0-9]{2})-02-(0[1-9]|1[0-9]|2[0-8]))|(((19|2[0-9])[0-9]{2})-(0[13578]|10|12)-(0[1-9]|[12][0-9]|3[01]))|(((19|2[0-9])[0-9]{2})-(0[469]|11)-(0[1-9]|[12][0-9]|30)))T((2[0-3]|[01][0-9]):([0-5][0-9]):([0-5][0-9])(\.[0-9]+)?)(Z|[+-][0-9]{2}:[0-9]{2})",
    )

    _datetime: Optional[datetime] = PrivateAttr()
    _timezone: Optional[timezone] = PrivateAttr()

    def model_post_init(self, __context: Any) -> None:
        patterns = re.match(
            r"^([0-9]{4})-([0][1-9]|1[0-2])-([0][1-9]|[1-2][0-9]|[3][0-1])T([0][1-9]|[1][0-2]):([0-5][0-9]):([0-5][0-9])(?:(?:\.)([0-9]+))?(Z|([+|-])([0-1][0-9]|2[0-3]):([0-5][0-9]))$",
            self.root,
        )
        # This shouldn't happen because of the filter, but this shuts up pylint
        if patterns is not None:
            self._datetime = datetime(
                int(patterns.group(1)),  # year
                int(patterns.group(2)),  # month
                int(patterns.group(3)),  # day
                int(patterns.group(4)),  # hour
                int(patterns.group(5)),  # minute
                int(patterns.group(6)),  # second
            )
            if patterns.group(7) is not None:  # Add microseconds if we got them
                self._datetime += timedelta(microseconds=int(patterns.group(7)))

            if patterns.group(8) is None:
                # No timezone was passed in. Throw a validation error
                raise ValidationError(
                    "Timezone is mandatory for this in datetime-with-timezone"
                )
            elif patterns.group(8) == "Z":
                # Zulu was passed in  - set timezone to UTD
                self._timezone = timezone.utc
            else:
                # Confirm that the proper values were passed in
                if patterns.group(9) == "-":
                    self._timezone = timezone(
                        timedelta(
                            hours=-int(patterns.group(10)),
                            minutes=int(patterns.group(11)),
                        )
                    )
                elif patterns.group(9) == "+":
                    self._timezone = timezone(
                        timedelta(
                            hours=int(patterns.group(10)),
                            minutes=int(patterns.group(11)),
                        )
                    )
                else:
                    raise ValidationError("Invalid offset character - should be + or -")


class Email(RootModel[EmailStr]):
    """
    A class to represent an OSCAL email address string formatted according to RFC 6531

    https://pages.nist.gov/OSCAL/reference/datatypes/#email

    Attributes:
        root: A string which must conform to the RFC 6531
    """

    root: EmailStr = Field(
        description="An email address string formatted according to RFC 6531"
    )


class Hostname(RootModel[str]):
    """
    A class to represent an internationalized Internet host name string formatted according to section 2.3.2.3 of RFC 5890.

    https://pages.nist.gov/OSCAL/reference/datatypes/#hostname

    Attributes:
        root: A host name string formatted according to section 3.5 of RFC 1034:
        The labels must follow the rules for ARPANET host names.  They must
        start with a letter, end with a letter or digit, and have as interior
        characters only letters, digits, and hyphen.  There are also some
        restrictions on the length.  Labels must be 63 characters or less.
        NOTE: current regex does not limit length of string
        TODO: Fix regex for hostname
    """

    root: str = Field(
        description="A host name string formatted according to section 2.3.2.3 of RFC 5890",
        pattern=r"^(([a-zA-Z]+[\d-]*[a-zA-Z0-9]+)(\.)?)+$",
    )


class IpV4Address(RootModel[str]):
    """
    A class representing an IpV4Address

    Attributes:
        root: An Internet Protocol version 4 address in dotted-quad ABNF syntax as defined in section 3.2 of RFC 2673
    """

    root: str = Field(
        description="An Internet Protocol version 4 address in dotted-quad ABNF syntax as defined in section 3.2 of RFC 2673",
        pattern=r"^((25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[1-9][0-9]|[0-9]).){3}(25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[1-9][0-9]|[0-9])$",
    )


class IpV6Adrress(RootModel[str]):
    """
    A class representing an IPV6 Address

    Attributes:
        root: An Internet Protocol version 6 address in dotted-quad ABNF syntax as defined in section 2.2 of RFC 3513.
    """

    root: str = Field(
        description="An Internet Protocol version 6 address in dotted-quad ABNF syntax as defined in section 2.2 of RFC 3513.",
        pattern=r"^(([0-9a-fA-F]{1,4}:){7,7}[0-9a-fA-F]{1,4}|([0-9a-fA-F]{1,4}:){1,7}:|([0-9a-fA-F]{1,4}:){1,6}:[0-9a-fA-F]{1,4}|([0-9a-fA-F]{1,4}:){1,5}(:[0-9a-fA-F]{1,4}){1,2}|([0-9a-fA-F]{1,4}:){1,4}(:[0-9a-fA-F]{1,4}){1,3}|([0-9a-fA-F]{1,4}:){1,3}(:[0-9a-fA-F]{1,4}){1,4}|([0-9a-fA-F]{1,4}:){1,2}(:[0-9a-fA-F]{1,4}){1,5}|[0-9a-fA-F]{1,4}:((:[0-9a-fA-F]{1,4}){1,6})|:((:[0-9a-fA-F]{1,4}){1,7}|:)|[fF][eE]80:(:[0-9a-fA-F]{0,4}){0,4}%[0-9a-zA-Z]{1,}|::([fF]{4}(:0{1,4}){0,1}:){0,1}((25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[1-9][0-9]|[0-9]).){3,3}(25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[1-9][0-9]|[0-9])|([0-9a-fA-F]{1,4}:){1,4}:((25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[1-9][0-9]|[0-9]).){3,3}(25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[1-9][0-9]|[0-9]))$",
    )


class String(RootModel[str]):
    """
    A class representing a string of Unicode characters, but not empty and not whitespace-only (whitespace is U+9, U+10, U+32 or [ \n\t]+).

    Attributes:
        root: A string of Unicode characters, but not empty and not whitespace-only (whitespace is U+9, U+10, U+32 or [ \n\t]+).
    """

    root: str = Field(
        description="A string of Unicode characters, but not empty and not whitespace-only (whitespace is U+9, U+10, U+32 or [ \n\t]+).",
        pattern=r"^\S+$",
    )


class Token(RootModel[str]):
    """
    A class representing a non-colonized name as defined by XML Schema Part 2: Datatypes Second Edition.

    Attributes:
        root: a non-colonized name as defined by XML Schema Part 2: Datatypes Second Edition.
    """

    root: str = Field(
        description="Non-colonized token type used for various identifiers",
        pattern=r"^([a-zA-Z_])([A-Za-z0-9.\-_])*$",  # any non-numeric character or "_", followed by a sequence of any alphanumeric character, "_", "-", or "."
    )


class Uri(RootModel[AnyUrl]):
    """
    A class representing a universal resource identifier (URI) formatted according to RFC3986.

    Attributes:
        root: a universal resource identifier (URI) formatted according to RFC3986.
    """

    root: AnyUrl = Field(
        description="A universal resource identifier (URI) formatted according to RFC3986."
    )


class RelativeURI(RootModel[AnyUrl | str]):
    """
    A class representing a relative resource identifier formatted according to section 4.1 of RFC3986.

    Attributes:
        root: a relative resource identifier formatted according to section 4.1 of RFC3986.

        4.2.  Relative Reference

        A relative reference takes advantage of the hierarchical syntax
        (Section 1.2.3) to express a URI reference relative to the name space
        of another hierarchical URI.

            relative-ref  = relative-part [ "?" query ] [ "#" fragment ]

            relative-part = "//" authority path-abempty
                            / path-absolute
                            / path-noscheme
                            / path-empty

        The URI referred to by a relative reference, also known as the target
        URI, is obtained by applying the reference resolution algorithm of
        Section 5.

        A relative reference that begins with two slash characters is termed
        a network-path reference; such references are rarely used.  A
        relative reference that begins with a single slash character is
        termed an absolute-path reference.  A relative reference that does
        not begin with a slash character is termed a relative-path reference.

        A path segment that contains a colon character (e.g., "this:that")
        cannot be used as the first segment of a relative-path reference, as
        it would be mistaken for a scheme name.  Such a segment must be
        preceded by a dot-segment (e.g., "./this:that") to make a relative-
        path reference.
    """

    root: str = Field(
        description="relative resource identifier formatted according to section 4.1 of RFC3986.",
        pattern=r"^(/|//)?([^:])*$|^./(\S)*$",  # TODO: We can do much better than this, but it's a start
    )


class UriReference(RootModel[Uri | RelativeURI]):
    """
    A class representing a URI Reference (either a URI or a relative-reference) formatted according to section 4.1 of RFC3986.

    Attributes:
        root: Uri or RelativeURI
    """

    root: Uri | RelativeURI


class UUID(RootModel[uuid.UUID]):
    """
    A class to represent an OSCAL UUID

    https://pages.nist.gov/OSCAL/reference/datatypes/#uuid

    A version 4 or 5 Universally Unique Identifier (UUID) as defined by RFC 4122.

    Attributes:
        root: (uuid.UUID)
    """

    root: uuid.UUID = Field(
        description="A machine-oriented, globally unique identifier with cross-instance scope that can be used to reference this defined property elsewhere in this or other OSCAL instances. This UUID should be assigned per-subject, which means it should be consistently used to identify the same subject across revisions of the document.",
        default=uuid.uuid4(),
    )


class MarkupLine(RootModel[str]):
    """
    A class to represent an OSCAL MarkupLine

    https://pages.nist.gov/OSCAL/reference/datatypes/#markup-line

    A line of text leveraging the OSCAL/CommonMark inspired standard.

    Attributes:
        root: (str)
    """

    root: str = Field(
        description="A line of text leveraging the OSCAL/CommonMark inspired standard, documented here: https://pages.nist.gov/OSCAL/reference/datatypes/#markup-line"
        # TODO: validate that the text is HTML or MD with only the permitted tags
        # TODO: Parameter insertion
    )


class MarkupMultiline(RootModel[str]):
    """
    A class to represent a markup-multiline body of text

    https://pages.nist.gov/OSCAL/reference/datatypes/#markup-line

    A body of text leveraging the OSCAL/CommonMark inspired standard.

    Attributes:
        root: (float)
    """

    root: str = Field(
        description="A line of text leveraging the OSCAL/CommonMark inspired standard, documented here: https://pages.nist.gov/OSCAL/reference/datatypes/#markup-multiline"
        # TODO: validate that the text is HTML or MD with only the permitted tags
    )


OscalDatatype = Union[
    Boolean,
    Decimal,
    Integer,
    NonNegativeInteger,
    PositiveInteger,
    Base64Binary,
    Date,
    DateWithTimezone,
    DateTime,
    DateTimeWithTimezone,
    Email,
    Hostname,
    IpV4Address,
    IpV6Adrress,
    String,
    Token,
    Uri,
    RelativeURI,
    UriReference,
    UUID,
    MarkupLine,
    MarkupMultiline,
]
