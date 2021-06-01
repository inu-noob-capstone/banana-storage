package com.example.leavemealoneapplication

import android.content.Context
import androidx.appcompat.app.AppCompatActivity
import android.os.Bundle
import android.util.Log
import com.example.leavemealoneapplication.databinding.ActivityLightManagementBinding
import com.example.leavemealoneapplication.databinding.ActivityMoistureManagementBinding
import kotlinx.coroutines.*
import org.json.JSONObject
import java.io.BufferedReader
import java.io.InputStreamReader
import java.net.HttpURLConnection
import java.net.URL

class MoistureManagement : AppCompatActivity() {
    val binding by lazy { ActivityMoistureManagementBinding.inflate(layoutInflater) }
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(binding.root)

        val sharedWater = getSharedPreferences("waterSetting", Context.MODE_PRIVATE)
        val waterEditor = sharedWater.edit()

        CoroutineScope(Dispatchers.IO).launch {
            var waterUrlText = "http://192.168.219.110/waterSetting.json"
            var waterUrl = URL(waterUrlText)

            var waterUrlConnection = waterUrl.openConnection() as HttpURLConnection
            waterUrlConnection.requestMethod = "GET"
            waterUrlConnection.setRequestProperty("Content-Type", "application/json; charset=UTF-8")

            var waterInputStream = waterUrlConnection.getInputStream()
            var waterBuffered = BufferedReader(InputStreamReader(waterInputStream, "UTF-8"))
            var waterContent = waterBuffered.readText()

            Log.d("waterResponse", "Size: " + waterContent.length)

            while (true) {
                if ((waterContent != null) && (waterContent.length != 0)) {
                    var waterJson = JSONObject(waterContent)

                    var humThreshold = "${waterJson.get("humThreshold")}"
                    waterEditor.putString("humThreshold", "${humThreshold}")
                    waterEditor.apply()

                    var allowingOfAUser = "${waterJson.get("allowingOfAUser")}"
                    waterEditor.putString("allowingOfAUser", "${allowingOfAUser}")
                    waterEditor.apply()

                    break
                } else {
                    waterUrlConnection.disconnect()
                    waterBuffered.close()

                    waterInputStream = waterUrlConnection.getInputStream()
                    waterBuffered = BufferedReader(InputStreamReader(waterInputStream, "UTF-8"))
                    waterContent = waterBuffered.readText()
                }
            }

            var humThreshold = sharedWater.getString("humThreshold", "0")
            var allowingOfAUser = sharedWater.getString("allowingOfAUser", "true")

            withContext(Dispatchers.Main) {
                binding.currentMoistureGoalAsPercent.text = "${humThreshold}" + "%"

                if (allowingOfAUser == "true") {
                    binding.waterOnOffToggleBtn.check(binding.on.id)
                } else {
                    binding.waterOnOffToggleBtn.check(binding.off.id)
                }
            }
        } // 서버에서 데이터를 읽어오는 데 필요한 코루틴 블록 끝.

            binding.saveMoistureSetting.setOnClickListener {
                // 이하의 if문은 설정 저장 버튼을 누를 시, 이를 휴대폰에 파일 데이터로 저장하는 과정.

                if(binding.editThreshold.text.toString().length != 0){
                    waterEditor.putString("humThreshold", binding.editThreshold.text.toString())
                    waterEditor.apply()
                    Log.d("waterUpdate","humThreshold : " + "${binding.editThreshold.text.toString()}")
                }

                if(binding.on.id == binding.waterOnOffToggleBtn.checkedId){
                    waterEditor.putString("allowingOfAUser","true")
                    waterEditor.apply()
                    Log.d("waterUpdate", "allowingOfAUser : true")
                } else if(binding.off.id == binding.waterOnOffToggleBtn.checkedId){
                    waterEditor.putString("allowingOfAUser","false")
                    waterEditor.apply()
                    Log.d("waterUpdate","allowingOfAUser : false")
                }

                // 아래부터는 humThreshold와 allowingOfAUser 데이터 전송

                while(true) {

                    var humThreshold = sharedWater.getString("humThreshold", "0")
                    var allowingOfAUser = sharedWater.getString("allowingOfAUser", "true")

                    var waterUrlText =
                        "http://192.168.219.110/cgi-bin/water.py?humThreshold=" + "${humThreshold}" +
                                "&allowingOfAUser=" + "${allowingOfAUser}"

                    var waterUrl = URL(waterUrlText)

                    var waterURLConnection = waterUrl.openConnection() as HttpURLConnection
                    waterURLConnection.requestMethod = "GET"
                    waterURLConnection.setRequestProperty(
                        "Content-Type",
                        "text/plain"
                    )

                    CoroutineScope(Dispatchers.IO).launch {
                        if (waterURLConnection.responseCode == HttpURLConnection.HTTP_OK) {
                            Log.d("Response1","HumThreshold & allowingOfAUser HTTP_OK")
                        }
                    }
                    break
                }// while(true) 블록 종료

                finish() // 현 액티비티 종료

            } // saveSetting 버튼 OnClickListener 블록 끝

        } // OnCreate 블록 끝
    } // 액티비티 클래스 블록 끝
