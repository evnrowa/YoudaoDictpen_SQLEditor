import os
import subprocess

class ADB:
    def __init__(self) -> None:
        pass

    def bypassVerification(self):
        adb_command = self.getCommand()
        output,error = self._execute(f'{adb_command} shell cat /Version')
        if output is None:
            print("Error: ADB command execution timed out.")
            return 5

        if output.find('login with "adb shell auth" to continue') != -1 or error.find('login with "adb shell auth" to continue') != -1:
            # 尝试第一个密码
            print("Attempting login...")
            auth_command = f'echo CherryYoudao | {adb_command} shell auth'
            auth_result = self._execute_with_timeout(auth_command)
            if auth_result and auth_result.find('success') != -1:
                print('DictPen is unlocked.')
                return 4
            else:
                print('Failed to unlock with default password.')
                print('Attempting new password...')
                new_auth_command = f'echo x3sbrY1d2@dictpen | {adb_command} shell auth'
                #尝试第二个密码
                new_auth_result = self._execute_with_timeout(new_auth_command)
                if new_auth_result and new_auth_result.find('success') != -1:
                    print('DictPen is unlocked with new password.')
                else:
                    print('Failed to unlock with new password.')
                    return 0
        elif output.find('no devices/emulators found') !=-1  or error.find('no devices/emulators found') !=-1:
            return 2
        elif output.find('more than one device/emulator') !=-1 or error.find('more than one device/emulator') !=-1:
            return 1
        elif output.find('DictPen') !=-1 or error.find('DictPen') !=-1:
            return 4
        else:
            return 5
    def getCommand(self) -> str:
        adb = 'adb'  # Assuming adb is in the PATH
        return adb if os.path.exists(adb) else 'adb'

    def _execute(self, cmd):
        process = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        stdout, stderr = process.communicate()
        return stdout.decode().strip(),stderr.decode().strip()

    def _execute_with_timeout(self, cmd, timeout=3):
        #设置超时防卡死
        process = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        try:
            stdout, stderr = process.communicate(timeout=timeout)
            return stdout.decode().strip()
        except subprocess.TimeoutExpired:
            process.kill()
            print("Error: ADB command execution timed out.")
            return None

# 初始化adb类
adb = ADB()
#用来确保adb连接OK的函数
def check_devices_okay():
    print("\n以下是已连接的设备:")
    os.system("adb devices")
    adb_login_state = adb.bypassVerification()
    
    if adb_login_state == 0:
        print("密码尝试失败，请手动输入密码或尝试使用另一版本的脚本。按下Enter输入密码。")
        os.system("adb shell auth")
        check_devices_okay()
    elif adb_login_state == 1:
        print("您有超过一台设备连接到了电脑上，请断开除词典笔外其它设备，然后按下Enter。")
        os.system("pause")
        check_devices_okay()
    elif adb_login_state == 2:
        print("您没有已连接的设备，请检查词典笔是否连接到电脑，词典笔是否启用adb，然后按下Enter。")
        os.system("pause")
        check_devices_okay()
    elif adb_login_state == 4:
        print("\n已成功连接到词典笔。请在脚本执行完成前不要连接其它设备，包括物理设备（手机、平板等）与虚拟设备（WSA或其它安卓虚拟机等），否则可能导致操作失败。")
        return True
    elif adb_login_state == 5:
        print("无法执行连接命令。您连接设备的可能不是词典笔。请检查您连接的设备，然后按下Enter。")
        os.system("pause")
        check_devices_okay()
def is_string_in_file(filename, search_string):#寻找字符串
      try:
            with open(filename, 'r') as file:
                  for line in file:
                        if search_string in line:
                              return True
      except FileNotFoundError:
            print(f"File '{filename}' not found.")
      return False
 
        #用户确认开始操作
print("请确认您的参数正确无误。如果发现错误，请退出本程序并修改。\n如果没有错误，按下Enter开始执行脚本\n")
os.system("pause")
#检查设备是否处于OK状态
check_devices_okay()
rcs_pull_command = "adb pull /etc/init.d/rcS"
rcs_push_command = "adb push rcS /etc/init.d/rcS"
reboot_command = "adb shell reboot"
start_command = "adb shell sshd_sevice start"
chmod_command = "adb shell chmod +x /etc/init.d/rcS"
pwd_command = "adb shell passwd"
os.system(rcs_pull_command) 

filename = 'rcS'
search_string = '/usr/sbin/dropbear'
 
if is_string_in_file(filename, search_string):#防止重复开启
    print("已经开启过了，无需再次开启")
    os.system("pause")

else:
    print("请确认您的参数正确无误。如果发现错误，请退出本程序并修改。\n如果没有错误，按下Enter开始执行脚本\n")
    os.system("pause")
    os.system("cls")
        #检查设备是否处于OK状态
    check_devices_okay()
    print("请输入新的root密码")
    os.system("adb shell passwd")
    os.system(start_command) 
    os.system(rcs_pull_command) 
    with open("rcS","a") as f:
        f.writelines('/usr/sbin/dropbear')
    os.system(rcs_push_command) 
    os.system(chmod_command) 
    print("操作已完成，重启后生效") 
    wait=input("是否重启y/n\n")
    msg=str(wait)
    if msg=="y":
        os.system(reboot_command) 
    else:
        exit




