package com.example.leavemealoneapplication

import android.content.Context
import androidx.appcompat.app.AppCompatActivity
import android.os.Bundle
import android.util.Log
import com.example.leavemealoneapplication.databinding.ActivityLightManagementBinding
import kotlinx.coroutines.*
import org.json.JSONObject
import java.io.*
import java.net.HttpURLConnection
import java.net.URL

class LightManagement : AppCompatActivity() {
    val binding by lazy { ActivityLightManagementBinding.inflate(layoutInflater) }
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(binding.root)

        var sharedLight = getSharedPreferences("lightSetting", Context.MODE_PRIVATE)
        var lightEditor = sharedLight.edit()

        CoroutineScope(Dispatchers.IO).launch {
            var lightUrlText = "http://192.168.219.110/lightSetting.json"
            var lightUrl = URL(lightUrlText)

            var lightUrlConnection = lightUrl.openConnection() as HttpURLConnection
            lightUrlConnection.requestMethod = "GET"
            lightUrlConnection.setRequestProperty("Content-Type", "application/json; charset=UTF-8")

            var lightInputStream = lightUrlConnection.getInputStream()
            var lightBuffered = BufferedReader(InputStreamReader(lightInputStream, "UTF-8"))
            var lightContent = lightBuffered.readText()

            Log.d("lightResponse", "Size: " + lightContent.length)

            while (true) {
                if ((lightContent != null) && (lightContent.length != 0)) {
                    var lightJson = JSONObject(lightContent)

                    var goalLux = "${lightJson.get("goalLux")}"
                    lightEditor.putString("goalLux", "${goalLux}")
                    lightEditor.apply()

                    var chlorophyll = "${lightJson.get("chlorophyll")}"
                    lightEditor.putString("chlorophyll", "${chlorophyll}")
                    lightEditor.apply()

                    var allowingOfAUser = "${lightJson.get("allowingOfAUser")}"
                    lightEditor.putString("allowingOfAUser", "${allowingOfAUser}")
                    lightEditor.apply()

                    break
                } else {
                    lightUrlConnection.disconnect()
                    lightBuffered.close()

                    lightInputStream = lightUrlConnection.getInputStream()
                    lightBuffered = BufferedReader(InputStreamReader(lightInputStream, "UTF-8"))
                    lightContent = lightBuffered.readText()
                }
            }

            var goalLux = sharedLight.getString("goalLux", "0")
            var chlorophyll = sharedLight.getString("chlorophyll", "A")
            var allowingOfAUser = sharedLight.getString("allowingOfAUser", "true")

            withContext(Dispatchers.Main) {
                binding.currentLuxGoalText.text = "${goalLux}" + " Lux"

                if (chlorophyll == "A") {
                    binding.chlorophyllBButton.selectButton(binding.less.id)
                } else if (chlorophyll == "B") {
                    binding.chlorophyllBButton.selectButton(binding.normal.id)
                } else {
                    binding.chlorophyllBButton.selectButton(binding.lots.id)
                }

                if (allowingOfAUser == "true") {
                    binding.lightOnOffToggleBtn.check(binding.on.id)
                } else {
                    binding.lightOnOffToggleBtn.check(binding.off.id)
                }
            }
        } // 서버에서 데이터 읽어오는데 필요한 코루틴 블록 끝.

        binding.saveSetting.setOnClickListener {
            // 이하 if문은 설정 저장 버튼을 누를 시, 이를 휴대폰에 파일 데이터로 저장하는 과정

            if (binding.editGoalLux.text.toString().length != 0) {
                lightEditor.putString("goalLux", binding.editGoalLux.text.toString())
                lightEditor.apply()
                Log.d("lightUpdate", "goalLux : " + "${binding.editGoalLux.text.toString()}")
            }

            if (binding.less.isSelected == true) {
                lightEditor.putString("chlorophyll", "A")
                lightEditor.apply()
                Log.d("lightUpdate", "chlorophyll : A")
            } else if (binding.normal.isSelected == true) {
                lightEditor.putString("chlorophyll", "B")
                lightEditor.apply()
                Log.d("lightUpdate", "chlorophyll : B")
            } else {
                lightEditor.putString("chlorophyll", "C")
                lightEditor.apply()
                Log.d("lightUpdate", "chlorophyll : C")
            }

            if (binding.on.id == binding.lightOnOffToggleBtn.checkedId) {
                lightEditor.putString("allowingOfAUser", "true")
                lightEditor.apply()
                Log.d("lightUpdate", "allowingOfAUser : true")
            } else if (binding.off.id == binding.lightOnOffToggleBtn.checkedId) {
                lightEditor.putString("allowingOfAUser", "false")
                lightEditor.apply()
                Log.d("lightUpdate", "allowingOfAUser : false")
            }

            // 아래부터는 goalLux와 chlorophyll, allowingOfAUser 데이터 전송

            var check = true

            while(check) {

                var goalLux = sharedLight.getString("goalLux", "0")
                var chlorophyll = sharedLight.getString("chlorophyll", "A")
                var allowingOfAUser = sharedLight.getString("allowingOfAUser", "true")

                var lightUrlText = "http://192.168.219.110/cgi-bin/light.py?goalLux=" +
                        "${goalLux}" + "&chlorophyll=" + "${chlorophyll}" + "&allowingOfAUser=" +
                        "${allowingOfAUser}"

                var lightUrl = URL(lightUrlText)

                var lightUrlConnection = lightUrl.openConnection() as HttpURLConnection
                lightUrlConnection.requestMethod = "GET"
                lightUrlConnection.setRequestProperty(
                    "Content-Type",
                    "text/plain"
                )

                CoroutineScope(Dispatchers.IO).launch {
                    if (lightUrlConnection.responseCode == HttpURLConnection.HTTP_OK) {
                        Log.d("Response2","goalLux & chlorophyll & allowingOfAUser HTTP_OK")

                    } // ResponseCode를 확인하는 if문 블록 끝.
                } // 코루틴 블록 종료.
                break
            } // while(true) 블록 종료

            finish() // 현 액티비티 종료

        } // 버튼 onClickListener 블록 끝

    } // OnCreate 블록 끝
} // 액티비티 클래스 블록 끝.