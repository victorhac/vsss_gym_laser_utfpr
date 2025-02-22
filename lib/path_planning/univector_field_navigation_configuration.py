from configuration.configuration import Configuration

DE = Configuration.univector_field_navigation_de
KR = Configuration.univector_field_navigation_kr
K_0 = Configuration.univector_field_navigation_k0
D_MIN = Configuration.univector_field_navigation_dmin
GAUSSIAN_DELTA = Configuration.univector_field_navigation_gaussian_delta

class UnivectorFieldNavigationConfiguration:
    def __init__(
        self,
        de: float = DE,
        kr: float = KR,
        k_0: float = K_0,
        d_min: float = D_MIN,
        gaussian_delta: float = GAUSSIAN_DELTA
    ):
        self.de = de
        self.kr = kr
        self.k_0 = k_0
        self.d_min = d_min
        self.gaussian_delta = gaussian_delta
