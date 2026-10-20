# HITS Made Simple v3.1 — Plan, Coverage Map and Build Prompts

Owner: Talent Development, People & Culture, Al Safy Group · Updated 20 Oct 2026

## 1. The plan (5 phases, one gate each)

| # | Phase | Output | Gate |
|---|---|---|---|
| 0 | Coverage map | Every HITS tile vs. the 31 screenshots and the v2.2 photos (section 2) | Done |
| 1 | Prompts & specs | Claude Design hero-screen prompt and Claude Code build spec, with the handoff between them (sections 3–4) | Done |
| 2 | Build v3.1 | Preview at `/v3/` on GitHub Pages; the site root keeps v2.2 | SaQr tests on a phone |
| 3 | Independent audit | Scored audit report + fixes (separate reviewer) | Sign-off |
| 4 | Launch | Promote v3 to the root link, QR code, announcement, optional tracking | Go-live |

## 2. Coverage map

Legend: ✅ covered with real screens · ⚠ covered, one step needs SME confirmation · ⛔ no screenshot yet (shown as "coming soon")

### Employee
| App tile / screen | Stop in the playbook | Screens used | Status |
|---|---|---|---|
| Login: Office 365 vs Work ID | Sign in to HITS (6 steps: open, OFFICE 365 choice, Work ID typed as 12345, password dots, LOGIN, home) | v2.2 login photos, home | ✅ |
| Forgot my password? | Forgot your password? | login, forgot | ✅ |
| Settings (theme, language) | Theme and language | login, settings | ✅ |
| My Leaves (balance, days taken, chart) | Check your leave balance (4 steps) | home, #30, #27, #26 | ✅ |
| Leaves Request › ⋮ › Balance | Check your balance before you request | #16, #18, #19, #20 | ⚠ (⋮ opens the menu) |
| Leaves Request › + (new) | Submit a leave request (7 steps) | v2.2 photos | ✅ |
| Leaves Request › Current / History | Follow up your leave requests | home, #25 | ✅ |
| My Permissions | Check your permission hours | v2.2 photos | ✅ |
| Permissions Request › Current / History | Follow up your permission requests | home, #24 | ⚠ (+ opens a new request) |
| My Attendance | Check your attendance | home, #23 | ⚠ (meaning of Over/Short Hours) |
| GEO Attendance (In, Out, History, filter) | Record attendance by location (5 steps) | #16, #04, #01 | ⚠ (location prompt, History) |
| My Payslip | — | none | ⛔ |
| My Profile (details) | — | list only (#17) | ⛔ |
| Changes Request | — | list only (#14) | ⛔ |
| Permissions Request › new form | — | none | ⛔ |
| Incomplete TK Request › new form | — | list only (#08) | ⛔ |
| Office 365 pages after the button | — | none | ⛔ |

### Manager / Approver
| App tile / screen | Stop | Screens used | Status |
|---|---|---|---|
| Notifications (bell) | See what's waiting for you | #16, #03 | ✅ |
| Permissions Approvals › Current › details › ✓ | Approve time permissions (5 steps) | home, #21, #22 | ⚠ (✓ then save) |
| Permissions Approvals › History › filter | Find past permission requests | #16, #10, #07 | ✅ |
| Leaves Approvals (Current / Monitoring / History, filter) | Approve leave requests | #16, #13 | ⚠ (meaning of Monitoring) |
| Incomplete TK Approvals (filter) | Approve missing-time requests | #16, #06 | ⚠ |
| Name list in My Leaves / My Attendance / My Permissions | Open a team member's record | #16, #15 | ⚠ (tap opens their record) |
| Changes Approvals | — | none | ⛔ |
| Attendance Tracking | — | none | ⛔ |
| Screen after Approve / Save | — | none | ⛔ |

Totals: 11 employee stops and 6 manager stops, 68 steps, each on a real masked screen.
Screens unused on purpose: #02, #05, #08, #11, #12, #14 and #17 repeat the name list from #15; #28 duplicates #30 under a screen-recorder overlay; #29 duplicates #13; #31 duplicates #26/#30.

## 3. Claude Design prompt — hero screens only

Use it in the "HITS Playbook" project with the **Al Safy HITS Playbook Design System**. Attach `HITS_v3.0_preview.png` and the current site link.

> Design three hero screens for **HITS Made Simple / HITS ببساطة**, a phone-first playbook that teaches employees the HITS Easy Go app. Keep the locked palette (Cream #FAF6F0, Tan #C9A87C, Navy #1B2A4A, Deep Navy #0E1526, Ink #262628), Montserrat + Source Sans 3, Noto Kufi Arabic + Noto Sans Arabic, and the dark, premium, product-led look. Never draw or imitate any HITS app screen: leave the phone screen as a flat placeholder labelled SCREEN.
> 1. **Routes home (390×844):** headline "What do you need to do?", Employee | Manager switch, points chip, and route cards (title, one-line outcome, progress bar "2 of 4 stops", numbered stops, Start route button). The metaphor is a journey: routes made of stops.
> 2. **Stop player (390×844):** progress row, the phone plate with a glowing gold pointer and a spotlight ring on one control, a two-tone headline (cream line, tan line) with a short gold rule, one line of text, and a fixed bottom bar with Back on the left (small) and Next on the right (large). The bar must keep the same positions in Arabic.
> 3. **Stop complete (390×844):** a gold medal, "Stop complete", points earned (+10 stop, +10 right answer), a route progress bar and a "Next stop" card. Also show a route-complete variant with a restrained gold confetti burst.
> Export each as **Standalone HTML**. Output only these three screens: no content, logic or extra pages.

## 4. Claude Code build spec (what this repository implements)

- **Static site** on GitHub Pages: `v3/index.html`, `assets/app.js`, `assets/app.css`, `assets/data.js` (generated), `assets/config.js`. An offline single-file build comes from `tools/build_offline.py`.
- **Content** lives only in `tools/build_data.py`: routes, stops, steps (screen, hotspot, two-tone headline, text, helper, optional typed input), one-at-a-time tips, and a final question per stop. Approved v2.2 copy is loaded verbatim from `tools/source_v22_content.json`.
- **Screens** come from `tools/process_screens.py`. Each is cropped to the 492:1052 slot and personal data is blurred and pixelated: names, IDs, titles, photos, balances and counts. The UI is never redrawn.
- **Player:** intro (title, outcome, step count, Start right away, phone preview) → steps (animated pointer, tap ripple, spotlight, slide transition, typing for Work ID / password) → tip card when one belongs to that step → final question (shuffled options, +10 for a right first answer, the correct answer and encouragement when wrong) → stop complete (points, route progress, next stop, confetti when the route is finished).
- **Fixed controls:** the header and bottom bar keep the same layout in English and Arabic; Arabic text is right-to-left, with Latin HITS labels isolated.
- **Tracking:** `assets/config.js` `mode` = `off` (default), `anonymous` or `workid`, posting to a Google Form.

### Handoff from Claude Design to Claude Code
1. Export the three hero screens as Standalone HTML and attach them in the Claude project chat.
2. Claude Code extracts only visual decisions (spacing, radii, shadows, card and button styles, motion timing) into `assets/app.css`. Content, logic and screens stay in this repository.
3. Re-run the QA sweep (17 stops × EN/AR × 360, 390 and 1440 widths), then publish to `/v3/` for review.

## 5. Tracking (optional — only if the director asks)

| Mode | What P&C sees | Needs |
|---|---|---|
| off | nothing | — |
| anonymous | opens, stops finished, points per stop, language, role | Google Form with 7 short-answer questions |
| workid | the above **plus Work ID**: who finished, who started, who never opened (compare with the employee list) | the same Form plus a Work ID question, P&C / director approval, and the notice shown to employees |

Form questions (Short answer): Event, Role, Language, Task, Score, Session, Work ID, Department. Send the pre-filled link; Claude wires the entry IDs into `assets/config.js`.

## 6. Open SME confirmations (shown with `?review=1`)
1. Permissions Approvals: ✓ opens Approve / Reject, then save.
2. Leaves Approvals: Monitoring = waiting for an earlier approver.
3. My Attendance: Over/Short Hours = hours above or below the shift.
4. GEO Attendance: location permission prompt; History shows recorded times; Time Keeping Filter.
5. Leaves Request: ⋮ opens Filter / Balance / New.
6. Permissions Request: + starts a new request.
7. Name lists: tapping a team member opens their record.

## 7. v3.2 — Arabic app screens (20 Oct 2026)
- 35 real Arabic-language screens (employee and manager views) added and masked: names, IDs, job titles, photos, balances, counts, address, attendance times.
- In Arabic, every stop now shows the Arabic app screen and names the Arabic button (e.g. طلب الإجازات, موافقة الإذونات). English keeps the English screens.
- Arabic-only stops (English screens still needed to make them bilingual): اطلب إذنًا (perm-request), متابعة الحضور والانصراف (attendance-tracking), اطلب تغيير بياناتك (changes-request), اعتمِد طلبات التغيير (changes-approvals). Leave approvals in Arabic now include موافقة الكل → confirmation dialog (closes audit H1 for leaves).
- Steps still on English screens in Arabic (no Arabic screen with data): permission request details and approval, request history list for permissions, GEO filter, team name list. Each says so in its helper.
