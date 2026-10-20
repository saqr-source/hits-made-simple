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
  'points': '{n#نقطة}', 'tasksDone': '{done} من {total#محطة}', 'earned': '+{n#نقطة}', 'stepsMeta': '{n#خطوة} · حوالي {m#دقيقة}', 'correct': 'صحيح!'})

data = {'version': '3.1', 'helpEmail': V22['meta']['helpEmail'], 'ui': UI, 'missions': MISSIONS, 'tasks': TASKS,
        'glossary': V22.get('glossary'), 'help': V22['pages'].get('help')}
# sanity: every check has exactly one correct option; every step has a screen
for k, t in TASKS.items():
    assert t['check'] and sum(o['correct'] for o in t['check']['options']) == 1, k
    for s in t['steps']: assert s['screen'], (k, s['id'])
open(OUT, 'w').write('window.HITS=' + json.dumps(data, ensure_ascii=False, separators=(',', ':')) + ';\n')
print('tasks', len(TASKS), 'steps', sum(len(t['steps']) for t in TASKS.values()))
