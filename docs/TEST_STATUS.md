# Current manual validation status

Stable combination:

```text
Smart Entity Timer       0.1.3
Smart Entity Timer Card  0.2.2
Card API                  2
```

The following behavior has been manually validated in Home Assistant OS:

| Area | Status |
|---|---|
| Clean integration installation | Passed |
| Helper/entity creation | Passed |
| Normal turn-on timer | Passed |
| Normal turn-off timer | Passed |
| Manual cancellation | Passed |
| Automatic early-state cancellation | Passed |
| Controls lock/unlock correctly | Passed |
| Restart before timer expiry | Passed |
| Expired OFF timer during downtime | Passed |
| Expired ON timer skipped during downtime | Passed |
| Multiple simultaneous timers | Passed |
| Target unavailable handling | Passed |
| Arbitrary duration values | Passed |
| Options update without entity recreation | Passed |
| Delete/recreate timer helper | Passed |
| Multi-browser synchronization | Passed (three simultaneous browsers) |
| HACS integration installation | Passed |
| HACS dashboard-card installation | Passed |
| Automatic HACS dashboard resource creation | Passed |
| Notification delivery to compatible device | Passed |

A clean HACS installation was also validated on Home Assistant OS running on a Raspberry Pi 5.

This status complements, but does not replace, the repeatable test cases in `TEST_PLAN.md`.
