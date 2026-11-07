"""Measuring the factory, never steering it: quota readings and their attribution to
attempts, tokens, each attempt's metadata, and the reports on them. The design is
docs/factory-quota.md.

The dispatcher's parts call in here; nothing here picks, gates or blocks a job, and a
failure here is logged, never raised into a job.
"""
