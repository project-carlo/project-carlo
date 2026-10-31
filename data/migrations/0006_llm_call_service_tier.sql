-- The service tier that served each update call (`flex`, or `default` when
-- flex had no capacity and the call was asked again at the standard tier), as
-- the response reports it. `cost_usd` is priced at this tier, so a row explains
-- its own cost, and how often the flex fallback fires is one query. Rows from
-- before flex have none and were served at the standard tier.

ALTER TABLE llm_call ADD COLUMN service_tier TEXT;
