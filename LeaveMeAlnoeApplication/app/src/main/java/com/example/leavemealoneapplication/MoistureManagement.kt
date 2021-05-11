package com.example.leavemealoneapplication

import android.content.Context
import androidx.appcompat.app.AppCompatActivity
import android.os.Bundle
import android.util.Log
import com.example.leavemealoneapplication.databinding.ActivityLightManagementBinding
import com.example.leavemealoneapplication.databinding.ActivityMoistureManagementBinding
import kotlinx.coroutines.CoroutineScope
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.launch
import kotlinx.coroutines.withContext
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

        CoroutineScope(Dispatchers.IO).launch{
            var waterUrlText = "http://192.168.219.110/waterSetting.json"
            var waterUrl = URL(waterUrlText)

            var waterUrlConnection = waterUrl.openConnection() as HttpURLConnection
            waterUrlConnection.requestMethod = "GET"
            waterUrlConnection.setRequestProperty("Content-Type", "application/json; charset=UTF-8")

            var waterInputStream = waterUrlConnection.getInputStream()
            var waterBuffered = BufferedReader(InputStreamReader(waterInputStream, "UTF-8"))
            var waterContent = waterBuffered.readText()

            Log.d("waterResponse", "Size: "+waterContent.length)

            while(true) {
                if ((waterContent != null) && (waterContent.length != 0)) {
                    var waterJson = JSONObject(waterContent)

                    var humThreshold = "${waterJson.get("humThreshold")}"
                    waterEditor.putString("humThreshold", "${humThreshold}")
                    waterEditor.apply()

                    var allowingOfAUser = "${waterJson.get("allowingOfAUser")}"
                    waterEditor.putString("allowingOfAUser","${allowingOfAUser}")
                    waterEditor.apply()

                    break
                }
                else{
                    waterUrlConnection.disconnect()
                    waterBuffered.close()

                    waterInputStream = waterUrlConnection.getInputStream()
                    waterBuffered = BufferedReader(InputStreamReader(waterInputStream, "UTF-8"))
                    waterContent = waterBuffered.readText()
                }
            }

            var humThreshold = sharedWater.getString("humThreshold","0")
            var allowingOfAUser = sharedWater.getString("allowingOfAUser", "true")

            withContext(Dispatchers.Main){
                binding.currentMoistureGoalAsPercent.text = "${humThreshold}"+"%"

                if (allowingOfAUser == "true"){
                    binding.waterOnOffToggleBtn.check(binding.on.id)
                }
                else{
                    binding.waterOnOffToggleBtn.check(binding.off.id)
                }
            }

            binding.saveMoistureSetting.setOnClickListener {
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

                // 아래부터는 humThreshold 데이터 전송

                var humThreshold = sharedWater.getString("humThreshold","0")

                var waterUrlText = "http//192.168.219.110:8081/?humThreshold=" + "${humThreshold}"

            } // saveSetting 버튼 OnClickListener 블록 끝

        }
    }
}