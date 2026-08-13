class PersonalityEngine:
    """
    Maintains persistent personality parameters (traits, values, facet tendencies).
    Personality must be distinct from state, experience, and behavior.
    """

    def __init__(self):
        self.traits = {}
        self.facets = {}

    def get_baseline_trait(self, trait_id: str) -> float:
        return self.traits.get(trait_id, 0.5)
