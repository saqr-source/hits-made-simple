# HITS Made Simple — Launch campaign: "Look closer / ركّز"

For every Al Safy employee in every function: head office, branches, warehouses, support teams.

## 1. Idea

Everyone in the group uses HITS for the same few things: leave, permissions, attendance and, for managers, approvals. Most people know the main button. Few know the details, for example:
- where past requests go;
- what the ⋮ button does;
- that nothing is approved until you press موافق.

The campaign shows one real detail of the HITS app, circles it with the playbook's gold ring and asks a question. It does not give the answer. The answer is one stop inside the playbook.

- Arabic line: **ركّز في التفاصيل.. كل طلب ليه طريق.**
- English line: **Look closer. Every request has a route.**
- Closing line on every piece: **اختار طريقك · عدّي كل المحطات · خُد الميدالية** / **Pick your route · Clear every stop · Earn the medal**

## 2. Rollout

| When | What | Where |
|---|---|---|
| Week −1 | 4 teasers, one every 2 days, with the line "The answer opens on [launch date]" | WhatsApp groups, notice boards at every site |
| Launch day | Reveal poster with QR, plus the launch email | Notice boards, WhatsApp, email |
| Weeks 1–3 | 4 answer cards, one per teaser, each naming the route and stop that answers it | WhatsApp, notice boards |
| Launch week | Manager card (see section 5) | Sent to managers only |

## 3. Teasers and answers

Each teaser uses a real screen from `details/` in the asset pack. Answer cards repeat the same screen with the ring and add the route and stop.

| # | Real screen | Arabic question | English question | Answer: route → stop |
|---|---|---|---|---|
| 1 | `ar/en_leave_balance` | رصيد إجازاتك قدامك.. تعرف تقراه صح؟ | Your leave balance is right here. Can you read it right? | My time off → Leave balance |
| 2 | `ar/en_permission_form` | إذن ساعتين.. تبدأ منين؟ | A two-hour permission. Where do you start? | My time & attendance → Request a permission |
| 3 | `ar/en_my_attendance` | حضورك متسجل.. بس فين؟ | Your attendance is recorded. But where? | My time & attendance → My attendance |
| 4 (managers) | `ar_approve_all_confirm` | دوست موافقة الكل.. وبعدين إلغاء. الطلبات راحت فين؟ | You tapped Approve All, then Cancel. What happened to the requests? | Approve your team's requests → Permission approvals |

## 4. Which Claude Design template to choose

| Template | Use it? | For |
|---|---|---|
| **Flier** | **Yes, the main one** | Teasers, answer cards, reveal poster, manager card |
| Animation | Optional, after the Fliers are approved | One 10-second teaser: the ring travels over a real screen and lands on the detail |
| HTML email | Yes | The launch email to staff who have company email |
| Mobile app design, UI mockups, Wireframe | **No** | These redraw app screens. HITS screens must stay real. |
| Slides, Document, Blank, Diagram, others | No | Not needed |

Use one Claude Design project per template, all with the **Al Safy HITS Playbook Design System** selected. Attach `HITS_Campaign_Asset_Pack.zip` to each.

## 5. Manager card (replaces the "managers' huddle")

"Huddle" meant a 2-minute talk a manager gives the team at the start of a shift or meeting. It is replaced by a simple one-page card. The manager can read it out or just forward it. It has three lines and the QR:
1. "Our HR requests now have a guide: HITS Made Simple."
2. "Pick Employee for your own requests. I use Manager for approvals."
3. "Try one stop today. It takes a few minutes."

## 6. Prompts (copy as is)

### A. Flier (main)

> Create the launch set for "HITS Made Simple / HITS ببساطة", an Al Safy Group guide that teaches every employee, in every function (head office, branches, warehouses, support), how to use the HITS HR app. The guide works like a journey: routes, stops, points, and a medal at the end. The campaign is called "Look closer / ركّز". Its job is to make people curious about a small detail of the app so they open the guide to find the answer.
>
> Use only the attached asset pack. The HITS screens in it are real app screens with dummy names. Never redraw, retype, translate, recolour, mirror or "improve" any HITS screen. You may only crop, scale, dim the area around a detail, and place the playbook's ring over the detail. Do not show people, stock photos, phones held by hands, or product shots. Do not add new logos. Use the Al Safy logo plate and the QR from the pack as they are.
>
> Make these pieces, each in an Arabic version (right-to-left, Egyptian everyday tone) and an English version:
> 1. Four teasers, 1080×1080 and A4 portrait. Each shows one real screen from `details/`, cropped close on one detail with the ring around it. It has one question and the line "The answer opens on [launch date] / الإجابة يوم [تاريخ الإطلاق]". No QR on teasers. The questions are:
>    - leave_balance: "رصيد إجازاتك قدامك.. تعرف تقراه صح؟" / "Your leave balance is right here. Can you read it right?"
>    - permission_form: "إذن ساعتين.. تبدأ منين؟" / "A two-hour permission. Where do you start?"
>    - my_attendance: "حضورك متسجل.. بس فين؟" / "Your attendance is recorded. But where?"
>    - ar_approve_all_confirm, for managers: "دوست موافقة الكل.. وبعدين إلغاء. الطلبات راحت فين؟" / "You tapped Approve All, then Cancel. What happened to the requests?"
> 2. A reveal poster, A3 portrait and 1080×1350. Headline: "ركّز في التفاصيل.. كل طلب ليه طريق." / "Look closer. Every request has a route." Show the journey (routes, stops, medal) using the real playbook screens from the pack: the home screen, one step with the ring, and the stop-complete screen. Include the QR and the line "اختار طريقك · عدّي كل المحطات · خُد الميدالية" / "Pick your route · Clear every stop · Earn the medal".
> 3. Four answer cards, 1080×1080. Each uses the same screen as its teaser and names the place in the guide that answers it: Route "My time off" → Stop "Leave balance"; "My time & attendance" → "Request a permission"; "My time & attendance" → "My attendance"; "Approve your team's requests" → "Permission approvals". Add the QR.
> 4. A manager card, A5 portrait, with three short lines and the QR: "Our HR requests now have a guide: HITS Made Simple." / "Pick Employee for your own requests. I use Manager for approvals." / "Try one stop today. It takes a few minutes." Write the Arabic version naturally; do not translate word for word.
>
> Keep text minimal: one question or headline per piece, and the detail is the hero. Never mix Arabic and English in one sentence. HITS screen labels stay exactly as they appear on the screen. Start with teaser 1 in both languages so I can approve the direction before you make the rest.

### B. Animation (optional, after the Fliers are approved)

> Using the approved "Look closer / ركّز" teaser 1 and the attached asset pack, make a 10-second square (1080×1080) teaser for WhatsApp, in Arabic and in English. Start on the full real screen `details/ar_leave_balance.png` (English: `en_leave_balance.png`), dimmed. The playbook's ring glides in and settles on the balance detail. The screen pushes in slowly (about 5%), the question appears, then the end frame shows "The answer opens on [launch date]". The motion should be calm and precise, with no bouncing or spinning. The HITS screen must stay exactly as supplied: no redrawing, no added UI. No sound needed.

### C. HTML email

> Using the approved reveal poster and the attached asset pack, make a launch email for all Al Safy employees, in one Arabic version (right-to-left) and one English version. Subject: "ركّز في التفاصيل.. HITS ببساطة وصل" / "Look closer: HITS Made Simple is here". Body:
> - one real playbook screen with the ring;
> - three lines: what the guide is, that it has a route for employees and for managers, and that each stop ends with a quick question and points;
> - one button, "ابدأ الآن" / "Start now", linking to [playbook URL];
> - the QR for people reading on a computer.
>
> Keep it short enough to read without scrolling on a phone. Use the Al Safy logo plate as supplied. Never redraw HITS screens.

## 7. Before sending anything
- Replace [launch date] and [playbook URL]. The QR in the pack points to https://saqr-source.github.io/hits-made-simple/, which serves the playbook after launch.
- Check every piece: real screens only, dummy names only, no mixed-language sentences.
