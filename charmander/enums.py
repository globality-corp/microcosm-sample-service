"""
Platform enums.

"""
from enum import Enum, unique


@unique
class Purpose(Enum):
    """
    The purpose of a resource.

    """
    def __str__(self):
        return self.name

    # The resource content is used by other resources
    CONTENT = "CONTENT"
    # The resource is used normally
    NORMAL = "NORMAL"
    # The resource is used for testing
    TEST = "TEST"
    # The resource is used by tutorials. Propagated only from projects to child resouces.
    TUTORIAL = "TUTORIAL"
    # The resource is used for dry runs of end user interactions
    REHEARSAL = "REHEARSAL"

    def is_project_match_allowed(self, service_provider_purpose):
        """
        Can a service project be matched to a service provider

        """
        # REHEARSAL projects and companies are allowed to be matched with anything
        # TUTORIAL projects can be matched to CONTENT companies (not the other way)
        return (
            self == service_provider_purpose or
            self == Purpose.REHEARSAL or
            service_provider_purpose == Purpose.REHEARSAL or
            (self == Purpose.TUTORIAL and service_provider_purpose == Purpose.CONTENT)
        )

    @property
    def allowed_matches(self):
        return [purpose for purpose in Purpose if self.is_project_match_allowed(purpose)]

    @property
    def forbidden_matches(self):
        return [purpose for purpose in Purpose if not self.is_project_match_allowed(purpose)]


@unique
class Resolution(Enum):
    """
    The resolution of a resource.

    """
    def __str__(self):
        return self.name

    # The resource is active
    ACTIVE = "ACTIVE"
    # The resource was dismissed by a system administrator
    ARCHIVED = "ARCHIVED"
    # The resource was dismissed by an end user
    ABANDONED = "ABANDONED"
    # The resource is no longer in use but can be reported on
    CLOSED = "CLOSED"
    # The resource was redacted
    REDACTED = "REDACTED"
    # The resource is viewable, but no longer reflects reality
    STALE = "STALE"

    @property
    def is_viewable(self):
        return self in (
            Resolution.ACTIVE,
            Resolution.REDACTED,
            Resolution.STALE,
        )
