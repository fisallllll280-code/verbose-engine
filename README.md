فيصـــــــل…
جاهز. هذا القوقو ككود — نسخة نظيفة، جاهزة تشتغل، وتتمدّد لاحقاً داخل V‑EMPIRE.

import os
import time
import traceback
from typing import Dict, Any, Optional, Callable


class GOQO:
    """
    GOQO Engine
    G = Gate   : بوابة الأوامر
    O = Origin : نقطة البداية
    Q = Quantum: منطق القرار والمعالجة
    O = Ops    : التنفيذ والعمليات
    """

    def __init__(
        self,
        watch_path: Optional[str] = None,
        recovery_enabled: bool = True,
        executor: Optional[Callable[[str], Any]] = None,
    ):
        # حالة النظام
        self.state: str = "IDLE"  # IDLE, PROCESSING, ERROR

        # سجل الظل
        self.shadow_log: list[str] = []

        # مراقبة الملفات
        self.watch_path: Optional[str] = watch_path
        self.last_snapshot: Dict[str, float] = {}

        # الاسترداد
        self.recovery_enabled: bool = recovery_enabled

        # منفذ الأوامر (يمكن استبداله بتنفيذ حقيقي)
        self._executor = executor if executor is not None else self._default_execute

    # -------------------------
    # SHADOW LOG
    # -------------------------
    def log(self, msg: str) -> None:
        entry = f"[SHADOW][{self.state}] {msg}"
        self.shadow_log.append(entry)
        print(entry)

    # -------------------------
    # SAFE RUN
    # -------------------------
    def safe_run(self, cmd: str) -> Any:
        """
        تنفيذ آمن للأوامر:
        - يغيّر الحالة إلى PROCESSING
        - ينفّذ الأمر
        - يرجع إلى IDLE إذا نجح
        - يدخل حالة ERROR إذا فشل، ويحاول الاسترداد
        """
        try:
            self.state = "PROCESSING"
            self.log(f"RUN: {cmd}")
            result = self._executor(cmd)
            self.state = "IDLE"
            self.log(f"OK: {cmd}")
            return result
        except Exception as e:
            self.state = "ERROR"
            self.log(f"FAULT: {str(e)}")
            self.log(traceback.format_exc())
            if self.recovery_enabled:
                self.recover()
            return None

    # -------------------------
    # CORE EXECUTION
    # -------------------------
    def _default_execute(self, cmd: str) -> str:
        """
        تنفيذ افتراضي (محاكاة).
        يمكن استبداله بمنفذ حقيقي (Shell, Queue, RPC, ...).
        """
        time.sleep(0.05)
        return f"[VX] {cmd}"

    # -------------------------
    # AUTO RECOVERY
    # -------------------------
    def recover(self) -> None:
        """
        استرداد تلقائي:
        - يسجل محاولة الإصلاح
        - يرجع الحالة إلى IDLE
        """
        self.log("RECOVERY: Attempting auto-fix…")
        time.sleep(0.1)
        self.state = "IDLE"
        self.log("RECOVERY: System restored")

    # -------------------------
    # FILE SNAPSHOT
    # -------------------------
    def snapshot(self) -> Dict[str, float]:
        """
        يأخذ لقطة لحالة الملفات في المجلد المراقَب:
        {اسم_الملف: آخر_تعديل}
        """
        if not self.watch_path or not os.path.isdir(self.watch_path):
            return {}
        return {
            f: os.path.getmtime(os.path.join(self.watch_path, f))
            for f in os.listdir(self.watch_path)
        }

    # -------------------------
    # FILE WATCHER
    # -------------------------
    def watch(self) -> None:
        """
        يراقب المجلد:
        - إذا تغيرت اللقطة عن السابقة → ينفّذ أمر تلقائي
        """
        if not self.watch_path:
            return

        current = self.snapshot()
        if current != self.last_snapshot:
            self.log("WATCHER: Change detected in watched directory")
            self.safe_run("AUTO-HANDLE-CHANGE")
            self.last_snapshot = current

    # -------------------------
    # DAEMON LOOP
    # -------------------------
    def daemon(self, interval: float = 0.2) -> None:
        """
        حلقة تشغيل مستمرة:
        - يراقب الملفات
        - يحافظ على النظام في حالة عمل دائمة
        """
        self.log("GOQO DAEMON ONLINE")
        self.last_snapshot = self.snapshot()

        while True:
            self.watch()
            time.sleep(interval)


if __name__ == "__main__":
    # مثال تشغيل بسيط
    engine = GOQO(watch_path=None, recovery_enabled=True)

    # تشغيل أمر يدوي
    engine.safe_run("INIT-SYSTEM")

    # تشغيل الديمون (مستمر)
    # engine.daemon()


لو تبغى الخطوة الجاية:

• نخلي GOQO يتكلم مع VX‑BEAST / V‑EMPIRE
• أو نربطه بملفات مشروعك في verbose-engine
• أو نحوله إلى State Machine كاملة مع أوامر مهيكلة


قول:
اربطه بالمشروع أو طوّره لآلة حالات. import time
import os
import traceback

class VBeast:
    def __init__(self, watch_path=None):
        self.state = "IDLE"
        self.shadow_log = []
        self.recovery_enabled = True
        self.watch_path = watch_path
        self.last_snapshot = self.snapshot() if watch_path else None

    # -------------------------
    # SHADOW LOG
    # -------------------------
    def log(self, msg):
        entry = f"[SHADOW] {msg}"
        self.shadow_log.append(entry)
        print(entry)

    # -------------------------
    # EXECUTION WRAPPER
    # -------------------------
    def safe_run(self, cmd):
        try:
            self.state = "PROCESSING"
            self.log(f"RUN: {cmd}")
            result = self.execute(cmd)
            self.state = "IDLE"
            return result

        except Exception as e:
            self.state = "ERROR"
            self.log(f"FAULT: {str(e)}")
            self.log(traceback.format_exc())
            if self.recovery_enabled:
                self.recover()

    # -------------------------
    # CORE EXECUTION
    # -------------------------
    def execute(self, cmd):
        time.sleep(0.05)
        return f"[VX] {cmd}"

    # -------------------------
    # AUTO RECOVERY
    # -------------------------
    def recover(self):
        self.log("RECOVERY: Attempting auto‑fix…")
        time.sleep(0.1)
        self.state = "IDLE"
        self.log("RECOVERY: System restored")

    # -------------------------
    # FILE WATCHER
    # -------------------------
    def snapshot(self):
        if not self.watch_path or not os.path.isdir(self.watch_path):
            return {}
        return {f: os.path.getmtime(os.path.join(self.watch_path, f))
                for f in os.listdir(self.watch_path)}

    def watch(self):
        if not self.watch_path:
            return
        current = self.snapshot()
        if current != self.last_snapshot:
            self.log("WATCHER: Change detected in watched directory")
            self.safe_run("AUTO‑HANDLE‑CHANGE")
            self.last_snapshot = current

    # -------------------------
    # DAEMON LOOP
    # -------------------------
    def daemon(self):
        self.log("VX‑BEAST DAEMON ONLINE")
        while True:
            self.watch()
            time.sleep(0.2)

# -------------------------
# SYSTEM ENTRY
# -------------------------
def vx_unified(watch_path=None):
    beast = VBeast(watch_path)
    beast.log("VX‑BEAST UNIFIED CORE ONLINE")

    while True:
        cmd = input("VX> ")
        if cmd == "exit":
            break
        elif cmd == "daemon":
            beast.daemon()
        else:
            beast.safe_run(cmd)

vx_unified()
verbose-engine
VX Sovereign Runtime - Event-driven decision, execution, governance, ledger, and distributed systems platform.
