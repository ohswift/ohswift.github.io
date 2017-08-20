#coding:utf-8
'''
Created on 2011-4-26

@author: vincent
'''
import os
import re


test = '''
Enclosure Device ID: 32
Slot Number: 23
Drive's position: DiskGroup: 2, Span: 0, Arm: 8
Enclosure position: 1
Device Id: 23
WWN: 5000C50055C0725C
Sequence Number: 3
Media Error Count: 4
Other Error Count: 0
Predictive Failure Count: 0
Last Predictive Failure Event Seq Number: 0
PD Type: SAS

Raw Size: 931.512 GB [0x74706db0 Sectors]
Non Coerced Size: 931.012 GB [0x74606db0 Sectors]
Coerced Size: 931.0 GB [0x74600000 Sectors]
Sector Size:  0
Firmware state: Offline
Device Firmware Level: AS06
Shield Counter: 0
Successful diagnostics completion on :  N/A
SAS Address(0): 0x5000c50055c0725d
SAS Address(1): 0x0
Connected Port Number: 0(path0) 
Inquiry Data: SEAGATE ST91000640SS    AS069XG35SMV            
FDE Capable: Not Capable
FDE Enable: Disable
Secured: Unsecured
Locked: Unlocked
Needs EKM Attention: No
Foreign State: None 
Device Speed: 6.0Gb/s 
Link Speed: 6.0Gb/s 
Media Type: Hard Disk Device
Drive Temperature :25C (77.00 F)
PI Eligibility:  No 
Drive is formatted for PI information:  No
PI: No PI
Port-0 :
Port status: Active
Port's Linkspeed: 6.0Gb/s 
Port-1 :
Port status: Active
Port's Linkspeed: Unknown 
Drive has flagged a S.M.A.R.T alert : No






Enclosure Device ID: 32
Slot Number: 21
Drive's position: DiskGroup: 2, Span: 0, Arm: 10
Enclosure position: 1
Device Id: 21
WWN: 5000C50055C0791C
Sequence Number: 63
Media Error Count: 2
Other Error Count: 0
Predictive Failure Count: 0
Last Predictive Failure Event Seq Number: 0
PD Type: SAS

Raw Size: 931.512 GB [0x74706db0 Sectors]
Non Coerced Size: 931.012 GB [0x74606db0 Sectors]
Coerced Size: 931.0 GB [0x74600000 Sectors]
Sector Size:  0
Firmware state: Online, Spun Up
Device Firmware Level: AS06
Shield Counter: 0
Successful diagnostics completion on :  N/A
SAS Address(0): 0x5000c50055c0791d
SAS Address(1): 0x0
Connected Port Number: 0(path0) 
Inquiry Data: SEAGATE ST91000640SS    AS069XG35SB9            
FDE Capable: Not Capable
FDE Enable: Disable
Secured: Unsecured
Locked: Unlocked
Needs EKM Attention: No
Foreign State: None 
Device Speed: 6.0Gb/s 
Link Speed: 6.0Gb/s 
Media Type: Hard Disk Device
Drive Temperature :24C (75.20 F)
PI Eligibility:  No 
Drive is formatted for PI information:  No
PI: No PI
Port-0 :
Port status: Active
Port's Linkspeed: 6.0Gb/s 
Port-1 :
Port status: Active
Port's Linkspeed: Unknown 
Drive has flagged a S.M.A.R.T alert : No
'''

slots = {}
slotNnum = 0

def work():
    f = r'''Z:\work\sphinx-doc\python\demo\slot.log'''
    reStr = r'''(?i)(?:Enclosure Device ID: (.*?)\n.*?Slot Number: (.*?)\n.*?Media Error Count: (.*?)\n.*?Other Error Count: (.*?)\n.*?Firmware state: (.*?)\n.*?)'''
# 
#     res = re.findall(reStr, test, re.S)
#     print res
    # 调用megacli生成信息
    text = open(f, 'r').read()
    
    # 对信息进行解析
    res = re.findall(reStr, text, re.S)
    
    # 打印磁盘状态异常信息   
    res.sort(cmp=lambda x,y: cmp(int(x[1]),int(y[1])))
    
    #print res
    #[('32', '21', '0', '0', 'Online, Spun Up'), ('32', '23', '0', '0', 'Offline')]
    
    # 打印时间戳
    #timeStr = time.strftime('[%Y-%m-%d %I:%M:%S]',time.localtime(time.time()))
    allStr = ''
    
    allDisk = []
    for i in range(12):
        allDisk.append(str(i))
        
    presentDisk = []
    # 打印磁盘状态异常信息
    abnormanStr = ''
    for t in res :
        if t[4] != 'Online, Spun Up':
            abnormanStr += '\tSlot %s %s\n' % (t[1], t[4])   
        presentDisk.append(t[1]) 
    
    if abnormanStr != '':    
        allStr += 'Disk(s) abnormal list: \n'
        allStr += abnormanStr 
    
    # 打印磁盘被拔掉的情况
    absentStr = ''
    absentDisk = list(set(allDisk)-set(presentDisk))
    absentDisk.sort(key=int)
    for i in absentDisk:
        absentStr += '%s,' % i
    
    if absentStr!='': 
        allStr += 'Disk(s) absent: \n'  
        absentStr = "\tSlot %s\n" % absentStr[0:-1]
        allStr += absentStr
    
    # 打印磁盘出现故障的情况   
    errorStr = ''
    for t in res :
        if t[2] != '0' or t[3]!='0':
            errorStr += '\tSlot %s error, MediaError %s, OtherError %s\n' % (t[1], t[2], t[3])   
    if errorStr != '':
        allStr += 'Disk(s) error: \n'
        allStr +=  errorStr+'\n'
        
    if allStr != '' :    
        print allStr
if __name__ == '__main__':
    work()
    
        
        
        
