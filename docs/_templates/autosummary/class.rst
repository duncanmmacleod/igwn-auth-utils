.. Copyright (C) 2022 Cardiff University
.. Custom autosummary template for classes:
..   - use objname instead of fullname in page title
..   - add :no-inherited-members: option to autoclass directives

{{ objname | escape | underline }}

.. currentmodule:: {{ module }}

.. autoclass:: {{ objname }}
   :no-inherited-members:
