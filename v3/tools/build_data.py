"""Builds assets/data.js for HITS Made Simple v3.
Approved v2.2 copy is loaded verbatim from data_v22_text.json; new tasks are defined below.
Run: python3 tools/build_data.py <data_v22_text.json> assets/data.js"""
import json, sys

V22 = json.load(open(sys.argv[1]))
OUT = sys.argv[2]
T22 = {t['id']: t for t in V22['tasks']}

def L(en, ar): return {'en': en, 'ar': ar}
def H(en1, en2, ar1, ar2): return {'en': [en1, en2], 'ar': [ar1, ar2]}
def hs(x, y, w, h): return {'x': x, 'y': y, 'w': w, 'h': h}

# ---------- hotspots (percent of the 492:1052 slot) ----------
DARK = {
    'myLeaves': hs(52.0, 22.5, 20.1, 14.3), 'leavesRequest': hs(76.1, 22.4, 20.8, 14.1),
    'myPermissions': hs(27.7, 38.0, 20.5, 13.9), 'permissionsRequest': hs(52.0, 38.0, 20.5, 14.0),
    'myAttendance': hs(52.0, 53.6, 20.5, 14.0),
}
LIGHT = {
    'bell': hs(75.5, 7.5, 9.0, 5.0), 'leavesApprovals': hs(28.5, 42.1, 19.5, 13.5),
    'permissionsApprovals': hs(5.6, 57.2, 19.4, 13.5), 'tkApprovals': hs(51.8, 57.2, 19.5, 13.5),
    'geo': hs(5.6, 72.7, 19.4, 13.5),
}
# hotspots of the approved v2.2 steps (unchanged)
V22HS = {
    'signin-app-01': None, 'signin-app-02': hs(4.5, 54.6, 90.6, 7.1), 'signin-app-03': hs(4.5, 64.4, 90.6, 7.1),
    'signin-app-04': hs(3.8, 64.1, 45, 5.7), 'signin-app-05': None,
    'forgot-app-01': hs(60.2, 80.7, 36.8, 3.2), 'forgot-app-02': hs(13.5, 38.7, 78.5, 18.4), 'forgot-app-03': hs(13.2, 61.3, 79.5, 5.6),
    'settings-app-01': hs(83, 1.2, 12, 5.5), 'settings-app-02': hs(7.6, 31.3, 85.1, 19.2), 'settings-app-03': hs(7.6, 21.5, 85.1, 8.1),
    'leave-app-01': DARK['leavesRequest'], 'leave-app-02': hs(62.9, 86.8, 14.7, 6.6), 'leave-app-03': hs(3.3, 14.5, 82.5, 4.5),
    'leave-app-04': None, 'leave-app-05': hs(3.3, 20.2, 61.1, 10.0), 'leave-app-06': hs(1.7, 35.1, 96.5, 49.8), 'leave-app-07': hs(62.9, 87.0, 15.2, 6.6),
    'myperm-app-01': DARK['myPermissions'], 'myperm-app-02': hs(1, 7.5, 98, 60),
    'balance-app-01': DARK['myLeaves'],
}
V22SCREEN = {
    'signin-app-01': 'login_empty', 'signin-app-02': 'login_empty', 'signin-app-03': 'login_empty', 'signin-app-04': 'login_filled', 'signin-app-05': 'home_dark',
    'forgot-app-01': 'login_empty', 'forgot-app-02': 'forgot', 'forgot-app-03': 'forgot',
    'settings-app-01': 'login_empty', 'settings-app-02': 'settings', 'settings-app-03': 'settings',
    'leave-app-01': 'home_dark', 'leave-app-02': 'leave_list', 'leave-app-03': 'leave_form', 'leave-app-04': 'leave_types',
    'leave-app-05': 'leave_form', 'leave-app-06': 'leave_form', 'leave-app-07': 'leave_form',
    'myperm-app-01': 'home_dark', 'myperm-app-02': 'my_permissions', 'balance-app-01': 'home_dark',
}

def from_v22(tid, extra_steps=None, replace_steps=None, check=None, gtk=None, outcome=None):
    t = T22[tid]
    plat = next(p for p in t['platforms'] if p['id'] == 'app')
    steps = []
    for s in plat['steps']:
        if replace_steps and s['id'] in replace_steps:
            steps.append(replace_steps[s['id']]); continue
        steps.append({'id': s['id'], 'headline': s['headline'], 'text': s['text'], 'helper': s.get('helper'),
                      'screen': V22SCREEN[s['id']], 'hotspot': V22HS[s['id']]})
    steps += extra_steps or []
    return {'id': tid, 'icon': t['icon'], 'name': t['name'], 'situation': t['situation'], 'title': t['title'],
            'purpose': t['purpose'], 'outcome': outcome, 'path': plat.get('path'),
            'goodToKnow': [g['text'] for g in (gtk if gtk is not None else (t.get('goodToKnow') or []))],
            'helpCard': bool(t.get('helpCard')), 'check': check or t.get('check'), 'steps': steps}

def S(i, screen, hot, headline, text, helper=None, verify=None):
    return {'id': i, 'screen': screen, 'hotspot': hot, 'headline': headline, 'text': text, 'helper': helper, 'verify': verify}

def Q(q, opts):
    return {'q': q, 'options': [{'text': o[0], 'correct': o[1], 'why': o[2]} for o in opts]}

TASKS = {}

# ===== Get started (approved v2.2) =====
TASKS['signin-app'] = from_v22('signin-app', outcome=L('You can sign in to HITS Easy Go.', 'تستطيع تسجيل الدخول إلى HITS Easy Go.'))
TASKS['forgot-password'] = from_v22('forgot-password', outcome=L('You can start recovering your HITS password.', 'تستطيع بدء استرجاع كلمة مرور HITS.'))
TASKS['app-settings'] = from_v22('app-settings', outcome=L('You can set the app to match this guide.', 'تستطيع ضبط التطبيق ليطابق هذا الدليل.'))

# ===== My time off =====
TASKS['leave-balance'] = from_v22('leave-balance',
    replace_steps={'balance-app-02': S('balance-app-02', 'balance', hs(2.8, 12.9, 94.2, 43.2),
        {'en': ['Read your', 'balance.'], 'ar': ['اقرأ', 'رصيدك.']},
        L('Leaves Balance shows your Annual, Holiday and Day Off balance, and what you have taken.',
          'يعرض قسم Leaves Balance رصيدك من Annual وHoliday وDay Off، وما استخدمته منها.'),
        L('Period shows the time range — here, Current Year.', 'يحدّد Period الفترة المعروضة، وهي هنا Current Year.'))},
    extra_steps=[S('balance-app-03', 'days_taken', hs(2.8, 32.3, 94.2, 53.6),
        H('See the days', 'you have taken.', 'اعرف', 'الأيام التي استخدمتها.'),
        L('Tap No. of Days Taken to see the days you have used for each leave type.',
          'اضغط No. of Days Taken لتعرف الأيام التي استخدمتها من كل نوع إجازة.'))],
    check=Q(L('Where do you check how many annual leave days you have left?', 'أين تعرف عدد أيام إجازتك السنوية المتبقية؟'), [
        (L('My Leaves', 'My Leaves'), True, L('My Leaves shows your balance and the days you have taken.', 'يعرض My Leaves رصيدك والأيام التي استخدمتها.')),
        (L('Leaves Approvals', 'Leaves Approvals'), False, L("Leaves Approvals is for approving other people's requests.", 'Leaves Approvals لاعتماد طلبات الآخرين.')),
        (L('Permissions Request', 'Permissions Request'), False, L('Permissions Request is for time permissions, not leave.', 'Permissions Request لطلبات الاستئذان، لا للإجازات.')),
    ]),
    outcome=L('You can find your leave balance and the days you have taken.', 'تستطيع معرفة رصيد إجازاتك والأيام التي استخدمتها.'))

TASKS['leave-request'] = from_v22('leave-request',
    gtk=[g for g in T22['leave-request']['goodToKnow'] if g.get('link') != 'managing-requests'],
    outcome=L('You can send a leave request for approval.', 'تستطيع إرسال طلب إجازة للاعتماد.'))

TASKS['leave-history'] = {
    'id': 'leave-history', 'icon': 'history',
    'name': L('Follow up your leave requests', 'متابعة طلبات إجازتك'),
    'situation': L('Has my leave been decided?', 'هل اتُّخذ قرار في إجازتي؟'),
    'title': H('Follow up your', 'leave requests.', 'تابِع', 'طلبات إجازتك.'),
    'purpose': L('Finds your waiting and past leave requests.', 'يعرض طلبات إجازتك المنتظِرة والسابقة.'),
    'outcome': L('You can find any leave request you have sent.', 'تستطيع العثور على أي طلب إجازة قدّمته.'),
    'path': 'Home › Leaves Request', 'goodToKnow': [], 'helpCard': False,
    'steps': [
        S('lh-01', 'home_dark', DARK['leavesRequest'], H('Tap', 'Leaves Request.', 'اضغط', 'Leaves Request.'),
          L('On the home page, tap Leaves Request.', 'من الصفحة الرئيسية، اضغط Leaves Request.')),
        S('lh-02', 'leave_history', hs(12, 11.2, 76, 5.0), H('Choose', 'Current or History.', 'اختر', 'Current أو History.'),
          L('Current shows requests waiting for a decision. History shows your past requests.',
            'تعرض Current الطلبات التي تنتظر قرارًا، وتعرض History طلباتك السابقة.')),
        S('lh-03', 'leave_history', hs(4.5, 30.6, 91, 11.2), H('Read your', 'request.', 'اقرأ', 'تفاصيل الطلب.'),
          L('Each request shows the leave type, the From and To dates, and the number of days.',
            'يعرض كل طلب نوع الإجازة، وتاريخَي From وTo، وعدد الأيام.')),
    ],
    'check': Q(L('You sent a leave request yesterday and no one has decided yet. Where do you find it?',
                 'قدّمت طلب إجازة أمس ولم يُتّخذ فيه قرار بعد. أين تجده؟'), [
        (L('Leaves Request › Current', 'Leaves Request › Current'), True, L('Current shows requests still waiting for a decision.', 'تعرض Current الطلبات التي ما زالت تنتظر قرارًا.')),
        (L('Leaves Request › History', 'Leaves Request › History'), False, L('History shows your past requests.', 'تعرض History طلباتك السابقة.')),
        (L('My Leaves', 'My Leaves'), False, L('My Leaves shows your balance, not your requests.', 'يعرض My Leaves رصيدك، لا طلباتك.')),
    ]),
}

# ===== My time & attendance =====
TASKS['my-permissions'] = from_v22('my-permissions', gtk=[],
    check=Q(L('Where do you see the permission hours you have used this month?', 'أين ترى ساعات الاستئذان التي استخدمتها هذا الشهر؟'), [
        (L('My Permissions', 'My Permissions'), True, L('Permission Hours shows the hours you have used in the selected Period.', 'يعرض Permission Hours الساعات التي استخدمتها خلال الفترة المحددة.')),
        (L('Permissions Request', 'Permissions Request'), False, L('Permissions Request lists your requests, not your total hours.', 'يعرض Permissions Request طلباتك، لا إجمالي ساعاتك.')),
        (L('My Attendance', 'My Attendance'), False, L('My Attendance shows your attendance, not your permission hours.', 'يعرض My Attendance حضورك، لا ساعات الاستئذان.')),
    ]),
    outcome=L('You can check the permission hours you have used.', 'تستطيع معرفة ساعات الاستئذان التي استخدمتها.'))

TASKS['permission-history'] = {
    'id': 'permission-history', 'icon': 'history',
    'name': L('Follow up your permission requests', 'متابعة طلبات الاستئذان'),
    'situation': L('Where is my permission request?', 'أين طلب الاستئذان الخاص بي؟'),
    'title': H('Follow up your', 'permission requests.', 'تابِع', 'طلبات الاستئذان.'),
    'purpose': L('Finds your waiting and past time-permission requests.', 'يعرض طلبات الاستئذان المنتظِرة والسابقة.'),
    'outcome': L('You can find any permission request you have sent.', 'تستطيع العثور على أي طلب استئذان قدّمته.'),
    'path': 'Home › Permissions Request', 'goodToKnow': [], 'helpCard': False,
    'steps': [
        S('ph-01', 'home_dark', DARK['permissionsRequest'], H('Tap', 'Permissions Request.', 'اضغط', 'Permissions Request.'),
          L('On the home page, tap Permissions Request.', 'من الصفحة الرئيسية، اضغط Permissions Request.')),
        S('ph-02', 'perm_history', hs(12, 11.2, 76, 5.0), H('Choose', 'Current or History.', 'اختر', 'Current أو History.'),
          L('Current shows requests waiting for a decision. History shows your past requests.',
            'تعرض Current الطلبات التي تنتظر قرارًا، وتعرض History طلباتك السابقة.')),
        S('ph-03', 'perm_history', hs(4.5, 32.0, 91, 11.6), H('Read your', 'request.', 'اقرأ', 'تفاصيل الطلب.'),
          L('Each request shows the permission type, the From and To times, and the hours.',
            'يعرض كل طلب نوع الإذن، ووقتَي From وTo، وعدد الساعات.'),
          L('Need a new request? Tap + at the bottom of the screen.', 'تحتاج طلبًا جديدًا؟ اضغط + أسفل الشاشة.'), verify='confirm'),
    ],
    'check': Q(L('Your manager has already decided on your permission request. Where do you find it now?',
                 'اتّخذ مديرك قرارًا في طلب الاستئذان. أين تجده الآن؟'), [
        (L('Permissions Request › History', 'Permissions Request › History'), True, L('History keeps your past requests.', 'تحتفظ History بطلباتك السابقة.')),
        (L('Permissions Request › Current', 'Permissions Request › Current'), False, L('Current only shows requests still waiting.', 'تعرض Current الطلبات المنتظِرة فقط.')),
        (L('My Permissions', 'My Permissions'), False, L('My Permissions shows the hours you have used, not your requests.', 'يعرض My Permissions الساعات التي استخدمتها، لا طلباتك.')),
    ]),
}

TASKS['my-attendance'] = {
    'id': 'my-attendance', 'icon': 'clock',
    'name': L('Check your attendance', 'مراجعة حضورك'),
    'situation': L('Am I over or short on hours?', 'هل ساعاتي زائدة أم ناقصة؟'),
    'title': H('Check your', 'attendance.', 'راجِع', 'حضورك.'),
    'purpose': L('Shows your over and short hours and your attendance for a period.', 'يعرض ساعاتك الزائدة والناقصة وحضورك خلال فترة محددة.'),
    'outcome': L('You can check your attendance for any period.', 'تستطيع مراجعة حضورك لأي فترة.'),
    'path': 'Home › My Attendance', 'goodToKnow': [], 'helpCard': False,
    'steps': [
        S('ma-01', 'home_dark', DARK['myAttendance'], H('Tap', 'My Attendance.', 'اضغط', 'My Attendance.'),
          L('On the home page, tap My Attendance.', 'من الصفحة الرئيسية، اضغط My Attendance.')),
        S('ma-02', 'attendance', hs(2.8, 12.9, 94.2, 51.8), H('Read', 'Over/Short Hours.', 'اقرأ', 'Over/Short Hours.'),
          L('Over/Short Hours shows the hours above or below your shift.', 'يعرض Over/Short Hours الساعات الزائدة أو الناقصة عن ورديتك.'), verify='confirm'),
        S('ma-03', 'attendance', hs(5.0, 20.6, 88, 4.4), H('Change the', 'Period.', 'غيّر', 'الفترة.'),
          L('Tap Period to choose the time range, such as Current Month.', 'اضغط Period لاختيار الفترة، مثل Current Month.')),
        S('ma-04', 'attendance', hs(2.8, 65.7, 94.2, 27.4), H('See your', 'attendance summary.', 'اعرف', 'ملخّص حضورك.'),
          L('Count attendence status and Occurrence of Shifts summarise your attendance and shifts for each Period.',
            'يلخّص قسما Count attendence status وOccurrence of Shifts حضورك وورديّاتك لكل فترة.')),
    ],
    'check': Q(L("You want last month's figures instead of this month's. What do you change?", 'تريد أرقام الشهر الماضي بدل الشهر الحالي. ماذا تغيّر؟'), [
        (L('Period', 'Period'), True, L('Period sets the time range for each section.', 'يحدّد Period الفترة لكل قسم.')),
        (L('Theme', 'Theme'), False, L('Theme only changes the app colours.', 'Theme يغيّر ألوان التطبيق فقط.')),
        (L('Language', 'Language'), False, L("Language changes the app's language, not the dates.", 'Language يغيّر لغة التطبيق، لا التواريخ.')),
    ]),
}

TASKS['geo-attendance'] = {
    'id': 'geo-attendance', 'icon': 'pin',
    'name': L('Record attendance by location', 'تسجيل الحضور بالموقع'),
    'situation': L('I need to clock in from my phone', 'أريد تسجيل حضوري من هاتفي'),
    'title': H('Record attendance', 'by location.', 'سجّل حضورك', 'بالموقع.'),
    'purpose': L('Records your arrival and departure from your phone with GEO Attendance.', 'يسجّل حضورك وانصرافك من هاتفك عبر GEO Attendance.'),
    'outcome': L('You can clock in and out with GEO Attendance.', 'تستطيع تسجيل الحضور والانصراف عبر GEO Attendance.'),
    'path': 'Home › GEO Attendance', 'goodToKnow': [], 'helpCard': False,
    'steps': [
        S('geo-01', 'home_light', LIGHT['geo'], H('Tap', 'GEO Attendance.', 'اضغط', 'GEO Attendance.'),
          L('On the home page, tap GEO Attendance.', 'من الصفحة الرئيسية، اضغط GEO Attendance.'),
          L('These screens show the app in the Light theme.', 'تظهر الشاشات هنا بالمظهر الفاتح Light.')),
        S('geo-02', 'geo', hs(57.0, 84.0, 18.2, 10.6), H('Arriving?', 'Tap In.', 'عند الوصول،', 'اضغط In.'),
          L('When you arrive, tap In to record your attendance.', 'عند وصولك، اضغط In لتسجيل حضورك.'),
          L('If your phone asks for your location, allow it.', 'إذا طلب هاتفك الوصول إلى موقعك، فاسمح بذلك.'), verify='confirm'),
        S('geo-03', 'geo', hs(75.2, 84.0, 18.6, 10.6), H('Leaving?', 'Tap Out.', 'عند الانصراف،', 'اضغط Out.'),
          L('When you leave, tap Out to record your departure.', 'عند انصرافك، اضغط Out لتسجيل الانصراف.')),
        S('geo-04', 'geo', hs(66.0, 13.4, 18.5, 4.4), H('Check your', 'History.', 'راجِع', 'History.'),
          L('Tap History to see the times you have recorded.', 'اضغط History لترى الأوقات التي سجّلتها.'), verify='confirm'),
    ],
    'check': Q(L("You're leaving work for the day. Which button do you tap?", 'ستغادر العمل في نهاية اليوم. أي زر تضغط؟'), [
        (L('Out', 'Out'), True, L('Out records the time you leave.', 'يسجّل Out وقت انصرافك.')),
        (L('In', 'In'), False, L('In records your arrival.', 'يسجّل In وقت وصولك.')),
        (L('History', 'History'), False, L('History only shows what you have recorded.', 'تعرض History ما سجّلته فقط.')),
    ]),
}

# ===== Manager / Approver =====
TASKS['notifications'] = {
    'id': 'notifications', 'icon': 'bell',
    'name': L('See requests waiting for you', 'معرفة الطلبات التي تنتظرك'),
    'situation': L('What needs my approval?', 'ما الذي ينتظر اعتمادي؟'),
    'title': H("See what's", 'waiting for you.', 'اعرف ما', 'ينتظر قرارك.'),
    'purpose': L('Uses notifications to show which team requests need your approval.', 'يعرض من خلال الإشعارات طلبات فريقك التي تنتظر اعتمادك.'),
    'outcome': L("You can see which of your team's requests need you.", 'تستطيع معرفة طلبات فريقك التي تحتاج قرارك.'),
    'path': 'Home › Notifications', 'goodToKnow': [], 'helpCard': False,
    'steps': [
        S('nt-01', 'home_light', LIGHT['bell'], H('Tap the', 'bell.', 'اضغط', 'أيقونة الجرس.'),
          L('On the home page, tap the bell at the top.', 'من الصفحة الرئيسية، اضغط أيقونة الجرس في الأعلى.'),
          L('These screens show the app in the Light theme.', 'تظهر الشاشات هنا بالمظهر الفاتح Light.')),
        S('nt-02', 'notifications', hs(3.4, 15.0, 93.2, 15.6), H('Read each', 'notification.', 'اقرأ', 'كل إشعار.'),
          L('Each card shows the request type, the employee, the dates and waiting your approval.',
            'تعرض كل بطاقة نوع الطلب، والموظف، والتواريخ، وعبارة waiting your approval.'),
          L('To decide, open the matching approvals page.', 'لاتخاذ القرار، افتح صفحة الاعتماد المناسبة.')),
    ],
    'check': Q(L('A notification says Vacation … waiting your approval. Where do you decide on it?', 'يظهر إشعار: Vacation … waiting your approval. أين تتخذ القرار؟'), [
        (L('Leaves Approvals', 'Leaves Approvals'), True, L('Leave requests are decided in Leaves Approvals.', 'تُعتمد طلبات الإجازة من Leaves Approvals.')),
        (L('Permissions Approvals', 'Permissions Approvals'), False, L('Permissions Approvals is for time permissions.', 'Permissions Approvals لطلبات الاستئذان.')),
        (L('Leaves Request', 'Leaves Request'), False, L('Leaves Request is for your own leave.', 'Leaves Request لإجازاتك أنت.')),
    ]),
}

TASKS['approve-permissions'] = {
    'id': 'approve-permissions', 'icon': 'check-badge',
    'name': L("Approve your team's time permissions", 'اعتماد طلبات الاستئذان لفريقك'),
    'situation': L('Someone asked to come in late', 'طلب أحد أفراد فريقي إذن تأخير'),
    'title': H('Approve', 'time permissions.', 'اعتمِد', 'طلبات الاستئذان.'),
    'purpose': L("Reviews your team's time-permission requests so you can approve or reject them.", 'يتيح مراجعة طلبات الاستئذان من فريقك لاعتمادها أو رفضها.'),
    'outcome': L("You can approve or reject your team's time permissions.", 'تستطيع اعتماد طلبات الاستئذان من فريقك أو رفضها.'),
    'path': 'Home › Permissions Approvals', 'goodToKnow': [], 'helpCard': False,
    'steps': [
        S('ap-01', 'home_light', LIGHT['permissionsApprovals'], H('Tap', 'Permissions Approvals.', 'اضغط', 'Permissions Approvals.'),
          L('On the home page, tap Permissions Approvals.', 'من الصفحة الرئيسية، اضغط Permissions Approvals.')),
        S('ap-02', 'perm_approvals', hs(5.0, 13.4, 23.0, 4.6), H('Open', 'Current.', 'افتح', 'Current.'),
          L('Current lists the requests waiting for your decision.', 'تعرض Current الطلبات التي تنتظر قرارك.')),
        S('ap-03', 'perm_approvals', hs(4.6, 19.2, 91, 9.8), H('Check the', 'request.', 'راجِع', 'الطلب.'),
          L('Each request shows the employee, the permission type, the From and To times, and the hours.',
            'يعرض كل طلب الموظف، ونوع الإذن، ووقتَي From وTo، وعدد الساعات.')),
        S('ap-04', 'perm_approvals', hs(67.4, 86.9, 13.8, 6.4), H('Approve or reject,', 'then save.', 'اعتمِد أو ارفض،', 'ثم احفظ.'),
          L('Use the ✓ button at the bottom to approve or reject, then save your decision.',
            'استخدم زر ✓ أسفل الشاشة للاعتماد أو الرفض، ثم احفظ قرارك.'),
          L('Your decision only counts once you save it.', 'لا يُعتمد قرارك إلا بعد حفظه.'), verify='confirm'),
    ],
    'check': Q(L('You approved three requests, then closed the page without saving. What happens?', 'اعتمدت ثلاثة طلبات ثم أغلقت الصفحة دون حفظ. ماذا يحدث؟'), [
        (L('The requests stay waiting', 'تبقى الطلبات منتظِرة'), True, L('Decisions only count once you save them.', 'لا تُعتمد القرارات إلا بعد حفظها.')),
        (L('The requests are approved', 'تُعتمد الطلبات'), False, L('Without saving, nothing is applied.', 'دون حفظ، لا يُطبَّق أي قرار.')),
        (L('The requests are rejected', 'تُرفض الطلبات'), False, L('Nothing changes until you save.', 'لا يتغيّر شيء حتى تحفظ.')),
    ]),
}

TASKS['leave-approvals'] = {
    'id': 'leave-approvals', 'icon': 'calendar-check',
    'name': L("Approve your team's leave", 'اعتماد إجازات فريقك'),
    'situation': L('Someone on my team asked for leave', 'طلب أحد أفراد فريقي إجازة'),
    'title': H('Approve', 'leave requests.', 'اعتمِد', 'طلبات الإجازة.'),
    'purpose': L("Shows your team's leave requests, what's still with other approvers, and what you've decided.", 'يعرض طلبات إجازة فريقك، وما زال لدى معتمِدين آخرين، وما اتخذت فيه قرارًا.'),
    'outcome': L("You can find, decide on and track your team's leave requests.", 'تستطيع العثور على طلبات إجازة فريقك، واتخاذ القرار فيها، ومتابعتها.'),
    'path': 'Home › Leaves Approvals', 'goodToKnow': [], 'helpCard': False,
    'steps': [
        S('la-01', 'home_light', LIGHT['leavesApprovals'], H('Tap', 'Leaves Approvals.', 'اضغط', 'Leaves Approvals.'),
          L('On the home page, tap Leaves Approvals.', 'من الصفحة الرئيسية، اضغط Leaves Approvals.')),
        S('la-02', 'leave_approvals', hs(5.0, 13.4, 23.0, 4.6), H('Start with', 'Current.', 'ابدأ من', 'Current.'),
          L('Current lists the leave requests waiting for your decision. Approve or reject them, then save.',
            'تعرض Current طلبات الإجازة التي تنتظر قرارك. اعتمِدها أو ارفضها، ثم احفظ.')),
        S('la-03', 'leave_approvals', hs(38.0, 13.4, 24.0, 4.6), H('Follow', 'Monitoring.', 'تابِع', 'Monitoring.'),
          L('Monitoring shows requests still waiting for an earlier approver.', 'تعرض Monitoring الطلبات التي ما زالت تنتظر قرار معتمِد قبلك.'), verify='confirm'),
        S('la-04', 'leave_approvals', hs(72.0, 13.4, 22.4, 4.6), H('Check', 'History.', 'راجِع', 'History.'),
          L('History lists the requests you have already decided.', 'تعرض History الطلبات التي اتخذت فيها قرارًا.')),
        S('la-05', 'leave_approvals', hs(80.6, 86.9, 14.2, 6.4), H('Filter', 'the list.', 'صفِّ', 'القائمة.'),
          L('Tap the filter button to show requests from specific dates.', 'اضغط زر التصفية لعرض الطلبات في تواريخ محددة.')),
    ],
    'check': Q(L("A request is still with the employee's first approver before it reaches you. Where do you see it?", 'طلب ما زال لدى المعتمِد الأول للموظف قبل أن يصل إليك. أين تراه؟'), [
        (L('Monitoring', 'Monitoring'), True, L('Monitoring shows requests waiting for an earlier approver.', 'تعرض Monitoring الطلبات التي تنتظر معتمِدًا قبلك.')),
        (L('Current', 'Current'), False, L('Current only shows requests waiting for you.', 'تعرض Current الطلبات التي تنتظرك أنت فقط.')),
        (L('History', 'History'), False, L('History shows requests you have already decided.', 'تعرض History الطلبات التي اتخذت فيها قرارًا.')),
    ]),
}

TASKS['tk-approvals'] = {
    'id': 'tk-approvals', 'icon': 'hourglass',
    'name': L('Approve missing-time requests', 'اعتماد طلبات استكمال الوقت'),
    'situation': L('Someone forgot to clock in or out', 'نسي أحد أفراد فريقي تسجيل الحضور أو الانصراف'),
    'title': H('Approve', 'missing-time requests.', 'اعتمِد', 'طلبات استكمال الوقت.'),
    'purpose': L("Shows your team's missing clock-in or clock-out requests for a date range.", 'يعرض طلبات فريقك لاستكمال الحضور أو الانصراف خلال فترة محددة.'),
    'outcome': L("You can load and decide on your team's missing-time requests.", 'تستطيع عرض طلبات استكمال الوقت لفريقك واتخاذ القرار فيها.'),
    'path': 'Home › Incomplete TK Approvals', 'goodToKnow': [], 'helpCard': False,
    'steps': [
        S('tk-01', 'home_light', LIGHT['tkApprovals'], H('Tap', 'Incomplete TK Approvals.', 'اضغط', 'Incomplete TK Approvals.'),
          L('On the home page, tap Incomplete TK Approvals.', 'من الصفحة الرئيسية، اضغط Incomplete TK Approvals.')),
        S('tk-02', 'tk_filter', hs(4.6, 51.0, 91, 7.4), H('Set the', 'dates.', 'حدِّد', 'التواريخ.'),
          L('In Incomplete TK Filter, set the two dates under Start Date Between.', 'في Incomplete TK Filter، حدِّد التاريخين في Start Date Between.')),
        S('tk-03', 'tk_filter', hs(55.0, 59.2, 11.6, 6.2), H('Tap', 'OK.', 'اضغط', 'OK.'),
          L('Tap OK to show the requests in that range. Approve or reject each one, then save.',
            'اضغط OK لعرض الطلبات في هذه الفترة. اعتمِد أو ارفض كل طلب، ثم احفظ.'), verify='confirm'),
    ],
    'check': Q(L("The list shows requests you don't need. How do you narrow it?", 'تعرض القائمة طلبات لا تحتاجها. كيف تحصرها؟'), [
        (L('Change the dates in the filter, then tap OK', 'غيّر التواريخ في الفلتر، ثم اضغط OK'), True, L('The dates decide which requests you see.', 'التواريخ تحدّد الطلبات التي تظهر لك.')),
        (L('Tap Cancel', 'اضغط Cancel'), False, L('Cancel closes the filter without changing the list.', 'يغلق Cancel الفلتر دون تغيير القائمة.')),
        (L('Open Incomplete TK Request', 'افتح Incomplete TK Request'), False, L('That is for your own missing-time requests.', 'هذا لطلباتك أنت لاستكمال الوقت.')),
    ]),
}

MISSIONS = [
    {'id': 'start', 'roles': ['employee', 'manager'], 'icon': 'rocket',
     'title': L('Get started', 'ابدأ هنا'),
     'outcome': L('Sign in, recover your password and set up the app.', 'سجّل الدخول، واسترجع كلمة المرور، واضبط التطبيق.'),
     'tasks': ['signin-app', 'forgot-password', 'app-settings']},
    {'id': 'timeoff', 'roles': ['employee'], 'icon': 'calendar',
     'title': L('My time off', 'إجازاتي'),
     'outcome': L('Check your balance, request leave and follow it up.', 'اعرف رصيدك، وقدّم طلب إجازة، وتابِعه.'),
     'tasks': ['leave-balance', 'leave-request', 'leave-history']},
    {'id': 'mytime', 'roles': ['employee'], 'icon': 'clock',
     'title': L('My time & attendance', 'وقتي وحضوري'),
     'outcome': L('Check your permission hours and attendance, and clock in by location.', 'اعرف ساعات استئذانك وحضورك، وسجّل حضورك بالموقع.'),
     'tasks': ['my-permissions', 'permission-history', 'my-attendance', 'geo-attendance']},
    {'id': 'approvals', 'roles': ['manager'], 'icon': 'check-badge',
     'title': L("Approve your team's requests", 'اعتمِد طلبات فريقك'),
     'outcome': L('Find what is waiting for you, decide on it and track past decisions.', 'اعرف ما ينتظر قرارك، واتخذ القرار، وتابِع قراراتك السابقة.'),
     'tasks': ['notifications', 'approve-permissions', 'leave-approvals', 'tk-approvals']},
]

UI = {
 'en': {
  'appName': 'HITS Made Simple', 'heroLine': ['What do you', 'need to do?'],
  'heroSub': 'Pick a mission. Each task shows you the real app, step by step.',
  'roleEmployee': 'Employee', 'roleManager': 'Manager / Approver', 'roleLabel': 'I am',
  'roleNoteManager': 'For your own leave and attendance, switch to Employee.',
  'points': '{n} pts', 'pointsLabel': 'Your points', 'tasksDone': '{done} of {total} tasks',
  'mission': 'Mission', 'missionOf': 'Task {n} of {total}', 'startMission': 'Start mission', 'continueMission': 'Continue',
  'reviewMission': 'Review', 'missionDone': 'Mission complete', 'missionDoneLine': 'You finished every task in this mission.',
  'searchPlaceholder': 'Search tasks', 'noResults': 'No tasks match your search.', 'search': 'Search', 'close': 'Close',
  'allMissions': 'All missions', 'missionsShort': 'Missions', 'whereToGo': 'Where to go', 'youWillBeAble': 'After this task',
  'startTask': 'Start', 'stepOf': 'Step {n} of {total}', 'back': 'Back', 'next': 'Next', 'toQuestion': 'Final question',
  'goodToKnow': 'Good to know', 'tapToEnlarge': 'Tap to enlarge', 'closeImage': 'Close', 'swipeHint': 'Swipe for the next step',
  'finalQuestion': 'Final question', 'questionWorth': 'Answer right for +{n} pts',
  'correct': 'Correct!', 'notQuite': 'Not quite.', 'rightAnswer': 'The right answer is:',
  'encourage': ["Good try — now you know.", "Nearly there — remember this one.", "No problem — that's how we learn."],
  'praise': ['Well done!', 'Spot on!', 'Great job!'],
  'taskComplete': 'Task complete', 'earned': '+{n} pts', 'earnedTask': 'Task finished', 'earnedAnswer': 'Right answer',
  'nextTask': 'Next task', 'backToMissions': 'Back to missions', 'replay': 'Watch again',
  'done': 'Done', 'notStarted': 'Not started', 'help': 'Help', 'needHelp': 'Need help?',
  'helpCardTitle': ['Office 365', 'password issue?'], 'helpCardLine': 'Email IT Support:',
  'dontMatch': "Screen looks different? Stop and contact IT Support rather than guessing.",
  'resetProgress': 'Reset my progress', 'resetConfirm': 'Clear your points and ticks on this device?',
  'privacy': 'Your progress is saved on this device only. We count visits and completed tasks anonymously to improve the guide — never your name.',
  'langSwitch': 'ع', 'langName': 'العربية', 'skipToContent': 'Skip to content',
  'department': 'Your department (optional)', 'departmentNone': 'Prefer not to say',
  'pointsTotal': 'pts', 'badge': 'Badge earned',
 },
 'ar': {
  'appName': 'HITS ببساطة', 'heroLine': ['ماذا تريد', 'أن تفعل؟'],
  'heroSub': 'اختر مهمة رئيسية. كل خطوة تعرض لك التطبيق الحقيقي.',
  'roleEmployee': 'الموظف', 'roleManager': 'المدير / المعتمِد', 'roleLabel': 'أنا',
  'roleNoteManager': 'لإجازاتك وحضورك أنت، اختر «الموظف».',
  'points': '{n} نقطة', 'pointsLabel': 'نقاطك', 'tasksDone': '{done} من {total} مهام',
  'mission': 'مهمة رئيسية', 'missionOf': 'المهمة {n} من {total}', 'startMission': 'ابدأ', 'continueMission': 'تابِع',
  'reviewMission': 'راجِع', 'missionDone': 'أنجزت المهمة الرئيسية', 'missionDoneLine': 'أكملت كل المهام في هذه المجموعة.',
  'searchPlaceholder': 'ابحث عن مهمة', 'noResults': 'لا توجد مهام تطابق بحثك.', 'search': 'بحث', 'close': 'إغلاق',
  'allMissions': 'كل المهام الرئيسية', 'missionsShort': 'المهام', 'whereToGo': 'أين تجدها', 'youWillBeAble': 'بعد هذه المهمة',
  'startTask': 'ابدأ', 'stepOf': 'الخطوة {n} من {total}', 'back': 'السابق', 'next': 'التالي', 'toQuestion': 'السؤال الأخير',
  'goodToKnow': 'من المفيد أن تعرف', 'tapToEnlarge': 'اضغط للتكبير', 'closeImage': 'إغلاق', 'swipeHint': 'اسحب للانتقال إلى الخطوة التالية',
  'finalQuestion': 'السؤال الأخير', 'questionWorth': 'أجب إجابة صحيحة واربح {n}+ نقاط',
  'correct': 'إجابة صحيحة!', 'notQuite': 'ليس تمامًا.', 'rightAnswer': 'الإجابة الصحيحة:',
  'encourage': ['محاولة جيدة، والآن عرفت الإجابة.', 'اقتربت، تذكّر هذه المعلومة.', 'لا بأس، هكذا نتعلّم.'],
  'praise': ['أحسنت!', 'إجابة في محلّها!', 'عمل رائع!'],
  'taskComplete': 'أنجزت المهمة', 'earned': '{n}+ نقاط', 'earnedTask': 'إنهاء المهمة', 'earnedAnswer': 'إجابة صحيحة',
  'nextTask': 'المهمة التالية', 'backToMissions': 'العودة إلى المهام', 'replay': 'شاهِد مرة أخرى',
  'done': 'تمّت', 'notStarted': 'لم تبدأ', 'help': 'المساعدة', 'needHelp': 'تحتاج مساعدة؟',
  'helpCardTitle': ['مشكلة في كلمة مرور', 'Office 365؟'], 'helpCardLine': 'راسِل الدعم الفني على:',
  'dontMatch': 'الشاشة مختلفة؟ توقّف وتواصل مع الدعم الفني بدلًا من التخمين.',
  'resetProgress': 'مسح تقدّمي', 'resetConfirm': 'هل تريد مسح نقاطك وما أنجزته على هذا الجهاز؟',
  'privacy': 'يُحفظ تقدّمك على هذا الجهاز فقط. نحصي الزيارات والمهام المكتملة دون أسماء لتحسين الدليل.',
  'langSwitch': 'EN', 'langName': 'English', 'skipToContent': 'انتقل إلى المحتوى',
  'department': 'إدارتك (اختياري)', 'departmentNone': 'أفضّل عدم الذكر',
  'pointsTotal': 'نقطة', 'badge': 'حصلت على وسام',
 }
}

# ================= v3.1 changes (feedback 20 Oct) =================
def TIP(after, en, ar): return {'after': after, 'text': L(en, ar)}

# --- Sign in: OFFICE 365 choice first, then Work ID with a dummy ID typed in ---
UNAME_BOX = hs(8.5, 45.2, 76.5, 5.4); PASS_BOX = hs(8.5, 55.8, 68, 4.2)
si = TASKS['signin-app']; st = {s['id']: s for s in si['steps']}
si['steps'] = [
    st['signin-app-01'],
    S('signin-app-o365', 'login_empty', hs(51.2, 74.2, 44.2, 5.6), H('Have a work email?', 'Tap OFFICE 365.', 'لديك بريد عمل؟', 'اضغط OFFICE 365.'),
      L('If you have a work email, tap OFFICE 365, then sign in with your work email and its password.',
        'إذا كان لديك بريد إلكتروني للعمل، فاضغط OFFICE 365، ثم ادخل ببريد العمل وكلمة مروره.'),
      L('No work email? Sign in with your Work ID — the next steps show you how.', 'ليس لديك بريد عمل؟ ادخل بالرقم الوظيفي، وتوضّح لك الخطوات التالية الطريقة.')),
    dict(st['signin-app-02'], screen='login_filled', hotspot=hs(4.5, 43.4, 91, 8.4),
         type=[{'box': UNAME_BOX, 'text': '12345', 'anim': True}, {'box': PASS_BOX, 'text': ''}],
         helper=L('12345 is only an example. Your Work ID and password come from your direct manager.', '12345 مجرد مثال. يسلّمك مديرك المباشر الرقم الوظيفي وكلمة المرور.')),
    dict(st['signin-app-03'], screen='login_filled', hotspot=hs(4.5, 54.4, 91, 7.4),
         type=[{'box': UNAME_BOX, 'text': '12345'}, {'box': PASS_BOX, 'text': '••••••••', 'anim': True, 'dots': True}]),
    dict(st['signin-app-04'], type=[{'box': UNAME_BOX, 'text': '12345'}, {'box': PASS_BOX, 'text': '••••••••', 'dots': True}], helper=None),
    st['signin-app-05'],
]
si['tips'] = [
    TIP('signin-app-01', 'Your app may look light instead of dark. The steps stay the same.', 'قد يظهر تطبيقك بلون فاتح بدلًا من الداكن. الخطوات لا تتغير.'),
    TIP('signin-app-03', 'Never share your password, including in screenshots or support messages.', 'لا تشارك كلمة المرور مع أحد، ولا تُظهرها في لقطات الشاشة أو رسائل الدعم.'),
    TIP('signin-app-04', 'The same Work ID and password work on HITS Web.', 'الرقم الوظيفي وكلمة المرور نفسهما يعملان على HITS Web.'),
]
TASKS['forgot-password']['tips'] = [TIP('forgot-app-02', 'Your direct manager provides your HITS username and password.', 'يسلّمك مديرك المباشر اسم المستخدم وكلمة المرور لـ HITS.')]
TASKS['app-settings']['tips'] = [TIP('settings-app-02', 'Leave Tenant ID as it is.', 'اترك Tenant ID كما هو.')]

# --- Leave balance: add Vacatin Days Count ---
lb = TASKS['leave-balance']
lb['steps'].append(S('balance-app-04', 'days_count', hs(2.8, 39.6, 94.2, 52.6), H('See your days', 'on a chart.', 'شاهِد أيامك', 'في رسم بياني.'),
    L('Vacatin Days Count shows the days you have taken, by leave type, for the selected Period.',
      'يعرض Vacatin Days Count الأيام التي أخذتها حسب نوع الإجازة خلال الفترة المحددة.')))
lb['tips'] = []

# --- New: balance from the Leaves Request menu (light screens) ---
TASKS['leave-menu'] = {
    'id': 'leave-menu', 'icon': 'calendar-days',
    'name': L('Check your balance before you request', 'معرفة رصيدك قبل الطلب'),
    'situation': L('Do I have enough days before I ask?', 'هل لديّ أيام كافية قبل أن أطلب؟'),
    'title': H('Check your balance', 'before you request.', 'اعرف رصيدك', 'قبل أن تطلب.'),
    'purpose': L('Opens your leave balance from the Leaves Request menu.', 'يفتح رصيد إجازاتك من قائمة Leaves Request.'),
    'outcome': L('You can check your balance from Leaves Request in seconds.', 'تستطيع معرفة رصيدك من Leaves Request في ثوانٍ.'),
    'path': 'Home › Leaves Request › ⋮ › Balance', 'goodToKnow': [], 'helpCard': False, 'tips': [],
    'steps': [
        S('lm-01', 'home_light', hs(5.6, 42.1, 19.4, 13.5), H('Tap', 'Leaves Request.', 'اضغط', 'Leaves Request.'),
          L('On the home page, tap Leaves Request.', 'من الصفحة الرئيسية، اضغط Leaves Request.'),
          L('These screens show the app in the Light theme.', 'تظهر الشاشات هنا بالمظهر الفاتح Light.')),
        S('lm-02', 'leave_history_light', hs(82.0, 88.6, 11.0, 6.4), H('Open the', 'menu.', 'افتح', 'القائمة.'),
          L('Tap ⋮ at the bottom of the screen.', 'اضغط ⋮ أسفل الشاشة.'), verify='confirm'),
        S('lm-03', 'leave_menu', hs(61.0, 81.4, 32.4, 5.8), H('Tap', 'Balance.', 'اضغط', 'Balance.'),
          L('The menu shows Filter, Balance and New. Tap Balance.', 'تعرض القائمة Filter وBalance وNew. اضغط Balance.')),
        S('lm-04', 'balance_periods', hs(2.5, 14.6, 95, 21.4), H('Read your', 'balance.', 'اقرأ', 'رصيدك.'),
          L('Each period shows your Annual, Holiday and Days Off, with what is due, taken and left in Balance.',
            'تعرض كل فترة رصيدك من Annual وHoliday وDays Off، مع المستحق في Due والمستخدم في Taken والمتبقي في Balance.')),
    ],
    'check': Q(L('You are in Leaves Request and want to see your balance. What do you tap?', 'أنت في Leaves Request وتريد معرفة رصيدك. ماذا تضغط؟'), [
        (L('⋮, then Balance', '⋮ ثم Balance'), True, L('Balance in the ⋮ menu shows your balance for each period.', 'يعرض Balance في قائمة ⋮ رصيدك لكل فترة.')),
        (L('⋮, then Filter', '⋮ ثم Filter'), False, L('Filter narrows your list of requests.', 'يحصر Filter قائمة طلباتك.')),
        (L('History', 'History'), False, L('History lists your past requests, not your balance.', 'تعرض History طلباتك السابقة، لا رصيدك.')),
    ]),
}

# --- Leave request tips (one at a time) ---
TASKS['leave-request']['tips'] = [
    TIP('leave-app-01', 'If a list of names appears when you open Leaves Request, tap your own name first. It is at the top.', 'إذا ظهرت قائمة أسماء عند فتح Leaves Request، فاضغط اسمك أولًا. ستجده في الأعلى.'),
    TIP('leave-app-04', 'Choosing Mission? You must fill in the mission destination, or the request will not send.', 'اخترت Mission؟ يجب كتابة جهة المأمورية، وإلا لن يُرسَل الطلب.'),
]
TASKS['leave-request']['goodToKnow'] = []

# --- Permissions: sourced tips ---
TASKS['my-permissions']['tips'] = [TIP('myperm-app-02', 'Personal late permission is capped at 2 hours a month. Above that, HITS blocks the request.', 'إذن التأخير الشخصي حدّه ساعتان في الشهر، وبعدها يرفض HITS الطلب.')]
TASKS['permission-history']['tips'] = [TIP('ph-03', 'When you request a permission, enter times in 24-hour format — 13:00 means 1 PM.', 'عند طلب إذن، اكتب الوقت بنظام 24 ساعة؛ 13:00 تعني الواحدة ظهرًا.')]

# --- GEO: add date filter ---
TASKS['geo-attendance']['steps'].append(S('geo-05', 'geo_filter', hs(5.0, 53.4, 90, 5.0), H('Check', 'past days.', 'راجِع', 'الأيام السابقة.'),
    L('In Time Keeping Filter, set Attend Date Between, then tap OK.', 'في Time Keeping Filter، حدِّد Attend Date Between، ثم اضغط OK.'), verify='confirm'))

# --- Manager: approve permissions on the full dark flow, with the detail screen ---
TASKS['approve-permissions']['steps'] = [
    S('ap-01', 'home_dark', hs(76.1, 38.0, 20.8, 14.0), H('Tap', 'Permissions Approvals.', 'اضغط', 'Permissions Approvals.'),
      L('On the home page, tap Permissions Approvals.', 'من الصفحة الرئيسية، اضغط Permissions Approvals.')),
    S('ap-02', 'perm_current', hs(7.0, 11.4, 20.4, 4.4), H('Open', 'Current.', 'افتح', 'Current.'),
      L('Current lists the requests waiting for your decision.', 'تعرض Current الطلبات التي تنتظر قرارك.')),
    S('ap-03', 'perm_current', hs(3.6, 17.8, 92.6, 16.2), H('Check the', 'request.', 'راجِع', 'الطلب.'),
      L('Each request shows the employee, the permission type, the From and To times, and the hours. Tap it for the details.',
        'يعرض كل طلب الموظف، ونوع الإذن، ووقتَي From وTo، وعدد الساعات. اضغطه لعرض التفاصيل.')),
    S('ap-04', 'perm_detail', hs(4.6, 28.8, 91.4, 27.0), H('Read the', 'details.', 'اقرأ', 'التفاصيل.'),
      L('Permission Details, Shift Details and Attendance Details show the request next to the shift and the actual times.',
        'تعرض Permission Details وShift Details وAttendance Details الطلب مع الوردية وأوقات الحضور الفعلية.')),
    S('ap-05', 'perm_current', hs(64.4, 88.6, 14.4, 7.2), H('Approve or reject,', 'then save.', 'اعتمِد أو ارفض،', 'ثم احفظ.'),
      L('Use the ✓ button at the bottom to approve or reject, then save your decision.', 'استخدم زر ✓ أسفل الشاشة للاعتماد أو الرفض، ثم احفظ قرارك.'),
      L('Your decision only counts once you save it.', 'لا يُعتمد قرارك إلا بعد حفظه.'), verify='confirm'),
]
TASKS['approve-permissions']['tips'] = [TIP('ap-05', 'Approve All and Reject All mark every request at once — they still need saving.', 'يحدّد Approve All وReject All كل الطلبات مرة واحدة، لكنها تحتاج الحفظ أيضًا.')]

TASKS['find-permissions'] = {
    'id': 'find-permissions', 'icon': 'search',
    'name': L('Find past permission requests', 'البحث في طلبات الاستئذان السابقة'),
    'situation': L('What did I decide last month?', 'بماذا قررت الشهر الماضي؟'),
    'title': H('Find past', 'permission requests.', 'ابحث في', 'طلبات الاستئذان السابقة.'),
    'purpose': L('Filters the permission requests you have decided by date and type.', 'يصفّي طلبات الاستئذان التي قررت فيها حسب التاريخ والنوع.'),
    'outcome': L("You can find any permission request you've decided.", 'تستطيع العثور على أي طلب استئذان اتخذت فيه قرارًا.'),
    'path': 'Home › Permissions Approvals › History', 'goodToKnow': [], 'helpCard': False, 'tips': [],
    'steps': [
        S('fp-01', 'home_light', LIGHT['permissionsApprovals'], H('Tap', 'Permissions Approvals.', 'اضغط', 'Permissions Approvals.'),
          L('On the home page, tap Permissions Approvals.', 'من الصفحة الرئيسية، اضغط Permissions Approvals.'),
          L('These screens show the app in the Light theme.', 'تظهر الشاشات هنا بالمظهر الفاتح Light.')),
        S('fp-02', 'perm_history_light', hs(72.4, 13.4, 21.8, 4.6), H('Open', 'History.', 'افتح', 'History.'),
          L('History lists the requests you have already decided.', 'تعرض History الطلبات التي اتخذت فيها قرارًا.')),
        S('fp-03', 'perm_history_light', hs(80.6, 86.9, 14.2, 6.4), H('Tap the', 'filter.', 'اضغط', 'زر التصفية.'),
          L('Tap the filter button at the bottom of the screen.', 'اضغط زر التصفية أسفل الشاشة.')),
        S('fp-04', 'perm_filter', hs(4.6, 47.2, 92.4, 14.6), H('Set dates', 'and type.', 'حدِّد التواريخ', 'والنوع.'),
          L('In Permissions Filter, set Start Date Between and, if you need, the Permission type.', 'في Permissions Filter، حدِّد Start Date Between، ونوع الإذن في Permission عند الحاجة.')),
        S('fp-05', 'perm_filter', hs(55.0, 62.6, 11.6, 6.4), H('Tap', 'OK.', 'اضغط', 'OK.'),
          L('Tap OK to show only the matching requests.', 'اضغط OK لعرض الطلبات المطابقة فقط.')),
    ],
    'check': Q(L('You want only last month’s requests in History. What do you change?', 'تريد طلبات الشهر الماضي فقط في History. ماذا تغيّر؟'), [
        (L('Start Date Between, in the filter', 'Start Date Between في الفلتر'), True, L('The dates in the filter decide which requests you see.', 'تواريخ الفلتر تحدّد الطلبات التي تظهر.')),
        (L('The Current tab', 'تبويب Current'), False, L('Current shows requests still waiting for you.', 'تعرض Current الطلبات التي ما زالت تنتظرك.')),
        (L('Cancel', 'Cancel'), False, L('Cancel closes the filter without changes.', 'يغلق Cancel الفلتر دون تغيير.')),
    ]),
}

TASKS['team-records'] = {
    'id': 'team-records', 'icon': 'users',
    'name': L("Open a team member's record", 'فتح سجلّ أحد أفراد فريقك'),
    'situation': L("How many days does my team member have?", 'كم يومًا لدى أحد أفراد فريقي؟'),
    'title': H("Open a team", "member's record.", 'افتح سجلّ', 'أحد أفراد فريقك.'),
    'purpose': L("Shows how managers pick a person from the list in My Leaves and similar pages.", 'يوضّح كيف يختار المدير شخصًا من القائمة في My Leaves والصفحات المشابهة.'),
    'outcome': L("You can open your own or a team member's record.", 'تستطيع فتح سجلّك أو سجلّ أحد أفراد فريقك.'),
    'path': 'Home › My Leaves', 'goodToKnow': [], 'helpCard': False,
    'tips': [TIP('tr-03', 'The same list appears in My Attendance, My Permissions and Permissions Request.', 'تظهر القائمة نفسها في My Attendance وMy Permissions وPermissions Request.')],
    'steps': [
        S('tr-01', 'home_light', hs(74.7, 27.0, 19.8, 13.1), H('Tap', 'My Leaves.', 'اضغط', 'My Leaves.'),
          L('On the home page, tap My Leaves.', 'من الصفحة الرئيسية، اضغط My Leaves.'),
          L('These screens show the app in the Light theme.', 'تظهر الشاشات هنا بالمظهر الفاتح Light.')),
        S('tr-02', 'team_list', hs(4.6, 15.8, 90.8, 10.2), H("You're", 'at the top.', 'اسمك', 'في الأعلى.'),
          L('Managers see a list of people. Your own name is first — tap it for your own record.', 'يرى المدير قائمة أشخاص، واسمك هو الأول. اضغطه لفتح سجلّك.')),
        S('tr-03', 'team_list', hs(4.6, 26.6, 90.8, 10.0), H('Tap a team', "member's name.", 'اضغط اسم', 'أحد أفراد فريقك.'),
          L("Tap a team member's name to open their leave record.", 'اضغط اسم أحد أفراد فريقك لفتح سجلّ إجازاته.'), verify='confirm'),
        S('tr-04', 'team_list', hs(76.4, 7.8, 8.6, 4.0), H('Search', 'by name.', 'ابحث', 'بالاسم.'),
          L('Tap the search icon at the top to find someone quickly.', 'اضغط أيقونة البحث في الأعلى للعثور على أي شخص بسرعة.')),
    ],
    'check': Q(L('You open My Leaves and see a list of names. Where is your own record?', 'فتحت My Leaves فظهرت قائمة أسماء. أين سجلّك أنت؟'), [
        (L('The first name at the top', 'الاسم الأول في الأعلى'), True, L('Your own name always comes first.', 'اسمك يأتي دائمًا أولًا.')),
        (L('The last name in the list', 'آخر اسم في القائمة'), False, L('Your name is at the top, not the bottom.', 'اسمك في الأعلى، لا في الأسفل.')),
        (L('In Leaves Approvals', 'في Leaves Approvals'), False, L('Leaves Approvals is for deciding on requests.', 'Leaves Approvals لاتخاذ القرار في الطلبات.')),
    ]),
}

for t in TASKS.values():
    t.setdefault('tips', [])
    t['goodToKnow'] = []  # replaced by one-at-a-time tips

MISSIONS[:] = [
    {'id': 'start', 'roles': ['employee', 'manager'], 'icon': 'rocket', 'title': L('Get started', 'ابدأ هنا'),
     'outcome': L('Sign in, recover your password and set up the app.', 'سجّل الدخول، واسترجع كلمة المرور، واضبط التطبيق.'),
     'tasks': ['signin-app', 'forgot-password', 'app-settings']},
    {'id': 'timeoff', 'roles': ['employee'], 'icon': 'calendar', 'title': L('My time off', 'إجازاتي'),
     'outcome': L('Check your balance, request leave and follow it up.', 'اعرف رصيدك، وقدّم طلب إجازة، وتابِعه.'),
     'tasks': ['leave-balance', 'leave-menu', 'leave-request', 'leave-history']},
    {'id': 'mytime', 'roles': ['employee'], 'icon': 'clock', 'title': L('My time & attendance', 'وقتي وحضوري'),
     'outcome': L('Check your permission hours and attendance, and clock in by location.', 'اعرف ساعات استئذانك وحضورك، وسجّل حضورك بالموقع.'),
     'tasks': ['my-permissions', 'permission-history', 'my-attendance', 'geo-attendance']},
    {'id': 'approvals', 'roles': ['manager'], 'icon': 'check-badge', 'title': L("Approve your team's requests", 'اعتمِد طلبات فريقك'),
     'outcome': L('See what is waiting for you and decide on it.', 'اعرف ما ينتظر قرارك، واتخذ القرار.'),
     'tasks': ['notifications', 'approve-permissions', 'leave-approvals', 'tk-approvals']},
    {'id': 'team', 'roles': ['manager'], 'icon': 'users', 'title': L('Keep an eye on your team', 'تابِع فريقك'),
     'outcome': L("Find past decisions and open your team's records.", 'اعثر على قراراتك السابقة، وافتح سجلّات فريقك.'),
     'tasks': ['find-permissions', 'team-records']},
]
COMING = L('More stops coming soon: My Payslip, My Profile, Changes Request, new permission and missing-time requests, Attendance Tracking.',
           'محطات قادمة قريبًا: My Payslip وMy Profile وChanges Request، وطلبات الاستئذان واستكمال الوقت الجديدة، وAttendance Tracking.')

UI['en'].update({
  'heroSub': 'Pick a route. Each stop shows you the real app, step by step.',
  'mission': 'Route', 'missionOf': 'Stop {n} of {total}', 'tasksDone': '{done} of {total} stops',
  'startMission': 'Start route', 'continueMission': 'Continue', 'reviewMission': 'Ride again',
  'missionDone': 'Route complete', 'missionDoneLine': 'You finished every stop on this route.',
  'allMissions': 'All routes', 'missionsShort': 'Routes', 'backToMissions': 'Back to routes',
  'youWillBeAble': 'After this stop', 'taskComplete': 'Stop complete', 'earnedTask': 'Stop finished',
  'nextTask': 'Next stop', 'tip': 'Good to know', 'gotIt': 'Got it', 'stepsMeta': '{n} steps · about {m} min',
  'coming': COMING['en'], 'badge': 'Route badge earned', 'toQuestion': 'Final question',
  'trackTitle': 'Enter your Work ID', 'trackLine': 'People & Culture uses your Work ID only to see who has completed the guide.', 'trackSave': 'Continue', 'trackPh': 'Work ID',
})
UI['ar'].update({
  'heroSub': 'اختر مشوارك. كل محطة تعرض لك التطبيق الحقيقي خطوة بخطوة.',
  'mission': 'مشوار', 'missionOf': 'المحطة {n} من {total}', 'tasksDone': '{done} من {total} محطات',
  'startMission': 'ابدأ المشوار', 'continueMission': 'تابِع', 'reviewMission': 'كرّر المشوار',
  'missionDone': 'أكملت المشوار', 'missionDoneLine': 'أنهيت كل محطات هذا المشوار.',
  'allMissions': 'كل المشاوير', 'missionsShort': 'المشاوير', 'backToMissions': 'العودة إلى المشاوير',
  'youWillBeAble': 'بعد هذه المحطة', 'taskComplete': 'أنهيت المحطة', 'earnedTask': 'إنهاء المحطة',
  'nextTask': 'المحطة التالية', 'tip': 'من المفيد أن تعرف', 'gotIt': 'فهمت', 'stepsMeta': '{n} خطوات · حوالي {m} دقيقة',
  'coming': COMING['ar'], 'badge': 'حصلت على وسام المشوار', 'toQuestion': 'السؤال الأخير',
  'trackTitle': 'أدخِل رقمك الوظيفي', 'trackLine': 'تستخدم إدارة الأفراد والثقافة رقمك الوظيفي فقط لمعرفة من أكمل الدليل.', 'trackSave': 'متابعة', 'trackPh': 'الرقم الوظيفي',
})
# every tip must point at a real step
for k, t in TASKS.items():
    ids = {s['id'] for s in t['steps']}
    for tp in t['tips']: assert tp['after'] in ids, (k, tp['after'])


# ================= v3.1 audit fixes =================
TASKS['approve-permissions']['steps'][3]['helper'] = L('This example is already approved. Requests waiting for you show the same details.', 'هذا المثال لطلب معتمَد بالفعل، والطلبات التي تنتظرك تعرض التفاصيل نفسها.')
la = TASKS['leave-approvals']; lst = {x['id']: x for x in la['steps']}
la['steps'] = [lst['la-01'],
  S('la-02', 'leave_approvals', hs(5.0, 13.4, 89.4, 4.6), H('Know the', 'three tabs.', 'اعرف', 'التبويبات الثلاثة.'),
    L('Current: waiting for your decision. Monitoring: still with an earlier approver. History: requests you have decided.',
      'Current: تنتظر قرارك. Monitoring: ما زالت لدى معتمِد قبلك. History: طلبات اتخذت فيها قرارًا.'),
    L('In Current, approve or reject each request, then save.', 'في Current، اعتمِد كل طلب أو ارفضه، ثم احفظ.'), verify='confirm'),
  S('la-03', 'leave_approvals', hs(4.6, 19.2, 91, 9.8), H('Read a', 'request.', 'اقرأ', 'الطلب.'),
    L('Each request shows the employee, the leave type, the From and To dates, and the days. This example is in History.',
      'يعرض كل طلب الموظف، ونوع الإجازة، وتاريخَي From وTo، وعدد الأيام. هذا المثال من History.')),
  lst['la-05']]
TASKS['geo-attendance']['steps'][-1]['text'] = L('To check past days, tap the filter button, set Attend Date Between in Time Keeping Filter, then tap OK.',
  'لمراجعة الأيام السابقة، اضغط زر التصفية، وحدِّد Attend Date Between في Time Keeping Filter، ثم اضغط OK.')
TASKS['my-permissions']['steps'][1]['helper'] = L('This screen shows the app in the Light theme.', 'تظهر هذه الشاشة بالمظهر الفاتح Light.')
TASKS['my-permissions']['steps'][1]['hotspot'] = hs(1, 7.5, 98, 82)
TASKS['my-permissions']['tips'][0]['text'] = L('Personal late permission is capped at 2 hours a month (HITS App User Guide). Above that, HITS blocks the request.',
  'إذن التأخير الشخصي حدّه ساعتان في الشهر (دليل استخدام تطبيق HITS)، وبعدها يرفض HITS الطلب.')
for st in TASKS['signin-app']['steps']:
    for f in st.get('type') or []:
        if f['box'] is UNAME_BOX or f['box'] == UNAME_BOX: f['box'] = hs(8.5, 45.2, 80.5, 5.4)
UI['en'].update({'searchPlaceholder': 'Search stops', 'noResults': 'No stops match your search.',
  'privacy': 'Your progress is saved on this device only. If tracking is switched on, we count visits and completed stops to improve the guide.',
  'replay': 'Do it again', 'reviewMission': 'Review route', 'praise': ['Well done!', 'Spot on!', 'Great job!']})
UI['ar'].update({'searchPlaceholder': 'ابحث عن محطة', 'noResults': 'لا توجد محطات تطابق بحثك.',
  'privacy': 'يُحفظ تقدّمك على هذا الجهاز فقط. إذا فُعِّلت المتابعة، نحصي الزيارات والمحطات المكتملة لتحسين الدليل.',
  'replay': 'أعِد المحطة', 'reviewMission': 'راجِع المشوار', 'praise': ['أحسنت!', 'في محلّها!', 'عمل رائع!'],
  'questionWorth': 'أجب إجابة صحيحة واربح {n#نقطة} إضافية', 'points': '{n#نقطة}', 'tasksDone': '{done} من {total#محطة}', 'earned': '+{n#نقطة}', 'stepsMeta': '{n#خطوة} · حوالي {m#دقيقة}', 'correct': 'صحيح!'})

# ================= v3.2: Arabic app screens (20 Oct, Arabic employee + manager views) =================
def P(x0, y0, x1, y1): return hs(round(x0 / 5.89, 1), round(y0 / 12.59, 1), round((x1 - x0) / 5.89, 1), round((y1 - y0) / 12.59, 1))
EH = {'leaveDetails': P(305,330,420,495), 'leaveReq': P(170,330,285,495), 'chgReq': P(440,330,555,495),
      'permData': P(440,520,555,690), 'permReq': P(305,520,420,690),
      'attDetails': P(305,710,420,880), 'attTrack': P(170,710,285,880), 'geo': P(35,710,150,880)}
MH = {'leaveDetails': P(30,340,145,505), 'chgAppr': P(165,340,280,505), 'permAppr': P(440,715,555,890),
      'leaveAppr': P(300,525,420,690), 'tkAppr': P(165,715,280,890), 'bell': P(92,102,142,152)}
FAB_PLUS = P(118,1100,202,1186); FAB_MENU = P(36,1100,116,1186); FAB_SEND = P(118,1100,202,1186)
NO = object()
def AR(screen, hot, h1, h2, text, helper=NO, **kw):
    d = {'screen': screen, 'hotspot': hot, 'headline': [h1, h2], 'text': text}
    if helper is not NO: d['helper'] = helper
    d.update(kw); return d
ARS = {
 'signin-app-05': {'screen': 'ar_home_emp', 'hotspot': None},
 'balance-app-01': AR('ar_home_emp', EH['leaveDetails'], 'اضغط', 'تفاصيل الإجازات.', 'من الصفحة الرئيسية، اضغط تفاصيل الإجازات.'),
 'balance-app-02': AR('ar_my_leaves', P(15,180,575,670), 'اقرأ', 'رصيدك.', 'يعرض قسم رصيد الأجازات رصيدك من سنوي وأعياد وعطلات، وما أخذته منها.', 'تحدّد الفترة المدة المعروضة، وهي هنا السنة الحالية.'),
 'balance-app-03': AR('ar_days', P(15,265,575,520), 'اعرف الأيام', 'التي استخدمتها.', 'افتح عدد الأيام المأخوذة لتعرف ما استخدمته من كل نوع إجازة.'),
 'balance-app-04': AR('ar_days', P(15,530,575,1135), 'شاهِد أيامك', 'في رسم بياني.', 'يعرض قسم عدد ايام الأجازات الأيام التي أخذتها حسب نوع الإجازة خلال الفترة المحددة.'),
 'lm-01': AR('ar_home_emp', EH['leaveReq'], 'اضغط', 'طلب الإجازات.', 'من الصفحة الرئيسية، اضغط طلب الإجازات.', None),
 'lm-02': AR('ar_leave_hist', FAB_MENU, 'افتح', 'القائمة.', 'اضغط ⋮ أسفل الشاشة.'),
 'lm-03': AR('ar_leave_menu', P(40,1008,300,1088), 'اضغط', 'رصيد الاجازات.', 'تعرض القائمة تصفية ورصيد الاجازات وجديد. اضغط رصيد الاجازات.'),
 'lm-04': AR('ar_balance', P(15,160,575,470), 'اقرأ', 'رصيدك.', 'تعرض كل فترة رصيدك من سنوي وعطلات وأسبوعية، مع المستحق والمأخوذ والرصيد المتبقي.'),
 'leave-app-01': AR('ar_home_emp', EH['leaveReq'], 'اضغط', 'طلب الإجازات.', 'من الصفحة الرئيسية، اضغط طلب الإجازات.'),
 'leave-app-02': AR('ar_leave_hist', FAB_PLUS, 'ابدأ', 'طلبًا جديدًا.', 'اضغط + أسفل الشاشة.', 'تعرض الحالية الطلبات التي تنتظر قرارًا، وتعرض السابقة طلباتك السابقة.'),
 'leave-app-03': AR('ar_leave_form', P(85,225,560,282), 'افتح قائمة', 'الأجازة.', 'اضغط خانة الأجازة لاختيار نوع الإجازة.'),
 'leave-app-04': AR('ar_leave_types', hs(40, 9.6, 56, 4.4), 'اختر', 'نوع الإجازة.', 'اختر النوع المناسب لطلبك، مثل اجازة سنوي أو 1/2 يوم سنوي.'),
 'leave-app-05': AR('ar_leave_form', P(85,285,560,402), 'حدِّد', 'التواريخ.', 'حدِّد تاريخ البداية في من وتاريخ النهاية في إلى.'),
 'leave-app-06': AR('ar_leave_form', P(15,440,575,975), 'أكمِل', 'باقي البيانات.', 'أكمِل أي بيانات أخرى مطلوبة منك.', 'قسم معلومات أخرى مخصّص لبيانات التواصل معك أثناء غيابك.'),
 'leave-app-07': AR('ar_leave_form', FAB_SEND, 'اضغط', 'زر الإرسال.', 'اضغط زر الإرسال لتقديم طلبك للاعتماد.', 'في قائمة ⋮ المجاورة يظهر الإجراء نفسه باسم ارسال، ومعه الدورة المستندية لمعرفة من سيعتمد طلبك.'),
 'lh-01': AR('ar_home_emp', EH['leaveReq'], 'اضغط', 'طلب الإجازات.', 'من الصفحة الرئيسية، اضغط طلب الإجازات.'),
 'lh-02': AR('ar_leave_hist', P(90,150,512,207), 'اختر', 'الحالية أو السابقة.', 'تعرض الحالية الطلبات التي تنتظر قرارًا، وتعرض السابقة طلباتك السابقة.'),
 'lh-03': AR('ar_leave_hist', P(15,240,575,362), 'اقرأ', 'تفاصيل الطلب.', 'يعرض كل طلب نوع الإجازة، وتاريخَي من وإلى، وعدد الأيام.'),
 'myperm-app-01': AR('ar_home_emp', EH['permData'], 'اضغط', 'بيانات الإذونات.', 'من الصفحة الرئيسية، اضغط بيانات الإذونات.'),
 'myperm-app-02': AR('ar_my_perm', P(15,170,575,860), 'اقرأ', 'ساعاتك.', 'يعرض قسما ساعات الإذن وعدد الإذونات ما استخدمته خلال الفترة المحددة.', None),
 'ph-01': AR('ar_home_emp', EH['permReq'], 'اضغط', 'طلب إذونات.', 'من الصفحة الرئيسية، اضغط طلب إذونات.'),
 'ph-02': AR('ar_perm_req', P(90,150,512,207), 'اختر', 'الحالية أو السابقة.', 'تعرض الحالية الطلبات التي تنتظر قرارًا، وتعرض السابقة طلباتك السابقة.'),
 'ph-03': {'helper': 'هذه الشاشة من التطبيق بالإنجليزية لعدم توفر طلبات في الشاشة العربية. لطلب إذن جديد، راجِع محطة «اطلب إذنًا».'},
 'ma-01': AR('ar_home_emp', EH['attDetails'], 'اضغط', 'تفاصيل الحضور والإنصراف.', 'من الصفحة الرئيسية، اضغط تفاصيل الحضور والإنصراف.'),
 'ma-02': AR('ar_attend', P(15,175,575,770), 'اقرأ', 'ساعات أضافية / تأخير.', 'يعرض قسم ساعات أضافية / تأخير الساعات الزائدة أو الناقصة عن ورديتك.'),
 'ma-03': AR('ar_attend', P(35,262,555,314), 'غيّر', 'الفترة.', 'اضغط الفترة لاختيار المدة، مثل الشهر الحالي.'),
 'ma-04': AR('ar_attend2', P(15,540,575,1195), 'اعرف', 'ملخّص حضورك.', 'يلخّص قسما تعداد حالة الحضور وعدد مرات حدوث الورديات حضورك وورديّاتك خلال الفترة.'),
 'geo-01': AR('ar_home_emp', EH['geo'], 'اضغط', 'تسجيل الحضور والإنصراف.', 'من الصفحة الرئيسية، اضغط تسجيل الحضور والإنصراف.', None),
 'geo-02': AR('ar_geo', P(168,1058,252,1182), 'عند الوصول،', 'اضغط دخول.', 'عند وصولك، اضغط دخول لتسجيل حضورك.'),
 'geo-03': AR('ar_geo', P(52,1058,140,1182), 'عند الانصراف،', 'اضغط خروج.', 'عند انصرافك، اضغط خروج لتسجيل الانصراف.'),
 'geo-04': AR('ar_geo', P(92,150,202,207), 'راجِع', 'السابقة.', 'تعرض الحالية أحدث تسجيلاتك مع الموقع الجغرافي، واضغط السابقة للأيام الأقدم.'),
 'geo-05': {'text': 'لمراجعة أيام محددة، اضغط زر التصفية وحدِّد التاريخين، ثم اضغط OK.', 'helper': 'شاشة التصفية هنا من التطبيق بالإنجليزية.'},
 'nt-01': AR('ar_home_mgr', MH['bell'], 'اضغط', 'أيقونة الجرس.', 'من الصفحة الرئيسية، اضغط أيقونة الجرس في الأعلى.', None),
 'nt-02': AR('ar_notif', P(15,205,575,378), 'اقرأ', 'كل إشعار.', 'تعرض كل بطاقة نوع الطلب والموظف والتواريخ، مع عبارة waiting your approval.', 'لاتخاذ القرار، افتح صفحة الموافقة المناسبة.'),
 'ap-01': AR('ar_home_mgr', MH['permAppr'], 'اضغط', 'موافقة الإذونات.', 'من الصفحة الرئيسية، اضغط موافقة الإذونات.'),
 'ap-02': AR('ar_perm_appr', P(433,150,548,210), 'افتح', 'الحالية.', 'تعرض الحالية الطلبات التي تنتظر قرارك.'),
 'ap-03': {'helper': 'هذه الشاشات من التطبيق بالإنجليزية لعدم وجود طلبات في الشاشة العربية.'},
 'la-01': AR('ar_home_mgr', MH['leaveAppr'], 'اضغط', 'موافقة الإجازات.', 'من الصفحة الرئيسية، اضغط موافقة الإجازات.'),
 'la-02': AR('ar_la_current', P(30,165,555,222), 'اعرف', 'التبويبات الثلاثة.', 'الحالية: تنتظر قرارك. القادمة: ما زالت لدى معتمِد قبلك. السابقة: طلبات اتخذت فيها قرارًا.', None),
 'la-03': AR('ar_la_current', P(15,245,575,362), 'اقرأ', 'الطلب.', 'يعرض كل طلب الموظف، ونوع الإجازة، وتاريخَي من وإلى، وعدد الأيام.'),
 'la-05': AR('ar_la_hist', P(30,1093,112,1177), 'صفِّ', 'القائمة.', 'اضغط زر التصفية لعرض الطلبات في تواريخ محددة.'),
 'tk-01': AR('ar_home_mgr', MH['tkAppr'], 'اضغط', 'موافقة القراءات الغير مكتملة.', 'من الصفحة الرئيسية، اضغط موافقة القراءات الغير مكتملة.'),
 'tk-02': AR('ar_tk_filter', P(60,640,560,730), 'حدِّد', 'التواريخ.', 'في تصفية طلب القراءات الغير مكتملة، حدِّد التاريخين في التاريخ بين.'),
 'tk-03': AR('ar_tk_filter', P(208,745,288,822), 'اضغط', 'موافق.', 'اضغط موافق لعرض الطلبات في هذه الفترة، ثم اعتمِد كل طلب أو ارفضه واحفظ.'),
 'fp-01': AR('ar_home_mgr', MH['permAppr'], 'اضغط', 'موافقة الإذونات.', 'من الصفحة الرئيسية، اضغط موافقة الإذونات.', None),
 'fp-02': AR('ar_perm_appr', P(52,150,142,210), 'افتح', 'السابقة.', 'تعرض السابقة الطلبات التي اتخذت فيها قرارًا.'),
 'fp-03': AR('ar_perm_appr', P(30,1082,112,1168), 'اضغط', 'زر التصفية.', 'اضغط زر التصفية أسفل الشاشة.'),
 'fp-04': AR('ar_perm_filter', P(50,580,565,770), 'حدِّد التواريخ', 'والنوع.', 'في اختيار الاذونات، حدِّد التاريخ بين، ونوع الإذن في الاذونات عند الحاجة.'),
 'fp-05': AR('ar_perm_filter', P(208,780,288,852), 'اضغط', 'موافق.', 'اضغط موافق لعرض الطلبات المطابقة فقط.'),
 'tr-01': AR('ar_home_mgr', MH['leaveDetails'], 'اضغط', 'تفاصيل الإجازات.', 'من الصفحة الرئيسية، اضغط تفاصيل الإجازات.', 'الخطوات التالية من التطبيق بالإنجليزية.'),
}
for t in TASKS.values():
    for st in t['steps']:
        if st['id'] in ARS: st['ar'] = ARS.pop(st['id'])
assert not ARS, ARS

def ins_after(tid, after, steps):
    lst = TASKS[tid]['steps']; i = [s['id'] for s in lst].index(after) + 1
    lst[i:i] = steps
def SA(i, screen, hot, h1, h2, text, helper=None, verify=None):
    s = S(i, screen, hot, {'en': [h1, h2], 'ar': [h1, h2]}, L(text, text), L(helper, helper) if helper else None, verify)
    s['only'] = 'ar'; return s
ins_after('leave-approvals', 'la-03', [
    SA('la-ar1', 'ar_la_current', FAB_MENU, 'افتح', 'القائمة.', 'لاعتماد كل الطلبات معًا، اضغط ⋮ أسفل الشاشة.'),
    SA('la-ar2', 'ar_la_menu', P(36,1093,268,1177), 'اختر', 'موافقة الكل.', 'تعرض القائمة تصفية ورفض الكل وموافقة الكل. اضغط موافقة الكل.'),
    SA('la-ar3', 'ar_la_confirm', P(15,555,572,847), 'أكّد', 'بموافق.', 'تطلب HITS التأكيد. اكتب السبب إن احتجت، ثم اضغط موافق.', 'رفض الكل يعمل بالطريقة نفسها.'),
])

def NEWAR(tid, icon, name, situation, t1, t2, purpose, outcome, path, steps, q, opts, tips=()):
    TASKS[tid] = {'id': tid, 'icon': icon, 'only': 'ar', 'name': L(name, name), 'situation': L(situation, situation),
        'title': {'en': [t1, t2], 'ar': [t1, t2]}, 'purpose': L(purpose, purpose), 'outcome': L(outcome, outcome),
        'path': path, 'path_ar': path, 'goodToKnow': [], 'helpCard': False, 'tips': [TIP(a, b, b) for a, b in tips], 'steps': steps,
        'check': Q(L(q, q), [(L(o, o), c, L(w, w)) for o, c, w in opts])}
NEWAR('perm-request', 'clock', 'طلب إذن', 'سأتأخر أو سأخرج مبكرًا', 'اطلب', 'إذنًا.', 'يُرسل طلب إذن تأخير أو انصراف أو مأمورية إلى المعتمِد.',
    'تستطيع إرسال طلب إذن للاعتماد.', 'الرئيسية › طلب إذونات › +', [
    SA('pr-01', 'ar_home_emp', EH['permReq'], 'اضغط', 'طلب إذونات.', 'من الصفحة الرئيسية، اضغط طلب إذونات.'),
    SA('pr-02', 'ar_perm_req', FAB_PLUS, 'ابدأ', 'طلبًا جديدًا.', 'اضغط + أسفل الشاشة.'),
    SA('pr-03', 'ar_perm_form', P(85,388,560,444), 'افتح قائمة', 'الإذن.', 'اضغط خانة الإذن لاختيار نوعه.'),
    SA('pr-04', 'ar_perm_types', P(4,975,585,1255), 'اختر', 'نوع الإذن.', 'اختر الإذن المناسب، مثل اذن شخصي - حضور متأخر، ثم اضغط ✓.'),
    SA('pr-05', 'ar_perm_mission', P(80,690,560,768), 'مأمورية؟', 'اكتب الجهة.', 'عند اختيار اذن مأمورية تظهر خانة جهة المأمورية، وهي إلزامية.', 'دون جهة المأمورية لن يُرسَل الطلب.'),
    SA('pr-06', 'ar_perm_form', P(85,450,560,562), 'حدِّد', 'الوقت.', 'حدِّد التاريخ والوقت في من وإلى.', 'اكتب الوقت بنظام 24 ساعة؛ 13:00 تعني الواحدة ظهرًا.'),
    SA('pr-07', 'ar_perm_send', P(34,1108,205,1198), 'اضغط', 'ارسال.', 'اضغط زر الإرسال، أو افتح ⋮ واختر ارسال، لتقديم الطلب للاعتماد.', 'الدورة المستندية تعرض من سيعتمد طلبك.'),
  ], 'اخترت اذن مأمورية. ما الخانة التي يجب ملؤها قبل الإرسال؟', [
    ('جهة المأمورية', True, 'جهة المأمورية إلزامية في طلبات المأمورية.'),
    ('معلومات أخرى', False, 'معلومات أخرى اختيارية، أما جهة المأمورية فإلزامية.'),
    ('الدورة المستندية', False, 'الدورة المستندية تعرض المعتمِدين فقط.')],
  tips=[('pr-04', 'إذن التأخير الشخصي حدّه ساعتان في الشهر، وبعدها يرفض HITS الطلب.')])
NEWAR('attendance-tracking', 'pin', 'متابعة الحضور والانصراف', 'متى سجّلت دخولي وخروجي؟', 'تابِع', 'حضورك وانصرافك.',
    'يعرض كل تسجيل دخول وخروج مع الوقت والموقع.', 'تستطيع مراجعة كل تسجيلات حضورك وانصرافك.', 'الرئيسية › متابعة الحضور والإنصراف', [
    SA('at-01', 'ar_home_emp', EH['attTrack'], 'اضغط', 'متابعة الحضور والإنصراف.', 'من الصفحة الرئيسية، اضغط متابعة الحضور والإنصراف.'),
    SA('at-02', 'ar_attend_log', P(15,232,575,388), 'اقرأ', 'سجلّك.', 'يعرض كل سطر دخول أو خروج مع التاريخ والوقت والموقع الجغرافي.', 'العلامة الخضراء للدخول، والحمراء للخروج.'),
    SA('at-03', 'ar_attend_log', P(92,150,202,207), 'للأيام الأقدم،', 'اضغط السابقة.', 'تعرض الحالية أحدث تسجيلاتك، وتعرض السابقة الأيام الأقدم.', verify='confirm'),
  ], 'ماذا تعني العلامة الحمراء في متابعة الحضور والإنصراف؟', [
    ('تسجيل خروج', True, 'الحمراء للخروج، والخضراء للدخول.'),
    ('تسجيل دخول', False, 'الدخول يظهر بالعلامة الخضراء.'),
    ('غياب', False, 'الغياب لا يظهر هنا، بل في تفاصيل الحضور والإنصراف.')])
NEWAR('changes-request', 'list', 'طلب تغيير بيانات', 'أريد تسجيل تغيير في بياناتي', 'اطلب', 'تغيير بياناتك.',
    'يُرسل طلب تغيير، مثل شهادات ميلاد الأبناء، إلى المعتمِد.', 'تستطيع إرسال طلب تغيير للاعتماد.', 'الرئيسية › طلب تغيرات الحالة › +', [
    SA('cr-01', 'ar_home_mgr', P(300,340,420,505), 'اضغط', 'طلب تغيرات الحالة.', 'من الصفحة الرئيسية، اضغط طلب تغيرات الحالة.'),
    SA('cr-02', 'ar_chg_list', FAB_PLUS, 'ابدأ', 'طلبًا جديدًا.', 'اضغط + أسفل الشاشة.', 'تعرض الحالية طلباتك المفتوحة، والسابقة طلباتك القديمة.'),
    SA('cr-03', 'ar_chg_form', P(85,225,560,292), 'اختر', 'حركه التغيير.', 'اضغط خانة حركه التغيير لاختيار نوع الطلب.'),
    SA('cr-04', 'ar_chg_pick', P(4,945,585,1255), 'اختر', 'نوع الطلب.', 'اختر من القائمة، مثل شهادات ميلاد ابناء العاملين، ثم اضغط ✓.'),
    SA('cr-05', 'ar_chg_filled', P(15,760,575,1150), 'أكمِل', 'البيانات المطلوبة.', 'تظهر خانات خاصة بنوع الطلب في قسم نموذجي الخاص. أكمِلها، وأضِف تعليقًا إن احتجت.', verify='confirm'),
    SA('cr-06', 'ar_chg_filled', FAB_SEND, 'اضغط', 'زر الإرسال.', 'اضغط زر الإرسال لتقديم الطلب للاعتماد.', verify='confirm'),
  ], 'اخترت حركه التغيير. أين تكتب البيانات الخاصة بطلبك؟', [
    ('في قسم نموذجي الخاص', True, 'تظهر فيه الخانات الخاصة بنوع الطلب.'),
    ('في خانة العمله', False, 'العمله تحدّد العملة فقط.'),
    ('في قائمة ⋮', False, 'القائمة للإرسال والدورة المستندية، لا لإدخال البيانات.')])
NEWAR('changes-approvals', 'check-badge', 'اعتماد طلبات تغيير البيانات', 'أرسل أحد أفراد فريقي طلب تغيير', 'اعتمِد', 'طلبات التغيير.',
    'يعرض طلبات تغيير البيانات من فريقك ويتيح حصرها.', 'تستطيع العثور على طلبات التغيير لفريقك.', 'الرئيسية › موافقة تغيرات الحالة', [
    SA('ca-01', 'ar_home_mgr', MH['chgAppr'], 'اضغط', 'موافقة تغيرات الحالة.', 'من الصفحة الرئيسية، اضغط موافقة تغيرات الحالة.'),
    SA('ca-02', 'ar_chg_appr', P(30,165,555,222), 'اعرف', 'التبويبات.', 'الحالية: تنتظر قرارك. القادمة: ما زالت لدى معتمِد قبلك. السابقة: ما اتخذت فيه قرارًا.', verify='confirm'),
    SA('ca-03', 'ar_chg_appr', P(30,1093,112,1177), 'اضغط', 'زر التصفية.', 'اضغط زر التصفية لحصر الطلبات.'),
    SA('ca-04', 'ar_chg_appr_filter', P(15,600,572,882), 'حدِّد', 'ما تبحث عنه.', 'حدِّد التاريخ بين، واختر حركه التغيير عند الحاجة، ثم اضغط موافق.'),
  ], 'تريد طلبات شهادات الميلاد فقط. ماذا تحدّد في التصفية؟', [
    ('حركه التغيير', True, 'حركه التغيير تحصر الطلبات حسب نوعها.'),
    ('التاريخ بين فقط', False, 'التاريخ يحصر الفترة، لا نوع الطلب.'),
    ('إلغاء', False, 'إلغاء يغلق التصفية دون تغيير.')])

# Arabic labels in titles, purposes, paths, tips and questions
def setar(o, v): o['ar'] = v
PATH_AR = {'leave-balance': 'الرئيسية › تفاصيل الإجازات', 'leave-menu': 'الرئيسية › طلب الإجازات › ⋮ › رصيد الاجازات', 'leave-request': 'الرئيسية › طلب الإجازات › +',
  'leave-history': 'الرئيسية › طلب الإجازات', 'my-permissions': 'الرئيسية › بيانات الإذونات', 'permission-history': 'الرئيسية › طلب إذونات',
  'my-attendance': 'الرئيسية › تفاصيل الحضور والإنصراف', 'geo-attendance': 'الرئيسية › تسجيل الحضور والإنصراف', 'notifications': 'الرئيسية › الإشعارات',
  'approve-permissions': 'الرئيسية › موافقة الإذونات', 'leave-approvals': 'الرئيسية › موافقة الإجازات', 'tk-approvals': 'الرئيسية › موافقة القراءات الغير مكتملة',
  'find-permissions': 'الرئيسية › موافقة الإذونات › السابقة', 'team-records': 'الرئيسية › تفاصيل الإجازات'}
for k, v in PATH_AR.items(): TASKS[k]['path_ar'] = v
setar(TASKS['leave-menu']['purpose'], 'يفتح رصيد إجازاتك من قائمة طلب الإجازات.')
setar(TASKS['team-records']['purpose'], 'يوضّح كيف يختار المدير شخصًا من القائمة في تفاصيل الإجازات والصفحات المشابهة.')
for tp in TASKS['leave-request']['tips']:
    if tp['after'] == 'leave-app-01': setar(tp['text'], 'إذا ظهرت قائمة أسماء عند فتح طلب الإجازات، فاضغط اسمك أولًا، وستجده في الأعلى.')
    if tp['after'] == 'leave-app-04': setar(tp['text'], 'اخترت مأمورية؟ يجب كتابة جهة المأمورية، وإلا لن يُرسَل الطلب.')
setar(TASKS['approve-permissions']['tips'][0]['text'], 'موافقة الكل ورفض الكل تحدّدان كل الطلبات مرة واحدة، وتحتاجان التأكيد أيضًا.')
setar(TASKS['team-records']['tips'][0]['text'], 'تظهر القائمة نفسها في تفاصيل الحضور والإنصراف وبيانات الإذونات وطلب إذونات.')
def qar(tid, opts_ar, why_ar=None, q=None):
    c = TASKS[tid]['check']
    if q: setar(c['q'], q)
    for o, a in zip(c['options'], opts_ar): setar(o['text'], a)
    for o, w in zip(c['options'], why_ar or []): setar(o['why'], w)
qar('leave-balance', ['تفاصيل الإجازات', 'موافقة الإجازات', 'طلب إذونات'], ['يعرض تفاصيل الإجازات رصيدك والأيام التي استخدمتها.', 'موافقة الإجازات لاعتماد طلبات الآخرين.', 'طلب إذونات لطلبات الاستئذان، لا للإجازات.'])
qar('leave-menu', ['⋮ ثم رصيد الاجازات', '⋮ ثم تصفية', 'السابقة'], ['رصيد الاجازات في قائمة ⋮ يعرض رصيدك لكل فترة.', 'تصفية تحصر قائمة طلباتك.', 'السابقة تعرض طلباتك القديمة، لا رصيدك.'],
    'أنت في طلب الإجازات وتريد معرفة رصيدك. ماذا تضغط؟')
qar('leave-request', ['في خانة الأجازة، باختيار 1/2 يوم سنوي.', 'في تاريخ إلى.', 'في خانة بيانات اخرى.'], ['تعرض خانة الأجازة كل الأنواع، ومنها نصف اليوم وربعه.', 'التواريخ تحدّد موعد الإجازة، لا نوعها.', 'بيانات اخرى للتفاصيل الإضافية، لا لنوع الإجازة.'])
qar('leave-history', ['طلب الإجازات › الحالية', 'طلب الإجازات › السابقة', 'تفاصيل الإجازات'], ['تعرض الحالية الطلبات التي ما زالت تنتظر قرارًا.', 'تعرض السابقة طلباتك القديمة.', 'تفاصيل الإجازات تعرض رصيدك، لا طلباتك.'])
qar('my-permissions', ['بيانات الإذونات', 'طلب إذونات', 'تفاصيل الحضور والإنصراف'], ['يعرض قسم ساعات الإذن ما استخدمته خلال الفترة المحددة.', 'طلب إذونات يعرض طلباتك، لا إجمالي ساعاتك.', 'تفاصيل الحضور تعرض حضورك، لا ساعات الإذن.'])
qar('permission-history', ['طلب إذونات › السابقة', 'طلب إذونات › الحالية', 'بيانات الإذونات'], ['تحتفظ السابقة بطلباتك القديمة.', 'تعرض الحالية الطلبات المنتظِرة فقط.', 'بيانات الإذونات تعرض الساعات، لا الطلبات.'])
qar('my-attendance', ['الفترة', 'Theme', 'Language'], ['تحدّد الفترة المدة لكل قسم.'])
qar('geo-attendance', ['خروج', 'دخول', 'السابقة'], ['يسجّل خروج وقت انصرافك.', 'يسجّل دخول وقت وصولك.', 'تعرض السابقة ما سجّلته فقط.'])
qar('notifications', ['موافقة الإجازات', 'موافقة الإذونات', 'طلب الإجازات'], ['تُعتمد طلبات الإجازة من موافقة الإجازات.', 'موافقة الإذونات لطلبات الاستئذان.', 'طلب الإجازات لإجازاتك أنت.'])
qar('leave-approvals', ['القادمة', 'الحالية', 'السابقة'], ['تعرض القادمة الطلبات التي تنتظر معتمِدًا قبلك.', 'تعرض الحالية الطلبات التي تنتظرك أنت فقط.', 'تعرض السابقة الطلبات التي اتخذت فيها قرارًا.'])
qar('tk-approvals', ['غيّر التواريخ في التصفية، ثم اضغط موافق', 'اضغط إلغاء', 'افتح طلب القراءات الغير مكتملة'], ['التواريخ تحدّد الطلبات التي تظهر لك.', 'إلغاء يغلق التصفية دون تغيير القائمة.', 'هذا لطلباتك أنت.'])
qar('find-permissions', ['التاريخ بين في التصفية', 'تبويب الحالية', 'إلغاء'], ['تواريخ التصفية تحدّد الطلبات التي تظهر.', 'تعرض الحالية الطلبات التي ما زالت تنتظرك.', 'إلغاء يغلق التصفية دون تغيير.'],
    'تريد طلبات الشهر الماضي فقط في السابقة. ماذا تغيّر؟')
qar('team-records', ['الاسم الأول في الأعلى', 'آخر اسم في القائمة', 'في موافقة الإجازات'], None, 'فتحت تفاصيل الإجازات فظهرت قائمة أسماء. أين سجلّك أنت؟')

MISSIONS[2]['tasks'] = ['my-permissions', 'perm-request', 'permission-history', 'my-attendance', 'attendance-tracking', 'geo-attendance']
MISSIONS.insert(3, {'id': 'mydata', 'roles': ['employee'], 'icon': 'list', 'title': L('My data', 'بياناتي'),
    'outcome': L('Request a change to your records.', 'اطلب تغييرًا في بياناتك.'), 'tasks': ['changes-request']})
MISSIONS[-1]['tasks'] = ['find-permissions', 'changes-approvals', 'team-records']
UI['ar']['coming'] = 'محطات قادمة قريبًا: كشف الراتب، وتغيير البيانات، وطلب القراءات الغير مكتملة.'
for t in TASKS.values():
    for st in t['steps']:
        assert st.get('ar', {}).get('screen', st['screen']), st['id']

# ================= v3.3: Arabic copy fully in Arabic (20 Oct) =================
def stepar(tid, sid, **kw):
    st = next(s for s in TASKS[tid]['steps'] if s['id'] == sid); st.setdefault('ar', {}).update(kw)
def H2(a, b): return [a, b]
# steps that still show an English screen: Arabic wording first, the on-screen English label in brackets
stepar('signin-app', 'signin-app-01', headline=H2('افتح', 'تطبيق HITS.'), text='افتح تطبيق HITS على هاتفك.')
stepar('signin-app', 'signin-app-o365', headline=H2('لديك بريد عمل؟', 'اضغط أوفيس 365.'), text='إذا كان لديك بريد إلكتروني للعمل، فاضغط زر أوفيس 365 (OFFICE 365)، ثم ادخل ببريد العمل وكلمة مروره.')
stepar('signin-app', 'signin-app-02', text='أدخِل رقمك الوظيفي في خانة اسم المستخدم (Username).')
stepar('signin-app', 'signin-app-03', text='أدخِل كلمة المرور في خانة كلمة المرور (Password).')
stepar('signin-app', 'signin-app-04', headline=H2('اضغط', 'زر الدخول.'), text='اضغط زر الدخول (LOGIN).')
stepar('forgot-password', 'forgot-app-01', headline=H2('اضغط', 'نسيت كلمة المرور؟'), text='في شاشة الدخول، اضغط رابط نسيت كلمة المرور (Forgot my password?).')
stepar('forgot-password', 'forgot-app-02', text='أدخِل اسم المستخدم (Username) وبريد الشركة الإلكتروني (Company Email).')
stepar('forgot-password', 'forgot-app-03', headline=H2('اضغط', 'إرسال.'), text='اضغط إرسال (SEND)، ثم اتبع التعليمات التي تصلك.', helper='تدخل ببريد الشركة؟ لكلمة مرور البريد، تواصل مع الدعم الفني.')
stepar('app-settings', 'settings-app-02', headline=H2('اختر', 'المظهر.'), text='من المظهر (Theme)، اختر تلقائي أو فاتح أو داكن.')
stepar('app-settings', 'settings-app-03', headline=H2('اختر', 'اللغة.'), text='من اللغة (Language)، اختر العربية ليطابق تطبيقك هذا الدليل.', helper='يتيح التطبيق أيضًا الإنجليزية والفرنسية.')
stepar('approve-permissions', 'ap-03', text='يعرض كل طلب الموظف، ونوع الإذن، ووقتَي البداية والنهاية، وعدد الساعات. اضغطه لعرض التفاصيل.')
stepar('approve-permissions', 'ap-04', text='تعرض أقسام تفاصيل الإذن والوردية والحضور الطلبَ مع الوردية وأوقات الحضور الفعلية.')
stepar('notifications', 'nt-02', text='تعرض كل بطاقة نوع الطلب والموظف والتواريخ، مع عبارة «بانتظار موافقتك».')
stepar('leave-approvals', 'la-ar3', text='يطلب التطبيق التأكيد. اكتب السبب إن احتجت، ثم اضغط موافق.')
for s in TASKS['permission-history']['steps']:
    if s['id'] == 'ph-03': s['only'] = 'en'
for s in TASKS['geo-attendance']['steps']:
    if s['id'] == 'geo-05': s['only'] = 'en'
for tp in TASKS['permission-history']['tips']: tp['after'] = 'ph-02'
# titles, purposes, tips
setar(TASKS['signin-app']['purpose'], 'يفتح تطبيق HITS بالرقم الوظيفي وكلمة المرور، للموظفين الذين ليس لديهم بريد إلكتروني للعمل.')
setar(TASKS['signin-app']['outcome'], 'تستطيع تسجيل الدخول إلى تطبيق HITS.')
setar(TASKS['forgot-password']['purpose'], 'يبدأ استرجاع كلمة المرور من شاشة الدخول في تطبيق HITS.')
setar(TASKS['app-settings']['purpose'], 'يغيّر مظهر تطبيق HITS واللغة التي يستخدمها.')
setar(TASKS['leave-request']['purpose'], 'يُرسل طلب إجازتك إلى المعتمِد عبر التطبيق.')
setar(TASKS['geo-attendance']['purpose'], 'يسجّل حضورك وانصرافك من هاتفك عبر تسجيل الحضور والإنصراف.')
setar(TASKS['geo-attendance']['outcome'], 'تستطيع تسجيل الحضور والانصراف من هاتفك.')
setar(TASKS['leave-menu']['outcome'], 'تستطيع معرفة رصيدك من طلب الإجازات في ثوانٍ.')
for t in TASKS.values():
    for tp in t['tips']:
        tp['text']['ar'] = (tp['text']['ar'].replace('يعملان على HITS Web', 'يعملان على موقع HITS')
            .replace('لـ HITS', 'للتطبيق').replace('اترك Tenant ID كما هو.', 'اترك رقم الجهة (Tenant ID) كما هو.')
            .replace(' (دليل استخدام تطبيق HITS)', '').replace('يرفض HITS الطلب', 'يرفض التطبيق الطلب'))
# questions: all Arabic
qar('signin-app', ['الرقم الوظيفي وكلمة المرور، ثم زر الدخول', 'زر أوفيس 365', 'رابط التسجيل وإعادة التفعيل'],
    ['الموظفون الذين ليس لديهم بريد عمل يدخلون بالرقم الوظيفي.', 'أوفيس 365 مخصّص للموظفين الذين لديهم بريد عمل.', 'هذا الرابط ليس للدخول اليومي.'])
qar('forgot-password', ['اسم المستخدم وبريد الشركة الإلكتروني'], ['تطلب الشاشة اسم المستخدم وبريد الشركة، ثم تضغط إرسال.'],
    'ما البيانات التي تطلبها شاشة نسيت كلمة المرور؟')
qar('app-settings', ['اللغة، من الإعدادات', 'المظهر', 'رقم الجهة (Tenant ID)'],
    ['اختر العربية من اللغة ليطابق تطبيقك هذا الدليل.', 'المظهر يغيّر الألوان الفاتحة أو الداكنة فقط.', 'اترك رقم الجهة كما هو.'])
qar('my-attendance', ['الفترة', 'المظهر', 'اللغة'], ['تحدّد الفترة المدة لكل قسم.', 'المظهر يغيّر ألوان التطبيق فقط.', 'اللغة تغيّر لغة التطبيق، لا التواريخ.'])
qar('notifications', ['موافقة الإجازات', 'موافقة الإذونات', 'طلب الإجازات'], None, 'وصلك إشعار إجازة بانتظار موافقتك. أين تتخذ القرار؟')
qar('team-records', ['الاسم الأول في الأعلى', 'آخر اسم في القائمة', 'في موافقة الإجازات'], ['اسمك يأتي دائمًا أولًا.', 'اسمك في الأعلى، لا في الأسفل.', 'موافقة الإجازات لاتخاذ القرار في الطلبات.'])
import re as _re
for k, t in TASKS.items():
    for o in [t['check']['q']] + [x['text'] for x in t['check']['options']] + [x['why'] for x in t['check']['options']]:
        left = _re.sub(r'\([^)]*\)', '', o['ar'])
        assert not _re.search(r'[A-Za-z]', left), (k, o['ar'])

# ================= v3.4: clean Arabic sentences (no mixed English), Arabic settings screen =================
SET_AR = 'ar_settings'
stepar('app-settings', 'settings-app-02', screen=SET_AR, hotspot=P(53,458,536,697), headline=H2('اختر', 'المظهر.'), text='اختر المظهر الذي يناسبك: تلقائي أو فاتح أو داكن.')
stepar('app-settings', 'settings-app-03', screen=SET_AR, hotspot=P(53,331,536,429), headline=H2('اختر', 'اللغة.'), text='من خانة اللغة، اختر العربية ليطابق تطبيقك هذا الدليل.', helper='يتيح التطبيق أيضًا الإنجليزية والفرنسية.')
stepar('signin-app', 'signin-app-o365', text='إذا كان لديك بريد إلكتروني للعمل، فاضغط زر أوفيس 365، ثم ادخل ببريد العمل وكلمة مروره.')
stepar('signin-app', 'signin-app-02', text='أدخِل رقمك الوظيفي في الخانة الأولى، خانة اسم المستخدم.')
stepar('signin-app', 'signin-app-03', text='أدخِل كلمة المرور في الخانة الثانية.')
stepar('signin-app', 'signin-app-04', text='اضغط زر الدخول على يسار زر أوفيس 365.')
stepar('forgot-password', 'forgot-app-01', text='في شاشة الدخول، اضغط رابط نسيت كلمة المرور أسفل الأزرار.')
stepar('forgot-password', 'forgot-app-02', text='أدخِل اسم المستخدم في الخانة الأولى، وبريد الشركة الإلكتروني في الخانة الثانية.')
stepar('forgot-password', 'forgot-app-03', text='اضغط زر الإرسال، ثم اتبع التعليمات التي تصلك.')
TASKS['signin-app']['path_ar'] = 'شاشة الدخول'; TASKS['forgot-password']['path_ar'] = 'شاشة الدخول › نسيت كلمة المرور'; TASKS['app-settings']['path_ar'] = 'الإعدادات'
for tp in TASKS['app-settings']['tips']: setar(tp['text'], 'اترك رقم الجهة كما هو، ولا تغيّره.')
TASKS['app-settings']['check']['options'][2]['text']['ar'] = 'رقم الجهة'
GL = {'وضع التطبيق (Application Mode)': 'وضع التطبيق', 'الدخول عبر Office 365': 'الدخول عبر أوفيس 365', 'مسار الاعتماد (Workflow)': 'مسار الاعتماد',
      'Incomplete TK': 'القراءات غير المكتملة', 'Run No.': 'رقم دورة الرواتب'}
for g in V22.get('glossary') or []:
    if g['term']['ar'] in GL: g['term']['ar'] = GL[g['term']['ar']]
    g['meaning']['ar'] = g['meaning']['ar'].replace('على HITS Web', 'على موقع HITS').replace('Office 365', 'أوفيس 365')
for x in V22['pages']['help'].get('support', []): x['ar'] = x['ar'].replace('Office 365', 'أوفيس 365')
UI['ar']['helpCardTitle'] = ['مشكلة في كلمة مرور', 'بريد الشركة؟']

# ================= v3.5: rewritten questions, new dark home, routes =================
def QQ(tid, q, opts):
    TASKS[tid]['check'] = {'q': {'en': q[0], 'ar': q[1]}, 'options': [{'text': {'en': o[0], 'ar': o[1]}, 'correct': o[2], 'why': {'en': o[3], 'ar': o[4]}} for o in opts]}
QQ('signin-app', ('A new colleague has no work email. How does she sign in?', 'زميلة جديدة ليس لديها بريد عمل. كيف تسجّل الدخول؟'), [
 ('Work ID in Username, her password, then LOGIN', 'رقمها الوظيفي في اسم المستخدم، ثم كلمة المرور، ثم زر الدخول', True, 'Without a work email, you sign in with your Work ID.', 'من ليس لديه بريد عمل يدخل برقمه الوظيفي.'),
 ('Tap OFFICE 365 and type her Work ID', 'تضغط أوفيس 365 وتكتب رقمها الوظيفي', False, 'OFFICE 365 needs a work email and its password.', 'أوفيس 365 يحتاج بريد عمل وكلمة مروره.'),
 ('Tap Register/Reactivate User', 'تضغط رابط التسجيل وإعادة التفعيل', False, 'That link is not for everyday sign-in.', 'هذا الرابط ليس للدخول اليومي.')])
QQ('forgot-password', ('You forgot your HITS password. What does the Forgot password screen ask for?', 'نسيت كلمة مرور HITS. ماذا تطلب منك شاشة نسيت كلمة المرور؟'), [
 ('Your username and company email, then SEND', 'اسم المستخدم وبريد الشركة، ثم زر الإرسال', True, 'Those two details start the recovery.', 'هاتان المعلومتان تبدآن الاسترجاع.'),
 ('Your old password and a new one', 'كلمة المرور القديمة وكلمة جديدة', False, "You don't type a password here — that's what you are recovering.", 'لا تكتب كلمة مرور هنا، فهي ما تحاول استرجاعه.'),
 ('Your phone number', 'رقم هاتفك', False, "The screen doesn't ask for it.", 'الشاشة لا تطلب رقم الهاتف.')])
QQ('app-settings', ("Your app's buttons don't match the language of this guide. What do you change?", 'أزرار تطبيقك بلغة غير لغة هذا الدليل. ماذا تغيّر؟'), [
 ('Language, in Settings', 'اللغة، من الإعدادات', True, 'Choose the same language as the guide you are following.', 'اختر لغة الدليل الذي تتابعه نفسها.'),
 ('Theme', 'المظهر', False, 'Theme only changes light or dark colours.', 'المظهر يغيّر الألوان الفاتحة أو الداكنة فقط.'),
 ('Tenant ID', 'رقم الجهة', False, 'Leave Tenant ID as it is.', 'اترك رقم الجهة كما هو.')])
QQ('leave-balance', ('You want to know how many annual leave days you have left this year. Where do you look?', 'تريد معرفة أيام إجازتك السنوية المتبقية هذا العام. أين تبحث؟'), [
 ('My Leaves › Leaves Balance', 'تفاصيل الإجازات › رصيد الأجازات', True, 'Leaves Balance shows what you have and what you have taken.', 'يعرض رصيد الأجازات ما لديك وما أخذته.'),
 ('Leaves Request › History', 'طلب الإجازات › السابقة', False, 'History lists past requests, not your balance.', 'تعرض السابقة طلباتك القديمة، لا رصيدك.'),
 ('My Permissions', 'بيانات الإذونات', False, 'My Permissions shows permission hours, not leave days.', 'بيانات الإذونات تعرض ساعات الإذن، لا أيام الإجازة.')])
QQ('leave-menu', ("You're in Leaves Request, about to apply. How do you check your balance first?", 'أنت في طلب الإجازات وستقدّم طلبًا. كيف تعرف رصيدك أولًا؟'), [
 ('Tap ⋮, then Balance', 'تضغط ⋮ ثم رصيد الاجازات', True, 'Balance in the ⋮ menu shows your balance for each period.', 'رصيد الاجازات في قائمة ⋮ يعرض رصيدك لكل فترة.'),
 ('Tap +, then Leave', 'تضغط + ثم الأجازة', False, '+ starts a new request; it does not show your balance.', '+ يبدأ طلبًا جديدًا، ولا يعرض الرصيد.'),
 ('Open History', 'تفتح السابقة', False, 'History lists past requests, not your balance.', 'تعرض السابقة طلباتك القديمة، لا رصيدك.')])
QQ('leave-request', ('You need half a day off next Sunday. What do you choose in the Leave field?', 'تحتاج نصف يوم إجازة الأحد القادم. ماذا تختار في خانة الأجازة؟'), [
 ('Annual 1/2 Day', '1/2 يوم سنوي', True, 'The half-day type takes half a day from your annual balance.', 'نوع نصف اليوم يخصم نصف يوم من رصيدك السنوي.'),
 ('Annual Leave, with the same From and To date', 'اجازة سنوي بتاريخ واحد في من وإلى', False, 'That books a full day, not half.', 'هذا يحجز يومًا كاملًا، لا نصف يوم.'),
 ('Annual Leave, and write "half day" in Other info', 'اجازة سنوي مع كتابة نصف يوم في بيانات اخرى', False, 'Other info does not change the leave type.', 'بيانات اخرى لا تغيّر نوع الإجازة.')])
QQ('leave-history', ("You sent a leave request yesterday and your manager hasn't replied. Where is it?", 'قدّمت طلب إجازة أمس ولم يردّ مديرك بعد. أين تجده؟'), [
 ('Leaves Request › Current', 'طلب الإجازات › الحالية', True, 'Current shows requests still waiting for a decision.', 'تعرض الحالية الطلبات التي ما زالت تنتظر قرارًا.'),
 ('Leaves Request › History', 'طلب الإجازات › السابقة', False, 'A request moves to History after a decision.', 'ينتقل الطلب إلى السابقة بعد اتخاذ القرار.'),
 ('My Leaves', 'تفاصيل الإجازات', False, 'My Leaves shows your balance, not your requests.', 'تفاصيل الإجازات تعرض رصيدك، لا طلباتك.')])
QQ('my-permissions', ('Do you still have personal permission hours left this month? Where do you check?', 'هل بقيت لك ساعات إذن هذا الشهر؟ أين تتحقق؟'), [
 ('My Permissions › Permission Hours', 'بيانات الإذونات › ساعات الإذن', True, 'Permission Hours shows the hours you have used this period.', 'يعرض قسم ساعات الإذن ما استخدمته خلال الفترة.'),
 ('Permissions Request › History', 'طلب إذونات › السابقة', False, 'History lists requests, not your total hours.', 'تعرض السابقة الطلبات، لا إجمالي ساعاتك.'),
 ('My Attendance', 'تفاصيل الحضور والإنصراف', False, 'My Attendance shows your attendance, not permission hours.', 'تعرض تفاصيل الحضور حضورك، لا ساعات الإذن.')])
QQ('permission-history', ('Your manager approved your permission request. Where do you find it now?', 'وافق مديرك على طلب الإذن. أين تجده الآن؟'), [
 ('Permissions Request › History', 'طلب إذونات › السابقة', True, 'Decided requests move to History.', 'تنتقل الطلبات المحسومة إلى السابقة.'),
 ('Permissions Request › Current', 'طلب إذونات › الحالية', False, 'Current only shows requests still waiting.', 'تعرض الحالية الطلبات المنتظِرة فقط.'),
 ('My Permissions', 'بيانات الإذونات', False, 'My Permissions shows hours used, not your requests.', 'بيانات الإذونات تعرض الساعات، لا الطلبات.')])
QQ('my-attendance', ('HR says you were short on hours last month. How do you check?', 'أخبرتك الموارد البشرية أن ساعاتك نقصت الشهر الماضي. كيف تتحقق؟'), [
 ('Open My Attendance and change the Period', 'تفتح تفاصيل الحضور والإنصراف وتغيّر الفترة', True, 'Over/Short Hours shows the gap for the Period you choose.', 'يعرض قسم ساعات أضافية / تأخير الفرق للفترة التي تختارها.'),
 ('Open GEO Attendance', 'تفتح تسجيل الحضور والإنصراف', False, 'GEO Attendance records your arrival and departure; it does not total your hours.', 'هذه الشاشة لتسجيل الدخول والخروج، لا لحساب الساعات.'),
 ('Open My Permissions', 'تفتح بيانات الإذونات', False, 'That shows permission hours only.', 'تعرض ساعات الإذن فقط.')])
QQ('geo-attendance', ('You arrive at a client site and must record your attendance from your phone. What do you tap?', 'وصلت إلى موقع عميل وعليك تسجيل حضورك من هاتفك. ماذا تضغط؟'), [
 ('GEO Attendance › In', 'تسجيل الحضور والإنصراف › دخول', True, 'In records your arrival with your location.', 'يسجّل دخول وقت وصولك مع موقعك.'),
 ('GEO Attendance › Out', 'تسجيل الحضور والإنصراف › خروج', False, 'Out is for when you leave.', 'خروج يُستخدم عند المغادرة.'),
 ('My Attendance', 'تفاصيل الحضور والإنصراف', False, 'My Attendance shows your record; it does not record attendance.', 'تعرض هذه الشاشة سجلّك، ولا تسجّل الحضور.')])
QQ('notifications', ('The bell shows a Vacation request waiting your approval. Where do you decide on it?', 'يظهر في الجرس طلب إجازة بانتظار موافقتك. أين تتخذ القرار؟'), [
 ('Leaves Approvals', 'موافقة الإجازات', True, 'Leave requests are decided in Leaves Approvals.', 'تُحسم طلبات الإجازة من موافقة الإجازات.'),
 ('Permissions Approvals', 'موافقة الإذونات', False, 'That page is for time permissions.', 'هذه الصفحة لطلبات الإذن.'),
 ('Leaves Request', 'طلب الإجازات', False, 'Leaves Request is for your own leave.', 'طلب الإجازات لإجازاتك أنت.')])
QQ('approve-permissions', ('You marked three permission requests as approved, then closed the page without saving. What happens?', 'حدّدت الموافقة على ثلاثة طلبات إذن ثم أغلقت الصفحة دون حفظ. ماذا يحدث؟'), [
 ('The requests stay waiting', 'تبقى الطلبات منتظِرة', True, 'Nothing is applied until you save.', 'لا يُطبَّق أي قرار قبل الحفظ.'),
 ('The requests are approved', 'تُعتمد الطلبات', False, 'Without saving, nothing is applied.', 'دون حفظ لا يُطبَّق شيء.'),
 ('The requests are rejected', 'تُرفض الطلبات', False, 'They are neither approved nor rejected.', 'لا تُعتمد ولا تُرفض.')])
QQ('leave-approvals', ("A team member's request is still with their first approver before it reaches you. Which tab shows it?", 'طلب أحد أفراد فريقك ما زال لدى معتمِده الأول قبل أن يصل إليك. في أي تبويب يظهر؟'), [
 ('Monitoring', 'القادمة', True, 'It shows requests waiting for an earlier approver.', 'يعرض الطلبات التي تنتظر معتمِدًا قبلك.'),
 ('Current', 'الحالية', False, 'Current shows requests waiting for you.', 'تعرض الحالية ما ينتظرك أنت.'),
 ('History', 'السابقة', False, 'History shows requests you have decided.', 'تعرض السابقة ما اتخذت فيه قرارًا.')])
QQ('tk-approvals', ('An employee forgot to clock out on 5 October and sent a request. How do you find it?', 'نسي موظف تسجيل انصرافه يوم ٥ أكتوبر وقدّم طلبًا. كيف تجده؟'), [
 ('Incomplete TK Approvals: set dates that include 5 Oct, then OK', 'موافقة القراءات الغير مكتملة: تواريخ تشمل ٥ أكتوبر، ثم موافق', True, 'The dates decide which requests load.', 'التواريخ تحدّد الطلبات التي تظهر.'),
 ('Permissions Approvals', 'موافقة الإذونات', False, 'Missing clock-ins and outs are not permissions.', 'القراءات الناقصة ليست إذنًا.'),
 ('Incomplete TK Request', 'طلب القراءات الغير مكتملة', False, 'That page is for your own missing times.', 'هذه الصفحة لقراءاتك أنت.')])
QQ('find-permissions', ("You need last month's permission decisions only. What do you change?", 'تحتاج قرارات الإذن للشهر الماضي فقط. ماذا تغيّر؟'), [
 ('The dates in the History filter', 'التواريخ في تصفية السابقة', True, 'The filter dates decide which requests show.', 'تواريخ التصفية تحدّد الطلبات الظاهرة.'),
 ('The Current tab', 'تبويب الحالية', False, 'Current shows requests still waiting.', 'تعرض الحالية ما زال ينتظر.'),
 ('Cancel', 'إلغاء', False, 'Cancel closes the filter without changes.', 'إلغاء يغلق التصفية دون تغيير.')])
QQ('team-records', ("You want to see a team member's leave record. What do you do?", 'تريد الاطلاع على سجلّ إجازات أحد أفراد فريقك. ماذا تفعل؟'), [
 ('Open My Leaves and tap their name', 'تفتح تفاصيل الإجازات وتضغط اسمه', True, 'Managers see their team in the list; your own name is first.', 'يرى المدير فريقه في القائمة، واسمه هو الأول.'),
 ('Open Leaves Approvals › History', 'تفتح موافقة الإجازات › السابقة', False, 'That only lists requests you have decided.', 'تعرض الطلبات التي حسمتها فقط.'),
 ('Open Leaves Request', 'تفتح طلب الإجازات', False, 'Leaves Request is for your own leave.', 'طلب الإجازات لإجازاتك أنت.')])

# new English dark home (clean screenshot, 12 tiles)
def T(c, r): return hs([5.5, 28.5, 51.5, 74.5][c], [26.5, 42.0, 57.5][r], 20, 14.5)
HOME = {'changes': T(0,0), 'myLeaves': T(1,0), 'leavesRequest': T(2,0), 'leavesApprovals': T(3,0), 'myPermissions': T(0,1),
        'permissionsRequest': T(1,1), 'permissionsApprovals': T(2,1), 'tkRequest': T(3,1), 'tkApprovals': T(0,2),
        'myAttendance': T(1,2), 'attTracking': T(2,2), 'geo': T(3,2)}
SETHOT = {'balance-app-01': 'myLeaves', 'leave-app-01': 'leavesRequest', 'lh-01': 'leavesRequest', 'myperm-app-01': 'myPermissions',
          'ph-01': 'permissionsRequest', 'ma-01': 'myAttendance', 'ap-01': 'permissionsApprovals'}
for t in TASKS.values():
    for s in t['steps']:
        if s['screen'] == 'home_dark' and s['id'] in SETHOT: s['hotspot'] = HOME[SETHOT[s['id']]]

# routes: data change requests belong to the manager view
MISSIONS[:] = [m for m in MISSIONS if m['id'] != 'mydata']
MISSIONS[-1]['tasks'] = ['find-permissions', 'changes-request', 'changes-approvals', 'team-records']

data = {'version': '3.5', 'helpEmail': V22['meta']['helpEmail'], 'ui': UI, 'missions': MISSIONS, 'tasks': TASKS,
        'glossary': V22.get('glossary'), 'help': V22['pages'].get('help')}
# sanity: every check has exactly one correct option; every step has a screen
for k, t in TASKS.items():
    assert t['check'] and sum(o['correct'] for o in t['check']['options']) == 1, k
    for s in t['steps']: assert s['screen'], (k, s['id'])
open(OUT, 'w').write('window.HITS=' + json.dumps(data, ensure_ascii=False, separators=(',', ':')) + ';\n')
print('tasks', len(TASKS), 'steps', sum(len(t['steps']) for t in TASKS.values()))
