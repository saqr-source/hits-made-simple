"""HITS Made Simple v4 — content builder.
Every step names its own screen per language: English steps use English-app screenshots,
Arabic steps use Arabic-app screenshots. A stop appears in a language only when it has screens in it.
Run: python3 tools/build_v4.py  (writes assets/data.js)"""
import json, os, re
import numpy as np
from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(HERE)
SCR = os.path.join(ROOT, 'assets', 'screens_v4')
BASE = json.load(open(os.path.join(HERE, 'ui_base.json')))

def hs(x, y, w, h): return {'x': x, 'y': y, 'w': w, 'h': h}
def L(en, ar): return {'en': en, 'ar': ar}

# ---------- home screens: tile hotspots (column counted from the LEFT edge of the screen) ----------
COLS = [5.4, 28.5, 51.5, 74.6]
def tile(c, r, rows): return hs(COLS[c], rows[r], 20, 14.2)
EN_EMP_HOME = 'en_emp_02'; R_EE = [26, 41.5, 56.8]
EN_MGR_HOME = 'en_mgr_17'; R_EM = [26.5, 41.8, 57, 72.5]
EN_DARK_HOME = 'en_mgr_21'; R_ED = [26.5, 41.8, 57.2]
AR_EMP_HOME = 'ar_emp_01'; R_AE = [25.5, 41, 56.5]
AR_MGR_HOME = 'ar_mgr_06'; R_AM = [26.5, 41.8, 57, 72.5]
EE = {'changesRequest': (0, 0), 'myLeaves': (1, 0), 'leavesRequest': (2, 0), 'leavesApprovals': (3, 0), 'myPermissions': (0, 1),
      'permissionsRequest': (1, 1), 'permissionsApprovals': (2, 1), 'tkRequest': (3, 1), 'tkApprovals': (0, 2), 'myAttendance': (1, 2),
      'attTracking': (2, 2), 'geo': (3, 2)}
EM = {'myProfile': (0, 0), 'changesRequest': (1, 0), 'changesApprovals': (2, 0), 'myLeaves': (3, 0), 'leavesRequest': (0, 1),
      'leavesApprovals': (1, 1), 'myPermissions': (2, 1), 'permissionsRequest': (3, 1), 'permissionsApprovals': (0, 2),
      'tkRequest': (1, 2), 'tkApprovals': (2, 2), 'myAttendance': (3, 2), 'geo': (0, 3)}
AE = {'leavesApprovals': (0, 0), 'leavesRequest': (1, 0), 'myLeaves': (2, 0), 'changesRequest': (3, 0), 'tkRequest': (0, 1),
      'permissionsApprovals': (1, 1), 'permissionsRequest': (2, 1), 'myPermissions': (3, 1), 'geo': (0, 2), 'attTracking': (1, 2),
      'myAttendance': (2, 2), 'tkApprovals': (3, 2)}
AM = {'myLeaves': (0, 0), 'changesApprovals': (1, 0), 'changesRequest': (2, 0), 'myProfile': (3, 0), 'permissionsRequest': (0, 1),
      'myPermissions': (1, 1), 'leavesApprovals': (2, 1), 'leavesRequest': (3, 1), 'myAttendance': (0, 2), 'tkApprovals': (1, 2),
      'tkRequest': (2, 2), 'permissionsApprovals': (3, 2), 'geo': (3, 3)}
def ee(k): return tile(*EE[k], R_EE)
def em(k): return tile(*EM[k], R_EM)
def ed(k): return tile(*EE[k], R_ED)
def ae(k): return tile(*AE[k], R_AE)
def am(k): return tile(*AM[k], R_AM)
BELL_EM = hs(74, 7, 8, 5.5); BELL_AM = hs(16.5, 7.5, 8, 5.5)

# common controls (percent of the phone slot)
EN_PLUS = hs(67, 87.5, 10, 7); EN_DOTS = hs(81, 87.5, 10, 7); EN_SEND = hs(67, 87.5, 10, 7)
EN_MENU_NEW = hs(57, 87.5, 37, 7); EN_MENU_BAL = hs(57, 79.8, 37, 6.5)
EN_FILTER = hs(78.5, 85, 13, 8.5); TICK = hs(84, 68.5, 11.5, 8)
AR_PLUS = hs(22, 87.5, 10, 7); AR_DOTS = hs(8, 87.5, 10, 7); AR_SEND = hs(22, 87.5, 10, 7)
AR_MENU_NEW = hs(6, 87.5, 38, 7); AR_FILTER = hs(5.5, 85, 13, 8.5)
TABS3 = hs(4, 11.5, 92, 5); TABS2 = hs(8, 11.5, 84, 5)
EN_TAB_CUR2 = hs(8, 11.5, 34, 5); EN_TAB_HIS2 = hs(56, 11.5, 34, 5)
AR_TAB_CUR2 = hs(58, 11.5, 34, 5); AR_TAB_HIS2 = hs(10, 11.5, 34, 5)
EN_TAB_HIS3 = hs(71, 11.5, 25, 5); AR_TAB_HIS3 = hs(4, 11.5, 25, 5); AR_TAB_CUR3 = hs(70, 11.5, 26, 5)
FIRST_ROW = hs(2, 19.3, 96, 10.5)

def V(screen, hot, h1, h2, text, helper=None, type_=None, verify=None):
    d = {'screen': screen, 'hot': hot, 'headline': [h1, h2], 'text': text}
    if helper: d['helper'] = helper
    if type_: d['type'] = type_
    if verify: d['verify'] = verify
    return d
def S(i, en=None, ar=None): return {'id': i, 'en': en, 'ar': ar}
def Q(q, opts):
    return {'q': {'en': q[0], 'ar': q[1]}, 'options': [{'text': {'en': o[0], 'ar': o[1]}, 'correct': o[2], 'why': {'en': o[3], 'ar': o[4]}} for o in opts]}
def TIP(after, en, ar): return {'after': after, 'text': {'en': en, 'ar': ar}}

T = {}
def task(tid, icon, name, situation, title, purpose, outcome, path, steps, check, tips=(), helpCard=False):
    T[tid] = {'id': tid, 'icon': icon, 'name': name, 'situation': situation, 'title': title, 'purpose': purpose,
              'outcome': outcome, 'path': path, 'steps': steps, 'check': check, 'tips': list(tips), 'helpCard': helpCard}

# =================================== GET STARTED ===================================
UN_EN = hs(6, 56.2, 70, 4.2); PW_EN = hs(6, 65.6, 70, 4.2)
UN_AR = hs(8, 60.2, 86, 4.6); PW_AR = hs(18, 70, 76, 4.6)
task('signin', 'log-in', L('Sign in to HITS', 'تسجيل الدخول إلى HITS'),
     L('How do I sign in?', 'كيف أسجّل الدخول؟'), L(['Sign in', 'to HITS.'], ['سجّل الدخول', 'إلى HITS.']),
     L('Opens HITS Easy Go with your work email (Office 365) or your Work ID.', 'يفتح تطبيق HITS ببريد العمل (أوفيس 365) أو بالرقم الوظيفي.'),
     L('You can sign in to HITS Easy Go.', 'تستطيع تسجيل الدخول إلى تطبيق HITS.'), L('Login screen', 'شاشة الدخول'), [
  S('si-1', V('en_login', None, 'Open', 'HITS Easy Go.', 'Open the HITS Easy Go app on your phone.'),
            V('ar_emp_30', None, 'افتح', 'تطبيق HITS.', 'افتح تطبيق HITS على هاتفك.', 'تظهر الشاشة هنا بالمظهر الداكن، والخطوات نفسها في المظهر الفاتح.')),
  S('si-2', V('en_login', hs(51, 73.2, 43.5, 5.2), 'Have a work email?', 'Tap OFFICE 365.', 'If you have a work email, tap OFFICE 365, then sign in with your work email and its password.',
              'No work email? Use your Work ID — the next steps show you how.'),
            V('ar_emp_30', hs(5, 78.4, 43, 5.8), 'لديك بريد عمل؟', 'اضغط أوفيس 365.', 'إذا كان لديك بريد إلكتروني للعمل، فاضغط زر أوفيس 365، ثم ادخل ببريد العمل وكلمة مروره.',
              'ليس لديك بريد عمل؟ ادخل برقمك الوظيفي، وتوضّح لك الخطوات التالية الطريقة.')),
  S('si-3', V('en_login', hs(4.5, 55, 90, 6.6), 'Enter your', 'Work ID.', 'Type your Work ID in the Username field.',
              '12345 is only an example. Your Work ID and password come from your direct manager.', [{'box': UN_EN, 'text': '12345', 'anim': True}]),
            V('ar_emp_30', hs(5, 59, 93.5, 7), 'أدخِل', 'رقمك الوظيفي.', 'اكتب رقمك الوظيفي في خانة اسم المستخدم.',
              '١٢٣٤٥ مجرد مثال. يسلّمك مديرك المباشر الرقم الوظيفي وكلمة المرور.', [{'box': UN_AR, 'text': '12345', 'anim': True, 'align': 'right'}])),
  S('si-4', V('en_login', hs(4.5, 64.4, 90, 6.6), 'Then your', 'password.', 'Type your password in the Password field.', None,
              [{'box': UN_EN, 'text': '12345'}, {'box': PW_EN, 'text': '••••••••', 'anim': True, 'dots': True}]),
            V('ar_emp_30', hs(5, 68.6, 93.5, 7), 'ثم', 'كلمة السر.', 'اكتب كلمة المرور في خانة كلمة السر.', None,
              [{'box': UN_AR, 'text': '12345', 'align': 'right'}, {'box': PW_AR, 'text': '••••••••', 'anim': True, 'dots': True, 'align': 'right'}])),
  S('si-5', V('en_login', hs(4.5, 73.2, 43.5, 5.2), 'Tap', 'LOGIN.', 'Tap LOGIN.', None,
              [{'box': UN_EN, 'text': '12345'}, {'box': PW_EN, 'text': '••••••••', 'dots': True}]),
            V('ar_emp_30', hs(51, 78.4, 43.5, 5.8), 'اضغط', 'دخول.', 'اضغط زر دخول.', None,
              [{'box': UN_AR, 'text': '12345', 'align': 'right'}, {'box': PW_AR, 'text': '••••••••', 'dots': True, 'align': 'right'}])),
  S('si-6', V(EN_EMP_HOME, None, "You're", 'in.', 'Your HITS services are on the home page.'),
            V(AR_EMP_HOME, None, 'تمّ', 'الدخول.', 'ستجد خدماتك كلها في الصفحة الرئيسية.')),
 ], Q(('A new colleague has no work email. How does she sign in?', 'زميلة جديدة ليس لديها بريد عمل. كيف تسجّل الدخول؟'), [
  ('Work ID in Username, her password, then LOGIN', 'رقمها الوظيفي في اسم المستخدم، ثم كلمة السر، ثم دخول', True, 'Without a work email, you sign in with your Work ID.', 'من ليس لديه بريد عمل يدخل برقمه الوظيفي.'),
  ('Tap OFFICE 365 and type her Work ID', 'تضغط أوفيس 365 وتكتب رقمها الوظيفي', False, 'OFFICE 365 needs a work email and its password.', 'أوفيس 365 يحتاج بريد عمل وكلمة مروره.'),
  ('Tap Register/Reactivate User every time', 'تضغط تسجيل / إعادة تفعيل المستخدم كل مرة', False, 'That link is not for everyday sign-in.', 'هذا الرابط ليس للدخول اليومي.'),
  ('Ask IT for an Office 365 password', 'تطلب من الدعم الفني كلمة مرور أوفيس 365', False, 'She has no work email, so she uses her Work ID.', 'ليس لديها بريد عمل، فتستخدم رقمها الوظيفي.')]),
 tips=[TIP('si-4', 'Never share your password, including in screenshots or support messages.', 'لا تشارك كلمة المرور مع أحد، ولا تُظهرها في لقطات الشاشة أو رسائل الدعم.')], helpCard=True)

task('forgot', 'lock', L('Forgot your password?', 'نسيت كلمة السر؟'), L('I forgot my password', 'نسيت كلمة السر'),
     L(['Forgot your', 'password?'], ['نسيت', 'كلمة السر؟']),
     L('Starts password recovery from the login screen.', 'يبدأ استرجاع كلمة السر من شاشة الدخول.'),
     L('You can start recovering your HITS password.', 'تستطيع بدء استرجاع كلمة سر HITS.'), L('Login screen', 'شاشة الدخول'), [
  S('fp-1', V('en_login', hs(62, 79.3, 33, 2.8), 'Tap', 'Forgot my password?', 'On the login screen, tap Forgot my password?',
              'Next, the app asks for your Username and Company Email, then you tap SEND.', verify='screen'),
            V('ar_emp_30', hs(5, 85, 30.5, 2.8), 'اضغط', 'هل نسيت كلمة السر؟', 'في شاشة الدخول، اضغط رابط هل نسيت كلمة السر؟')),
  S('fp-2', None, V('ar_emp_33', hs(8.5, 43, 85, 19.5), 'أدخِل', 'بياناتك.', 'اكتب اسم المستخدم، ثم البريد الإلكتروني للشركة.')),
  S('fp-3', None, V('ar_emp_33', hs(8.5, 66, 85, 6.4), 'اضغط', 'ارسال.', 'اضغط ارسال، ثم اتبع التعليمات التي تصلك.',
                    'تدخل ببريد الشركة؟ لكلمة مرور البريد، تواصل مع الدعم الفني.')),
 ], Q(('You forgot your HITS password. What does the recovery screen ask for?', 'نسيت كلمة سر HITS. ماذا تطلب منك شاشة الاسترجاع؟'), [
  ('Your username and company email', 'اسم المستخدم والبريد الإلكتروني للشركة', True, 'Those two details start the recovery.', 'هاتان المعلومتان تبدآن الاسترجاع.'),
  ('Your old password and a new one', 'كلمة السر القديمة وكلمة جديدة', False, "You don't type a password here — that's what you are recovering.", 'لا تكتب كلمة سر هنا، فهي ما تحاول استرجاعه.'),
  ('Your phone number', 'رقم هاتفك', False, "The screen doesn't ask for it.", 'الشاشة لا تطلب رقم الهاتف.'),
  ("Your manager's Work ID", 'الرقم الوظيفي لمديرك', False, 'You only enter your own details.', 'تكتب بياناتك أنت فقط.')]),
 tips=[TIP('fp-1', 'Your direct manager provides your HITS username and password.', 'يسلّمك مديرك المباشر اسم المستخدم وكلمة السر.')], helpCard=True)

task('settings', 'info', L('Change the theme or language', 'تغيير المظهر أو اللغة'), L('The app looks different from this guide', 'التطبيق يبدو مختلفًا عن هذا الدليل'),
     L(['Theme and', 'language.'], ['المظهر', 'واللغة.']),
     L('Changes how the app looks (light or dark) and its language.', 'يغيّر شكل التطبيق (فاتح أو داكن) ولغته.'),
     L('You can set the app to match this guide.', 'تستطيع ضبط التطبيق ليطابق هذا الدليل.'), L('Login screen › ⚙', 'شاشة الدخول › ⚙'), [
  S('st-1', V('en_login', hs(86, 0.5, 9, 5.5), 'Tap the', 'gear icon.', 'On the login screen, tap the gear icon at the top.'),
            V('ar_emp_30', hs(4.5, 5.5, 9, 6), 'اضغط', 'أيقونة الترس.', 'في شاشة الدخول، اضغط أيقونة الترس في الأعلى.')),
  S('st-2', V('en_emp_01', hs(7.5, 34, 85, 18.5), 'Choose a', 'Theme.', 'Under Theme, choose Auto, Light or Dark.', 'This guide mostly shows the Light theme.'),
            V('ar_mgr_20', hs(8, 36, 84, 19.5), 'اختر', 'المظهر.', 'في قسم المظهر، اختر تلقائي أو فاتح أو داكن.', 'يعرض هذا الدليل غالبًا المظهر الفاتح.')),
  S('st-3', V('en_emp_01', hs(7.5, 25, 85, 8), 'Choose a', 'Language.', 'Under Language, choose English to match this guide.'),
            V('ar_emp_31', hs(8, 26, 84, 8.5), 'اختر', 'اللغة.', 'في خانة اللغة، اختر العربية ليطابق تطبيقك هذا الدليل.')),
 ], Q(("Your app's buttons are in a different language from this guide. What do you change?", 'أزرار تطبيقك بلغة غير لغة هذا الدليل. ماذا تغيّر؟'), [
  ('Language, in Settings', 'اللغة، من الإعدادات', True, 'Choose the same language as the guide.', 'اختر لغة الدليل نفسها.'),
  ('Theme', 'المظهر', False, 'Theme only changes light or dark colours.', 'المظهر يغيّر الألوان الفاتحة أو الداكنة فقط.'),
  ('Tenant ID', 'رقم الجهة', False, 'Leave Tenant ID as it is.', 'اترك رقم الجهة كما هو.'),
  ('Log out and in again', 'تسجيل الخروج ثم الدخول', False, 'That does not change the language.', 'هذا لا يغيّر اللغة.')]),
 tips=[TIP('st-2', 'Leave Tenant ID as it is.', 'اترك رقم الجهة كما هو، ولا تغيّره.')])

# =================================== EMPLOYEE · TIME OFF ===================================
task('leave-balance', 'calendar-days', L('Check your leave balance', 'معرفة رصيد إجازاتك'), L('How many leave days do I have left?', 'كم يومًا تبقّى من إجازاتي؟'),
     L(['Check your', 'leave balance.'], ['اعرف', 'رصيد إجازاتك.']), L('Shows the days you have and the days you have taken.', 'يعرض أيامك المتاحة والأيام التي أخذتها.'),
     L('You can find your leave balance and the days you have taken.', 'تستطيع معرفة رصيد إجازاتك والأيام التي أخذتها.'), L('Home › My Leaves', 'الرئيسية › تفاصيل الإجازات'), [
  S('lb-1', V(EN_EMP_HOME, ee('myLeaves'), 'Tap', 'My Leaves.', 'On the home page, tap My Leaves.'),
            V(AR_EMP_HOME, ae('myLeaves'), 'اضغط', 'تفاصيل الإجازات.', 'من الصفحة الرئيسية، اضغط تفاصيل الإجازات.')),
  S('lb-2', V('en_emp_09', hs(2, 15, 96, 38.5), 'Read your', 'balance.', 'Leaves Balance shows Annual, Holiday and Day Off, with what is left and what you have taken.', 'Period shows the time range — here, Current Year.'),
            V('ar_emp_07', hs(2, 15, 96, 39), 'اقرأ', 'رصيدك.', 'يعرض رصيد الأجازات رصيدك من سنوي وأعياد وعطلات، وما أخذته منها.', 'تحدّد الفترة المدة المعروضة، وهي هنا السنة الحالية.')),
  S('lb-3', V('en_emp_09', hs(2, 55, 96, 17.5), 'See the days', 'you have taken.', 'No. of Days Taken lists the days used for each leave type this year (YTD).'),
            V('ar_emp_07', hs(2, 55, 96, 18.5), 'اعرف الأيام', 'التي أخذتها.', 'يعرض عدد الأيام المأخوذة ما استخدمته من كل نوع إجازة منذ بداية السنة.')),
  S('lb-4', V('en_emp_10', hs(2, 49, 96, 44), 'See your days', 'on a chart.', 'Vacatin Days Count shows the same days as a chart, by leave type.'),
            V('ar_emp_08', hs(2, 42, 96, 52), 'شاهِد أيامك', 'في رسم بياني.', 'يعرض عدد ايام الأجازات الأيام نفسها في رسم بياني حسب نوع الإجازة.')),
 ], Q(('You want to know how many annual leave days you have left this year. Where do you look?', 'تريد معرفة أيام إجازتك السنوية المتبقية هذا العام. أين تبحث؟'), [
  ('My Leaves › Leaves Balance', 'تفاصيل الإجازات › رصيد الأجازات', True, 'Leaves Balance shows what you have left and what you have taken.', 'يعرض رصيد الأجازات ما تبقّى لك وما أخذته.'),
  ('Leaves Request › History', 'طلب الإجازات › السابقة', False, 'History lists past requests, not your balance.', 'تعرض السابقة طلباتك القديمة، لا رصيدك.'),
  ('My Permissions', 'بيانات الإذونات', False, 'That shows permission hours, not leave days.', 'تعرض ساعات الإذن، لا أيام الإجازة.'),
  ('Leaves Approvals', 'موافقة الإجازات', False, "That page is for approving other people's requests.", 'هذه الصفحة لاعتماد طلبات الآخرين.')]))

task('leave-menu', 'calendar-days', L('Check your balance before you apply', 'معرفة رصيدك قبل الطلب'), L('Do I have enough days before I apply?', 'هل لديّ أيام كافية قبل أن أطلب؟'),
     L(['Check your balance', 'before you apply.'], ['اعرف رصيدك', 'قبل أن تطلب.']), L('Opens your balance from the Leaves Request menu.', 'يفتح رصيدك من قائمة طلب الإجازات.'),
     L('You can check your balance from Leaves Request in seconds.', 'تستطيع معرفة رصيدك من طلب الإجازات في ثوانٍ.'), L('Home › Leaves Request › ⋮ › Balance', 'الرئيسية › طلب الإجازات › ⋮ › رصيد الاجازات'), [
  S('lm-1', V(EN_EMP_HOME, ee('leavesRequest'), 'Tap', 'Leaves Request.', 'On the home page, tap Leaves Request.'),
            V(AR_EMP_HOME, ae('leavesRequest'), 'اضغط', 'طلب الإجازات.', 'من الصفحة الرئيسية، اضغط طلب الإجازات.')),
  S('lm-2', V('en_emp_12', EN_DOTS, 'Open the', 'menu.', 'Tap ⋮ at the bottom of the screen.'),
            V('ar_emp_09', AR_DOTS, 'افتح', 'القائمة.', 'اضغط ⋮ أسفل الشاشة.')),
  S('lm-3', V('en_emp_13', EN_MENU_BAL, 'Tap', 'Balance.', 'The menu shows Filter, Balance and New. Tap Balance.'),
            V('ar_emp_13', hs(6, 80, 40, 6.5), 'اضغط', 'رصيد الاجازات.', 'تعرض القائمة تصفية ورصيد الاجازات وجديد. اضغط رصيد الاجازات.')),
  S('lm-4', V('en_emp_14', hs(2, 13.5, 96, 26), 'Read your', 'balance.', 'Each period shows Prev.Bal, Due, Taken and Balance for Annual, Holiday and Days Off.'),
            V('ar_emp_14', hs(2, 13.5, 96, 26), 'اقرأ', 'رصيدك.', 'تعرض كل فترة الرصيد السابق والمستحق والمأخوذ والرصيد لسنوي وعطلات وأسبوعية.')),
 ], Q(("You're in Leaves Request, about to apply. How do you check your balance first?", 'أنت في طلب الإجازات وستقدّم طلبًا. كيف تعرف رصيدك أولًا؟'), [
  ('Tap ⋮, then Balance', 'تضغط ⋮ ثم رصيد الاجازات', True, 'Balance in the ⋮ menu shows your balance for each period.', 'رصيد الاجازات في قائمة ⋮ يعرض رصيدك لكل فترة.'),
  ('Tap +, then Leave', 'تضغط + ثم الأجازة', False, '+ starts a new request; it does not show your balance.', '+ يبدأ طلبًا جديدًا، ولا يعرض الرصيد.'),
  ('Open History', 'تفتح السابقة', False, 'History lists past requests.', 'تعرض السابقة طلباتك القديمة.'),
  ('Tap ⋮, then Filter', 'تضغط ⋮ ثم تصفية', False, 'Filter narrows your request list.', 'تصفية تحصر قائمة طلباتك.')]))

task('leave-request', 'calendar-days', L('Submit a leave request', 'تقديم طلب إجازة'), L('I want to take a day off', 'أريد أخذ يوم إجازة'),
     L(['Submit a', 'leave request.'], ['قدِّم', 'طلب إجازة.']), L('Sends your leave request to your approver.', 'يرسل طلب إجازتك إلى المعتمِد.'),
     L('You can send a leave request for approval.', 'تستطيع إرسال طلب إجازة للاعتماد.'), L('Home › Leaves Request › +', 'الرئيسية › طلب الإجازات › +'), [
  S('lr-1', V(EN_EMP_HOME, ee('leavesRequest'), 'Tap', 'Leaves Request.', 'On the home page, tap Leaves Request.'),
            V(AR_EMP_HOME, ae('leavesRequest'), 'اضغط', 'طلب الإجازات.', 'من الصفحة الرئيسية، اضغط طلب الإجازات.')),
  S('lr-2', V('en_emp_12', EN_PLUS, 'Start a', 'new request.', 'Tap + at the bottom of the screen.', 'Current shows requests waiting for a decision; History shows past ones.'),
            V('ar_emp_09', AR_PLUS, 'ابدأ', 'طلبًا جديدًا.', 'اضغط + أسفل الشاشة.', 'تعرض الحالية الطلبات التي تنتظر قرارًا، وتعرض السابقة طلباتك القديمة.')),
  S('lr-3', V('en_emp_15', hs(31, 17.8, 66, 4.6), 'Open the', 'Leave list.', 'Tap the Leave field.'),
            V('ar_emp_10', hs(14, 17.8, 84, 4.6), 'افتح قائمة', 'الأجازة.', 'اضغط خانة الأجازة.')),
  S('lr-4', V('en_emp_17', hs(1, 85, 98, 6), 'Choose your', 'leave type.', 'Scroll to the type you need — for example Annual Leave or Annual 1/2 Day — then tap ✓.'),
            V('ar_emp_11', hs(40, 8.6, 57, 5), 'اختر', 'نوع الإجازة.', 'اختر النوع المناسب، مثل 1/2 يوم سنوي أو اجازة سنوي.')),
  S('lr-5', V('en_emp_15', hs(2, 22.3, 64, 8.8), 'Set your', 'dates.', 'Set the From and To dates.'),
            V('ar_emp_10', hs(14, 22.3, 84, 9), 'حدِّد', 'التواريخ.', 'حدِّد تاريخ البداية في من وتاريخ النهاية في إلى.')),
  S('lr-6', V('en_emp_15', hs(2, 34.5, 96, 40), 'Add your', 'contact details.', 'Under Other Information, add how to reach you while you are away.'),
            V('ar_emp_10', hs(2, 35, 96, 40), 'أضِف', 'بيانات التواصل.', 'في معلومات أخرى، أضِف طريقة التواصل معك أثناء غيابك.')),
  S('lr-7', V('en_emp_15', EN_SEND, 'Tap', 'send.', 'Tap the send button to submit your request for approval.'),
            V('ar_emp_12', hs(6, 87.5, 32, 7), 'اضغط', 'ارسال.', 'اضغط زر الإرسال، أو افتح ⋮ واختر ارسال، لتقديم الطلب للاعتماد.', 'الدورة المستندية تعرض من سيعتمد طلبك.')),
  S('lr-8', V('en_emp_23', hs(2, 13.5, 96, 14), 'See who', 'approves.', 'The workflow shows who approves your request — here, your 1st Line Manager.'), None),
 ], Q(('You need half a day off next Sunday. What do you choose in the Leave field?', 'تحتاج نصف يوم إجازة الأحد القادم. ماذا تختار في خانة الأجازة؟'), [
  ('Annual 1/2 Day', '1/2 يوم سنوي', True, 'The half-day type takes half a day from your annual balance.', 'نوع نصف اليوم يخصم نصف يوم من رصيدك السنوي.'),
  ('Annual Leave, with the same From and To date', 'اجازة سنوي بتاريخ واحد في من وإلى', False, 'That books a full day, not half.', 'هذا يحجز يومًا كاملًا، لا نصف يوم.'),
  ('Annual 1/4 Day', '1/4 يوم سنوي', False, 'A quarter day is shorter than you need.', 'ربع اليوم أقل مما تحتاج.'),
  ('Annual Leave, and write "half day" in Other info', 'اجازة سنوي مع كتابة نصف يوم في بيانات اخرى', False, 'Other info does not change the leave type.', 'بيانات اخرى لا تغيّر نوع الإجازة.')]),
 tips=[TIP('lr-4', 'Choosing Mission? You must fill in the mission destination, or the request will not send.', 'اخترت مأمورية؟ يجب كتابة جهة المأمورية، وإلا لن يُرسَل الطلب.')])

task('leave-history', 'history', L('Follow up your leave requests', 'متابعة طلبات إجازتك'), L('Has my leave been decided?', 'هل اتُّخذ قرار في إجازتي؟'),
     L(['Follow up your', 'leave requests.'], ['تابِع', 'طلبات إجازتك.']), L('Finds your waiting and past leave requests.', 'يعرض طلبات إجازتك المنتظِرة والسابقة.'),
     L('You can find any leave request you have sent.', 'تستطيع العثور على أي طلب إجازة قدّمته.'), L('Home › Leaves Request', 'الرئيسية › طلب الإجازات'), [
  S('lh-1', V(EN_EMP_HOME, ee('leavesRequest'), 'Tap', 'Leaves Request.', 'On the home page, tap Leaves Request.'),
            V(AR_EMP_HOME, ae('leavesRequest'), 'اضغط', 'طلب الإجازات.', 'من الصفحة الرئيسية، اضغط طلب الإجازات.')),
  S('lh-2', V('en_emp_11', TABS2, 'Choose', 'Current or History.', 'Current shows requests waiting for a decision. History shows past requests.'),
            V('ar_emp_09', TABS2, 'اختر', 'الحالية أو السابقة.', 'تعرض الحالية الطلبات التي تنتظر قرارًا، وتعرض السابقة طلباتك القديمة.')),
  S('lh-3', V('en_emp_11', FIRST_ROW, 'Read your', 'request.', 'Each request shows the leave type, the From and To dates, and the number of days.'),
            V('ar_emp_09', FIRST_ROW, 'اقرأ', 'الطلب.', 'يعرض كل طلب نوع الإجازة، وتاريخَي من وإلى، وعدد الأيام.')),
 ], Q(("You sent a leave request yesterday and your manager hasn't replied. Where is it?", 'قدّمت طلب إجازة أمس ولم يردّ مديرك بعد. أين تجده؟'), [
  ('Leaves Request › Current', 'طلب الإجازات › الحالية', True, 'Current shows requests still waiting for a decision.', 'تعرض الحالية الطلبات التي ما زالت تنتظر قرارًا.'),
  ('Leaves Request › History', 'طلب الإجازات › السابقة', False, 'A request moves to History after a decision.', 'ينتقل الطلب إلى السابقة بعد اتخاذ القرار.'),
  ('My Leaves', 'تفاصيل الإجازات', False, 'My Leaves shows your balance, not your requests.', 'تفاصيل الإجازات تعرض رصيدك، لا طلباتك.'),
  ('Notifications', 'الإشعارات', False, 'Notifications are for requests waiting for you to approve.', 'الإشعارات للطلبات التي تنتظر اعتمادك أنت.')]))

# =================================== EMPLOYEE · TIME & ATTENDANCE ===================================
task('my-permissions', 'clock', L('Check your permission hours', 'معرفة ساعات الإذن'), L('How many permission hours have I used?', 'كم ساعة إذن استخدمت؟'),
     L(['Check your', 'permission hours.'], ['اعرف', 'ساعات الإذن.']), L('Shows the permission hours and count you have used.', 'يعرض ساعات الإذن وعدد الإذونات التي استخدمتها.'),
     L('You can check the permission hours you have used.', 'تستطيع معرفة ساعات الإذن التي استخدمتها.'), L('Home › My Permissions', 'الرئيسية › بيانات الإذونات'), [
  S('mp-1', V(EN_EMP_HOME, ee('myPermissions'), 'Tap', 'My Permissions.', 'On the home page, tap My Permissions.'),
            V(AR_EMP_HOME, ae('myPermissions'), 'اضغط', 'بيانات الإذونات.', 'من الصفحة الرئيسية، اضغط بيانات الإذونات.')),
  S('mp-2', V('en_emp_27', hs(2, 13.5, 96, 55), 'Read your', 'hours.', 'Permission Hours shows the hours you have used in the Period; Permission Count shows how many times.'),
            V('ar_emp_17', hs(2, 14, 96, 54), 'اقرأ', 'ساعاتك.', 'يعرض ساعات الإذن ما استخدمته خلال الفترة، ويعرض عدد الإذونات كم مرة استأذنت.')),
 ], Q(('Do you still have personal permission hours this month? Where do you check?', 'هل بقيت لك ساعات إذن هذا الشهر؟ أين تتحقق؟'), [
  ('My Permissions › Permission Hours', 'بيانات الإذونات › ساعات الإذن', True, 'It shows the hours you have used this period.', 'يعرض ما استخدمته خلال الفترة.'),
  ('Permissions Request › History', 'طلب إذونات › السابقة', False, 'History lists requests, not your total hours.', 'تعرض السابقة الطلبات، لا إجمالي ساعاتك.'),
  ('My Attendance', 'تفاصيل الحضور والإنصراف', False, 'That shows your attendance.', 'تعرض حضورك، لا ساعات الإذن.'),
  ('Permissions Approvals', 'موافقة الإذونات', False, "That page is for approving others' requests.", 'هذه الصفحة لاعتماد طلبات الآخرين.')]),
 tips=[TIP('mp-2', 'Personal late permission is capped at 2 hours a month. Above that, HITS blocks the request.', 'إذن التأخير الشخصي حدّه ساعتان في الشهر، وبعدها يرفض التطبيق الطلب.')])

task('perm-request', 'clock', L('Request a time permission', 'طلب إذن'), L("I'll be late or leave early", 'سأتأخر أو سأخرج مبكرًا'),
     L(['Request a', 'time permission.'], ['اطلب', 'إذنًا.']), L('Sends a late-in, early-out or mission permission to your approver.', 'يرسل طلب إذن تأخير أو انصراف أو مأمورية إلى المعتمِد.'),
     L('You can send a time permission for approval.', 'تستطيع إرسال طلب إذن للاعتماد.'), L('Home › Permissions Request › +', 'الرئيسية › طلب إذونات › +'), [
  S('pr-1', V(EN_EMP_HOME, ee('permissionsRequest'), 'Tap', 'Permissions Request.', 'On the home page, tap Permissions Request.'),
            V(AR_EMP_HOME, ae('permissionsRequest'), 'اضغط', 'طلب إذونات.', 'من الصفحة الرئيسية، اضغط طلب إذونات.')),
  S('pr-2', V('en_emp_29', EN_MENU_NEW, 'Start a', 'new request.', 'Tap +, or open ⋮ and tap New.'),
            V('ar_emp_19', AR_PLUS, 'ابدأ', 'طلبًا جديدًا.', 'اضغط + أسفل الشاشة.')),
  S('pr-3', V('en_emp_30', hs(31, 30.8, 66, 4.6), 'Open the', 'Permission list.', 'Tap the Permission field.'),
            V('ar_emp_20', hs(14, 30.8, 84, 4.6), 'افتح قائمة', 'الإذن.', 'اضغط خانة الإذن.')),
  S('pr-4', V('en_emp_33', hs(1, 85, 98, 6), 'Choose the', 'permission type.', 'Choose the type — for example Personal Permission Short [Late In] — then tap ✓.'),
            V('ar_emp_21', hs(40, 15, 57, 5), 'اختر', 'نوع الإذن.', 'اختر الإذن المناسب، مثل اذن شخصي - حضور متأخر.')),
  S('pr-5', V('en_emp_31', hs(2, 53, 96, 8), 'Mission?', 'Add the location.', 'A mission permission adds Mission Location under My Form. It is required.', 'Without the mission location, the request will not send.'),
            V('ar_mgr_04', hs(2, 56, 96, 6.5), 'مأمورية؟', 'اكتب الجهة.', 'عند اختيار اذن مأمورية تظهر خانة جهة المأمورية، وهي إلزامية.', 'دون جهة المأمورية لن يُرسَل الطلب.')),
  S('pr-6', V('en_emp_30', hs(2, 35.8, 96, 9.6), 'Set the', 'time.', 'Set the date and time in From and To.', 'Use 24-hour time: 13:00 means 1 PM.'),
            V('ar_emp_20', hs(14, 35.8, 84, 9.4), 'حدِّد', 'الوقت.', 'حدِّد التاريخ والوقت في من وإلى.', 'اكتب الوقت بنظام ٢٤ ساعة؛ 13:00 تعني الواحدة ظهرًا.')),
  S('pr-7', V('en_emp_30', hs(83.5, 69.5, 13, 6.5), 'Confirm,', 'then send.', 'Tap ✓ to confirm your choice, then tap the send button at the bottom to submit the request.', verify='screen'),
            V('ar_mgr_02', hs(6, 88, 32, 7), 'اضغط', 'ارسال.', 'اضغط زر الإرسال، أو افتح ⋮ واختر ارسال.', 'الدورة المستندية تعرض من سيعتمد طلبك.')),
 ], Q(('You chose a mission permission. What must you fill in before sending?', 'اخترت إذن مأمورية. ما الخانة التي يجب ملؤها قبل الإرسال؟'), [
  ('Mission Location', 'جهة المأمورية', True, 'The mission location is required for mission permissions.', 'جهة المأمورية إلزامية في طلبات المأمورية.'),
  ('Other Info.', 'معلومات أخرى', False, 'Other Info. is optional.', 'معلومات أخرى اختيارية.'),
  ("Your manager's name", 'اسم مديرك', False, 'The workflow finds your approver for you.', 'الدورة المستندية تحدّد المعتمِد تلقائيًا.'),
  ('Nothing — just send', 'لا شيء، أرسل مباشرة', False, 'Without the location, HITS will not send it.', 'دون جهة المأمورية لن يُرسَل الطلب.')]),
 tips=[TIP('pr-4', 'Personal late permission is capped at 2 hours a month.', 'إذن التأخير الشخصي حدّه ساعتان في الشهر.')])

task('perm-history', 'history', L('Follow up your permission requests', 'متابعة طلبات الإذن'), L('Where is my permission request?', 'أين طلب الإذن الخاص بي؟'),
     L(['Follow up your', 'permission requests.'], ['تابِع', 'طلبات الإذن.']), L('Finds your waiting and past permission requests.', 'يعرض طلبات الإذن المنتظِرة والسابقة.'),
     L('You can find any permission request you have sent.', 'تستطيع العثور على أي طلب إذن قدّمته.'), L('Home › Permissions Request', 'الرئيسية › طلب إذونات'), [
  S('ph-1', V(EN_EMP_HOME, ee('permissionsRequest'), 'Tap', 'Permissions Request.', 'On the home page, tap Permissions Request.'),
            V(AR_EMP_HOME, ae('permissionsRequest'), 'اضغط', 'طلب إذونات.', 'من الصفحة الرئيسية، اضغط طلب إذونات.')),
  S('ph-2', V('en_emp_28', TABS2, 'Choose', 'Current or History.', 'Current shows requests waiting for a decision. History shows decided ones.'),
            V('ar_emp_19', TABS2, 'اختر', 'الحالية أو السابقة.', 'تعرض الحالية الطلبات التي تنتظر قرارًا، وتعرض السابقة ما حُسم منها.')),
  S('ph-3', V('en_emp_29', hs(64, 81.5, 31, 5.5), 'Narrow', 'the list.', 'Open ⋮ and tap Filter to show requests from specific dates.'), None),
 ], Q(('Your manager approved your permission request. Where do you find it now?', 'وافق مديرك على طلب الإذن. أين تجده الآن؟'), [
  ('Permissions Request › History', 'طلب إذونات › السابقة', True, 'Decided requests move to History.', 'تنتقل الطلبات المحسومة إلى السابقة.'),
  ('Permissions Request › Current', 'طلب إذونات › الحالية', False, 'Current only shows requests still waiting.', 'تعرض الحالية المنتظِرة فقط.'),
  ('My Permissions', 'بيانات الإذونات', False, 'That shows hours used, not requests.', 'تعرض الساعات، لا الطلبات.'),
  ('Notifications', 'الإشعارات', False, 'Notifications show requests waiting for you to approve.', 'الإشعارات للطلبات التي تنتظر اعتمادك.')]))

task('tk-request', 'hourglass', L('Fix a missing clock-in or out', 'استكمال قراءة حضور ناقصة'), L('I forgot to clock in or out', 'نسيت تسجيل الحضور أو الانصراف'),
     L(['Fix a missing', 'time record.'], ['استكمِل', 'قراءة ناقصة.']), L('Sends a request to add a missing clock-in or clock-out.', 'يرسل طلبًا لإضافة قراءة حضور أو انصراف ناقصة.'),
     L('You can request a missing time record.', 'تستطيع طلب استكمال قراءة ناقصة.'), L('Home › Incomplete TK Request › +', 'الرئيسية › طلب القراءات الغير مكتملة › +'), [
  S('tr-1', V(EN_EMP_HOME, ee('tkRequest'), 'Tap', 'Incomplete TK Request.', 'On the home page, tap Incomplete TK Request.'),
            V(AR_EMP_HOME, ae('tkRequest'), 'اضغط', 'طلب القراءات الغير مكتملة.', 'من الصفحة الرئيسية، اضغط طلب القراءات الغير مكتملة.')),
  S('tr-2', V('en_emp_39', EN_MENU_NEW, 'Start a', 'new request.', 'Tap +, or open ⋮ and tap New.'),
            V('ar_emp_24', AR_PLUS, 'ابدأ', 'طلبًا جديدًا.', 'اضغط + أسفل الشاشة.', verify='screen')),
  S('tr-3', V('en_emp_40', hs(3, 16.5, 94, 5.5), 'Choose the', 'Entry Date.', 'Tap Entry Date.'), None),
  S('tr-4', V('en_emp_41', hs(1, 84, 98, 12), 'Pick the day', 'with a missing time.', 'Choose All, or the day with the missing reading, then tap ✓.'), None),
  S('tr-5', V('en_emp_40', EN_SEND, 'Add the time,', 'then send.', 'Add the missing time in 24-hour format, then tap send.', 'Attach a supporting document if you have one.', verify='confirm'), None),
 ], Q(('You forgot to clock out at 6 PM. How do you enter the time?', 'نسيت تسجيل انصرافك الساعة ٦ مساءً. كيف تكتب الوقت؟'), [
  ('18:00', '18:00', True, 'HITS uses 24-hour time.', 'يستخدم التطبيق نظام ٢٤ ساعة.'),
  ('06:00', '06:00', False, '06:00 means 6 in the morning.', '06:00 تعني السادسة صباحًا.'),
  ('6 PM', '6 مساءً', False, 'Type the time in 24-hour format.', 'اكتب الوقت بنظام ٢٤ ساعة.'),
  ('Leave it empty', 'تتركه فارغًا', False, 'The missing time is what you are requesting.', 'الوقت الناقص هو ما تطلبه.')]))

task('my-attendance', 'clock', L('Check your attendance', 'مراجعة حضورك'), L('Am I over or short on hours?', 'هل ساعاتي زائدة أم ناقصة؟'),
     L(['Check your', 'attendance.'], ['راجِع', 'حضورك.']), L('Shows your over and short hours and your attendance for a period.', 'يعرض ساعاتك الزائدة والناقصة وحضورك خلال فترة.'),
     L('You can check your attendance for any period.', 'تستطيع مراجعة حضورك لأي فترة.'), L('Home › My Attendance', 'الرئيسية › تفاصيل الحضور والإنصراف'), [
  S('ma-1', V(EN_EMP_HOME, ee('myAttendance'), 'Tap', 'My Attendance.', 'On the home page, tap My Attendance.'),
            V(AR_EMP_HOME, ae('myAttendance'), 'اضغط', 'تفاصيل الحضور والإنصراف.', 'من الصفحة الرئيسية، اضغط تفاصيل الحضور والإنصراف.')),
  S('ma-2', V('en_emp_46', hs(2, 15.5, 96, 45), 'Read', 'Over/Short Hours.', 'Over/Short Hours shows the hours above or below your shift.', verify='confirm'),
            V('ar_emp_26', hs(2, 15, 96, 47), 'اقرأ', 'ساعات أضافية / تأخير.', 'يعرض هذا القسم الساعات الزائدة أو الناقصة عن ورديتك.', verify='confirm')),
  S('ma-3', V('en_emp_46', hs(3, 21.3, 94, 4.6), 'Change the', 'Period.', 'Tap Period to choose the time range, such as Current Month.'),
            V('ar_emp_26', hs(4, 21.3, 92, 4.6), 'غيّر', 'الفترة.', 'اضغط الفترة لاختيار المدة، مثل الشهر الحالي.')),
  S('ma-4', V('en_emp_47', hs(2, 49, 96, 47), 'See your', 'summary.', 'Count attendence status and Occurrence of Shifts summarise your attendance, leave days and shift hours.'),
            V('ar_emp_27', hs(2, 44, 96, 52), 'اعرف', 'ملخّص حضورك.', 'يلخّص تعداد حالة الحضور وعدد مرات حدوث الورديات حضورك وأيام إجازتك وساعات ورديتك.')),
 ], Q(('HR says you were short on hours last month. How do you check?', 'أخبرتك الموارد البشرية أن ساعاتك نقصت الشهر الماضي. كيف تتحقق؟'), [
  ('Open My Attendance and change the Period', 'تفتح تفاصيل الحضور والإنصراف وتغيّر الفترة', True, 'Over/Short Hours shows the gap for the Period you choose.', 'يعرض القسم الفرق للفترة التي تختارها.'),
  ('Open GEO Attendance', 'تفتح تسجيل الحضور والإنصراف', False, 'That records arrival and departure; it does not total your hours.', 'هذه الشاشة لتسجيل الدخول والخروج، لا لحساب الساعات.'),
  ('Open My Permissions', 'تفتح بيانات الإذونات', False, 'That shows permission hours only.', 'تعرض ساعات الإذن فقط.'),
  ('Change the Theme', 'تغيّر المظهر', False, 'Theme only changes colours.', 'المظهر يغيّر الألوان فقط.')]))

task('att-tracking', 'pin', L('Check your clock-in records', 'متابعة الحضور والانصراف'), L('When did I clock in and out?', 'متى سجّلت دخولي وخروجي؟'),
     L(['Check your', 'clock-in records.'], ['تابِع', 'حضورك وانصرافك.']), L('Lists every clock-in and clock-out with its time.', 'يعرض كل تسجيل دخول وخروج مع وقته.'),
     L('You can review your clock-in and clock-out records.', 'تستطيع مراجعة تسجيلات حضورك وانصرافك.'), L('Home › Attendance Tracking', 'الرئيسية › متابعة الحضور والإنصراف'), [
  S('at-1', V(EN_EMP_HOME, ee('attTracking'), 'Tap', 'Attendance Tracking.', 'On the home page, tap Attendance Tracking.'),
            V(AR_EMP_HOME, ae('attTracking'), 'اضغط', 'متابعة الحضور والإنصراف.', 'من الصفحة الرئيسية، اضغط متابعة الحضور والإنصراف.')),
  S('at-2', V('en_emp_48', hs(2, 19.3, 96, 10.5), 'Read your', 'records.', 'Each line shows IN or Out, the date and time, and the location.', 'Green marks IN, red marks Out.'),
            V('ar_emp_28', hs(2, 19.3, 96, 10.5), 'اقرأ', 'سجلّك.', 'يعرض كل سطر دخول أو خروج مع التاريخ والوقت والموقع.', 'العلامة الخضراء للدخول، والحمراء للخروج.')),
  S('at-3', V('en_emp_49', EN_FILTER, 'Older days?', 'Use the filter.', 'Open History and tap the filter button.'),
            V('ar_emp_28', AR_TAB_HIS2, 'للأيام الأقدم،', 'افتح السابقة.', 'تعرض الحالية أحدث تسجيلاتك، وتعرض السابقة الأيام الأقدم.')),
  S('at-4', V('en_emp_50', hs(3, 53.3, 94, 6.5), 'Set the dates,', 'then OK.', 'Set Attend Date Between, then tap OK.'), None),
 ], Q(('What does a red mark mean in Attendance Tracking?', 'ماذا تعني العلامة الحمراء في متابعة الحضور والإنصراف؟'), [
  ('A clock-out', 'تسجيل خروج', True, 'Red marks Out; green marks IN.', 'الحمراء للخروج، والخضراء للدخول.'),
  ('A clock-in', 'تسجيل دخول', False, 'Clock-ins are green.', 'الدخول يظهر بالعلامة الخضراء.'),
  ('An absence', 'غياب', False, 'Absences are not shown here.', 'الغياب لا يظهر هنا.'),
  ('A late arrival', 'تأخير', False, 'The colour shows IN or Out only.', 'اللون يوضّح الدخول أو الخروج فقط.')]))

task('geo', 'pin', L('Clock in by location', 'تسجيل الحضور بالموقع'), L('I need to clock in from my phone', 'أريد تسجيل حضوري من هاتفي'),
     L(['Clock in', 'by location.'], ['سجّل حضورك', 'بالموقع.']), L('Records your arrival and departure from your phone.', 'يسجّل حضورك وانصرافك من هاتفك.'),
     L('You can clock in and out from your phone.', 'تستطيع تسجيل الحضور والانصراف من هاتفك.'), L('Home › GEO Attendance', 'الرئيسية › تسجيل الحضور والإنصراف'), [
  S('ge-1', V(EN_EMP_HOME, ee('geo'), 'Tap', 'GEO Attendance.', 'On the home page, tap GEO Attendance.'),
            V(AR_EMP_HOME, ae('geo'), 'اضغط', 'تسجيل الحضور والإنصراف.', 'من الصفحة الرئيسية، اضغط تسجيل الحضور والإنصراف.')),
  S('ge-2', V('en_emp_51', hs(56, 83, 17, 11), 'Arriving?', 'Tap In.', 'When you arrive, tap In to record your attendance.', 'If your phone asks for your location, allow it.', verify='confirm'),
            V('ar_emp_29', hs(27, 83, 17, 11), 'عند الوصول،', 'اضغط دخول.', 'عند وصولك، اضغط دخول لتسجيل حضورك.', 'إذا طلب هاتفك الوصول إلى موقعك، فاسمح بذلك.', verify='confirm')),
  S('ge-3', V('en_emp_51', hs(75, 83, 17, 11), 'Leaving?', 'Tap Out.', 'When you leave, tap Out to record your departure.'),
            V('ar_emp_29', hs(8, 83, 17, 11), 'عند الانصراف،', 'اضغط خروج.', 'عند انصرافك، اضغط خروج لتسجيل الانصراف.')),
  S('ge-4', V('en_emp_51', hs(2, 13, 96, 15), 'Check', 'what you recorded.', 'Your latest records appear at the top with the location and time.'),
            V('ar_emp_29', hs(2, 13, 96, 15), 'راجِع', 'ما سجّلته.', 'تظهر أحدث تسجيلاتك في الأعلى مع الموقع والوقت.')),
  S('ge-5', V('en_emp_53', hs(3, 53.3, 94, 6.5), 'Older days?', 'Filter by date.', 'Open History, tap the filter button, set Attend Date Between, then tap OK.'), None),
 ], Q(("You're leaving work for the day. What do you tap?", 'ستغادر العمل في نهاية اليوم. ماذا تضغط؟'), [
  ('GEO Attendance › Out', 'تسجيل الحضور والإنصراف › خروج', True, 'Out records the time you leave.', 'يسجّل خروج وقت انصرافك.'),
  ('GEO Attendance › In', 'تسجيل الحضور والإنصراف › دخول', False, 'In records your arrival.', 'يسجّل دخول وقت وصولك.'),
  ('Attendance Tracking', 'متابعة الحضور والإنصراف', False, 'That only lists records.', 'تعرض التسجيلات فقط.'),
  ('My Attendance', 'تفاصيل الحضور والإنصراف', False, 'That shows totals; it does not record.', 'تعرض الإجماليات ولا تسجّل.')]))

# =================================== EMPLOYEE · MY DATA ===================================
task('changes-request', 'list', L('Request a change to your data', 'طلب تغيير بياناتك'), L('I need to update my records', 'أريد تحديث بياناتي'),
     L(['Request a', 'data change.'], ['اطلب', 'تغيير بياناتك.']), L("Sends a change request — for example children's birth certificates — for approval.", 'يرسل طلب تغيير، مثل شهادات ميلاد الأبناء، للاعتماد.'),
     L('You can send a data change request.', 'تستطيع إرسال طلب تغيير بيانات.'), L('Home › Changes Request › +', 'الرئيسية › طلب تغيرات الحالة › +'), [
  S('cr-1', V(EN_EMP_HOME, ee('changesRequest'), 'Tap', 'Changes Request.', 'On the home page, tap Changes Request.'),
            V(AR_EMP_HOME, ae('changesRequest'), 'اضغط', 'طلب تغيرات الحالة.', 'من الصفحة الرئيسية، اضغط طلب تغيرات الحالة.')),
  S('cr-2', V('en_emp_05', EN_MENU_NEW, 'Start a', 'new request.', 'Tap +, or open ⋮ and tap New.'),
            V('ar_emp_03', AR_MENU_NEW, 'ابدأ', 'طلبًا جديدًا.', 'اضغط +، أو افتح ⋮ واختر جديد.')),
  S('cr-3', V('en_emp_06', hs(31, 18.3, 66, 4.6), 'Choose the', 'Transaction.', 'Tap Transaction.'),
            V('ar_emp_04', hs(14, 18.3, 84, 4.6), 'اختر', 'حركه التغيير.', 'اضغط خانة حركه التغيير.')),
  S('cr-4', V('en_emp_07', hs(1, 85, 98, 6), 'Choose', 'the change.', 'Choose the change you need, such as Employees Kids Birth Certificates, then tap ✓.'),
            V('ar_emp_05', hs(1, 84, 98, 7), 'اختر', 'نوع التغيير.', 'اختر التغيير المطلوب، مثل شهادات ميلاد ابناء العاملين، ثم اضغط ✓.')),
  S('cr-5', V('en_emp_08', hs(2, 48.5, 96, 26), 'Complete', 'the details.', 'Fields for that change appear under My Form. Fill them in.', verify='confirm'),
            V('ar_emp_06', hs(2, 60.5, 96, 30), 'أكمِل', 'البيانات.', 'تظهر خانات هذا التغيير في نموذجي الخاص. أكمِلها.', verify='confirm')),
  S('cr-6', V('en_emp_06', hs(65, 87.5, 11, 7), 'Tap', 'send.', 'Tap the send button to submit the request for approval.'),
            V('ar_emp_06', AR_SEND, 'اضغط', 'زر الإرسال.', 'اضغط زر الإرسال لتقديم الطلب للاعتماد.')),
 ], Q(('You chose the change type. Where do you type its details?', 'اخترت نوع التغيير. أين تكتب بياناته؟'), [
  ('Under My Form', 'في نموذجي الخاص', True, 'The fields for that change appear there.', 'تظهر فيه خانات هذا التغيير.'),
  ('In Currency', 'في خانة العمله', False, 'Currency only sets the currency.', 'العمله تحدّد العملة فقط.'),
  ('In the ⋮ menu', 'في قائمة ⋮', False, 'The menu sends the request.', 'القائمة للإرسال.'),
  ('In Effective date', 'في تاريخ التغيير', False, 'That sets when the change starts.', 'يحدّد موعد بدء التغيير فقط.')]))

# =================================== MANAGER ===================================
task('notifications', 'bell', L('See requests waiting for you', 'معرفة الطلبات التي تنتظرك'), L('What needs my approval?', 'ما الذي ينتظر اعتمادي؟'),
     L(["See what's", 'waiting for you.'], ['اعرف ما', 'ينتظر قرارك.']), L('Notifications list the team requests that need your approval.', 'تعرض الإشعارات طلبات فريقك التي تحتاج اعتمادك.'),
     L("You can see which of your team's requests need you.", 'تستطيع معرفة طلبات فريقك التي تحتاج قرارك.'), L('Home › 🔔', 'الرئيسية › 🔔'), [
  S('nt-1', V(EN_MGR_HOME, BELL_EM, 'Tap the', 'bell.', 'On the home page, tap the bell at the top.'),
            V(AR_MGR_HOME, BELL_AM, 'اضغط', 'أيقونة الجرس.', 'من الصفحة الرئيسية، اضغط أيقونة الجرس في الأعلى.')),
  S('nt-2', V('en_mgr_01', hs(2, 15.5, 96, 14.5), 'Read each', 'notification.', 'Each card shows the request type, the employee, the dates and "waiting your approval".', 'To decide, open the matching approvals page.'),
            V('ar_mgr_01', hs(2, 15.5, 96, 14.5), 'اقرأ', 'كل إشعار.', 'تعرض كل بطاقة نوع الطلب والموظف والتواريخ، وأنه بانتظار موافقتك.', 'لاتخاذ القرار، افتح صفحة الموافقة المناسبة.')),
 ], Q(('The bell shows a Vacation request waiting your approval. Where do you decide on it?', 'يظهر في الجرس طلب إجازة بانتظار موافقتك. أين تتخذ القرار؟'), [
  ('Leaves Approvals', 'موافقة الإجازات', True, 'Leave requests are decided in Leaves Approvals.', 'تُحسم طلبات الإجازة من موافقة الإجازات.'),
  ('Permissions Approvals', 'موافقة الإذونات', False, 'That page is for time permissions.', 'هذه الصفحة لطلبات الإذن.'),
  ('Leaves Request', 'طلب الإجازات', False, 'That is for your own leave.', 'هذه لإجازاتك أنت.'),
  ('Incomplete TK Approvals', 'موافقة القراءات الغير مكتملة', False, 'That is for missing clock-ins and outs.', 'هذه للقراءات الناقصة.')]))

task('approve-perms', 'check-badge', L("Approve your team's permissions", 'اعتماد طلبات الإذن لفريقك'), L('Someone asked to come in late', 'طلب أحد أفراد فريقي إذن تأخير'),
     L(['Approve', 'time permissions.'], ['اعتمِد', 'طلبات الإذن.']), L("Reviews your team's permission requests so you can approve or reject them.", 'يتيح مراجعة طلبات الإذن من فريقك لاعتمادها أو رفضها.'),
     L("You can approve or reject your team's time permissions.", 'تستطيع اعتماد طلبات الإذن من فريقك أو رفضها.'), L('Home › Permissions Approvals', 'الرئيسية › موافقة الإذونات'), [
  S('ap-1', V(EN_DARK_HOME, ed('permissionsApprovals'), 'Tap', 'Permissions Approvals.', 'On the home page, tap Permissions Approvals.', 'These screens show the app in the Dark theme.'),
            V(AR_MGR_HOME, am('permissionsApprovals'), 'اضغط', 'موافقة الإذونات.', 'من الصفحة الرئيسية، اضغط موافقة الإذونات.')),
  S('ap-2', V('en_mgr_23', hs(4, 11.5, 26, 5), 'Open', 'Current.', 'Current lists the requests waiting for your decision.'),
            V('ar_emp_22', TABS3, 'اعرف', 'التبويبات.', 'الحالية: تنتظر قرارك. القادمة: ما زالت لدى معتمِد قبلك. السابقة: ما اتخذت فيه قرارًا.')),
  S('ap-3', V('en_mgr_23', hs(2, 19.3, 96, 15), 'Check the', 'request.', 'Each request shows the employee, the permission type, the times and the hours. Tap it for details.'), None),
  S('ap-4', V('en_mgr_22', hs(2, 31.5, 96, 24.5), 'Read the', 'details.', 'Permission, Shift and Attendance Details show the request next to the shift and the actual times.'), None),
  S('ap-5', V('en_mgr_23', hs(65, 88.5, 11, 8), 'Approve or reject,', 'then save.', 'Use the ✓ button at the bottom to approve or reject, then confirm.', 'Your decision only counts once you save it.', verify='confirm'),
            V('ar_emp_22', AR_FILTER, 'صفِّ', 'القائمة.', 'اضغط زر التصفية لعرض الطلبات في تواريخ محددة.')),
  S('ap-6', None, V('ar_emp_23', hs(3, 50, 94, 6.5), 'حدِّد التواريخ،', 'ثم موافق.', 'حدِّد التاريخ بين، ونوع الإذن عند الحاجة، ثم اضغط موافق.',
                    'عند ظهور الطلبات، اعتمِد أو ارفض ثم احفظ؛ لا يُعتمد قرارك قبل الحفظ.', verify='screen')),
 ], Q(('You marked three permission requests as approved, then closed the page without saving. What happens?', 'حدّدت الموافقة على ثلاثة طلبات إذن ثم أغلقت الصفحة دون حفظ. ماذا يحدث؟'), [
  ('The requests stay waiting', 'تبقى الطلبات منتظِرة', True, 'Nothing is applied until you save.', 'لا يُطبَّق أي قرار قبل الحفظ.'),
  ('The requests are approved', 'تُعتمد الطلبات', False, 'Without saving, nothing is applied.', 'دون حفظ لا يُطبَّق شيء.'),
  ('The requests are rejected', 'تُرفض الطلبات', False, 'They are neither approved nor rejected.', 'لا تُعتمد ولا تُرفض.'),
  ('Only the first request is approved', 'يُعتمد الطلب الأول فقط', False, 'No decision is applied without saving.', 'لا يُطبَّق أي قرار دون حفظ.')]))

task('leave-approvals', 'calendar-check', L("Approve your team's leave", 'اعتماد إجازات فريقك'), L('Someone on my team asked for leave', 'طلب أحد أفراد فريقي إجازة'),
     L(['Approve', 'leave requests.'], ['اعتمِد', 'طلبات الإجازة.']), L("Shows your team's leave requests so you can decide on them.", 'يعرض طلبات إجازة فريقك لتتخذ فيها قرارًا.'),
     L("You can find and decide on your team's leave requests.", 'تستطيع العثور على طلبات إجازة فريقك واتخاذ القرار فيها.'), L('Home › Leaves Approvals', 'الرئيسية › موافقة الإجازات'), [
  S('la-1', V(EN_MGR_HOME, em('leavesApprovals'), 'Tap', 'Leaves Approvals.', 'On the home page, tap Leaves Approvals.'),
            V(AR_MGR_HOME, am('leavesApprovals'), 'اضغط', 'موافقة الإجازات.', 'من الصفحة الرئيسية، اضغط موافقة الإجازات.')),
  S('la-2', V('en_emp_24', TABS3, 'Know the', 'three tabs.', 'Current: waiting for you. Monitoring: still with an earlier approver. History: requests you have decided.', verify='confirm'),
            V('ar_mgr_11', TABS3, 'اعرف', 'التبويبات الثلاثة.', 'الحالية: تنتظر قرارك. القادمة: ما زالت لدى معتمِد قبلك. السابقة: طلبات اتخذت فيها قرارًا.', verify='confirm')),
  S('la-3', V('en_mgr_13', FIRST_ROW, 'Read a', 'request.', 'Each request shows the employee, the leave type, the dates and the days. This example is from History.'),
            V('ar_mgr_11', FIRST_ROW, 'اقرأ', 'الطلب.', 'يعرض كل طلب الموظف، ونوع الإجازة، وتاريخَي من وإلى، وعدد الأيام.')),
  S('la-4', None, V('ar_mgr_11', hs(7, 86, 10, 8), 'افتح', 'القائمة.', 'لاتخاذ القرار في كل الطلبات معًا، اضغط ⋮ أسفل الشاشة.')),
  S('la-5', None, V('ar_mgr_07', hs(6, 86.5, 36, 7.5), 'اختر', 'موافقة الكل.', 'تعرض القائمة تصفية ورفض الكل وموافقة الكل. اضغط موافقة الكل.', 'رفض الكل يعمل بالطريقة نفسها.')),
  S('la-6', None, V('ar_mgr_08', hs(34.5, 61, 12, 7.5), 'أكّد', 'بموافق.', 'يطلب التطبيق التأكيد. اكتب السبب إن احتجت، ثم اضغط موافق.')),
  S('la-7', V('en_mgr_13', hs(80, 85.5, 13, 8.5), 'Filter', 'the list.', 'Tap the filter button to show requests from specific dates.'),
            V('ar_mgr_10', hs(3, 50.5, 94, 6.5), 'صفِّ', 'القائمة.', 'من زر التصفية، حدِّد تاريخ الاجازه بين، ثم اضغط موافق.')),
 ], Q(("A team member's request is still with their first approver. Which tab shows it?", 'طلب أحد أفراد فريقك ما زال لدى معتمِده الأول. في أي تبويب يظهر؟'), [
  ('Monitoring', 'القادمة', True, 'It shows requests waiting for an earlier approver.', 'يعرض الطلبات التي تنتظر معتمِدًا قبلك.'),
  ('Current', 'الحالية', False, 'Current shows requests waiting for you.', 'تعرض الحالية ما ينتظرك أنت.'),
  ('History', 'السابقة', False, 'History shows requests you have decided.', 'تعرض السابقة ما حسمته.'),
  ('Notifications', 'الإشعارات', False, 'Notifications show what is waiting for you.', 'الإشعارات تعرض ما ينتظرك أنت.')]))

task('tk-approvals', 'hourglass', L('Approve missing-time requests', 'اعتماد طلبات القراءات الناقصة'), L('Someone forgot to clock in or out', 'نسي أحد أفراد فريقي تسجيل الحضور'),
     L(['Approve', 'missing-time requests.'], ['اعتمِد', 'القراءات الناقصة.']), L("Loads your team's missing clock-in or out requests for a date range.", 'يعرض طلبات فريقك لاستكمال القراءات خلال فترة محددة.'),
     L("You can load and decide on your team's missing-time requests.", 'تستطيع عرض طلبات القراءات الناقصة لفريقك والبتّ فيها.'), L('Home › Incomplete TK Approvals', 'الرئيسية › موافقة القراءات الغير مكتملة'), [
  S('ta-1', V(EN_MGR_HOME, em('tkApprovals'), 'Tap', 'Incomplete TK Approvals.', 'On the home page, tap Incomplete TK Approvals.'),
            V(AR_MGR_HOME, am('tkApprovals'), 'اضغط', 'موافقة القراءات الغير مكتملة.', 'من الصفحة الرئيسية، اضغط موافقة القراءات الغير مكتملة.')),
  S('ta-2', V('en_emp_42', hs(80.5, 85, 12.5, 8.5), 'Tap the', 'filter.', 'Tap the filter button at the bottom.'),
            V('ar_emp_25', AR_FILTER, 'اضغط', 'زر التصفية.', 'اضغط زر التصفية أسفل الشاشة.')),
  S('ta-3', V('en_mgr_06', hs(3, 53.5, 94, 6), 'Set the', 'dates.', 'Set the two dates under Start Date Between.'),
            V('ar_mgr_05', hs(3, 53.5, 94, 6), 'حدِّد', 'التواريخ.', 'حدِّد التاريخين في التاريخ بين.')),
  S('ta-4', V('en_mgr_06', hs(55, 58.5, 11, 7.5), 'Tap', 'OK.', 'Tap OK to load the requests, then approve or reject each one and save.', verify='confirm'),
            V('ar_mgr_05', hs(36, 59.5, 11.5, 7.5), 'اضغط', 'موافق.', 'اضغط موافق لعرض الطلبات، ثم اعتمِد كل طلب أو ارفضه واحفظ.', verify='confirm')),
 ], Q(('An employee forgot to clock out on 5 October and sent a request. How do you find it?', 'نسي موظف تسجيل انصرافه يوم ٥ أكتوبر وقدّم طلبًا. كيف تجده؟'), [
  ('Incomplete TK Approvals, dates that include 5 Oct, then OK', 'موافقة القراءات، بتواريخ تشمل ٥ أكتوبر، ثم موافق', True, 'The dates decide which requests load.', 'التواريخ تحدّد الطلبات التي تظهر.'),
  ('Permissions Approvals', 'موافقة الإذونات', False, 'Missing clock-ins are not permissions.', 'القراءات الناقصة ليست إذنًا.'),
  ('Incomplete TK Request', 'طلب القراءات الغير مكتملة', False, 'That page is for your own missing times.', 'هذه الصفحة لقراءاتك أنت.'),
  ('Attendance Tracking', 'متابعة الحضور والإنصراف', False, 'That shows records, not requests.', 'تعرض التسجيلات، لا الطلبات.')]))

task('find-perms', 'search', L('Find past permission decisions', 'البحث في قرارات الإذن السابقة'), L('What did I decide last month?', 'بماذا قررت الشهر الماضي؟'),
     L(['Find past', 'permission decisions.'], ['ابحث في', 'قرارات الإذن.']), L('Filters the permission requests you have decided.', 'يصفّي طلبات الإذن التي حسمتها.'),
     L("You can find any permission request you've decided.", 'تستطيع العثور على أي طلب إذن حسمته.'), L('Home › Permissions Approvals › History', 'الرئيسية › موافقة الإذونات › السابقة'), [
  S('fd-1', V(EN_MGR_HOME, em('permissionsApprovals'), 'Tap', 'Permissions Approvals.', 'On the home page, tap Permissions Approvals.'),
            V(AR_MGR_HOME, am('permissionsApprovals'), 'اضغط', 'موافقة الإذونات.', 'من الصفحة الرئيسية، اضغط موافقة الإذونات.')),
  S('fd-2', V('en_mgr_09', EN_TAB_HIS3, 'Open', 'History.', 'History lists the requests you have already decided.'),
            V('ar_emp_22', AR_TAB_HIS3, 'افتح', 'السابقة.', 'تعرض السابقة الطلبات التي اتخذت فيها قرارًا.')),
  S('fd-3', V('en_mgr_09', hs(80, 85.5, 13, 8.5), 'Tap the', 'filter.', 'Tap the filter button at the bottom.'),
            V('ar_emp_22', AR_FILTER, 'اضغط', 'زر التصفية.', 'اضغط زر التصفية أسفل الشاشة.')),
  S('fd-4', V('en_mgr_08', hs(3, 50, 94, 12), 'Set dates', 'and type.', 'Set Start Date Between and, if needed, the Permission type.'),
            V('ar_emp_23', hs(3, 50, 94, 11.5), 'حدِّد التواريخ', 'والنوع.', 'حدِّد التاريخ بين، ونوع الإذن في الاذونات عند الحاجة.')),
  S('fd-5', V('en_mgr_08', hs(55, 62, 11, 7.5), 'Tap', 'OK.', 'Tap OK to show only the matching requests.'),
            V('ar_emp_23', hs(36, 62, 11.5, 7.5), 'اضغط', 'موافق.', 'اضغط موافق لعرض الطلبات المطابقة فقط.')),
 ], Q(("You need last month's permission decisions only. What do you change?", 'تحتاج قرارات الإذن للشهر الماضي فقط. ماذا تغيّر؟'), [
  ('The dates in the History filter', 'التواريخ في تصفية السابقة', True, 'The filter dates decide which requests show.', 'تواريخ التصفية تحدّد الطلبات الظاهرة.'),
  ('The Current tab', 'تبويب الحالية', False, 'Current shows requests still waiting.', 'تعرض الحالية ما زال ينتظر.'),
  ('Cancel', 'إلغاء', False, 'Cancel closes the filter without changes.', 'إلغاء يغلق التصفية دون تغيير.'),
  ('My Permissions', 'بيانات الإذونات', False, 'That shows your own hours.', 'تعرض ساعاتك أنت.')]))

task('changes-approvals', 'check-badge', L('Approve data change requests', 'اعتماد طلبات تغيير البيانات'), L('A team member sent a change request', 'أرسل أحد أفراد فريقي طلب تغيير'),
     L(['Approve', 'change requests.'], ['اعتمِد', 'طلبات التغيير.']), L("Finds your team's data change requests.", 'يعرض طلبات تغيير البيانات من فريقك.'),
     L("You can find your team's change requests.", 'تستطيع العثور على طلبات التغيير لفريقك.'), L('Home › Changes Approvals', 'الرئيسية › موافقة تغيرات الحالة'), [
  S('ca-1', None, V(AR_MGR_HOME, am('changesApprovals'), 'اضغط', 'موافقة تغيرات الحالة.', 'من الصفحة الرئيسية، اضغط موافقة تغيرات الحالة.')),
  S('ca-2', None, V('ar_mgr_16', TABS3, 'اعرف', 'التبويبات.', 'الحالية: تنتظر قرارك. القادمة: ما زالت لدى معتمِد قبلك. السابقة: ما اتخذت فيه قرارًا.', verify='confirm')),
  S('ca-3', None, V('ar_mgr_16', hs(5.5, 85.5, 13, 8.5), 'اضغط', 'زر التصفية.', 'اضغط زر التصفية لحصر الطلبات.')),
  S('ca-4', None, V('ar_mgr_17', hs(3, 50, 94, 12), 'حدِّد', 'ما تبحث عنه.', 'حدِّد التاريخ بين، واختر حركه التغيير عند الحاجة، ثم اضغط موافق.')),
 ], Q(('You only want birth-certificate requests. What do you set in the filter?', 'تريد طلبات شهادات الميلاد فقط. ماذا تحدّد في التصفية؟'), [
  ('Transaction type', 'حركه التغيير', True, 'It narrows requests by type.', 'تحصر الطلبات حسب نوعها.'),
  ('Only the dates', 'التاريخ بين فقط', False, 'Dates narrow the period, not the type.', 'التاريخ يحصر الفترة، لا النوع.'),
  ('Cancel', 'إلغاء', False, 'Cancel closes the filter.', 'إلغاء يغلق التصفية.'),
  ('The Upcoming tab', 'تبويب القادمة', False, 'That shows requests still with an earlier approver.', 'يعرض ما زال لدى معتمِد قبلك.')]))

task('team-records', 'users', L("Open a team member's record", 'فتح سجلّ أحد أفراد فريقك'), L("How many days does my team member have?", 'كم يومًا لدى أحد أفراد فريقي؟'),
     L(['Open a team', "member's record."], ['افتح سجلّ', 'أحد أفراد فريقك.']), L('Shows how managers pick a person from the list in My Leaves.', 'يوضّح كيف يختار المدير شخصًا من القائمة في تفاصيل الإجازات.'),
     L("You can open your own or a team member's record.", 'تستطيع فتح سجلّك أو سجلّ أحد أفراد فريقك.'), L('Home › My Leaves', 'الرئيسية › تفاصيل الإجازات'), [
  S('tm-1', V(EN_MGR_HOME, em('myLeaves'), 'Tap', 'My Leaves.', 'On the home page, tap My Leaves.'), None),
  S('tm-2', V('en_mgr_14', hs(2, 15, 96, 10.8), "You're", 'at the top.', 'Managers see a list of people. Your own name is first — tap it for your own record.'), None),
  S('tm-3', V('en_mgr_14', hs(2, 26, 96, 10.8), 'Tap a team', "member's name.", "Tap a team member's name to open their record.", verify='confirm'), None),
  S('tm-4', V('en_mgr_14', hs(77.5, 7.5, 7.5, 5.5), 'Search', 'by name.', 'Tap the search icon to find someone quickly.'), None),
 ], Q(("You want to see a team member's leave record. What do you do?", 'تريد الاطلاع على سجلّ إجازات أحد أفراد فريقك. ماذا تفعل؟'), [
  ('Open My Leaves and tap their name', 'تفتح تفاصيل الإجازات وتضغط اسمه', True, 'Managers see their team in the list; your own name is first.', 'يرى المدير فريقه في القائمة، واسمه هو الأول.'),
  ('Open Leaves Approvals › History', 'تفتح موافقة الإجازات › السابقة', False, 'That only lists decided requests.', 'تعرض الطلبات المحسومة فقط.'),
  ('Open Leaves Request', 'تفتح طلب الإجازات', False, 'That is for your own leave.', 'هذه لإجازاتك أنت.'),
  ('Ask IT for access', 'تطلب صلاحية من الدعم الفني', False, 'Managers already see their team.', 'المدير يرى فريقه بالفعل.')]),
 tips=[TIP('tm-3', 'The same list appears in My Attendance, My Permissions and Permissions Request.', 'تظهر القائمة نفسها في تفاصيل الحضور وبيانات الإذونات وطلب إذونات.')])

MISSIONS = [
 {'id': 'start', 'roles': ['employee', 'manager'], 'icon': 'rocket', 'title': L('Get started', 'ابدأ هنا'),
  'outcome': L('Sign in, recover your password and set up the app.', 'سجّل الدخول، واسترجع كلمة السر، واضبط التطبيق.'), 'tasks': ['signin', 'forgot', 'settings']},
 {'id': 'timeoff', 'roles': ['employee'], 'icon': 'calendar', 'title': L('My time off', 'إجازاتي'),
  'outcome': L('Check your balance, request leave and follow it up.', 'اعرف رصيدك، وقدّم طلب إجازة، وتابِعه.'), 'tasks': ['leave-balance', 'leave-menu', 'leave-request', 'leave-history']},
 {'id': 'mytime', 'roles': ['employee'], 'icon': 'clock', 'title': L('My time & attendance', 'وقتي وحضوري'),
  'outcome': L('Permissions, missing times, attendance and clock-in.', 'الإذونات والقراءات الناقصة والحضور والتسجيل.'),
  'tasks': ['my-permissions', 'perm-request', 'perm-history', 'tk-request', 'my-attendance', 'att-tracking', 'geo']},
 {'id': 'mydata', 'roles': ['employee'], 'icon': 'list', 'title': L('My data', 'بياناتي'),
  'outcome': L('Request a change to your records.', 'اطلب تغييرًا في بياناتك.'), 'tasks': ['changes-request']},
 {'id': 'approvals', 'roles': ['manager'], 'icon': 'check-badge', 'title': L("Approve your team's requests", 'اعتمِد طلبات فريقك'),
  'outcome': L('See what is waiting for you and decide on it.', 'اعرف ما ينتظر قرارك، واتخذ القرار.'), 'tasks': ['notifications', 'approve-perms', 'leave-approvals', 'tk-approvals']},
 {'id': 'team', 'roles': ['manager'], 'icon': 'users', 'title': L('Keep an eye on your team', 'تابِع فريقك'),
  'outcome': L("Past decisions, change requests and your team's records.", 'القرارات السابقة وطلبات التغيير وسجلّات فريقك.'), 'tasks': ['find-perms', 'changes-approvals', 'team-records']},
]

# stops whose screens exist only in part of one language: keep or drop explicitly
LANGS = {'forgot': ['en', 'ar'], 'tk-request': ['en']}

# ---------- typing colours sampled from the real field ----------
def sample(screen, box):
    im = Image.open(os.path.join(SCR, screen + '.webp')).convert('RGB'); W, H = im.size
    x0, y0 = int(W * box['x'] / 100), int(H * box['y'] / 100); x1, y1 = int(W * (box['x'] + box['w']) / 100), int(H * (box['y'] + box['h']) / 100)
    a = np.asarray(im.crop((x0, y0, x1, y1))).reshape(-1, 3).astype(int)
    bg = np.median(a, 0).astype(int); lum = bg @ [0.299, 0.587, 0.114]
    return '#%02x%02x%02x' % tuple(bg), ('#1b1b1f' if lum > 128 else '#f4f6fa')
for t in T.values():
    t['langs'] = [lg for lg in ('en', 'ar') if sum(1 for s in t['steps'] if s.get(lg)) >= 2]
    t['langs'] = LANGS.get(t['id'], t['langs'])
    for s in t['steps']:
        for lg in ('en', 'ar'):
            v = s.get(lg)
            if not v: continue
            assert os.path.exists(os.path.join(SCR, v['screen'] + '.webp')), v['screen']
            for f in v.get('type') or []:
                f['bg'], f['fg'] = sample(v['screen'], f['box'])
    ids = {s['id'] for s in t['steps']}
    for tp in t['tips']: assert tp['after'] in ids, (t['id'], tp['after'])
    assert sum(o['correct'] for o in t['check']['options']) == 1, t['id']
    arabic = [t['check']['q']['ar']] + [x['text']['ar'] for x in t['check']['options']] + [x['why']['ar'] for x in t['check']['options']] + [x['text']['ar'] for x in t['tips']]
    arabic += [t[k]['ar'] if isinstance(t[k]['ar'], str) else ' '.join(t[k]['ar']) for k in ('name', 'situation', 'title', 'purpose', 'outcome')]
    for s_ in t['steps']:
        v = s_.get('ar')
        if v: arabic += [' '.join(v['headline']), v['text'], v.get('helper') or '']
    for a_ in arabic:
        left = re.sub(r'(HITS|OFFICE 365|\d+[:/]\d+|\d+)', '', a_)
        assert not re.search(r'[A-Za-z]', left), (t['id'], a_)

UI = BASE['ui']
UI['en'].update({'home': 'Home', 'coming': 'Coming soon: My Payslip.', 'shownIn': 'Shown in: {lang}'})
UI['ar'].update({'home': 'الرئيسية', 'coming': 'قريبًا: كشف الراتب.', 'shownIn': 'متاح في: {lang}'})
used = sorted({v['screen'] for t in T.values() for s in t['steps'] for v in (s.get('en'), s.get('ar')) if v})
data = {'version': '4.0', 'helpEmail': BASE['helpEmail'], 'ui': UI, 'missions': MISSIONS, 'tasks': T,
        'glossary': BASE['glossary'], 'help': BASE['help'], 'screens': used}
open(os.path.join(ROOT, 'assets', 'data.js'), 'w').write('window.HITS=' + json.dumps(data, ensure_ascii=False, separators=(',', ':')) + ';\n')
for lg in ('en', 'ar'):
    for role in ('employee', 'manager'):
        n = [k for m in MISSIONS if role in m['roles'] for k in m['tasks'] if lg in T[k]['langs']]
        print(lg, role, len(n), 'stops')
print('screens used', len(used), 'steps', sum(1 for t in T.values() for s in t['steps'] for v in (s.get('en'), s.get('ar')) if v))
