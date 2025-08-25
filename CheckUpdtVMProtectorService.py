import win32serviceutil
import win32service
import win32event
import servicemanager
import winreg
import time
import subprocess
import win32ts
import win32security
import win32api

class CheckUpdtVMProtector(win32serviceutil.ServiceFramework):
    _svc_name_ = "CheckUpdtVMProtector"
    _svc_display_name_ = "CheckUpdtVM Registry Protection"
    _svc_description_ = "Keeps the CheckUpdtVM registry value set to 0."

    def __init__(self, args):
        super().__init__(args)
        self.hWaitStop = win32event.CreateEvent(None, 0, 0, None)
        self.running = True

    def SvcStop(self):
        self.ReportServiceStatus(win32service.SERVICE_STOP_PENDING)
        self.running = False
        win32event.SetEvent(self.hWaitStop)

    import subprocess

    def _set_automatic_delayed_start(self):
        try:
            scm = win32service.OpenSCManager(None, None, win32service.SC_MANAGER_ALL_ACCESS)
            try:
                svc = win32service.OpenService(
                    scm,
                    self._svc_name_,
                    win32service.SERVICE_CHANGE_CONFIG | win32service.SERVICE_QUERY_CONFIG
                )
                try:
                    win32service.ChangeServiceConfig(
                        svc,
                        win32service.SERVICE_NO_CHANGE,
                        win32service.SERVICE_AUTO_START,
                        win32service.SERVICE_NO_CHANGE,
                        "",
                        None,
                        0,
                        None,
                        None,
                        None,
                        ""
                    )

                    win32service.ChangeServiceConfig2(
                        svc,
                        win32service.SERVICE_CONFIG_DELAYED_AUTO_START_INFO,
                        {'fDelayedAutostart': 1}
                    )

                    servicemanager.LogInfoMsg("✅ Set to 'Automatic (delayed startup)' ChangeServiceConfig2.")
                finally:
                    win32service.CloseServiceHandle(svc)
            finally:
                win32service.CloseServiceHandle(scm)

        except Exception as e:
            servicemanager.LogErrorMsg(f"❌ Failed to set Automatic (Delayed Start) WinAPI: {e}")

            try:
                subprocess.run(
                    ["sc", "config", self._svc_name_, "start=", "delayed-auto"],
                    check=True, capture_output=True, text=True
                )
                servicemanager.LogInfoMsg("✅ Fallback: 'sc config ... start= delayed-auto' aplicado.")
            except Exception as e2:
                servicemanager.LogErrorMsg(f"❌ Fallback sc.exe also failed: {e2}")



    def SvcDoRun(self):
        servicemanager.LogInfoMsg("Service started: CheckUpdtVMProtector")
        self._set_automatic_delayed_start()
        self.main()


    def get_logged_in_user_sid(self):
        try:
            session_id = win32ts.WTSGetActiveConsoleSessionId()
            token = win32ts.WTSQueryUserToken(session_id)
            user_sid = win32security.GetTokenInformation(token, win32security.TokenUser)[0]
            sid_str = win32security.ConvertSidToStringSid(user_sid)
            servicemanager.LogInfoMsg(f"Detected SID from active session: {sid_str}")
            return sid_str
        except Exception as e:
            servicemanager.LogErrorMsg(f"Error obtaining SID from active session: {e}")
            return None

    def main(self):
        sid = self.get_logged_in_user_sid()
        if not sid:
            servicemanager.LogErrorMsg("No SID detected. Service stopped.")
            return

        reg_path = rf"{sid}\SOFTWARE\DownloadManager"
        reg_value = "CheckUpdtVM"
        expected_value = "0"

        while self.running:
            try:
                key = winreg.OpenKey(
                    winreg.HKEY_USERS,
                    reg_path,
                    0,
                    winreg.KEY_SET_VALUE | winreg.KEY_QUERY_VALUE
                )
                try:
                    current_value, reg_type = winreg.QueryValueEx(key, reg_value)
                except FileNotFoundError:
                    current_value = None

                if current_value != expected_value:
                    winreg.SetValueEx(key, reg_value, 0, winreg.REG_SZ, expected_value)
                    servicemanager.LogInfoMsg("✅ CheckUpdtVM restored to 0")
                winreg.CloseKey(key)
            except Exception as e:
                servicemanager.LogErrorMsg(f"❌ ERROR: {str(e)}")

            time.sleep(2)

    @classmethod
    def install(cls, *args):
        win32serviceutil.install(cls)
        print(f"✅ Service {cls._svc_name_} installed. Startup type will be set on next run.")


if __name__ == '__main__':
    win32serviceutil.HandleCommandLine(CheckUpdtVMProtector)
