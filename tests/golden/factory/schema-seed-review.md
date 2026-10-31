{
 "status": "done | partial | blocked",
 "summary": "one or two sentences",
 "flags": [
  {
   "severity": "blocking | advisory",
   "scope": "parish | run",
   "subject": "roster:id or parish slug",
   "question": "what needs deciding",
   "evidence": [
    "path#section or URL with date"
   ],
   "suggestion": "what you would do"
  }
 ],
 "leads": [
  {
   "touches": "batch id or roster:id",
   "note": "..."
  }
 ],
 "lessons": [
  "reusable publisher or rule lesson"
 ],
 "seeds": [
  {
   "parish": "slug",
   "verdict": "approve | send_back",
   "answers": [
    {
     "slot": "slot id",
     "question": "...",
     "choice": "option index | dropped | edited",
     "entry": "only for edited",
     "basis": "rule | precedent | judgment",
     "why": "..."
    }
   ],
   "problems": [
    "..."
   ]
  }
 ]
}
