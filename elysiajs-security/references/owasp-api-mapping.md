# OWASP API Security Top 10 — Mapping to Checklist

Use this only when the user wants findings labeled with OWASP API Security
Top 10 categories (e.g. for a formal report). Otherwise, use plain-language
findings from `checklist.md`.

| OWASP API Top 10 | Checklist section(s) |
|---|---|
| API1: Broken Object Level Authorization (IDOR) | §2 Authorization — ownership checks |
| API2: Broken Authentication | §1 Authentication |
| API3: Broken Object Property Level Authorization | §2 Authorization — mass assignment |
| API4: Unrestricted Resource Consumption | §6 Rate limiting, §3 input bounds, file upload size |
| API5: Broken Function Level Authorization | §2 Authorization — role/permission macros |
| API6: Unrestricted Access to Sensitive Business Flows | §6 Rate limiting on sensitive flows (checkout, signup) |
| API7: Server Side Request Forgery | Not covered by default checklist — check any route that fetches a user-supplied URL server-side |
| API8: Security Misconfiguration | §4 CORS, §9 Dependencies & config, §7 error verbosity |
| API9: Improper Inventory Management | §9 — check for undocumented/legacy routes still mounted |
| API10: Unsafe Consumption of APIs | Check any outbound calls to third-party APIs for unvalidated responses trusted downstream |
