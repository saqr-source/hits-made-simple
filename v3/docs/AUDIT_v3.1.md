# HITS Made Simple v3.1 — Independent QA Audit

Date: 2026-10-20 · Build: http://localhost:8765/v3/ · Source: /home/claude/hits-made-simple/v3/
Method: overlaid all 75 step hotspots on their real screens (`audit/overlay/*.png`); full-size PII inspection of all 30 screens; Playwright sweep of all 18 stops × every step/tip/quiz/result at 390×844, 360×740 (touch), 1440×900, EN + AR (`audit/shots/`, metrics in `audit/sweep_*.json`); gamification run (`audit/game/game_log.txt`); zoom-fidelity run (`audit/zoom/`); manager home/search/help (`audit/shots/MGR_*`, `help_*`).
All paths below are relative to `/tmp/claude-0/-home-claude/19d6f8f5-c286-53d2-bab7-4ae3f11ea842/scratchpad/audit/`.

## Overall score: 81 / 100

| Area | Score | Rationale |
|---|---|---|
| 1. Accuracy | 72 | All 75 hotspots sit on the right control; the gaps are process claims the screens don't show (approve → save, filter entry points) and four steps that use a screen from a different tab or state. |
| 2. Personal data | 78 | Names, photos, IDs and balance numbers are masked well. Leaks remain: the leave-taken bar heights can be read against the axis, and the first letters of names show in notifications and on the light home screen. |
| 3. Arabic | 80 | The Arabic is natural and HITS labels stay in English as intended. Problems: the brand name is cut off in the header, the Start arrow points the wrong way, some number/noun pairs are ungrammatical, and the percent sign is flipped. |
| 4. Gamification | 95 | Points are awarded once (10 + 10), replay adds nothing, wrong answers show the right answer plus encouragement, confetti fires once, progress bars are correct, and answer order is shuffled (12 runs: 4/5/3). Only cosmetic issues. |
| 5. Layout | 88 | No step scrolls at 360/390 in either language. Back is always left and Next always right. Start is always visible above the fold. Zoom shows the same screen, including 12345 and the dots. Minor overlaps and truncation. |
| 6. Copy | 80 | Plain and consistent overall, but "task"/"mission" wording is still in search, the privacy line and page metadata. "Watch again" and "Ride again" are wrong metaphors. |
| 7. Console | 100 | No page or console errors in any run. |

## Findings

| ID | Sev | Stop / step / file | What is wrong | Evidence | Suggested fix |
|---|---|---|---|---|---|
| H1 | High | approve-permissions ap-05 (+ tip), leave-approvals la-02, tk-approvals tk-03 | These steps say "approve or reject, then save" and mention Approve All / Reject All, but no screen shows the decision controls or the save action. That is the core outcome of the approval stops, and the ap-05 quiz ("closed without saving") tests a step learners never see. Undocumented process → SOURCE VALIDATION REQUIRED. | overlay/perm_current.png, shots/m390_en_ap-05.png, overlay/leave_approvals.png, overlay/tk_filter.png | Capture the ✓ sheet (Approve/Reject/Approve All/Save) and the confirmation, then add steps. Until then, remove the save claims or mark them as pending validation. |
| H2 | High | assets/screens/days_count.webp (balance-app-04) | The value labels are blurred, but each bar's height is still readable against the y-axis (about 8, 8, 5, 22, 1, 1 days). That reveals the person's leave taken, which balance.webp and balance_periods.webp deliberately hide. | overlay/days_count.png | Blur the whole plot area, or crop/fill the bars and keep only the axis labels. |
| M1 | Medium | assets/screens/notifications.webp (nt-02) | The first letter of each employee name is unmasked ("employee E…", "Y…", "E…", "A…"), and so are the "…cation:" fragments. Together with the exact leave and permission dates, a small team could be re-identified. | z_notif.png | Widen the blur boxes left to cover the word after "employee". |
| M2 | Medium | assets/screens/home_light.webp | The greeting shows "Hi … El…": the first two letters of the second name line are unmasked. | z_homelight.png | Extend the blur to x≈140. |
| M3 | Medium | approve-permissions ap-04 | The detail screen shows Status: Approved for an 11/10/2026 request, which is not in the Current list from ap-03. A learner on the "waiting for you" flow sees an already-approved item. | overlay/perm_detail.png | Use a detail capture of a pending Current request, or say on screen that this is an example request. |
| M4 | Medium | leave-approvals la-02, la-03 | The Current and Monitoring steps run on a capture with the History tab selected and History content. The ring sits on the tab label, but the list contradicts the text. | overlay/leave_approvals.png | Capture the Current and Monitoring tabs separately. |
| M5 | Medium | find-permissions fp-04/fp-05 | The Permissions Filter was captured over the Monitoring tab (underlined), but the stop says it is in History. | overlay/perm_filter.png | Recapture from the History tab. |
| M6 | Medium | geo-attendance geo-04 → geo-05 | The flow jumps from tapping History straight to the Time Keeping Filter dialog. No step shows how the filter opens (the funnel button is only visible faded in the background). | overlay/geo.png, overlay/geo_filter.png | Add a step "Tap the filter button" on the History list, or confirm the dialog opens automatically. |
| M7 | Medium | app-settings settings-app-01/02 | The step says Settings opens from the gear on the login screen, but the Settings capture shows LOG OUT, which is a signed-in state. Entry point and screen may not match. | overlay/settings.png | Validate with SME. If it is reached after login, change the path to Home › gear. |
| M8 | Medium | my-permissions tip; permission-history tip | Policy claims that no screen shows: "Personal late permission is capped at 2 hours a month… HITS blocks the request", and that times must be entered in 24-hour format. | data.js tips | Cite the manual or SME, or remove. Policy numbers need P&C sign-off. |
| M9 | Medium | UI strings (data.js ui.*), index.html meta description | Old terminology is still there: EN "Search tasks", "No tasks match your search.", privacy "…completed tasks…"; AR "ابحث عن مهمة", "لا توجد مهام تطابق بحثك.", "المهام المكتملة"; meta description "step-by-step missions". | shots/MGR_search_m390_ar.png | Change to "Search stops" / "ابحث عن محطة", "No stops match" / "لا توجد محطات", "completed stops" / "المحطات المكتملة", and "routes" in the meta tag. |
| M10 | Medium | Header brand (AR, all mobile widths) | Because the header is forced LTR, "HITS ببساطة" truncates to "HITS ة…" or "HITS …طة", which garbles the series name. EN is also cut to "HIT…" at 360. | shots/m360_ar_signin-app-o365.png, game/g6ar_ans.png | Hide the wordmark under 400px or let the header shrink it. Give the brand its own `dir="rtl"` in AR. |
| M11 | Medium | Task intro (AR) | The Start button uses the right-pointing arrow (`ic('arrow')` is hard-coded), and so does the "كل المشاوير" back link. In Arabic, forward and back point the same way. | shots/m360_ar_signin-app_intro.png | Use `ic(S.lang==='ar'?'back':'arrow')` on #startbtn, as the home route CTA already does. |
| L1 | Low | Arabic plurals/number formats | "{n} نقطة" gives "١٠ نقطة" (should be "١٠ نقاط"). Total "٠ من ١١ محطات" should use "محطة" for 11 and up. A 2-stop route reads "٢ من ٢ محطات" (should be "محطتين"). "حوالي ١ دقيقة" should be "حوالي دقيقة". "٠+ نقاط" for a wrong answer. "%٠" should be "٠٪". | shots/home_m390_ar_*.png, game/g6ar_result.png | Add a small Arabic plural helper. Format percentages with Intl ('ar-EG', style:'percent'). |
| L2 | Low | AR praise | "إجابة صحيحة! إجابة في محلّها!" repeats "إجابة". | game/g7ar_ans.png | Change the praise to "في محلّها!". |
| L3 | Low | Digits (AR) | The UI uses Arabic-Indic digits, but helper copy and HITS data show Latin "12345" and dates. The mixing is acceptable, but decide on it. | shots/m360_ar_signin-app-02.png | Record a decision in the log: Arabic-Indic for app counters, Latin for anything typed into HITS. |
| L4 | Low | Result screen copy | "Watch again" (شاهِد مرة أخرى) when there is no video, and "Ride again" on a completed route card. "+0 pts" is shown for a wrong answer. | game/g6ar_result.png, game/home_after.png | "Do it again" / "أعِد المحطة"; "Review route" / "راجِع المشوار"; hide the answer row when 0. |
| L5 | Low | signin-app-o365 | The stop is for employees without a work email, yet step 2 teaches the Office 365 path (one audience, one task). | shots/m390_en_signin-app-o365.png | Move it to a separate "Sign in with Office 365" stop, or keep it as a branching tip only. |
| L6 | Low | Unverified helper claims | settings-app-03 says the app "also offers Arabic and French". leave-app-07 says the ⋮ menu has "Submit" (the list ⋮ menu shows Filter/Balance/New). The leave tip says the Mission destination is mandatory. tr-02 says "your own name is always first" (masked, can't be verified). | overlay/leave_menu.png | Confirm with SME or the manual, or drop. |
| L7 | Low | Ring scope | leave-app-04 has no ring on the types list (it could ring Annual 1/2 Day). myperm-app-02 rings only Permission Hours although the text names Count too. balance-app-03 rings the expanded panel, not the header you tap. geo-05 text says "tap OK", but only the dates are ringed. | overlay/leave_types.png, overlay/my_permissions.png | Adjust the hotspots. |
| L8 | Low | my-permissions | A light-theme capture sits inside a dark-theme stop with no "Light theme" helper, unlike the other stops. | overlay/my_permissions.png | Add the helper or recapture in dark. |
| L9 | Low | login_filled.webp | The 12345 overlay box ends at x≈85%, so a sliver of the blurred real username (olive) shows beside the X. It is not readable. | zoom/m360_ar_s3_zoom.png | Widen the type box to w≈80 or fill the blurred patch. |
| L10 | Low | Unused asset | assets/screens/perm_approvals.webp (with blurred real photos) is shipped but no step references it. | overlay/perm_approvals.png | Remove from the build. |
| L11 | Low | Zoom chip at 360 | "Tap to enlarge" overlaps the bottom of the phone screen (the © footer and home bar). | shots/m360_en_signin-app-02.png | Move it below the stage, or give it a smaller offset. |
| L12 | Low | Quiz at 360×740 | After answering, the feedback needs 100–200px of scrolling and sits partly behind the fixed bar until it auto-scrolls. Intros scroll 30–350px, but Start stays visible. | sweep_m360_*.json, shots/m360_en_forgot-password_quizans.png | Collapse the dimmed options after answering, or put the answer explanation in a smaller font. |
| L13 | Low | RTL gestures | In Arabic, swipe-left and ArrowRight still mean Next, and the image slides LTR. | app.js bindStage / keydown | Mirror the swipe direction and arrow keys when `lang==='ar'`. |
| L14 | Low | Manager role | The manager view hides "My time off" and "My time & attendance". This is noted in the UI, but search still lists employee stops, which is fine. No issue beyond the note's wording. | shots/MGR_home_m390_en.png | None required. |

### Verified OK
- All 75 hotspots are on the control the text names. Overlays: overlay/*.png.
- Zoom shows the same screen as the step, including the typed 12345 and the password dots: zoom/*.png, matched to the stage `src` at every sign-in step in EN and AR, mobile and desktop.
- Points: 10 + 10 on the first right answer, 10 on a wrong one, 0 on replay. The total went 20 → 20 (replay) → 30 → 50 → 50 (replay). The quiz hides the "+10" badge on replay.
- The route completion celebration fires once and not on replay. The next-stop card points to the first stop still not done. Home bars showed 100% / 0% / 0% after the "Get started" route.
- Back is left and Next right at every measured state, in all 6 viewport and language combinations. No horizontal scroll anywhere.
- No console or page errors (the server restart mid-run did not affect results; all 900 measurements are complete).

## Fix log (applied after the audit, same day)
| ID | Status | Action |
|---|---|---|
| H1 | Open — SME | Save step is sourced from the HITS App User Guide and My HR Operational Manual; screens of the ✓ sheet and Save confirmation still needed. Kept with `?review=1` tag. |
| H2 | Fixed | Chart plot area and scale labels heavily blurred. |
| M1, M2 | Fixed | Notification and greeting masks widened. |
| M3 | Fixed | Helper says the detail screen is an approved example. |
| M4 | Fixed | Leave approvals rewritten: tabs explained in one step, the History example labelled as History. |
| M5 | Accepted | Filter dialog over a dimmed tab; content of the step is correct. |
| M6 | Fixed | GEO filter step now says "tap the filter button" first (SME confirm). |
| M7 | Open — SME | Settings entry point (approved in v2.2). |
| M8 | Fixed | Late-permission cap and 24-hour format are cited from the HITS App User Guide. |
| M9 | Fixed | Search, privacy and page description use stops/routes wording. |
| M10 | Fixed | Brand name wraps to two lines on small phones; correct direction per language. |
| M11 | Fixed | Start arrow points forward in Arabic. |
| L1, L2, L4 | Fixed | Arabic counted nouns, percent, praise wording, "Do it again" / "Review route", 0-point row hidden. |
| L8, L9, L10, L12 | Fixed | Light-theme helper, wider type box, unused screen removed, dimmed options collapse after answering. |
| L5, L13 | Decision | Office 365 shown inside the sign-in stop at SaQr's request; swipe/arrow keys follow the fixed Back-left / Next-right layout in both languages. |
