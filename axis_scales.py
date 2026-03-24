import matplotlib as mpl



class CenteredSymLogScale(mpl.scale.SymmetricalLogScale):
    # symmetric logarithm scale centered around a given point, rather than 0
    # TODO: axis labels are generally quite sparse around the center since they are unchanged from normal symlog

    name = "centered_symlog"

    def __init__(self, axis, *, center, **kwargs):
        self.center = center
        super().__init__(axis, **kwargs)

    def get_transform(self):
        forward = lambda x: x - self.center
        inverse = lambda x: x + self.center

        # affine part + non-affine part = whole transform
        unscaled_transform = super().get_transform()
        full_transform = mpl.scale.FuncTransform(forward, inverse) + unscaled_transform

        # expects symmetric log transform with base, linthresh, linscale attributes
        full_transform.base = unscaled_transform.base
        full_transform.linthresh = unscaled_transform.linthresh
        full_transform.linscale = unscaled_transform.linscale

        return full_transform

    def set_default_locators_and_formatters(self, axis):
        super().set_default_locators_and_formatters(axis)
        axis.set_major_formatter(mpl.ticker.LogFormatterMathtext())