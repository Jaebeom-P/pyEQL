"""
pyEQL utilities

:copyright: 2023 by Ryan S. Kingsbury
:license: LGPL, see LICENSE for more details.

"""

from collections import UserDict

from pymatgen.core.ion import Ion


def standardize_formula(formula: str):
    """
    Convert a chemical formula into standard form.

    Args:
        formula: the chemical formula to standardize.

    Returns:
        A standardized chemical formula

    Raises:
        ValueError if `formula` cannot be processed or is invalid.

    Notes:
        Currently this method standardizes formulae by passing them through pymatgen.core.ion.Ion.reduced_formula(). For ions, this means that 1) the
        charge number will always be listed explicitly and 2) the charge number will be enclosed in square brackets to remove any ambiguity in the meaning of the formula. For example, 'Na+', 'Na+1', and 'Na[+]' will all
        standardize to "Na[+1]"
    """
    rform = Ion.from_formula(formula).reduced_formula
    # TODO - this is a workaround for a shortcoming of Ion that I would like to fix in pymatgen
    if rform.split("(aq)")[0] in ["H", "O", "N", "F", "Cl"]:
        rform = rform.split("(aq)")[0] + "2(aq)"
    return rform


class FormulaDict(UserDict):
    """
    Automatically converts keys on get/set using pymatgen.core.Ion.from_formula(key).reduced_formula.

    This allows getting/setting/updating of Solution.components using flexible
    formula notation (e.g., "Na+", "Na+1", "Na[+]" all have the same effect)
    """

    def __getitem__(self, key):
        return super().__getitem__(standardize_formula(key))

    def __setitem__(self, key, value):
        super().__setitem__(standardize_formula(key), value)

    def __delitem__(self, key):
        super().__delitem__(standardize_formula(key))
