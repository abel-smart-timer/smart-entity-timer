# Smart Entity Timer 1.0.0 — Release Gate Test Plan

This plan validates the all-in-one packaging transition before publishing the immutable `v1.0.0` release.

## A. Static / repository checks

- A1 `manifest.json` version is `1.0.0`.
- A2 Manifest dependencies include `frontend` and `http`.
- A3 `const.py` version is `1.0.0`; Card API remains `2`.
- A4 `www/smart-entity-timer-card.js` exists and reports Card version `1.0.0`.
- A5 Bundled card keeps `custom:smart-entity-timer-card`.
- A6 Bundled card still includes Mini and Tile layouts.
- A7 `frontend.py` uses `async_register_static_paths` and `add_extra_js_url`.
- A8 Python compile and unit/regression tests pass.
- A9 Hassfest passes in GitHub Actions.
- A10 HACS integration validation passes in GitHub Actions.

## B. Clean manual installation

Use a Home Assistant instance where neither Smart Entity Timer nor Smart Entity Timer Card is installed.

1. Back up Home Assistant.
2. Install the candidate integration manually.
3. Restart Home Assistant.
4. Confirm there are no Smart Entity Timer startup errors.
5. Add Smart Entity Timer under Settings > Devices & services.
6. Add at least two timer Config Subentries.
7. Confirm each timer creates status, duration, action, start and cancel entities.
8. Open a dashboard editor and confirm **Smart Entity Timer Card** appears in the card picker.
9. Add a card without adding any separate Lovelace resource.
10. Verify Expanded, Compact, Mini and Tile.
11. Verify visual editor saves changes.

PASS: one integration installation provides both backend and card.

## C. Clean HACS installation from `main` before release

After candidate files are uploaded to GitHub `main` and GitHub Actions is green:

1. In the clean test Home Assistant instance, add/find `abel-smart-timer/smart-entity-timer` in HACS.
2. Choose Download/Redownload.
3. Under **Need a different version?**, select the default branch `main`.
4. Restart Home Assistant.
5. Add/configure Smart Entity Timer.
6. Confirm the card appears without installing `smart-entity-timer-card`.
7. Confirm HACS shows only Smart Entity Timer as the downloaded product for this test.

PASS: HACS `main` installs a working all-in-one package before a stable release exists.

## D. Upgrade from the current separated 0.3.0 installation

Start with:

- Smart Entity Timer 0.3.0 installed from HACS;
- Smart Entity Timer Card 0.3.0 installed from HACS;
- at least two existing timer Config Subentries;
- at least one existing Mini card and one other layout;
- at least one automation referencing an existing timer status sensor.

Procedure:

1. Wait for every timer to become idle.
2. Create a full Home Assistant backup.
3. Record existing status-sensor entity IDs and card YAML.
4. HACS > Smart Entity Timer > Redownload > choose `main`.
5. **Do not restart yet.**
6. HACS > Smart Entity Timer Card > Remove.
7. Confirm the old standalone card files/resource are removed by HACS.
8. Restart Home Assistant.
9. Fully close/reopen the Companion App or hard-refresh the browser.
10. Confirm all timer Config Subentries still exist.
11. Confirm all recorded entity IDs are unchanged.
12. Confirm all existing dashboard cards render without YAML edits.
13. Confirm Mini still collapses editing controls while active.
14. Confirm existing automations still reference valid entity IDs.

PASS: the 0.3.0 + Card 0.3.0 setup becomes 1.0.0 all-in-one without dashboard or entity migration.

## E. Timer functional regression

For at least one `switch`/`light` and one mode-style target such as `climate` if available:

- E1 Start an OFF timer and let it finish.
- E2 Start an ON timer and let it finish.
- E3 Cancel manually.
- E4 Reach the requested target state externally before expiry; verify auto-cancel.
- E5 Verify start is rejected when target is unavailable.
- E6 Verify start is rejected when target is already in the desired state.
- E7 Verify final race-safe target recheck still works.
- E8 Verify duration/action changes synchronize between two open clients.

## F. Restart persistence

- F1 Start a timer, restart HA before expiry, verify it resumes to the original finish time.
- F2 OFF timer expires while HA is down; verify configured post-start execution behavior.
- F3 ON timer expires while HA is down; verify safe skip behavior by default.
- F4 Verify no duplicate timer action after restart.

## G. Notifications and events

- G1 Completion notification.
- G2 Error notification.
- G3 Manual-cancel notification when enabled.
- G4 Auto-cancel notification when enabled.
- G5 Custom title/message placeholders still render correctly.
- G6 Confirm lifecycle events: started, completed, cancelled, skipped, error.

## H. Frontend packaging / cache

- H1 Browser console logs `SMART ENTITY TIMER CARD 1.0.0`.
- H2 No `/hacsfiles/smart-entity-timer-card/...` resource is needed after standalone card removal.
- H3 No `CustomElementRegistry` duplicate-definition error appears.
- H4 Hard refresh / app restart loads the same bundled card.
- H5 Restart Home Assistant twice and confirm frontend registration remains stable.

## I. Release gate

Do not publish `v1.0.0` until A–H pass.

Before pressing **Publish release**:

- GitHub Actions is green on `main`.
- `manifest.json` and bundled `CARD_VERSION` both say `1.0.0`.
- Release notes are final.
- No timer is active on the instance used for the final upgrade verification.
- The immutable release warning is understood: the tag/assets cannot be replaced after publication.

After publishing `v1.0.0`, verify HACS offers `1.0.0` normally, then request removal of `smart-entity-timer-card` from the default HACS catalog.
