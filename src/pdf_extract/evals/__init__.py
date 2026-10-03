"""Scoring classifiers against the ground-truth labels in data/labels/.

`run` runs any registered classifier over the labeled bulletins and writes its
output, one file per bulletin in the label's event-row shape, under
`data/runs/<classifier>/eval/<version>/`.
"""
