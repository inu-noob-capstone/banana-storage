from FileIO import *

#설정 파일 변경. App에서 파일을 변경한 걸 시뮬레이션
def keyboardInput(lightSetting, waterSetting, keyboard):
    if keyboard.is_pressed('l'):
        goalLux = int(input('목표 lux 값 설정 :'))
        lightSetting.changeGoalLux(goalLux)
        saveSettingAsFile(lightSetting, waterSetting)
        
    elif keyboard.is_pressed('h'):
        humThreshold = int(input('문턱 습도 값 설정 :'))
        waterSetting.changeHumThreshold(humThreshold)
        saveSettingAsFile(lightSetting, waterSetting)
        
    elif keyboard.is_pressed('c'):
        chlorophyll = input('엽록소B 함량을 알파벳으로 선택. A:적음, B:중간, C:많음 ::')
        lightSetting.changeChlorophyll(chlorophyll)
        saveSettingAsFile(lightSetting, waterSetting)

    elif keyboard.is_pressed('o'):
        allowingOfAUser = input('allowingOfAUser(전구 작동) 선택. 켜기:true, 끄기:false :: ')
        if allowingOfAUser == "true":
            allowingOfAUser = True
        else:
            allowingOfAUser = False
        
        lightSetting.changeAllowingOfAUser(allowingOfAUser)
        saveSettingAsFile(lightSetting, waterSetting)


#데이터가 들어있는 setting 객체 내용을 출력하는 함수.
def printSetting(lightSetting, waterSetting):   
    print()
    print('현재 조도 : %dlux' % int(lightSetting.dict["currentLux"]))
    print('현재 습도 : %d%%' % waterSetting.dict["humidity"])
    print()
    #time.sleep(0.7)
